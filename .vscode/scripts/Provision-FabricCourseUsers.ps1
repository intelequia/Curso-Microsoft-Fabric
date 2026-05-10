<#
.SYNOPSIS
    Aprovisiona los usuarios del curso Microsoft Fabric en el tenant de Aurora Energía
    y genera un Excel con las credenciales temporales.

.DESCRIPTION
    - Crea los usuarios en Entra ID (auroraenergiasl.onmicrosoft.com)
    - Asigna licencia Microsoft 365 Business Premium (SKU: SPB)
    - Exporta la lista de usuarios y contraseñas temporales a un archivo Excel

.REQUIREMENTS
    Install-Module Microsoft.Graph        -Scope CurrentUser
    Install-Module ImportExcel            -Scope CurrentUser

.NOTES
    Autor  : Intelequia — CTO Office
    Versión: 1.0
    Fecha  : 2026-05-04
#>

[CmdletBinding(SupportsShouldProcess)]
param (
    [string]$TenantDomain = "auroraenergiasl.onmicrosoft.com",
    [string]$OutputExcel  = "$PSScriptRoot\usuarios-fabric-curso.xlsx"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

# ─────────────────────────────────────────────
# 0. Verificar módulos necesarios e importar en orden
# ─────────────────────────────────────────────
$requiredModules = @("Microsoft.Graph.Authentication", "Microsoft.Graph.Users", "Microsoft.Graph.Identity.DirectoryManagement", "ImportExcel")
foreach ($mod in $requiredModules) {
    if (-not (Get-Module -ListAvailable -Name $mod)) {
        throw "Módulo '$mod' no encontrado. Ejecútalo: Install-Module $mod -Scope CurrentUser"
    }
}

# Importar en orden correcto para evitar conflictos de versión de ensamblado
Remove-Module Microsoft.Graph.Authentication, Microsoft.Graph.Users, Microsoft.Graph.Identity.DirectoryManagement -ErrorAction SilentlyContinue
Import-Module Microsoft.Graph.Authentication                   -Force
Import-Module Microsoft.Graph.Users                           -Force
Import-Module Microsoft.Graph.Identity.DirectoryManagement    -Force

# ─────────────────────────────────────────────
# 1. Autenticación interactiva
# ─────────────────────────────────────────────
Write-Host "`n🔐 Conectando a Microsoft Graph (tenant: $TenantDomain)..." -ForegroundColor Cyan

Connect-MgGraph `
    -TenantId $TenantDomain `
    -Scopes "User.ReadWrite.All", "Directory.ReadWrite.All", "Organization.Read.All" `
    -NoWelcome

$context = Get-MgContext
Write-Host "✅ Conectado como: $($context.Account)" -ForegroundColor Green

# ─────────────────────────────────────────────
# 2. Obtener SKU de Microsoft 365 Business Premium
# ─────────────────────────────────────────────
Write-Host "`n🔍 Buscando SKU de Microsoft 365 Business Premium..." -ForegroundColor Cyan

$skus = Get-MgSubscribedSku | Where-Object { $_.SkuPartNumber -in @("SPB", "O365_BUSINESS_PREMIUM", "SMB_BUSINESS_PREMIUM") }

if (-not $skus) {
    Write-Warning "No se encontró la licencia Microsoft 365 Business Premium disponible en el tenant."
    Write-Warning "SKUs disponibles:"
    Get-MgSubscribedSku | Select-Object SkuPartNumber, SkuId, ConsumedUnits | Format-Table
    $skuId = Read-Host "Introduce manualmente el SkuId a asignar"
} else {
    $sku   = $skus | Select-Object -First 1
    $skuId = $sku.SkuId
    Write-Host "✅ SKU encontrado: $($sku.SkuPartNumber) → $skuId" -ForegroundColor Green

    $unitsAvailable = $sku.PrepaidUnits.Enabled - $sku.ConsumedUnits
    Write-Host "   Licencias disponibles: $unitsAvailable de $($sku.PrepaidUnits.Enabled)" -ForegroundColor Yellow
}

# ─────────────────────────────────────────────
# 3. Lista de usuarios
#    Formato: OriginalEmail | DisplayName | FirstName | LastName
# ─────────────────────────────────────────────
$userList = @(
    [PSCustomObject]@{ OriginalEmail = "john.doe@doe.com";        DisplayName = "John Doe";         FirstName = "John";     LastName = "Doe" }
    [PSCustomObject]@{ OriginalEmail = "jane.doe@doe.com";          DisplayName = "Jane Doe";         FirstName = "Jane";       LastName = "Doe" }
)

# ─────────────────────────────────────────────
# 4. Función para generar contraseñas temporales seguras
# ─────────────────────────────────────────────
function New-TemporaryPassword {
    [OutputType([string])]
    param ([int]$Length = 14)

    $upper   = 'ABCDEFGHJKLMNPQRSTUVWXYZ'.ToCharArray()
    $lower   = 'abcdefghjkmnpqrstuvwxyz'.ToCharArray()
    $digits  = '23456789'.ToCharArray()
    $special = '!@#$%&*'.ToCharArray()

    # Al menos uno de cada tipo
    $pwd = @(
        ($upper  | Get-Random)
        ($lower  | Get-Random)
        ($digits | Get-Random)
        ($special| Get-Random)
    )

    # Rellenar el resto
    $all = $upper + $lower + $digits + $special
    $pwd += (1..($Length - 4) | ForEach-Object { $all | Get-Random })

    # Mezclar
    return (-join ($pwd | Sort-Object { Get-Random }))
}

# ─────────────────────────────────────────────
# 5. Derivar UPN en el tenant destino a partir del email original
# ─────────────────────────────────────────────
function Get-NewUPN {
    param ([string]$OriginalEmail, [string]$Domain)

    $localPart = ($OriginalEmail -split '@')[0].ToLower()

    # pf.francisco.alvarez → francisco.alvarez (eliminar prefijo de iniciales "pf.")
    if ($localPart -match '^[a-z]{1,2}\.[a-z]+\.[a-z]+$') {
        $parts    = $localPart -split '\.'
        $localPart = "$($parts[1]).$($parts[2])"
    }

    return "$localPart@$Domain"
}

# ─────────────────────────────────────────────
# 6. Crear usuarios y asignar licencias
# ─────────────────────────────────────────────
Write-Host "`n👥 Creando usuarios..." -ForegroundColor Cyan

$results = [System.Collections.Generic.List[PSCustomObject]]::new()

foreach ($user in $userList) {

    $upn      = Get-NewUPN -OriginalEmail $user.OriginalEmail -Domain $TenantDomain
    $tempPass = New-TemporaryPassword

    Write-Host "  ► $upn" -NoNewline

    try {
        # ── Crear usuario ──────────────────────────────────────────────
        $newUser = New-MgUser -BodyParameter @{
            DisplayName       = $user.DisplayName
            GivenName         = $user.FirstName
            Surname           = $user.LastName
            UserPrincipalName = $upn
            MailNickname      = ($upn -split '@')[0]
            AccountEnabled    = $true
            PasswordProfile   = @{
                Password                      = $tempPass
                ForceChangePasswordNextSignIn = $true
            }
            UsageLocation     = "ES"    # Requerido para asignar licencias
        }

        # ── Asignar licencia ───────────────────────────────────────────
        Set-MgUserLicense -UserId $newUser.Id -AddLicenses @(@{ SkuId = $skuId }) -RemoveLicenses @()

        Write-Host " ✅" -ForegroundColor Green

        $results.Add([PSCustomObject]@{
            "Nombre completo"    = $user.DisplayName
            "UPN (tenant curso)" = $upn
            "Email original"     = $user.OriginalEmail
            "Contraseña temporal"= $tempPass
            "Licencia"           = "Microsoft 365 Business Premium"
            "Estado"             = "Creado"
            "ID Entra"           = $newUser.Id
        })

    } catch {
        Write-Host " ❌ ERROR: $($_.Exception.Message)" -ForegroundColor Red

        $results.Add([PSCustomObject]@{
            "Nombre completo"    = $user.DisplayName
            "UPN (tenant curso)" = $upn
            "Email original"     = $user.OriginalEmail
            "Contraseña temporal"= $tempPass
            "Licencia"           = "Microsoft 365 Business Premium"
            "Estado"             = "ERROR: $($_.Exception.Message)"
            "ID Entra"           = ""
        })
    }
}

# ─────────────────────────────────────────────
# 7. Exportar a Excel
# ─────────────────────────────────────────────
Write-Host "`n📊 Exportando resultados a Excel..." -ForegroundColor Cyan

$excelParams = @{
    Path          = $OutputExcel
    WorksheetName = "Usuarios Fabric"
    AutoSize      = $true
    FreezeTopRow  = $true
    BoldTopRow    = $true
    TableName     = "UsuariosFabric"
    TableStyle    = "Medium9"
    PassThru      = $true
}

$excel = $results | Export-Excel @excelParams

# Destacar en rojo las filas con error
$ws = $excel.Workbook.Worksheets["Usuarios Fabric"]
for ($row = 2; $row -le ($results.Count + 1); $row++) {
    $estadoCell = $ws.Cells[$row, 6]   # Columna "Estado"
    if ($estadoCell.Text -like "ERROR*") {
        $estadoCell.Style.Font.Color.SetColor([System.Drawing.Color]::Red)
    }
}

# Ocultar columna ID Entra (columna 7) — datos internos, no necesarios en el entregable
$ws.Column(7).Hidden = $true

Close-ExcelPackage $excel

Write-Host "✅ Excel generado en: $OutputExcel" -ForegroundColor Green

# ─────────────────────────────────────────────
# 8. Resumen final
# ─────────────────────────────────────────────
$ok     = ($results | Where-Object { $_."Estado" -eq "Creado" }).Count
$errors = ($results | Where-Object { $_."Estado" -like "ERROR*" }).Count

Write-Host "`n─────────────────────────────────" -ForegroundColor DarkGray
Write-Host "  Resumen de aprovisionamiento" -ForegroundColor White
Write-Host "─────────────────────────────────" -ForegroundColor DarkGray
Write-Host "  ✅ Creados correctamente : $ok" -ForegroundColor Green
Write-Host "  ❌ Con errores           : $errors" -ForegroundColor $(if ($errors -gt 0) { "Red" } else { "DarkGray" })
Write-Host "  📄 Excel                 : $OutputExcel" -ForegroundColor Cyan
Write-Host "─────────────────────────────────`n" -ForegroundColor DarkGray

Disconnect-MgGraph | Out-Null
Write-Host "🔒 Sesión cerrada." -ForegroundColor DarkGray

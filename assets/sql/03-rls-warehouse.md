# Configuración RLS en el warehouse

RLS in Fabric Warehouse sigue la misma sintaxis T-SQL estándar (`CREATE SECURITY POLICY`). Para el ejercicio, el flujo completo es:

## 1. Crear el rol de base de datos

```sql
CREATE ROLE comercial_andalucia;
-- Asignar el usuario de Entra ID al rol
ALTER ROLE comercial_andalucia ADD MEMBER [usuario@tenant.com];
```

## 2. Crear la función predicado (inline TVF)

```sql
CREATE SCHEMA Security;
GO

CREATE FUNCTION Security.fn_rls_estacion(@provincia VARCHAR(100))
RETURNS TABLE
WITH SCHEMABINDING
AS
RETURN
    SELECT 1 AS ok
    WHERE IS_MEMBER('comercial_andalucia') = 0   -- admins/otros ven todo
       OR @provincia IN (
              'Sevilla','Málaga','Granada','Cádiz',
              'Córdoba','Almería','Huelva','Jaén'
          );
GO
```

> `IS_MEMBER(...) = 0` hace que quien **no** pertenezca al rol vea todos los datos. Si quieres la lógica inversa (todos restringidos salvo `db_owner`), sustituye esa condición por `IS_MEMBER('db_owner') = 1`.

## 3. Crear la política de seguridad

```sql
CREATE SECURITY POLICY dbo.PolEstacion
ADD FILTER PREDICATE Security.fn_rls_estacion(provincia)
ON dbo.dim_estacion
WITH (STATE = ON);
```

## Consideraciones importantes para Fabric Warehouse

| Aspecto | Detalle |
|---|---|
| **Soporte** | Fabric Warehouse sí soporta `CREATE SECURITY POLICY` y `FILTER PREDICATE` |
| **Autenticación** | Los miembros de rol se asignan con Entra ID (no SQL logins) |
| **Alcance del filtro** | El predicado filtra `dim_estacion`, pero `fact_ventas` queda sin filtrar si se consulta directamente |
| **Propagación via JOIN** | Si el usuario consulta a través de `vw_kpi_ventas_diarias`, el JOIN con `dim_estacion` hace que el filtro se propague |

## Para filtrar también `fact_ventas` directamente

```sql
-- Función predicado sobre estacion_id
CREATE FUNCTION Security.fn_rls_fact(@estacion_id INT)
RETURNS TABLE
WITH SCHEMABINDING
AS
RETURN
    SELECT 1 AS ok
    WHERE IS_MEMBER('comercial_andalucia') = 0
       OR EXISTS (
           SELECT 1 FROM dbo.dim_estacion
           WHERE estacion_id = @estacion_id
             AND provincia IN (
                 'Sevilla','Málaga','Granada','Cádiz',
                 'Córdoba','Almería','Huelva','Jaén')
       );
GO

ALTER SECURITY POLICY dbo.PolEstacion
ADD FILTER PREDICATE Security.fn_rls_fact(estacion_id)
ON dbo.fact_ventas;
```

## Verificación

```sql
-- Simular vista como miembro del rol (en sesión separada del usuario asignado)
SELECT IS_MEMBER('comercial_andalucia');   -- debe devolver 1
SELECT DISTINCT provincia FROM dbo.dim_estacion;  -- solo las 8 provincias
```

Para deshabilitar temporalmente (ej. en mantenimiento):
```sql
ALTER SECURITY POLICY dbo.PolEstacion WITH (STATE = OFF);
```

The Row-Level Security setup for Fabric Warehouse uses standard T-SQL `CREATE SECURITY POLICY` with an inline TVF predicate. The key Fabric-specific consideration is that role members are Entra ID identities, not SQL logins. 


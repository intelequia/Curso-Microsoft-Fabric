"""
Generador de datasets ficticios para el curso Microsoft Fabric (Aurora Energía).
Ejecutar:
    python generar_datos.py
Crea CSV en ./assets/data/
"""
import csv
import json
import os
import random
from datetime import datetime, timedelta

random.seed(42)
OUT = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(OUT, exist_ok=True)

# -----------------------------------------------------------------------------
# Maestros ficticios
# -----------------------------------------------------------------------------
NOMBRES = ["Marta","Carlos","Lucía","Andrés","Sofía","Pablo","Elena","Diego","Marina","Iván",
           "Paula","Javier","Nuria","Adrián","Clara","Raúl","Beatriz","Ismael","Patricia","Jorge"]
APELLIDOS = ["García","Rodríguez","López","Martín","Sánchez","Pérez","Gómez","Ruiz","Díaz","Hernández",
             "Moreno","Muñoz","Álvarez","Romero","Alonso","Gutiérrez","Navarro","Torres","Vázquez","Ramos"]
DOMINIOS = ["aurora-corp.test","aurora-mail.test","mailbox.test","correo.test"]
SEGMENTOS = ["Particular","Empresa","Flota","Administración"]

PROVINCIAS = [
    ("Madrid","Comunidad de Madrid"),("Barcelona","Cataluña"),("Sevilla","Andalucía"),
    ("Málaga","Andalucía"),("Valencia","Comunidad Valenciana"),("Zaragoza","Aragón"),
    ("Murcia","Región de Murcia"),("Bilbao","País Vasco"),("Granada","Andalucía"),
    ("Santa Cruz de Tenerife","Canarias"),("Las Palmas","Canarias"),("Palma","Islas Baleares"),
    ("Valladolid","Castilla y León"),("Vigo","Galicia"),("Alicante","Comunidad Valenciana"),
    ("Cádiz","Andalucía"),("Córdoba","Andalucía"),("Toledo","Castilla-La Mancha"),
]

PRODUCTOS = [
    (1,"Gasolina 95","combustible","litro"),
    (2,"Gasolina 98","combustible","litro"),
    (3,"Diésel A","combustible","litro"),
    (4,"Diésel A+","combustible","litro"),
    (5,"AdBlue","combustible","litro"),
    (6,"Carga EV Rápida 50kW","electricidad","kWh"),
    (7,"Carga EV Ultrarrápida 150kW","electricidad","kWh"),
    (8,"Gas Natural Vehicular","gas","kg"),
    (9,"GLP Auto","gas","litro"),
    (10,"Lubricante 5W30","lubricante","unidad"),
    (11,"Lubricante 10W40","lubricante","unidad"),
    (12,"Líquido limpiaparabrisas","lubricante","unidad"),
]
PRECIO_BASE = {1:1.55,2:1.69,3:1.48,4:1.62,5:1.10,6:0.45,7:0.55,8:1.20,9:0.95,10:25.0,11:22.0,12:4.5}

CANALES = ["pos","app","web"]

# -----------------------------------------------------------------------------
# dim_cliente
# -----------------------------------------------------------------------------
N_CLIENTES = 1500
clientes = []
for cid in range(1, N_CLIENTES + 1):
    nombre = f"{random.choice(NOMBRES)} {random.choice(APELLIDOS)} {random.choice(APELLIDOS)}"
    dominio = random.choice(DOMINIOS)
    email_local = nombre.lower().replace(" ", ".").replace("á","a").replace("é","e") \
                                .replace("í","i").replace("ó","o").replace("ú","u")
    email = f"{email_local}{cid}@{dominio}"
    fecha_alta = (datetime(2022,1,1) + timedelta(days=random.randint(0, 1400))).date()
    clientes.append({
        "cliente_id": cid,
        "nombre_cliente": nombre,
        "email": email,
        "dominio_email": dominio,
        "segmento": random.choices(SEGMENTOS, weights=[60,25,10,5])[0],
        "fecha_alta": fecha_alta.isoformat(),
    })

with open(os.path.join(OUT, "clientes.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=clientes[0].keys())
    w.writeheader(); w.writerows(clientes)

# -----------------------------------------------------------------------------
# dim_producto
# -----------------------------------------------------------------------------
with open(os.path.join(OUT, "productos.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["producto_id","nombre_producto","categoria","unidad_medida"])
    w.writerows(PRODUCTOS)

# -----------------------------------------------------------------------------
# dim_estacion
# -----------------------------------------------------------------------------
estaciones = []
eid = 0
for prov, com in PROVINCIAS:
    n = random.randint(2, 6)
    for i in range(1, n + 1):
        eid += 1
        tipo = random.choices(["gasolinera","ev_charger","multi"], weights=[60,15,25])[0]
        estaciones.append({
            "estacion_id": eid,
            "nombre_estacion": f"Aurora {prov} {i:02d}",
            "provincia": prov,
            "comunidad": com,
            "tipo": tipo,
            "fecha_apertura": (datetime(2018,1,1) + timedelta(days=random.randint(0, 2200))).date().isoformat(),
        })
with open(os.path.join(OUT, "estaciones.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=estaciones[0].keys())
    w.writeheader(); w.writerows(estaciones)

# -----------------------------------------------------------------------------
# fact_ventas (~50.000 filas) entre 2024-01-01 y 2026-03-31
# -----------------------------------------------------------------------------
N_VENTAS = 50_000
inicio = datetime(2024, 1, 1)
fin    = datetime(2026, 3, 31, 23, 59)
delta_seg = int((fin - inicio).total_seconds())
producto_ids = [p[0] for p in PRODUCTOS]
estacion_ids = [e["estacion_id"] for e in estaciones]
cliente_ids  = [c["cliente_id"] for c in clientes]

with open(os.path.join(OUT, "ventas.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["transaccion_id","fecha_venta","cliente_id","producto_id","estacion_id",
                "cantidad","precio_unitario","importe","canal"])
    for tid in range(1, N_VENTAS + 1):
        ts = inicio + timedelta(seconds=random.randint(0, delta_seg))
        cli = random.choice(cliente_ids) if random.random() > 0.20 else ""  # 20% anónimas
        prod = random.choice(producto_ids)
        est = random.choice(estacion_ids)
        if prod in (1,2,3,4):       cant = round(random.uniform(15, 70), 2)
        elif prod == 5:             cant = round(random.uniform(2, 10), 2)
        elif prod in (6,7):         cant = round(random.uniform(8, 60), 2)
        elif prod in (8,9):         cant = round(random.uniform(5, 30), 2)
        else:                       cant = float(random.randint(1, 3))
        precio = round(PRECIO_BASE[prod] * random.uniform(0.92, 1.08), 4)
        importe = round(cant * precio, 2)
        canal = random.choices(CANALES, weights=[70,20,10])[0]
        w.writerow([tid, ts.isoformat(sep=" ", timespec="seconds"), cli, prod, est,
                    cant, precio, importe, canal])

# -----------------------------------------------------------------------------
# Telemetría sintética para Eventhouse (JSON lines)
# -----------------------------------------------------------------------------
N_EVENTOS = 10_000
EVENTOS = ["caudal","temperatura","presion","error_caudalimetro","reset","mantenimiento"]
SEVERIDADES = {"caudal":"info","temperatura":"info","presion":"info",
               "error_caudalimetro":"error","reset":"warning","mantenimiento":"info"}

with open(os.path.join(OUT, "telemetria_eventos.json"), "w", encoding="utf-8") as f:
    for _ in range(N_EVENTOS):
        ts = inicio + timedelta(seconds=random.randint(0, delta_seg))
        ev = random.choices(EVENTOS, weights=[40,15,15,5,10,15])[0]
        est = random.choice(estacion_ids)
        valor = (round(random.uniform(20, 80), 2) if ev == "caudal"
                 else round(random.uniform(15, 90), 2) if ev == "temperatura"
                 else round(random.uniform(1, 8), 2)  if ev == "presion"
                 else 0.0)
        evento = {
            "timestamp": ts.isoformat(sep=" ", timespec="seconds"),
            "estacion_id": est,
            "surtidor_id": f"S{est:03d}-{random.randint(1,8):02d}",
            "evento": ev,
            "valor": valor,
            "severidad": SEVERIDADES[ev],
        }
        f.write(json.dumps(evento, ensure_ascii=False) + "\n")

print("Datasets generados en", OUT)
print("- clientes.csv :", len(clientes))
print("- productos.csv:", len(PRODUCTOS))
print("- estaciones.csv:", len(estaciones))
print("- ventas.csv   :", N_VENTAS)
print("- telemetria_eventos.json:", N_EVENTOS)

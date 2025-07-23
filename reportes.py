
import sqlite3
from openpyxl import Workbook
from datetime import datetime
from collections import Counter

def generar_reporte_anual(año):
    conn = sqlite3.connect("parqueadero.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT placa, tipo, hora_entrada, hora_salida, total_pagado
        FROM parqueo
        WHERE strftime('%Y', hora_salida) = ?
    """, (str(año),))
    datos = cursor.fetchall()
    conn.close()

    if not datos:
        return None

    wb = Workbook()
    ws = wb.active
    ws.title = f"Reporte {año}"
    ws.append(["Placa", "Tipo", "Entrada", "Salida", "Total Pagado"])

    total_ingresos = 0
    tipos = []

    for fila in datos:
        ws.append(fila)
        tipos.append(fila[1])  # tipo de vehículo
        if fila[4]:
            total_ingresos += fila[4]

    # Totales por tipo
    conteo_tipos = Counter(tipos)

    # Espacio y resumen
    ws.append([])
    ws.append(["Resumen"])
    ws.append(["Tipo de Vehículo", "Cantidad"])
    for tipo, cantidad in conteo_tipos.items():
        ws.append([tipo, cantidad])

    # Total ingresos
    ws.append([])
    ws.append(["Total Ingresos:", total_ingresos])

    nombre_archivo = f"reporte_parqueadero_{año}.xlsx"
    wb.save(nombre_archivo)
    return nombre_archivo

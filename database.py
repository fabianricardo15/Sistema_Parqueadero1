import sqlite3
from datetime import datetime

def conectar():
    return sqlite3.connect("parqueadero.db")

def crear_tabla():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS parqueo (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            placa TEXT NOT NULL,
            tipo TEXT,
            hora_entrada TEXT,
            hora_salida TEXT,
            total_pagado REAL
        )
    """)
    conn.commit()
    conn.close()

def registrar_entrada(placa, tipo):
    conn = conectar()
    cursor = conn.cursor()
    hora_entrada = datetime.now().isoformat()
    cursor.execute("INSERT INTO parqueo (placa, tipo, hora_entrada) VALUES (?, ?, ?)",
                   (placa.upper(), tipo, hora_entrada))
    conn.commit()
    conn.close()

def registrar_salida(placa, tarifa_por_hora):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, hora_entrada FROM parqueo WHERE placa = ? AND hora_salida IS NULL", (placa.upper(),))
    registro = cursor.fetchone()
    if registro:
        id_registro, hora_entrada = registro
        hora_salida = datetime.now()
        entrada = datetime.fromisoformat(hora_entrada)
        duracion_horas = (hora_salida - entrada).total_seconds() / 3600
        total = round(duracion_horas * tarifa_por_hora, 2)
        cursor.execute("""
            UPDATE parqueo
            SET hora_salida = ?, total_pagado = ?
            WHERE id = ?
        """, (hora_salida.isoformat(), total, id_registro))
        conn.commit()
        conn.close()
        return round(duracion_horas, 2), total
    else:
        conn.close()
        return None, None

def obtener_vehiculos_en_parqueo():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT placa, tipo, hora_entrada FROM parqueo WHERE hora_salida IS NULL")
    datos = cursor.fetchall()
    conn.close()
    return datos


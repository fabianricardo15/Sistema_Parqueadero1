
from reportlab.lib.pagesizes import A6
from reportlab.pdfgen import canvas
from datetime import datetime
import os

def generar_recibo(placa, tipo, entrada, salida, duracion, total):
    nombre_archivo = f"recibo_{placa}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    c = canvas.Canvas(nombre_archivo, pagesize=A6)
    c.setFont("Helvetica", 10)

    c.drawString(30, 200, "RECIBO DE PARQUEADERO")
    c.drawString(30, 180, f"Placa: {placa}")
    c.drawString(30, 165, f"Tipo: {tipo}")
    c.drawString(30, 150, f"Entrada: {entrada}")
    c.drawString(30, 135, f"Salida: {salida}")
    c.drawString(30, 120, f"Tiempo: {duracion:.2f} horas")
    c.drawString(30, 105, f"Total pagado: ${total:,.0f}")
    c.drawString(30, 80, "Gracias por su visita")

    c.save()
    os.startfile(nombre_archivo)  # Abre el PDF automáticamente en Windows





import tkinter as tk
from tkinter import messagebox, ttk
from database import crear_tabla, registrar_entrada, registrar_salida, obtener_vehiculos_en_parqueo
from tarifas import TARIFA_POR_HORA

def actualizar_lista():
    for row in tree.get_children():
        tree.delete(row)
    for placa, tipo, entrada in obtener_vehiculos_en_parqueo():
        tree.insert("", "end", values=(placa, tipo, entrada))

def registrar_vehiculo():
    placa = entry_placa.get()
    tipo = tipo_var.get()
    if placa and tipo:
        registrar_entrada(placa, tipo)
        messagebox.showinfo("Éxito", "Vehículo registrado correctamente.")
        entry_placa.delete(0, tk.END)
        actualizar_lista()
    else:
        messagebox.showwarning("Datos faltantes", "Debe ingresar placa y tipo.")

def salida_vehiculo():
    placa = entry_placa.get()
    if placa:
        horas, total = registrar_salida(placa, TARIFA_POR_HORA)
        if horas is not None:
            messagebox.showinfo("Salida registrada",
                                f"Duración: {horas:.2f} horas\nTotal a pagar: ${total:,.0f}")
            actualizar_lista()
        else:
            messagebox.showerror("Error", "Vehículo no encontrado o ya ha salido.")
def reporte():
    año = simpledialog.askstring("Reporte Anual", "Ingrese el año (YYYY):")
    if año and año.isdigit():
        archivo = generar_reporte_anual(int(año))
        if archivo:
            messagebox.showinfo("Reporte generado", f"Reporte guardado como {archivo}")
        else:
            messagebox.showwarning("Sin datos", f"No hay registros para el año {año}")

    else:
        messagebox.showwarning("Placa faltante", "Debe ingresar la placa.")

# GUI
crear_tabla()
root = tk.Tk()
root.title("Sistema de Parqueadero")

frame = tk.Frame(root, padx=10, pady=10)
frame.pack()

tk.Label(frame, text="Placa:").grid(row=0, column=0)
entry_placa = tk.Entry(frame)
entry_placa.grid(row=0, column=1)

tk.Label(frame, text="Tipo:").grid(row=1, column=0)
tipo_var = tk.StringVar()
tipo_menu = ttk.Combobox(frame, textvariable=tipo_var, values=["Carro", "Moto", "Otro"])
tipo_menu.grid(row=1, column=1)
tipo_menu.set("Carro")

tk.Button(frame, text="Registrar Entrada", command=registrar_vehiculo, bg="lightgreen").grid(row=2, column=0, pady=5)
tk.Button(frame, text="Registrar Salida", command=salida_vehiculo, bg="salmon").grid(row=2, column=1, pady=5)
tk.Button(frame, text="Reporte Anual", command=reporte, bg="lightblue").grid(row=3, column=0, columnspan=2, pady=5)


# Lista
tree = ttk.Treeview(root, columns=("Placa", "Tipo", "Hora Entrada"), show="headings")
tree.heading("Placa", text="Placa")
tree.heading("Tipo", text="Tipo")
tree.heading("Hora Entrada", text="Hora Entrada")
tree.pack(padx=10, pady=10)

actualizar_lista()
root.mainloop()

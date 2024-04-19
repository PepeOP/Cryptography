import tkinter as tk
from tkinter import messagebox, simpledialog
from math import gcd
import numpy as np

def matrix_mult_mod(A, B, n):
    # Multiplicación de dos matrices A y B módulo n
    result = (A @ B) % n
    return result

def matrix_inverse_mod(A, n):
    # Cálculo del inverso de una matriz A módulo n usando el método de adjuntos
    det = int(round(np.linalg.det(A))) % n
    if det == 0:
        return None, f"El determinante de la matriz es cero ({det}). No tiene inverso modular."

    if gcd(det, n) != 1:
        return None, f"El determinante ({det}) y el módulo ({n}) no son coprimos. No tiene inverso modular."

    # Calcula el adjunto de A
    adj = np.round(np.linalg.inv(A) * det) % n

    # Calcula el inverso multiplicativo de det
    det_inv = pow(det, -1, n)

    # Calcula la matriz inversa
    A_inv = (adj * det_inv) % n
    return A_inv.astype(int), f"Inverso de la matriz calculado correctamente."

def get_matrix_from_user(size):
    # Obtiene una matriz del usuario a través de una ventana de diálogo
    matrix = []
    for i in range(size):
        row = []
        for j in range(size):
            val = simpledialog.askinteger("Valor", f"Ingrese el valor para la posición ({i+1}, {j+1}):")
            row.append(val)
        matrix.append(row)
    return np.array(matrix)

def handle_multiply():
    global result_label
    size = int(size_var.get())
    modulus = int(modulus_var.get())

    # Obtener las matrices A y B del usuario
    matrix_A = get_matrix_from_user(size)
    matrix_B = get_matrix_from_user(size)

    # Realizar la multiplicación de matrices módulo n
    result_matrix = matrix_mult_mod(matrix_A, matrix_B, modulus)
    result_text = f"Resultado de A x B mod {modulus}:\n{result_matrix}"
    result_label.config(text=result_text)
    messagebox.showinfo("Operación Completa", result_text)

def handle_inverse():
    global result_label
    size = int(size_var.get())
    modulus = int(modulus_var.get())

    # Obtener la matriz A del usuario
    matrix_A = get_matrix_from_user(size)

    # Calcular la inversa de A módulo n
    inverse_matrix, message = matrix_inverse_mod(matrix_A, modulus)
    if inverse_matrix is not None:
        result_text = f"Inverso de A mod {modulus}:\n{inverse_matrix}"
        result_label.config(text=result_text)
        messagebox.showinfo("Operación Completa", message)
    else:
        messagebox.showerror("Error", message)

# Configuración de la ventana principal
root = tk.Tk()
root.title("Multiplicación y Inverso de Matrices Modulares")

# Crear y posicionar elementos en la ventana
tk.Label(root, text="Tamaño de la matriz (n):").pack()
size_var = tk.StringVar(value="2")
size_entry = tk.Entry(root, textvariable=size_var)
size_entry.pack()

tk.Label(root, text="Módulo (n):").pack()
modulus_var = tk.StringVar(value="10")
modulus_entry = tk.Entry(root, textvariable=modulus_var)
modulus_entry.pack()

tk.Button(root, text="Multiplicar A x B", command=handle_multiply).pack()
tk.Button(root, text="Calcular Inverso de A", command=handle_inverse).pack()

result_label = tk.Label(root, text="")
result_label.pack()

root.mainloop()
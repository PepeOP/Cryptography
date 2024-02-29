import tkinter as tk
from tkinter import filedialog, messagebox
import string


def cipher(text, shift):
    """
    Cifra el texto utilizando el método de cifrado por corrimiento.
    :param text: El texto a cifrar.
    :param shift: El número de corrimientos.
    :return: El texto cifrado.
    """
    shifted_text = ''
    for char in text:
        if char.isalpha():
            shifted_char = chr(((ord(char.lower()) - ord('a') + shift) % 26) + ord('a'))
            if char.isupper():
                shifted_char = shifted_char.upper()
            shifted_text += shifted_char
        else:
            shifted_text += char
    return shifted_text


def decipher(text, shift):
    """
    Descifra el texto cifrado utilizando el método de cifrado por corrimiento.
    :param text: El texto cifrado.
    :param shift: El número de corrimientos.
    :return: El texto descifrado.
    """
    return cipher(text, -shift)


def load_and_process_file():
    """
    Carga un archivo de texto, elimina comas y espacios, y lo cifra.
    """
    file_path = filedialog.askopenfilename()
    if file_path:
        with open(file_path, 'r') as file:
            text = file.read()
            text = text.replace(',', '').replace(' ', '')
            shift = int(shift_entry.get())
            ciphered_text = cipher(text, shift)
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, ciphered_text)


def save_file():
    """
    Guarda un archivo de texto.
    """
    file_path = filedialog.asksaveasfilename(defaultextension='.txt')
    if file_path:
        text = result_text.get(1.0, tk.END)
        with open(file_path, 'w') as file:
            file.write(text)


def decipher_and_save_file():
    """
    Descifra un archivo de texto y lo guarda.
    """
    file_path = filedialog.asksaveasfilename(defaultextension='.txt')
    if file_path:
        shift = int(shift_entry.get())
        text = result_text.get(1.0, tk.END)
        deciphered_text = decipher(text, shift)
        with open(file_path, 'w') as file:
            file.write(deciphered_text)


root = tk.Tk()
root.title('Cifrado por corrimiento')

# Frame para el contenido
content_frame = tk.Frame(root)
content_frame.pack(padx=10, pady=10)

# Frame para el resultado
result_frame = tk.Frame(root)
result_frame.pack(padx=10, pady=10)

# Etiqueta y entrada para el número de corrimientos
shift_label = tk.Label(content_frame, text='Número de corrimientos:')
shift_label.grid(row=0, column=0, sticky='w')
shift_entry = tk.Entry(content_frame)
shift_entry.grid(row=0, column=1, sticky='w')

# Botón para cargar el archivo y cifrar
load_and_process_button = tk.Button(content_frame, text='Cargar y Cifrar', command=load_and_process_file)
load_and_process_button.grid(row=1, columnspan=2)

# Botón para guardar el archivo cifrado
save_button = tk.Button(content_frame, text='Guardar Cifrado', command=save_file)
save_button.grid(row=2, columnspan=2)

# Botón para descifrar el archivo y guardarlo
decipher_and_save_button = tk.Button(content_frame, text='Descifrar y Guardar', command=decipher_and_save_file)
decipher_and_save_button.grid(row=3, columnspan=2)

# Texto para mostrar el resultado
result_text = tk.Text(result_frame, height=10, width=50)
result_text.pack()

root.mainloop()
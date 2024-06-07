import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import numpy as np

def load_image(image_path):
    try:
        return Image.open(image_path).convert("RGB")
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {image_path}")
        exit()
    except PermissionError:
        print(f"Error: Permiso denegado para abrir el archivo {image_path}")
        exit()
    except Exception as e:
        print(f"Error al abrir el archivo {image_path}: {e}")
        exit()

def save_image(image_array, path):
    try:
        image = Image.fromarray(image_array)
        image.save(path)
    except Exception as e:
        print(f"Error al guardar el archivo {path}: {e}")
        exit()

def validate_key(key):
    if len(key) not in [8, 16]:
        raise ValueError("La llave debe ser de 8 o 16 bytes")
    if len(key) == 8:
        key = key * 2
    return key

def validate_iv(iv):
    if len(iv) != 16:
        raise ValueError("El vector de inicialización debe ser de 16 bytes")
    return iv

def encrypt_image(image_array, key, iv, mode):
    if mode == AES.MODE_ECB:
        cipher = AES.new(key, mode)
    else:
        cipher = AES.new(key, mode, iv)

    image_bytes = image_array.tobytes()
    padded_image_bytes = pad(image_bytes, AES.block_size)
    encrypted_bytes = cipher.encrypt(padded_image_bytes)
    encrypted_array = np.frombuffer(encrypted_bytes[:len(image_bytes)], dtype=np.uint8).reshape(image_array.shape)
    return encrypted_array, encrypted_bytes

def decrypt_image(encrypted_bytes, image_shape, key, iv, mode):
    if mode == AES.MODE_ECB:
        cipher = AES.new(key, mode)
    else:
        cipher = AES.new(key, mode, iv)

    decrypted_bytes = unpad(cipher.decrypt(encrypted_bytes), AES.block_size)
    decrypted_array = np.frombuffer(decrypted_bytes, dtype=np.uint8).reshape(image_shape)
    return decrypted_array

def select_image():
    global image_path
    image_path = filedialog.askopenfilename(filetypes=[("BMP files", "*.bmp")])
    if image_path:
        image = load_image(image_path)
        img.thumbnail((150, 150))
        img = ImageTk.PhotoImage(image)
        img_label.configure(image=img)
        img_label.image = img

def encrypt():
    try:
        key = validate_key(key_entry.get().encode())
        iv = validate_iv(iv_entry.get().encode())
        mode = modes[mode_var.get()]

        image = load_image(image_path)
        image_array = np.array(image)

        encrypted_array, encrypted_bytes = encrypt_image(image_array, key, iv, mode)
        encrypted_path = os.path.splitext(image_path)[0] + mode_var.get() + "E.bmp"
        save_image(encrypted_array, encrypted_path)
        with open(encrypted_path + '.bin', 'wb') as f:
            f.write(encrypted_bytes)
        messagebox.showinfo("Éxito", f"Imagen cifrada guardada en {encrypted_path}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def decrypt():
    try:
        key = validate_key(key_entry.get().encode())
        iv = validate_iv(iv_entry.get().encode())
        mode = modes[mode_var.get()]

        encrypted_path = image_path
        with open(encrypted_path + '.bin', 'rb') as f:
            encrypted_bytes = f.read()

        image = load_image(image_path)
        image_array = np.array(image)

        decrypted_array = decrypt_image(encrypted_bytes, image_array.shape, key, iv, mode)
        decrypted_path = os.path.splitext(image_path)[0] + mode_var.get() + "D.bmp"
        save_image(decrypted_array, decrypted_path)
        messagebox.showinfo("Éxito", f"Imagen descifrada guardada en {decrypted_path}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Configurar la ventana principal de tkinter
root = tk.Tk()
root.title("Cifrado de Imágenes BMP con AES")
root.geometry("400x400")

modes = {
    "CBC": AES.MODE_CBC,
    "OFB": AES.MODE_OFB,
    "ECB": AES.MODE_ECB,
    "CFB": AES.MODE_CFB,
}

# Elementos de la interfaz
tk.Label(root, text="Llave (8 o 16 bytes):").pack()
key_entry = tk.Entry(root)
key_entry.pack()

tk.Label(root, text="Vector de Inicialización (16 bytes):").pack()
iv_entry = tk.Entry(root)
iv_entry.pack()

tk.Label(root, text="Modo de Operación:").pack()
mode_var = tk.StringVar(root)
mode_var.set("CBC")  # valor por defecto
mode_menu = tk.OptionMenu(root, mode_var, *modes.keys())
mode_menu.pack()

tk.Button(root, text="Seleccionar Imagen", command=select_image).pack()
img_label = tk.Label(root)
img_label.pack()

tk.Button(root, text="Cifrar", command=encrypt).pack()
tk.Button(root, text="Descifrar", command=decrypt).pack()

# Ejecutar la aplicación
root.mainloop()

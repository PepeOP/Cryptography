import os
from PIL import Image
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import numpy as np
import matplotlib.pyplot as plt

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

def main():
    # Solicitar datos al usuario
    input_path = input("Ingrese el path de la imagen BMP: ")
    if not os.path.isfile(input_path):
        print(f"Error: El archivo {input_path} no existe.")
        exit()

    key = validate_key(input("Ingrese la llave (8 o 16 bytes): ").encode())
    iv = validate_iv(input("Ingrese el vector de inicialización (16 bytes): ").encode())

    # Cargar imagen
    image = load_image(input_path)
    image_array = np.array(image)

    # Definir modos de cifrado
    modes = {
        "CBC": AES.MODE_CBC,
        "OFB": AES.MODE_OFB,
        "ECB": AES.MODE_ECB,
        "CFB": AES.MODE_CFB,
    }

    fig, axs = plt.subplots(2, len(modes) + 1, figsize=(15, 8))
    axs[0, 0].imshow(image_array)
    axs[0, 0].set_title('Original')
    axs[0, 0].axis('off')

    for i, (mode_name, mode) in enumerate(modes.items(), start=1):
        # Cifrar imagen
        encrypted_array, encrypted_bytes = encrypt_image(image_array, key, iv, mode)
        encrypted_path = os.path.splitext(input_path)[0] + mode_name + "E.bmp"
        save_image(encrypted_array, encrypted_path)

        # Mostrar imagen cifrada
        axs[0, i].imshow(encrypted_array)
        axs[0, i].set_title(f'Encriptado {mode_name}')
        axs[0, i].axis('off')

        # Descifrar imagen
        decrypted_array = decrypt_image(encrypted_bytes, image_array.shape, key, iv, mode)
        decrypted_path = os.path.splitext(input_path)[0] + mode_name + "D.bmp"
        save_image(decrypted_array, decrypted_path)

        # Mostrar imagen descifrada
        axs[1, i].imshow(decrypted_array)
        axs[1, i].set_title(f'Desencriptado {mode_name}')
        axs[1, i].axis('off')

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()



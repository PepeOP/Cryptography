import secrets
import string

def generate_alphanumeric_key_iv(length):
    characters = string.ascii_letters + string.digits
    key = ''.join(secrets.choice(characters) for _ in range(length))
    iv = ''.join(secrets.choice(characters) for _ in range(length))
    return key, iv

# Generar una llave y un IV de 16 caracteres alfanuméricos
key, iv = generate_alphanumeric_key_iv(16)

print("Llave (key):", key)
print("Vector de inicialización (IV):", iv)

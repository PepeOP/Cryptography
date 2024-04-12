def gcd(a, b):
    """Calcula el máximo común divisor de dos números."""
    while b != 0:
        a, b = b, a % b
    return a

def egcd(a, b):
    """Encuentra el máximo común divisor extendido de dos números."""
    if a == 0:
        return (b, 0, 1)
    else:
       
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)
    
    

def modinv(a, n):
    """Encuentra el inverso multiplicativo de 'a' módulo 'm'."""
    g, x, y = egcd(a, n)
    if g != 1:
        raise Exception('El inverso multiplicativo no existe')
    else:
        return x % n

def affine_encrypt_equation(a, b, n):
    """Imprime la ecuación de cifrado usando el cifrado Affine."""
    print(f"Ecuación de cifrado: E(x) = {a}x + {b} mod {n}")

def affine_decrypt_equation_with_additive_inverse(a, b, n):
    """Imprime la ecuación de descifrado usando el inverso aditivo."""
    a_inv = modinv(a, n)
     
    print(f"Ecuación de descifrado con inverso aditivo: D(x) = {a_inv}(x + {n-b}) mod {n}")

def affine_decrypt_equation_with_multiplicative_inverse(a, b, n):
    """Imprime la ecuación de descifrado usando el inverso multiplicativo."""
    additive_inverse = (n-b)%n
    a_inv = modinv(a, n)
    print(f"Ecuación de descifrado con inverso multiplicativo: D(x) = {a_inv}x + {(a_inv*additive_inverse)%n} mod {n}")

# Pedir al usuario los valores de alfa (a), beta (b) y n (m)
while True:
    try:
        alfa = int(input("Ingrese el valor de alfa (a): "))
        n = int(input("Ingrese el valor de n: "))
        if gcd(alfa, n) != 1:
            print("El valor de alfa (a) debe ser coprimo con n. Intente de nuevo.")
        else:
            break
    except ValueError:
        print("Por favor, ingrese números enteros.")

beta = int(input("Ingrese el valor de beta (b): "))

# Imprimir las ecuaciones de cifrado y descifrado con ambos inversos
affine_encrypt_equation(alfa, beta, n)
affine_decrypt_equation_with_additive_inverse(alfa, beta, n)
affine_decrypt_equation_with_multiplicative_inverse(alfa, beta, n)
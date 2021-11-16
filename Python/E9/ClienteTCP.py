import argparse
import socket
from cryptography.fernet import Fernet

#Argumentos
description="""Modo de uso:  
    clienteTCP.py -msj "Mensaje a enviar" """
parser=argparse.ArgumentParser(description="Port scanning", epilog=description,formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument("-msj", metavar="MSJ", dest="msj", help="Mensaje a enviar", required=True)
params=parser.parse_args()

#Generar el objeto a cifrar
clave=Fernet.generate_key
cipher_suite=Fernet(clave)

#Almacenar clave
file=open("clave.key", "wb") #wb se guarda en bytes
file.write(clave)
file.close()

#Se convierte en bytes el argumento
mensaje=params.msj 
mensajeBytes=mensaje.encode()

#ciframos el mensaje 
msj_cifrado=cipher_suite.encrypt(mensajeBytes)
print("Mensaje enviado:\n", mensaje)

#preparar conexion
TCP_IP="127.0.0.1"
TCP_PORT=5005
BUFFER_SIZE=2048

#Establecer conexion
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(TCP_IP, TCP_PORT)
    s.send(msj_cifrado)
    respuesta=s.recv(BUFFER_SIZE).decode()
    s.close()

print("Respuesta recibida: ",respuesta)
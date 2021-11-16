import socket
import argparse
from cryptography.fernet import Fernet

#Datos de la conexion
TCP_IP="127.0.0.1"
TCP_PORT=5005
BUFFER_SIZE=2048

#Establecer conexion
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((TCP_IP, TCP_PORT))
    s.listen(1)
    (conn, addr)=s.accept()
    print("Dirección de conexion: ", addr)
    while True:
        msj_cifrado = bytes(conn.recv(BUFFER_SIZE))
        if not msj_cifrado:
            break
        conn.send(b"Enterado. Bye!")
        break
    conn.close

#Para generar el objeto a cifrar
#abrir "rb" en bytes
file=open("clave.key","rb")
#La clave será tipo bytes
clave=file.read()
file.close()
cipher_suite=Fernet(clave)

mensajeBytes=cipher_suite.decrypt(msj_cifrado,None)
mensaje=mensajeBytes.decode()
print("Mensaje recibido\n", mensaje)
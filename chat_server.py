import socket
import threading
import logging
import os
from datetime import datetime
from coding import codificar,decodificar,crear_tabla_conversion

#se crea la tabla de codificacion
tabla_conversion=crear_tabla_conversion(8,254,2)

# Define la dirección IP y el puerto del servidor
HOST = '127.0.0.1'
PORT = 5000

# Define una lista de clientes conectados y sus nombres de usuario
clientes = {}
clientes_lock = threading.Lock()

# Define la función para registrar los mensajes del servidor
def log_message(msg, level, nombre):
    now = datetime.now().strftime("%H:%M:%S")
    logging.basicConfig(filename='server.log', level=logging.INFO, filemode='a')
    logging.log(level, f"{now} {nombre} {msg}")

# Define la función de manejo de mensajes
def manejar_mensaje(cliente, mensaje):
    """
    Maneja los mensajes recibidos por un cliente
    y los reenvía a todos los demás clientes.
    """
    global clientes
    nombre = clientes[cliente]
    # Aquí se podría agregar el algoritmo de cifrado
    mensaje_cifrado = codificar(mensaje,tabla_conversion) # Convertir el mensaje a bytes
    with clientes_lock:
        try:
            for c in clientes:
                # Enviar el mensaje a todos los clientes excepto el remitente
                if c != cliente:
                    c.sendall(codificar(nombre+": ",tabla_conversion) + mensaje_cifrado)

            log_message("envió mensaje", logging.INFO, nombre)
        except ConnectionResetError:
            log_message("se ha desconectado", logging.WARNING, nombre)
            del clientes[cliente]
        except Exception as e:
            log_message("Error: "+str(e), logging.WARNING, nombre)
        

# Define la función para manejar la conexión de un nuevo cliente
def manejar_cliente(cliente, direccion):  
    nombre = decodificar(cliente.recv(1024),tabla_conversion)
    try:
        """
        aneja la conexión de un nuevo cliente
        """
        global clientes
        with clientes_lock:
            clientes[cliente] = nombre
        log_message("se ha conectado desde "+str(direccion), logging.INFO, nombre)
        while True:
            mensaje = decodificar(cliente.recv(1024),tabla_conversion)
            if nombre == "admin":
                if mensaje=="/end":
                    manejar_mensaje(cliente, mensaje)
                    log_message("ha cerrado el servidor, hasta la próxima",logging.INFO,nombre)
                    os._exit(0)
            if mensaje == '/quit':
                with clientes_lock:
                    del clientes[cliente]
                log_message("se ha desconectado", logging.INFO, nombre)
                break
            manejar_mensaje(cliente, mensaje)
    except WindowsError:
        log_message("se ha desconectado: se ha forzado su cierre cerrando la terminal",logging.WARNING,nombre)
    except Exception as e:
        log_message(": Error: "+str(e),logging.INFO,nombre)


# Define la función principal del servidor
def main():
    """
    Función principal del servidor
    """
    # Crea un socket TCP/IP
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Vincula el socket a una dirección IP y un puerto
        s.bind((HOST, PORT))
        # Escucha conexiones entrantes
        s.listen()
        log_message("ha iniciado el servidor, escuchando en "+str(HOST)+":"+str(PORT),logging.INFO,"El host")
        #print(f"Servidor escuchando en {HOST}:{PORT}")
        while True:
            # Espera una conexión entrante
            cliente, direccion = s.accept()
            # Crea un hilo para manejar la conexión del cliente
            hilo_cliente = threading.Thread(target=manejar_cliente, args=(cliente, direccion))
            hilo_cliente.start()

if __name__ == '__main__':
    main()

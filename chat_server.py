import socket
import threading

# Define la dirección IP y el puerto del servidor
HOST = '127.0.0.1'
PORT = 5000

# Define una lista de clientes conectados y sus nombres de usuario
clientes = {}
clientes_lock = threading.Lock()

# Define la función de manejo de mensajes
def manejar_mensaje(cliente, mensaje):
    """
    Maneja los mensajes recibidos por un cliente
    y los reenvía a todos los demás clientes.
    """
    global clientes
    nombre = clientes[cliente]
    # Aquí se podría agregar el algoritmo de cifrado
    mensaje_cifrado = mensaje.encode('utf-8') # Convertir el mensaje a bytes
    with clientes_lock:
        for c in clientes:
            # Enviar el mensaje a todos los clientes excepto el remitente
            if c != cliente:
                c.sendall(nombre.encode('utf-8') + b": " + mensaje_cifrado)

# Define la función para manejar la conexión de un nuevo cliente
def manejar_cliente(cliente, direccion):
    """
    Maneja la conexión de un nuevo cliente
    """
    global clientes
    nombre = cliente.recv(1024).decode('utf-8')
    with clientes_lock:
        clientes[cliente] = nombre
    print(f"{nombre} se ha conectado desde {direccion}")
    while True:
        mensaje = cliente.recv(1024).decode('utf-8')
        if mensaje == '/quit':
            with clientes_lock:
                del clientes[cliente]
            print(f"{nombre} se ha desconectado")
            cliente.close()
            break
        manejar_mensaje(cliente, mensaje)

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
        print(f"Servidor escuchando en {HOST}:{PORT}")
        while True:
            # Espera una conexión entrante
            cliente, direccion = s.accept()
            # Crea un hilo para manejar la conexión del cliente
            hilo_cliente = threading.Thread(target=manejar_cliente, args=(cliente, direccion))
            hilo_cliente.start()

if __name__ == '__main__':
    main()

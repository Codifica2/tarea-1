import socket
import threading
import tkinter as tk
from tkinter import ttk

# Define la dirección IP y el puerto del servidor
HOST = '127.0.0.1'
PORT = 5000

# Crea un socket TCP/IP
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conecta el socket al puerto donde el servidor está escuchando
cliente.connect((HOST, PORT))

# Pide al usuario que ingrese su nombre de usuario
nombre = input("Ingresa tu nombre de usuario: ")

# Envía el nombre de usuario al servidor
cliente.sendall(nombre.encode('utf-8'))

# Define la función de manejo de mensajes
def manejar_mensaje(mensaje, remitente):
    """
    Agrega un mensaje a la ventana de chat
    """
    chat.config(state=tk.NORMAL)
    if remitente == nombre:
        chat.insert(tk.END, f"{remitente}: {mensaje}\n", 'derecha')
    else:
        chat.insert(tk.END, f"{remitente}: {mensaje}\n", 'izquierda')
    chat.see(tk.END)
    chat.config(state=tk.DISABLED)

# Define la función para manejar la entrada del usuario
def manejar_entrada(event):
    """
    Maneja la entrada de texto del usuario y la envía al servidor
    """
    mensaje = entrada.get()
    cliente.sendall(mensaje.encode('utf-8'))
    manejar_mensaje(mensaje, nombre)
    entrada.delete(0, tk.END)

# Define la función para recibir mensajes del servidor
def recibir_mensajes():
    """
    Recibe mensajes del servidor y los maneja
    """
    while True:
        mensaje = cliente.recv(1024).decode('utf-8')
        if mensaje == '/quit':
            break
        remitente, mensaje = mensaje.split(':', 1)
        manejar_mensaje(mensaje, remitente)

# Crea la ventana de chat
ventana = tk.Tk()
ventana.title("Chat")
ventana.geometry("600x900")

# Crea un área de texto para mostrar los mensajes
chat = tk.Text(ventana, state=tk.DISABLED, bg="#f5f5f5", font=("Arial", 12))
chat.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Crea un scrollbar para el área de texto
scrollbar = ttk.Scrollbar(chat, orient=tk.VERTICAL, command=chat.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)
chat['yscrollcommand'] = scrollbar.set

# Crea una entrada de texto para que el usuario escriba sus mensajes
frame_entrada = tk.Frame(ventana)
frame_entrada.pack(fill=tk.X, padx=10, pady=10)

# Crea una entrada de texto para que el usuario escriba sus mensajes
entrada = tk.Entry(frame_entrada, font=("Arial", 12), bd=0, bg="#f5f5f5", width=30)
entrada.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
entrada.bind('<Return>', manejar_entrada)

# Crea un botón para enviar mensajes

boton_enviar = tk.Button(frame_entrada, text="Enviar", font=("Arial", 12), bg="#4caf50", fg="white", bd=0, padx=10, pady=5, command=lambda: manejar_entrada(None))
boton_enviar.pack(side=tk.RIGHT)


# Inicia un hilo para recibir mensajes del servidor
hilo_mensajes = threading.Thread(target=recibir_mensajes)
hilo_mensajes.start()

# Inicia la ventana principal
ventana.mainloop()

# Cierra la conexión con el servidor
cliente.sendall('/quit'.encode('utf-8'))
cliente.close()

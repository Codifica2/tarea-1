import socket
import os
import threading
import tkinter as tk
from tkinter import ttk
from coding import codificar,decodificar,crear_tabla_conversion

#se crea la tabla de codificacion
tabla_conversion=crear_tabla_conversion(32,256,2)

# Define la dirección IP y el puerto del servidor
HOST = '127.0.0.1'
PORT = 5000
cliente_cerrado = False

# Crea un socket TCP/IP
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conecta el socket al puerto donde el servidor está escuchando
cliente.connect((HOST, PORT))

# Pide al usuario que ingrese su nombre de usuario
nombre = input("Ingresa tu nombre de usuario: ")

# Envía el nombre de usuario al servidor
nombre_codificado=codificar(nombre, tabla_conversion)
cliente.sendall(nombre_codificado)

def on_closing():
    global cliente_cerrado
    
    # Detener el socket antes de cerrar la ventana
    cliente.sendall(codificar("/quit",tabla_conversion))
    cliente.close()
    
    # Establecer la bandera de cierre
    cliente_cerrado = True
    
    # Cerrar la ventana y salir del programa
    ventana.destroy()

# Define la función de manejo de mensajes
def manejar_mensaje(mensaje, emisor):
    """
    Agrega un mensaje a la ventana de chat
    """
    chat.config(state=tk.NORMAL)
    if emisor == nombre:
        # Yo soy el emisor, así que alineo el texto a la derecha
        chat.tag_config('yo', justify='right')
        chat.insert(tk.END, mensaje + '\n', 'yo')
    else:
        # El otro es el emisor, así que alineo el texto a la izquierda
        chat.tag_config('otro', justify='left')
        chat.insert(tk.END, f"{emisor}: {mensaje}\n",'otro')
    chat.see(tk.END)
    chat.config(state=tk.DISABLED)

# Define la función para manejar la entrada del usuario
def manejar_entrada(event):
    """
    Maneja la entrada de texto del usuario y la envía al servidor
    """
    mensaje = entrada.get()
    if mensaje == '/quit':
        on_closing()
    # Si el mensaje no está vacío, lo envía al servidor
    if mensaje.strip():
        mensaje_codificado=codificar(mensaje,tabla_conversion)
        cliente.sendall(mensaje_codificado)
        manejar_mensaje(mensaje, nombre)
        entrada.delete(0, tk.END)
    else:
        entrada.delete(0, tk.END)

# Define la función para recibir mensajes del servidor
def recibir_mensajes():
    """
    Recibe mensajes del servidor y los maneja
    """
    while True:
        mensaje =decodificar(cliente.recv(1024),tabla_conversion)
        partes = mensaje.split(':')
        emisor = partes[0]
        mensaje = ':'.join(partes[1:])
        manejar_mensaje(mensaje, emisor)

# Crea la ventana de chat
ventana = tk.Tk()
ventana.title("Chat")
ventana.geometry("600x900")

# Crea un frame para el área de texto y la scrollbar
chat_frame = tk.Frame(ventana)
chat_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Crea un área de texto para mostrar los mensajes, espacio a la derecha
chat = tk.Text(chat_frame, font=("Arial", 12), bd=0, bg="#f5f5f5", height="8", width="50", padx=5, pady=5)
chat.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Crea un scrollbar para el área de texto
scrollbar = ttk.Scrollbar(chat_frame, orient=tk.VERTICAL, command=chat.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)


chat['yscrollcommand'] = scrollbar.set

chat.tag_configure('yo', foreground='black', background='#aae5ad')
chat.tag_configure('otro', foreground='black', background='#f0f0f0')

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

# Protocolo para cerrar la ventana
ventana.protocol("WM_DELETE_WINDOW", on_closing)
# Inicia la ventana principal
ventana.mainloop()

# Espera hasta que el cliente sea cerrado
while not cliente_cerrado:
    pass
print("Cliente cerrado")
# Forzar detención del programa
os._exit(0)

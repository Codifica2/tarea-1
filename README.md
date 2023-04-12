# Tarea 1: Codifica2 Chat

## Nombres
* Javier Tralma
* Jorge Moreno

## Descripción

Este programa permite establecer una conexión local mediante el protocolo TCP/IP para enviar y recibir mensajes de texto en tiempo real. Cuenta con una interfaz gráfica intuitiva y fácil de usar que permite a los usuarios comunicarse de forma eficiente. Con este programa, los usuarios pueden mantenerse en contacto de manera efectiva y eficiente, facilitando la comunicación en un entorno de trabajo o en un grupo de amigos.

## Instalación

Primero se debe clonar el repositorio en el entorno local. Mediante la consola de [git en Windows](https://git-scm.com/download/win) (instalar de ser necesario) o la terminal de ubuntu, o cualquier medio equivalente que permita comandos de git, usar el siguiente comando:

```bash
git clone https://github.com/Codifica2/tarea-1.git
```
### Opcional
Si no cuentas con Python o con Pip (sistema de gestión de paquetes de Python) entonces debes realizar algunos de estos pasos:

1. Instalar [Python](https://www.python.org/downloads/)
2. Instalar Pip:
    
    En Windows: 
    * Descarga el archivo get-pip.py desde la página oficial de pip: https://bootstrap.pypa.io/get-pip.py

    * Abre una terminal o línea de comandos en tu sistema operativo y navega hasta el directorio donde descargaste el archivo get-pip.py.

    * Ejecuta el comando python get-pip.py en la terminal.

    * Espera a que se complete la instalación. Al finalizar, deberías ver un mensaje indicando que pip se ha instalado correctamente.

    * Verifica que pip se haya instalado correctamente ejecutando el comando pip --version en la terminal. Si se muestra la versión de pip instalada, significa que la instalación fue exitosa.

    En linux: Linux trae por defecto Python, por lo que en adición, bastaría con usar los siguientes comandos:
    ```bash
    sudo apt-get update
    sudo apt-get install python3-pip
    ```

Luego se deberá instalar la dependencia "tkinter", la cual se instala de la siguiente manera:

```bash
pip install tkinter
```

Con esto ya tenemos todo lo que se requiere para empezar a utilizar nuestro software. Si se desea utilizar otro equipo, para cada uno debe realizar esta configuración. Además, los equipos deben pertenecer a una misma red (entorno local).

## Cómo usar

### Configuración del servidor

Debe haber un equipo hosteando el servidor para permitir que los clientes se comuniquen entre sí. Quien decida hostear el servidor debe abrir la terminal y ejecutar el siguiente comando:
```bash
python3 chat_server.py
```
Por defecto se hostea en la dirección 127.0.0.1 (localhost) y en el puerto 5000. Si se quisiera llevar esta implementación a un entorno no local, entonces se tendría que configurar el firewall para permitir que el puerto se hostee, además de configurar el router para permitir conexiones entrantes. Una vez hecho esto se deberá cambiar en el código la dirección ip por la dirección ip privada de uno y compartir la dirección ip pública con los clientes para que puedan acceder. Sin embargo, como consideramos trabajo netamente local, nos señiremos a seguir con las indicaciones para esta situación.

### Configuración del cliente

Para cada cliente que quiera interactuar, debe abrir una terminal y ejecutar el siguiente comando:

```bash
python3 chat_cliente.py
```

Luego se le solicitará ingresar un nombre de usuario a elección, y una vez enviado, se abrirá el chat en el cual podrá enviar y recibir los mensajes por medio de esta red local.

### Comandos en el chat

* \quit : El cliente que utilice este comando se desconectará del servidor y cerrará su chat. Es el equivalente a salirse con la cruz que se encuentra en la esquina superior derecha.
* \end: Si el usuario llamado "admin" es quien manda este comando, entonces cierra el servidor y la conexión establecida de todos los clientes.



## Cómo contribuir

En caso de que desees contribuir con el desarrollo y mejora de este proyecto, nos encantaría recibir tu ayuda. Puedes contribuir ya sea reportando errores, sugiriendo nuevas características, mejorando la documentación, entre otras formas que se te ocurran.

Si encuentras algún problema o error en el proyecto, puedes crear un issue detallando el problema y cómo reproducirlo. Si tienes alguna idea la cual pueda mejorar el proyecto, crea un issue para discutir la idea y cómo podría implementarse. Si quieres agregar una nueva característica o solucionar algún problema, puedes hacer una pull request con los cambios que propones.

Agradecemos cualquier contribución que puedas hacer para ayudar a mejorar este proyecto.

## Licencia

El proyecto se distribuye bajo la Licencia [MIT](https://choosealicense.com/licenses/mit/), la cual permite a cualquier persona utilizar, copiar, modificar, fusionar, publicar, distribuir, sublicenciar y vender el software sin restricciones, siempre que esta persona incluya el aviso de derechos de autor y la licencia en todas las copias del software. La Licencia MIT es una licencia de software libre que permite el uso del software con propósito libre, incluyendo el uso comercial. Para utilizar el software, se deben aceptar los términos y condiciones de la licencia previamente mencionada.

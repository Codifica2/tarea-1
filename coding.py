def codificar(cadena, tabla_conversion):
    bytes = []
    caracter_desconocido=False
    for caracter in cadena:
        if caracter in tabla_conversion:
            bytes.append(tabla_conversion[caracter]) #se añaden los caracteres como bytes a la lista
        else:
            caracter_desconocido=True
    if caracter_desconocido:
        bytes.append(1)
    else: bytes.append(0) #si hay caracter desconocido se agrega un 1, sino un 0  
    return bytearray(bytes) #se retorna como bytearray para que sea un byte-like object

def decodificar(cadena, tabla_conversion):
    caracter_desconocido=False
    if cadena[len(cadena)-1]==1:
        caracter_desconocido=True #se guarda si hubo o no un caracter desconocido
    cadena.pop(len(cadena)-1) #se borra lo que se agregó en el final de codificar para saber lo anterior
    tabla_contraria=dict()
    for letra,numero in tabla_conversion.items(): #se invierte la tabla
        tabla_contraria[numero]=letra   
    palabra=""
    for caracter in cadena:
        palabra+=tabla_contraria[caracter] #se convierte a string
    return [palabra,caracter_desconocido] 

def crear_tabla_conversion(a,b,n):#con a y b el rango del codigo ascii, y n el numero a sumar a cada uno
                                  #desde 32 a 127 incluye desde el espacio hasta el ~ que es el 126
                                  #hasta el 238 incluye todas las letras con tilde
    tabla=dict()
    for i in range(a, b):
        tabla[chr(i)]=i+n
    #Ejemplo de tabla: tabla=crear_tabla_conversion(32,127,0)
    return tabla
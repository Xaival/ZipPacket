# Tkinter para interfaz gráfica
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog # Abrir y guardar un archivo
from tkinter import messagebox # Importar de cuadros de alerta
import os # Directorio y cosas del sistema
from os.path import exists # Comprueba si existe el archivo o directorio
import shutil # Directorio y comprimidos

root = tk.Tk() # Crear la variable ventana
root.title("ZipPacket") # Título de la ventana
root.iconbitmap(os.path.dirname(__file__)+"\datos\logo.ico") # Mostrar icono
root.config(bg="black", pady=20, padx=20) # Poner fondo negro
root.resizable(False, False) # No permite cambiar el alto y ancho

# Posicionar en el centro de la pantalla
AnchoVentana = 400 # Ancho ventana
AltoVentana = 175 # Alto ventana
PosX = root.winfo_screenwidth() // 2 - AnchoVentana // 2 # Calcular posición horizontal
PosY = root.winfo_screenheight() // 2 - AltoVentana # Calcular posición vertical

root.geometry(str(AnchoVentana)+ "x" +str(AltoVentana)+ "+" +str(PosX)+ "+" +str(PosY)) # Tamaño de ventana y posición inicial


# Funciones-------------------------------------------------------------------

# Seleccionar ruta
def explorador():
    # Cuadro de diálogo de selección de carpeta y poner ruta elegida en el input
    RutaDirectorio.set(filedialog.askdirectory(title="Seleccionar carpeta"))
    
# Comprueba la ruta
def Check(Ruta, Aviso):
    Continua=False
    if Ruta!="":
        if exists(RutaDirectorio.get()): # La ruta existe
            # Si contiene más de 10 documentos y se van a comprimir
            if len(os.listdir(RutaDirectorio.get())) > 10 and Aviso: 
                if messagebox.askyesno(title="¿Continuar?", message="Hay más de 10 que se comprimirán ¿estás seguro?"): Continua=True
            else: Continua=True
        else: messagebox.showwarning(title="Aviso", message='La ruta no es válida')
    else: messagebox.showwarning(title="Aviso", message='El campo de la ruta está vacío')
    return Continua

# Comprimir todo en zips
def Comprimir():
    # Extraer ruta
    Ruta = RutaDirectorio.get()
    # Si pasa el chequeo
    if Check(Ruta, True):
        try:
            # Recorrer carpetas y archivos de la raíz de la ruta
            for document in os.listdir(Ruta):
                # Comprimir
                shutil.make_archive(Ruta+"/"+os.path.splitext(document)[0], 'zip', root_dir=Ruta, base_dir=document)

                # Si es un archivo
                if os.path.isfile(Ruta+"/"+document): os.remove(Ruta+"\\"+document) # Borrar archivo
                else: shutil.rmtree(Ruta+"/"+document) # Borrar carpeta

            messagebox.showinfo(title="Completado", message="La operación se ha completado correctamente")
        except: messagebox.showwarning(title="Error", message='Ha habido un error inesperado durante la ejecución')

# Descomprimir todos los zip
def Descomprimir():
    # Extraer ruta
    Ruta = RutaDirectorio.get()
    # Si pasa el chequeo
    if Check(Ruta, False):
        try:
            # Recorrer .zip de la raíz de la ruta
            for document in os.listdir(Ruta):
                if ".zip" in document:
                    # Descomprimir
                    shutil.unpack_archive(Ruta+"/"+document, extract_dir=Ruta)

                    # Si es un archivo
                    if os.path.isfile(Ruta+"/"+document): os.remove(Ruta+"/"+document) # Borrar archivo
                    else: shutil.rmtree(Ruta+"/"+document) # Borrar carpeta

            messagebox.showinfo(title="Completado", message="La operación se ha completado correctamente")
        except: messagebox.showwarning(title="Error", message='Ha habido un error inesperado durante la ejecución')


# Funciones-------------------------------------------------------------------
# Contenido-------------------------------------------------------------------


# Frame
ContDinamic=tk.Frame(root, bg="black", pady=10, padx=10) # Declarar y configurar
ContDinamic.grid(row="0", column="0", columnspan="2",  sticky="nswe") # Mostrar
ContDinamic.columnconfigure(0, weight=True)
# Ruta del archivo
RutaDirectorio = tk.StringVar()
tk.Label(ContDinamic, text="Ruta del archivo", font=("Roboto", 10, "bold"), bg="black", fg="white").grid(row="0", column="0", sticky="nw", padx=0, columnspan="2")
ttk.Entry(ContDinamic, textvariable=RutaDirectorio).grid(row="1", column="0", sticky="nsew", pady=10)
ttk.Button(ContDinamic, text="...", width=5, command=explorador).grid(row="1", column="1", sticky="nsew", padx=5, pady=10)

# Botón
tk.Button(root, text="Comprimir todo", font=("Roboto", 10, "bold"), pady=5, padx=5, bg="black", fg="white", command=Comprimir).grid(row="1", column="0", sticky="nswe", pady=10, padx=10)
# Botón
tk.Button(root, text="Descomprimir todo", font=("Roboto", 10, "bold"), pady=5, padx=5, bg="black", fg="white", command=Descomprimir).grid(row="1", column="1", sticky="nswe", pady=10, padx=10)

# Configuración de columnas
root.columnconfigure(0, weight=True)
root.columnconfigure(1, weight=True)


# Contenido-------------------------------------------------------------------

root.mainloop() # Abrir ventana
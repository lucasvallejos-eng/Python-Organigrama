"""
The code defines a class tkinterApp, which inherits from the tk.Tk class.
This class represents the main window of the GUI.
In the constructor of tkinterApp, a container frame is created, and
three frames (principal, crear_organigrama, abrir_organigrama)
are initialized and stored in a dictionary called frames.
The show_frame() method is defined to switch between frames.

The principal, crear_organigrama, and abrir_organigrama classes are subclasses of the tk.Frame class.
Each of these classes defines the layout of a particular page of the GUI.
They contain various widgets like labels and buttons, which are used to create the user interface.

Finally, an object of the tkinterApp class is created, which launches the GUI.

Overall, this code demonstrates a simple way to create a multi-page GUI using tkinter in Python.

startpage será el menú principal de el programa
    tendrá tres botones: crear organigrama, modificar organigrama, eliminar organigrama

crear organigrama llevará a otra página, que tendrá:

modificar organigrama llevará a otra página, que tendrá:

eliminar organigrama llevará a otra página, que tendrá:


para añadir nueva pagina:
    definir nueva clase en el main
    definir su layout
    darle un boton de acceso en la pagina deseada
    inicializar en el loop for de principal
"""

import tkinter as tk
from tkinter import filedialog

# from PIL import ImageTk, Image
from tkinter import ttk
import os
from tkinter import messagebox

# librerias para el pdf
from tkinter.ttk import *

# from tkPDFViewer import tkPDFViewer as pdf


LARGEFONT = ("Verdana", 20)
SMALLFONT = ("Verdana", 10)


# centrar ventana del programa
def centrar_ventana(window, ancho, alto):
    # centrar ventana
    # encontrar las dimensiones de la ventana
    pantalla_ancho = window.winfo_screenwidth()
    pantalla_alto = window.winfo_screenheight()

    # encontrar el punto central de la ventana
    centro_x = int(pantalla_ancho / 2 - ancho / 2)
    centro_y = int(pantalla_alto / 2 - alto / 2)

    # posicionar en medio de la pantalla
    window.geometry(f"{ancho}x{alto}+{centro_x}+{centro_y}")


# leer input de campo de texto
def retrieve_input(campos, datos):
    """
    :param campos: lista de los campos de los que leer datos
    :param datos: lista donde se guardan los datos de los campos
    :return:
    """
    for i in range(len(campos)):
        leer = campos[i].get("1.0", 'end-1c')
        datos.append(leer)
        print(f"dato {i}: {datos[i]}")

    # insertar función para guardar el input


# funcion para el boton imagenatras para un aviso


class tkinterApp(tk.Tk):

    # __init__ function for class tkinterApp

    def __init__(self, *args, **kwargs):
        # __init__ function for class Tk
        tk.Tk.__init__(self, *args, **kwargs)

        # creating a container
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # initializing frames to an empty array
        self.frames = {}

        # iterating through a tuple consisting
        # of the different page layouts
        for F in (principal, crear_organigrama, modificar_organigrama, eliminar_organigrama, Manual):
            frame = F(container, self)

            # initializing frame of that object from
            # startpage, page1, page2 respectively with
            # for loop
            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(principal)

    # to display the current frame passed as
    # parameter
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


# cada frame es una página de el programa
# principal es el menú principal de opciones

class principal(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)
        label = ttk.Label(self,
                          text="Programa de organigramas",
                          font=LARGEFONT,
                          anchor="center",
                          justify="center", )

        # putting the grid in its place by using
        # grid
        label.grid(row=0, column=0, padx=10, pady=10, columnspan=2)

        """buffer = ttk.Label(self)
        buffer.grid(row=0, column=0, padx=50, pady=10)"""

        boton_crear = ttk.Button(self, text="Crear organigrama",
                                 command=lambda: controller.show_frame(crear_organigrama))

        # putting the button in its place by
        # using grid
        boton_crear.grid(row=1, column=0, padx=10, pady=10, ipady=15)

        # button to show frame 2 with text layout2
        boton_modificar = ttk.Button(self, text="Modificar Organigrama",
                                     command=lambda: controller.show_frame(modificar_organigrama))
        boton_modificar.grid(row=2, column=0, padx=10, pady=10, ipady=15)

        boton_eliminar = ttk.Button(self, text="Eliminar organigrama",
                                    command=lambda: controller.show_frame(eliminar_organigrama))
        boton_eliminar.grid(row=3, column=0, padx=10, pady=10, ipady=15)

        boton_manual = ttk.Button(self, text="Manual del programa",
                                  command=lambda: controller.show_frame(Manual))
        boton_manual.grid(row=4, column=0, padx=10, pady=10, ipady=15)

        """boton_tema = ttk.Button(self, image=self.imagenclaro,)
        boton_tema.grid(row=4, column=2, padx=10, pady=10)"""


# segunda ventana "Crear organigrama"

"""class crear_organigrama(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        # titulo principal
        label = ttk.Label(self, text="Crear organigrama", font=fuente_grande)
        label.grid(row=0, column=0, padx=10, pady=10, columnspan=2)

        # para este programa se usa una grilla para ubicar los objetos

        # botones
        # botón para ir atrás
        self.imagenatras = tk.PhotoImage(file=r"imagenes/atras_boton.png")
        button1 = ttk.Button(self,
                             image=self.imagenatras,
                             command=lambda: controller.show_frame(principal))

        button1.grid(row=0, column=0, padx=0, pady=0, ipadx=0, ipady=0, sticky="nw")

        # campos de texto
        # campo para el nombre de organigrama
        cuerpotemp = ttk.Label(self, text="Nombre de organigrama:", font=fuente_chica, justify="left")
        cuerpotemp.grid(row=2, column=0, padx=10, pady=10)

        campo_nombre = tk.Text(self, height=1, width=10)
        campo_nombre.grid(row=2, column=1, pady=30, ipadx=20, sticky="w")

        campos = [campo_nombre]
        datos = []

        button2 = ttk.Button(self, text="Confirmar",
                             command=lambda: retrieve_input(campos, datos))
        button2.grid(row=3, column=1, padx=10, sticky="e")
"""

"""
# no funka 
            =(
#funcion para que si no se guarda el organigrama primero pregunte 

def confirmar_salir():
    respuesta = messagebox.askyesno("Confirmar", "¿Desea volver atrás y limpiar todo?")

    if respuesta :
        # Acción al aceptar (volver atrás y limpiar los campos)
        controller.show_frame(principal)
        # Limpia los campos
        campo_nombre.delete('1.0', 'end')
        campo_cargo.delete('1.0', 'end')
        dependencias_combobox.set('')"""


class crear_organigrama(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # self.num_dependencias = None

        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        # título principal
        label = ttk.Label(self, text="Crear organigrama", font=LARGEFONT)
        label.grid(row=0, column=0, padx=10, pady=10, columnspan=2)

        # para este programa se usa una grilla para ubicar los objetos

        # botones
        # botón para ir atrás
        self.imagenatras = tk.PhotoImage(file=r"imagenes/atras_boton.png")
        button1 = ttk.Button(self,
                             image=self.imagenatras,
                             command=lambda: controller.show_frame(principal))  # command = confirmar_salir
        button1.grid(row=0, column=0, padx=0, pady=0, ipadx=0, ipady=0, sticky="nw")

        # campos de texto
        # campo para el nombre de organigrama
        cuerpotemp = ttk.Label(self, text="Nombre de organigrama:", font=SMALLFONT, justify="left")
        cuerpotemp.grid(row=2, column=0, padx=10, pady=10)

        campo_nombre = tk.Text(self, height=1, width=10)
        campo_nombre.grid(row=2, column=1, pady=30, ipadx=20, sticky="w")

        campos = [campo_nombre]
        datos = []

        # Función para mostrar el campo "Cargo Principal"
        def dependencias():
            self.num_dependencias = dependencias_combobox.get()
            dependencias_label.grid(row=4, column=0, padx=10, pady=10, sticky="e")
            dependencias_combobox.grid(row=4, column=1, padx=10, pady=10, sticky="w")

        def mostrar_campo_cargo():
            campo_cargo_label.grid(row=3, column=0, padx=10, pady=10, sticky="e")
            campo_cargo.grid(row=3, column=1, padx=10, pady=10, sticky="w")
            button2.grid(row=4, column=1, padx=10, sticky="e")
            campo_cargo.bind("<Return>", lambda event: dependencias())

        def on_enter(event):
            mostrar_campo_cargo()

        """
        FALTAAAA 
        
        agregar la funcion para que vaya apareciendo las dependencias siguientes y terminar si se elije 
        0 depencias 
        """

        campo_nombre.bind("<Return>", on_enter)

        campo_cargo_label = ttk.Label(self, text="Cargo Principal:", font=SMALLFONT)
        campo_cargo = tk.Text(self, height=1, width=10)

        dependencias_label = ttk.Label(self, text="Dependencias (máximo 5):", font=SMALLFONT)
        dependencias_combobox = ttk.Combobox(self, values=["1", "2", "3", "4", "5"], state="readonly")

        campo_cargo_principal = tk.Text(self, height=1, width=10)
        campos.append(campo_cargo_principal)

        button2 = ttk.Button(self, text="Confirmar", command=lambda: retrieve_input(campos, datos))
        button2.grid(row=4, column=1, padx=10, sticky="e")


# "Modificar organigrama"

def abrir_explorador_archivos():
    ruta_archivo = filedialog.askopenfilename()
    # Hacer algo con la ruta del archivo seleccionado
    print("Archivo seleccionado:", ruta_archivo)


"""
class abrir_organigrama(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Modificar organigrama", font=fuente_grande)
        label.grid(row=0, column=0, padx=50, pady=10)

        # Botón para ir atrás
        self.imagenatras = tk.PhotoImage(file=r"imagenes/atras_boton.png")
        button1 = ttk.Button(self,
                             image=self.imagenatras,
                             command=lambda: controller.show_frame(principal))

        button1.grid(row=0, column=0, padx=0, pady=0, ipadx=0, ipady=0, sticky="nw")

        cuerpotemp = ttk.Label(self, text="Seleccionar organigrama a modificar", font=fuente_chica)
        cuerpotemp.grid(row=2, column=0, padx=10, pady=10)

        lista_archivos = tk.Listbox(self, width=50)


        for name in os.listdir(r"D:\Lucas\POLI - copia\2do semestr\TP"):
            lista_archivos.insert("end", name)

        lista_archivos.grid(row=3, column=0)
"""


class modificar_organigrama(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Modificar organigrama", font=LARGEFONT)
        label.grid(row=0, column=0, padx=50, pady=10)

        # Botón para ir atrás
        self.imagenatras = tk.PhotoImage(file=r"imagenes/atras_boton.png")
        button1 = ttk.Button(self,
                             image=self.imagenatras,
                             command=lambda: controller.show_frame(principal))

        button1.grid(row=0, column=0, padx=0, pady=0, ipadx=0, ipady=0, sticky="nw")

        cuerpotemp = ttk.Label(self, text="Seleccionar organigrama a modificar", font=SMALLFONT)
        cuerpotemp.grid(row=2, column=0, padx=10, pady=10)

        lista_archivos = tk.Listbox(self, width=50)

        """
          #intento fallido de crear unn boton para buscar los organigramas en el explorador 
                                       >=(
          
          # Función para abrir el explorador de archivos
          def abrir_explorador_archivos():
              ruta_archivo = filedialog.askopenfilename()
              # Hacer algo con la ruta del archivo seleccionado
              print("Archivo seleccionado:", ruta_archivo)
          # Cargar la imagen del botón
          imagen_boton = Image.open("imagenes/carpeta.png")
          imagen_boton = imagen_boton.resize((40, 40))  # Ajusta el tamaño de la imagen
          imagen_boton_tk = ImageTk.PhotoImage(imagen_boton)

          # Crear el botón utilizando la imagen
          boton = tk.Button(self, image=imagen_boton_tk, command=abrir_explorador_archivos)
          boton.grid(row=4, column=0, padx=10, pady=10)
          """

        # Función para seleccionar una carpeta
        def seleccionar_carpeta():
            carpeta_seleccionada = filedialog.askdirectory()
            if carpeta_seleccionada:
                limpiar_pantalla()
                archivos_db = [name for name in os.listdir(carpeta_seleccionada) if name.endswith('.db')]
                for name in os.listdir(carpeta_seleccionada):
                    # nombre_base_datos = os.path.splitext(name)[0]  no funciona como debe 
                    lista_archivos.insert("end", name)

        # Función para limpiar la pantalla
        def limpiar_pantalla():
            lista_archivos.delete(0, tk.END)

        # Botón para seleccionar una carpeta
        boton_carpeta = ttk.Button(self, text="Seleccionar Carpeta", command=seleccionar_carpeta)
        boton_carpeta.grid(row=3, column=0, padx=10, pady=10)

        lista_archivos.grid(row=4, column=0)


class eliminar_organigrama(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Eliminar organigrama", font=LARGEFONT)
        label.grid(row=0, column=0, padx=10, pady=10)

        button1 = ttk.Button(self, text="Atrás",
                             command=lambda: controller.show_frame(principal))
        button1.grid(row=1, column=0, padx=0, pady=0)

        cuerpotemp = ttk.Label(self, text="Insertar funcionalidades de modificar aquí", font=SMALLFONT)
        cuerpotemp.grid(row=2, column=0, padx=10, pady=10)


# pagina de manual de instrucciones


"""
class Manual(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Manual", font=fuente_grande)
        label.grid(row=0, column=0, padx=70, pady=10)
"""


class Manual(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = ttk.Label(self, text="Manual", font=LARGEFONT)
        label.pack(pady=10)

        # Botón para ir atrás
        self.imagenatras = tk.PhotoImage(file=r"imagenes/atras_boton.png")
        button1 = ttk.Button(self,
                             image=self.imagenatras,
                             command=lambda: controller.show_frame(principal))
        button1.pack(side="left", padx=10, pady=5)


"""
#intento fallido de mostrar un pdf para las instrucciones 
# y si le pagamos al profe y nos pone 100 ?

        # Frame para mostrar el PDF
        pdf_frame = tk.Frame(self)
        pdf_frame.pack(pady=10)

        # Función para abrir el PDF
        def open_pdf(filepath):
            v = pdf.ShowPdf()
            v.pdf_view(filepath)
            v.pack(side="top", fill="both", expand=True)

        # Método para abrir el PDF por defecto
        def open_default_pdf():
            default_filepath = "ruta_del_archivo.pdf"  # Reemplaza con la ruta real del PDF por defecto
            open_pdf(default_filepath)

        # Botón para abrir el PDF por defecto
        default_button = ttk.Button(pdf_frame, text="Abrir PDF por defecto", command=open_default_pdf)
        default_button.pack(pady=5)
"""

# Driver Code

app = tkinterApp()

centrar_ventana(app, 600, 400)
app.resizable(False, False)

"""imgfondotemp = tk.Image("fondo.jpg")
img2 = imgfondotemp.re"""

app.title("Programa de organigramas")

app.mainloop()

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
# TODO: VALIDAR LOS DATOS PARA QUE ESTEN COMO INDICA EL PDF
import tkinter as tk
from tkinter import ttk
import os
import Clases as clases
import Funciones as funct


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


def es_bisiesto(year):
    # si es divisible entre 4 y no es dividible entre 100
    # o si es divisible entre 400
    bisiesto = False
    if (year % 4 == 0 and year % 100 != 0) or year % 400 == 0:
        bisiesto = True

    return bisiesto


class tkinterApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # crear un contenedor
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # inicializar los frames a un array vacío
        self.frames = {}

        # se comparte entre toda la app
        self.organigrama_actual = tk.StringVar(value="PLACEHOLDER")
        self.lista_dependencias = []  # lista de dependencias del organigrama actual
        self.lista_dependencias_print = []  # la misma lista con formato para imprimir en pantalla
        self.dependencia_actual = tk.StringVar(value="PLACEHOLDER")
        self.cedula_actual = tk.StringVar(value="PLACEHOLDER")

        """"# modo claro/oscuro
        self.tema = tk.StringVar(value="#f0f0f0")
        self.color_botones = tk.StringVar(value="#d6cbcb")
        self.imagen_tema = tk.StringVar(value=r"imagenes/claro.png")
        self.color_letra = tk.StringVar(value="black")"""

        # modo rosado
        self.tema = tk.StringVar(value="#f29ad8")
        self.color_botones = tk.StringVar(value="#f658b8")
        self.imagen_tema = tk.StringVar(value=r"imagenes/claro.png")
        self.color_letra = tk.StringVar(value="#582876")

        # fuentes
        self.fuente_grande = ("Verdana", 30, "bold")
        self.fuente_chica = ("Verdana", 12, "bold")
        self.fuente_botones_grandes = ("Verdana", 15, "bold")
        self.fuente_botones_chicos = ("Verdana", 11, "bold")

        # imagen del boton atras
        self.imagen_atras = tk.StringVar(value=r"imagenes/atras_boton.png")

        # iterating through a tuple consisting
        # of the different page layouts
        for F in (principal, crear_organigrama, abrir_organigrama, eliminar_organigrama, primera_dependencia,
                  menu_abrir, crear_dependencia, eliminar_dependencia):
            frame = F(self.container, self)

            self.frames[F] = frame
            self.current_frame = None
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(principal)

    # to display the current frame passed as
    # parameter

    def show_frame(self, cont):
        if self.current_frame:
            self.current_frame.destroy()

        self.current_frame = cont(self.container, controller=self)
        self.current_frame.grid(row=0, column=0, sticky="nsew")


# cada frame es una página de el programa
# principal es el menú principal de opciones

class principal(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.config(background=controller.tema.get())

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)

        titulo = tk.Label(self,
                          text="Programa de organigramas",
                          font=controller.fuente_grande,
                          anchor="center",
                          justify="center",
                          background=controller.tema.get(),
                          fg=controller.color_letra.get())

        titulo.grid(row=0, column=0, padx=10, pady=10, columnspan=3)

        boton_crear = tk.Button(self, text="Crear organigrama", background=controller.color_botones.get(),
                                fg=controller.color_letra.get(),
                                font=controller.fuente_botones_grandes,
                                command=lambda: controller.show_frame(crear_organigrama))
        boton_crear.grid(row=1, column=0, padx=200, ipadx=10, pady=10, ipady=30, sticky="ew")

        boton_modificar = tk.Button(self, text="Abrir Organigrama", background=controller.color_botones.get(),
                                    fg=controller.color_letra.get(),
                                    font=controller.fuente_botones_grandes,
                                    command=lambda: controller.show_frame(abrir_organigrama))
        boton_modificar.grid(row=2, column=0, padx=200, ipadx=10, pady=10, ipady=30, sticky="ew")

        boton_eliminar = tk.Button(self, text="Eliminar organigrama", background=controller.color_botones.get(),
                                   fg=controller.color_letra.get(),
                                   font=controller.fuente_botones_grandes,
                                   command=lambda: controller.show_frame(eliminar_organigrama))
        boton_eliminar.grid(row=3, column=0, padx=200, ipadx=10, pady=10, ipady=30, sticky="ew")

        self.foto = tk.PhotoImage(file=controller.imagen_tema.get())
        boton_tema = tk.Button(self, image=self.foto, background=controller.color_botones.get(),
                               fg=controller.color_letra.get(),
                               command=lambda: cambiar_tema())
        boton_tema.grid(row=4, column=0, padx=10, pady=10, sticky="e", ipadx=0, ipady=0)

        def cambiar_tema():
            if controller.tema.get() == "#f0f0f0":
                controller.tema.set("#344f72")
                controller.imagen_tema.set(r"imagenes/oscuro.png")
                controller.color_letra.set("white")
                controller.color_botones.set("#273b59")
                controller.imagen_atras.set(r"imagenes/atras_boton_oscuro.png")
                controller.show_frame(principal)
            else:
                controller.tema.set("#f0f0f0")
                controller.imagen_tema.set(r"imagenes/claro.png")
                controller.color_letra.set("black")
                controller.color_botones.set("#d6cbcb")
                controller.imagen_atras.set(r"imagenes/atras_boton.png")
                controller.show_frame(principal)


# segunda ventana "Crear organigrama"
class crear_organigrama(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.config(background=controller.tema.get())

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(2, pad=30)
        # titulo principal
        titulo = tk.Label(self, text="Crear organigrama", background=controller.tema.get(),
                          fg=controller.color_letra.get(),
                          font=controller.fuente_grande, justify="center")
        titulo.grid(row=0, column=0, padx=10, pady=10, columnspan=4)

        # para este programa se usa una grilla para ubicar los objetos

        # botones
        # botón para ir atrás
        self.imagenatras = tk.PhotoImage(file=controller.imagen_atras.get())
        boton_atras = tk.Button(self,
                                image=self.imagenatras,
                                background=controller.color_botones.get(),
                                command=lambda: controller.show_frame(principal))

        boton_atras.grid(row=0, column=0, padx=0, pady=0, ipadx=0, ipady=0, sticky="nw")

        # campos de texto
        # campo para el nombre de organigrama
        label_nombre = tk.Label(self, text="Nombre de organigrama:", background=controller.tema.get(),
                                fg=controller.color_letra.get(),
                                font=controller.fuente_chica, justify="right")
        label_nombre.grid(row=2, column=0, pady=10, sticky="ew")

        campo_nombre = tk.Text(self, height=1, width=10)
        campo_nombre.grid(row=2, column=1, pady=30, ipadx=50, sticky="ew")

        lista_dias = []
        for i in range(1, 32, 1):
            lista_dias.append(str(i))

        lista_meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Setiembre", "Octubre",
                       "Noviembre", "Diciembre"]

        lista_anhos = []
        for i in range(2023, 2000, -1):
            lista_anhos.append(str(i))

        label_fecha = tk.Label(self, text="Fecha de validez:", background=controller.tema.get(),
                               fg=controller.color_letra.get(),
                               font=controller.fuente_chica, justify="right")
        label_fecha.grid(row=3, column=0, padx=10, pady=10)

        # campo_fecha = tk.Text(self, height=1, width=10)
        # campo_fecha.grid(row=3, column=1, pady=30, ipadx=20, sticky="w")

        dia = tk.StringVar(self)
        dia.set("Dia")
        # fecha_dia = tk.OptionMenu(self, dia, *dias_fecha)
        # fecha_dia.grid(row=3, column=1, pady=30, sticky="w")
        dia_input = ttk.Combobox(self, textvariable=dia, background=controller.tema.get(), state="readonly",
                                 values=lista_dias, width=5, )
        dia_input.grid(row=3, column=1, pady=30, sticky="w", ipadx=5)

        mes = tk.StringVar(self)
        mes.set("Mes")
        mes_input = ttk.Combobox(self, textvariable=mes, background=controller.tema.get(), state="readonly",
                                 values=lista_meses, width=10)
        mes_input.grid(row=3, column=1, pady=30, ipadx=5)

        anho = tk.StringVar(self)
        anho.set("Año")
        anho_input = ttk.Combobox(self, textvariable=anho, background=controller.tema.get(), state="readonly",
                                  values=lista_anhos, width=5)
        anho_input.grid(row=3, column=1, pady=30, ipadx=5, sticky="e")

        # Si hay algun error se modifica esta etiqueta para indicar cuál era el error
        self.label_error = tk.Label(self, font=controller.fuente_chica,
                                    background=controller.tema.get(),
                                    fg=controller.color_letra.get(),
                                    justify="center")
        self.label_error.grid(row=4, column=0, pady=30, padx=10, columnspan=2)

        boton_confirmar = tk.Button(self, text="Confirmar", background=controller.color_botones.get(),
                                    fg=controller.color_letra.get(),
                                    font=controller.fuente_botones_chicos,
                                    command=lambda: check_input())
        boton_confirmar.grid(row=4, column=2, padx=10, ipadx=10, ipady=10, sticky="e")

        # leer input de campo de texto
        def check_input():
            leer = campo_nombre.get("1.0", 'end-1c')
            if dia.get() == "Dia" or mes.get() == "Mes" or anho.get() == "Año":
                self.label_error.config(text="Por favor ingrese una fecha.")
                # controller.show_frame(crear_organigrama)
            else:
                valor_dia = int(dia.get())
                valor_mes = mes.get()
                valor_anho = int(anho.get())
                ruta = os.getcwd() + "\\" + leer + ".db"
                if len(leer) > 20:
                    self.label_error.config(text="El nombre debe ser\nmenos de 20 caracteres.")
                    # controller.show_frame(crear_organigrama)
                elif len(leer) < 1:
                    self.label_error.config(text="Por favor ingrese un nombre.")
                    # controller.show_frame(crear_organigrama)
                elif os.path.exists(ruta):
                    self.label_error.config(text="Ese nombre de archivo\nya existe.\nPor favor ingrese otro.")
                    # controller.show_frame(crear_organigrama)
                elif valor_dia == 31 and (valor_mes == ("Abril" or "Junio" or "Setiembre" or "Noviembre")):
                    self.label_error.config(text="Fecha no válida.")
                    # controller.show_frame(crear_organigrama)
                elif valor_dia >= 30 and valor_mes == "Febrero":
                    self.label_error.config(text="Fecha no válida.")
                    # controller.show_frame(crear_organigrama)
                elif (es_bisiesto(valor_anho) is False) and valor_dia == 29 and valor_mes == "Febrero":
                    self.label_error.config(text="Fecha no válida.")
                    # controller.show_frame(crear_organigrama)
                else:
                    # hacer el tipo correcto de dato y mandarlo a la funcion
                    fecha = str(valor_dia) + "/" + valor_mes + "/" + str(valor_anho)
                    org = clases.Organigrama
                    org.ORG = leer
                    org.FEC = fecha
                    funct.CrearOrg(org)
                    self.label_error.config(text="")
                    controller.organigrama_actual.set(leer)
                    controller.show_frame(primera_dependencia)


# sub ventana de crear organigrama
class primera_dependencia(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.config(background=controller.tema.get())

        # organigrama es un objeto de tipo organigrama que se le pasa al frame para poder
        # crear la primera dependencia

        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        self.rowconfigure(2, pad=30)
        # titulo principal
        titulo = tk.Label(self, text="Crear organigrama", font=controller.fuente_grande,
                          background=controller.tema.get(),
                          fg=controller.color_letra.get())
        titulo.grid(row=0, column=0, padx=10, pady=10, columnspan=4)

        cuerpo = tk.Label(self, text="¡Organigrama creado con éxito!", font=controller.fuente_chica,
                          fg=controller.color_letra.get(),
                          background=controller.tema.get(),
                          justify="center")
        cuerpo.grid(row=1, column=0, padx=10, pady=10, columnspan=4)

        label_cuerpo = tk.Label(self, text="Nombre de la primera dependencia:", background=controller.tema.get(),
                                fg=controller.color_letra.get(),
                                font=controller.fuente_chica, justify="left")
        label_cuerpo.grid(row=2, column=0, padx=10, pady=10)

        campo_nombre = tk.Text(self, height=1, width=10)
        campo_nombre.grid(row=2, column=1, pady=30, ipadx=30, sticky="w")

        self.label_error = tk.Label(self, text="", font=controller.fuente_chica,
                                           background=controller.tema.get(),
                                           fg=controller.color_letra.get(),
                                           justify="center")
        self.label_error.grid(row=3, column=0, pady=30, padx=10, columnspan=2)

        boton_confirmar = tk.Button(self, text="Confirmar", background=controller.color_botones.get(),
                                    fg=controller.color_letra.get(),
                                    font=controller.fuente_botones_chicos,
                                    command=lambda: check_input())
        boton_confirmar.grid(row=3, column=3, padx=10, ipadx=10, ipady=10, sticky="e")

        def check_input():
            leer = campo_nombre.get("1.0", 'end-1c')
            if len(leer) > 25:
                self.label_error.config(text="El nombre debe tener\nmenos de 25 caracteres.")
            elif len(leer) < 1:
                self.label_error.config(text="Por favor ingrese un nombre.")
            else:
                base = controller.organigrama_actual.get() + ".db"
                self.label_error.config(text="")
                funct.CrearDep(base, "Principal", leer)
                controller.show_frame(menu_abrir)


# "Abrir organigrama"
class abrir_organigrama(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.config(background=controller.tema.get())

        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=0)

        titulo = tk.Label(self, text="Abrir organigrama", font=controller.fuente_grande,
                          background=controller.tema.get(),
                          fg=controller.color_letra.get(),
                          justify="center", anchor="center")
        titulo.grid(row=0, column=1, padx=10, pady=10, columnspan=3)

        # putting the button in its place by
        # using grid
        # botón para ir atrás
        self.imagenatras = tk.PhotoImage(file=controller.imagen_atras.get())
        boton_atras = tk.Button(self,
                                image=self.imagenatras, background=controller.color_botones.get(),
                                fg=controller.color_letra.get(),
                                command=lambda: controller.show_frame(principal))

        boton_atras.grid(row=0, column=0, padx=0, pady=0, ipadx=0, ipady=0, sticky="nw")

        cuerpo = tk.Label(self, text="Seleccionar organigrama a modificar", font=controller.fuente_chica,
                          fg=controller.color_letra.get(),
                          background=controller.tema.get(),
                          justify="center")
        cuerpo.grid(row=2, column=1, padx=10, pady=10, columnspan=3)

        self.archivo = open("Nombres_Organigrama.txt")
        lista = []
        for objeto in self.archivo:
            lista.append(objeto)

        lista_organigramas = tk.Variable(value=lista)
        listbox_organigramas = tk.Listbox(self, listvariable=lista_organigramas, width=100)
        scroll = tk.Scrollbar(self, orient=tk.VERTICAL, command=listbox_organigramas.yview,
                              background=controller.tema.get(), highlightcolor="black")
        listbox_organigramas.config(yscrollcommand=scroll.set)
        listbox_organigramas.grid(row=3, column=1, sticky="e")
        scroll.grid(row=3, column=2, sticky="w", ipady=55)

        boton_confirmar = tk.Button(self, text="Confirmar", background=controller.color_botones.get(),
                                    fg=controller.color_letra.get(),
                                    font=controller.fuente_botones_chicos,
                                    command=lambda: funcion_abrir())
        boton_confirmar.grid(row=4, column=2, padx=10, sticky="e")

        self.label_error = tk.Label(self, text="", font=controller.fuente_chica,
                                    background=controller.tema.get(),
                                    fg=controller.color_letra.get(),
                                    justify="center")
        self.label_error.grid(row=4, column=1, pady=30, padx=10, sticky="w", columnspan=2)

        def funcion_abrir():
            # tomar el nombre de archivo abierto y guardarlo en organigrama_actual
            selec = listbox_organigramas.curselection()
            if selec == ():
                self.label_error.config(text="Por favor seleccione una base.")
            else:
                leer = listbox_organigramas.get(selec)
                controller.organigrama_actual.set(leer)
                controller.show_frame(menu_abrir)


# ventana del menu de abrir organigrama
class menu_abrir(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.config(background=controller.tema.get())

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)
        self.rowconfigure(5, weight=1)
        self.rowconfigure(6, weight=1)
        self.rowconfigure(7, weight=1)

        # botón para ir atrás
        self.imagenatras = tk.PhotoImage(file=controller.imagen_atras.get())
        boton_atras = tk.Button(self,
                                image=self.imagenatras,
                                background=controller.color_botones.get(),
                                command=lambda: controller.show_frame(abrir_organigrama))

        boton_atras.grid(row=0, column=0, padx=0, pady=0, ipadx=0, ipady=0, sticky="nw")

        self.org = controller.organigrama_actual.get()[:-1]
        self.orgD = self.org + ".db"

        self.titulo = tk.Label(self, text=f"Organigrama {self.org}", font=controller.fuente_grande,
                               background=controller.tema.get(),
                               fg=controller.color_letra.get(),
                               justify="center"
                               )
        self.titulo.grid(row=0, column=0, padx=10, pady=10, columnspan=4)

        cuerpo = tk.Label(self, text="Seleccione una acción", font=controller.fuente_chica,
                          background=controller.tema.get(),
                          fg=controller.color_letra.get(),
                          justify="center",
                          )
        cuerpo.grid(row=1, column=0, padx=10, pady=5, columnspan=4, sticky="n")

        boton_crear_dependencia = tk.Button(self, text="Crear dependencia",
                                            background=controller.color_botones.get(),
                                            fg=controller.color_letra.get(),
                                            font=controller.fuente_botones_chicos,
                                            command=lambda: abrir_crear_dependencia())
        boton_crear_dependencia.grid(row=2, column=0, ipady=7, pady=5, padx=10, sticky="ew")

        boton_eliminar_dependencia = tk.Button(self, text="Eliminar dependencia",
                                               background=controller.color_botones.get(),
                                               fg=controller.color_letra.get(),
                                               font=controller.fuente_botones_chicos,
                                               command=lambda: abrir_eliminar_dependencia())
        boton_eliminar_dependencia.grid(row=3, column=0, ipady=7, pady=5, padx=10, sticky="ew")

        boton_modificar_dependencia = tk.Button(self, text="Modificar dependencia",
                                                background=controller.color_botones.get(),
                                                fg=controller.color_letra.get(),
                                                font=controller.fuente_botones_chicos,
                                                command=lambda: abrir_modificar_dependencia())
        boton_modificar_dependencia.grid(row=4, column=0, ipady=7, pady=5, padx=10, sticky="ew")

        boton_editar_ubicacion_dependencia = tk.Button(self, text="Editar ubicacion de dependencia",
                                                       background=controller.color_botones.get(),
                                                       fg=controller.color_letra.get(),
                                                       font=controller.fuente_botones_chicos,
                                                       command=lambda: abrir_editar_ubic_dependencia())
        boton_editar_ubicacion_dependencia.grid(row=5, column=0, ipady=7, pady=5, padx=10, sticky="ew")

        boton_fusionar_dependencia = tk.Button(self, text="Fusionar dependencias",
                                               background=controller.color_botones.get(),
                                               fg=controller.color_letra.get(),
                                               font=controller.fuente_botones_chicos,
                                               )
        boton_fusionar_dependencia.grid(row=6, column=0, ipady=7, pady=5, padx=10, sticky="ew")

        boton_crear_informe = tk.Button(self, text="Crear informe",
                                        background=controller.color_botones.get(),
                                        fg=controller.color_letra.get(),
                                        font=controller.fuente_botones_chicos,
                                        )
        boton_crear_informe.grid(row=7, column=0, ipady=5, pady=7, padx=10, sticky="ew")

        # columna 2 de botones

        boton_agregar_personas_dependencia = tk.Button(self, text="Agregar personas a dependencia",
                                                       fg=controller.color_letra.get(),
                                                       background=controller.color_botones.get(),
                                                       font=controller.fuente_botones_chicos,
                                                       command=lambda: abrir_agregar_personas_dep())
        boton_agregar_personas_dependencia.grid(row=2, column=1, ipady=7, pady=5, padx=10, sticky="ew")

        boton_modificar_personas = tk.Button(self, text="Modificar personas",
                                             fg=controller.color_letra.get(),
                                             background=controller.color_botones.get(),
                                             font=controller.fuente_botones_chicos,
                                             command=lambda: controller.show_frame(modificar_persona))
        boton_modificar_personas.grid(row=3, column=1, ipady=7, pady=5, padx=10, sticky="ew")

        boton_copiar_organigrama = tk.Button(self, text="Copiar organigrama",
                                             fg=controller.color_letra.get(),
                                             background=controller.color_botones.get(),
                                             font=controller.fuente_botones_chicos,
                                             command=lambda: controller.show_frame(copiar_organigrama))
        boton_copiar_organigrama.grid(row=4, column=1, ipady=7, pady=5, padx=10, sticky="ew")

        boton_graficar_organigrama = tk.Button(self, text="Graficar organigrama",
                                               fg=controller.color_letra.get(),
                                               background=controller.color_botones.get(),
                                               font=controller.fuente_botones_chicos,
                                               command=lambda: controller.show_frame(graficar_organigrama))
        boton_graficar_organigrama.grid(row=5, column=1, ipady=7, pady=5, padx=10, sticky="ew")

        boton_eliminar_organigrama = tk.Button(self, text="Eliminar organigrama",
                                               fg=controller.color_letra.get(),
                                               background=controller.color_botones.get(),
                                               font=controller.fuente_botones_chicos,
                                               command=lambda: controller.show_frame(confirmar_eliminacion))
        boton_eliminar_organigrama.grid(row=6, column=1, ipady=7, pady=5, padx=10, sticky="ew")

        def abrir_crear_dependencia():
            # cargar las dependencias del organigrama actual
            controller.lista_dependencias = funct.DependenciasTodas(self.orgD, "Principal")
            controller.lista_dependencias_print = []

            self.aux = 0
            self.aux_str = ""
            self.rango = len(controller.lista_dependencias)
            for i in range(0, self.rango, 1):
                self.aux = funct.NivelDependencia(self.orgD, controller.lista_dependencias[i])
                self.aux_str = ("   " * self.aux) + controller.lista_dependencias[i]
                controller.lista_dependencias_print.append(self.aux_str)

            controller.show_frame(crear_dependencia)

        def abrir_eliminar_dependencia():
            # cargar las dependencias del organigrama actual
            controller.lista_dependencias = funct.DependenciasTodas(self.orgD, "Principal")
            controller.lista_dependencias_print = []

            self.aux = 0
            self.aux_str = ""
            self.rango = len(controller.lista_dependencias)
            for i in range(0, self.rango, 1):
                self.aux = funct.NivelDependencia(self.orgD, controller.lista_dependencias[i])
                self.aux_str = ("   " * self.aux) + controller.lista_dependencias[i]
                controller.lista_dependencias_print.append(self.aux_str)

            controller.show_frame(eliminar_dependencia)

        def abrir_modificar_dependencia():
            # cargar las dependencias del organigrama actual
            controller.lista_dependencias = funct.DependenciasTodas(self.orgD, "Principal")
            controller.lista_dependencias_print = []

            self.aux = 0
            self.aux_str = ""
            self.rango = len(controller.lista_dependencias)
            for i in range(0, self.rango, 1):
                self.aux = funct.NivelDependencia(self.orgD, controller.lista_dependencias[i])
                self.aux_str = ("   " * self.aux) + controller.lista_dependencias[i]
                controller.lista_dependencias_print.append(self.aux_str)

            controller.show_frame(modificar_dependencia)

        def abrir_editar_ubic_dependencia():
            # cargar las dependencias del organigrama actual
            controller.lista_dependencias = funct.DependenciasTodas(self.orgD, "Principal")
            controller.lista_dependencias_print = []

            self.aux = 0
            self.aux_str = ""
            self.rango = len(controller.lista_dependencias)
            for i in range(0, self.rango, 1):
                self.aux = funct.NivelDependencia(self.orgD, controller.lista_dependencias[i])
                self.aux_str = ("   " * self.aux) + controller.lista_dependencias[i]
                controller.lista_dependencias_print.append(self.aux_str)

            controller.show_frame(editar_ubic_dependencia)

        def abrir_agregar_personas_dep():
            # cargar las dependencias del organigrama actual
            controller.lista_dependencias = funct.DependenciasTodas(self.orgD, "Principal")
            controller.lista_dependencias_print = []

            self.aux = 0
            self.aux_str = ""
            self.rango = len(controller.lista_dependencias)
            for i in range(0, self.rango, 1):
                self.aux = funct.NivelDependencia(self.orgD, controller.lista_dependencias[i])
                self.aux_str = ("   " * self.aux) + controller.lista_dependencias[i]
                controller.lista_dependencias_print.append(self.aux_str)

            controller.show_frame(agregar_personas_dep)


class crear_dependencia(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.config(background=controller.tema.get())

        if controller.organigrama_actual.get()[-1] == "\n":
            self.org = controller.organigrama_actual.get()[:-1]
        else:
            self.org = controller.organigrama_actual.get()

        self.orgD = self.org + ".db"

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)

        # botón para ir atrás
        self.imagenatras = tk.PhotoImage(file=controller.imagen_atras.get())
        boton_atras = tk.Button(self,
                                image=self.imagenatras,
                                background=controller.color_botones.get(),
                                command=lambda: controller.show_frame(menu_abrir))

        boton_atras.grid(row=0, column=0, padx=0, pady=0, ipadx=0, ipady=0, sticky="nw")

        titulo = tk.Label(self, text="Crear dependencia",
                          font=controller.fuente_grande,
                          background=controller.tema.get(),
                          fg=controller.color_letra.get(),
                          justify="center",
                          anchor="center")
        titulo.grid(row=0, column=0, padx=10, pady=10, columnspan=4)

        label_cuerpo = tk.Label(self, text="Nombre de la nueva dependencia:", font=controller.fuente_chica,
                                fg=controller.color_letra.get(),
                                background=controller.tema.get(), justify="left")
        label_cuerpo.grid(row=2, column=0, padx=10, pady=10)

        campo_nombre = tk.Text(self, height=1, width=10)
        campo_nombre.grid(row=2, column=1, pady=30, ipadx=30, sticky="ew")

        self.label_error = tk.Label(self, text="", font=controller.fuente_chica,
                                           background=controller.tema.get(),
                                           fg=controller.color_letra.get(),
                                           justify="center")
        self.label_error.grid(row=4, column=0, pady=30, padx=10, sticky="w", columnspan=2)

        label_lista = tk.Label(self, text="Dependencia de la\ncual va a descender:", font=controller.fuente_chica,
                               fg=controller.color_letra.get(),
                               background=controller.tema.get(), justify="left")
        label_lista.grid(row=3, column=0, padx=10, pady=10)

        dependencia_parent = tk.StringVar(self)
        dependencia_parent.set("Elegir dependencia")
        input_dependencias = ttk.Combobox(self, textvariable=dependencia_parent, background=controller.tema.get(),
                                          state="readonly", values=controller.lista_dependencias_print, width=50)
        input_dependencias.grid(row=3, column=1)

        boton_confirmar = tk.Button(self, text="Confirmar", background=controller.color_botones.get(),
                                    fg=controller.color_letra.get(),
                                    font=controller.fuente_botones_chicos,
                                    command=lambda: check_input())
        boton_confirmar.grid(row=4, column=2, padx=10, ipadx=10, ipady=10, sticky="e")

        def check_input():
            nombre = campo_nombre.get("1.0", 'end-1c')
            superior = controller.lista_dependencias[input_dependencias.current()]
            if len(nombre) > 25:
                self.label_error.config(text="El nombre debe tener\nmenos de 25 caracteres.")
            elif len(nombre) < 1:
                self.label_error.config(text="Por favor ingrese un nombre.")
            elif funct.VerificarExistTabla(self.orgD, nombre):
                self.label_error.config(text="Ese nombre de dependencia ya existe.")
            elif not funct.EspacioDependencia(self.orgD, superior):
                self.label_error.config(
                    text="La dependencia ingresada no puede\ntener mas dependencias sucesoras")
            else:
                self.label_error.config(text="")
                funct.CrearDep(self.orgD, superior, nombre)
                controller.show_frame(exito_operacion)


class eliminar_dependencia(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.config(background=controller.tema.get())

        if controller.organigrama_actual.get()[-1] == "\n":
            self.org = controller.organigrama_actual.get()[:-1]
        else:
            self.org = controller.organigrama_actual.get()

        self.orgD = self.org + ".db"

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        # botón para ir atrás
        self.imagenatras = tk.PhotoImage(file=controller.imagen_atras.get())
        boton_atras = tk.Button(self,
                                image=self.imagenatras,
                                background=controller.color_botones.get(),
                                command=lambda: controller.show_frame(menu_abrir))

        boton_atras.grid(row=0, column=0, padx=0, pady=0, ipadx=0, ipady=0, sticky="nw")

        titulo = tk.Label(self, text="Eliminar dependencia",
                          font=controller.fuente_grande,
                          background=controller.tema.get(),
                          fg=controller.color_letra.get(),
                          justify="center",
                          anchor="center")
        titulo.grid(row=0, column=0, padx=10, pady=10, columnspan=4)

        self.label_confirmar = tk.Label(self, text="", font=controller.fuente_chica,
                                        background=controller.tema.get(),
                                        fg=controller.color_letra.get(),
                                        justify="center")
        self.label_confirmar.grid(row=4, column=0, pady=30, padx=10, sticky="w", columnspan=2)

        label_lista = tk.Label(self, text="Dependencia a eliminar:\nObs: Se eliminarán todas\nlas subdependencias",
                               font=controller.fuente_chica,
                               fg=controller.color_letra.get(),
                               background=controller.tema.get(), justify="center")
        label_lista.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

        dependencia_parent = tk.StringVar(self)
        dependencia_parent.set("Elegir dependencia")
        input_dependencias = ttk.Combobox(self, textvariable=dependencia_parent, background=controller.tema.get(),
                                          state="readonly", values=controller.lista_dependencias_print, width=50)
        input_dependencias.grid(row=3, column=1)

        boton_confirmar = tk.Button(self, text="Siguiente", background=controller.color_botones.get(),
                                    fg=controller.color_letra.get(),
                                    font=controller.fuente_botones_chicos,
                                    command=lambda: confirmar_eliminacion_dep_funct())
        boton_confirmar.grid(row=4, column=3, padx=10, sticky="e")

        def confirmar_eliminacion_dep_funct():
            dep = controller.lista_dependencias[input_dependencias.current()]
            controller.dependencia_actual.set(dep)
            controller.show_frame(confirmar_eliminacion_dep)


class confirmar_eliminacion_dep(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.config(background=controller.tema.get())

        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=0)

        self.imagenatras = tk.PhotoImage(file=controller.imagen_atras.get())
        boton_atras = tk.Button(self,
                                image=self.imagenatras,
                                background=controller.color_botones.get(),
                                command=lambda: controller.show_frame(eliminar_dependencia))

        boton_atras.grid(row=0, column=0, padx=0, pady=0, ipadx=0, ipady=0, sticky="nw")

        if controller.organigrama_actual.get()[-1] == "\n":
            self.org = controller.organigrama_actual.get()[:-1]
        else:
            self.org = controller.organigrama_actual.get()

        self.orgD = self.org + ".db"

        if controller.dependencia_actual.get()[-1] == "\n":
            self.dep = controller.dependencia_actual.get()[:-1]
        else:
            self.dep = controller.dependencia_actual.get()

        cuerpo = tk.Label(self, text=f"Seguro que desea eliminar el departamento {self.dep}",
                          font=controller.fuente_chica,
                          fg=controller.color_letra.get(),
                          background=controller.tema.get(),
                          justify="center")
        cuerpo.grid(row=2, column=1, padx=10, pady=10)

        boton_confirmar = tk.Button(self, text="Confirmar",
                                    background=controller.color_botones.get(),
                                    fg=controller.color_letra.get(),
                                    font=controller.fuente_botones_chicos,
                                    command=lambda: eliminar_dep())
        boton_confirmar.grid(row=4, column=0, padx=10, ipady=20, sticky="ew", columnspan=2)

        def eliminar_dep():
            funct.EliminarDep(self.orgD, self.dep)
            controller.show_frame(exito_operacion)


class modificar_dependencia(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.config(background=controller.tema.get())

        if controller.organigrama_actual.get()[-1] == "\n":
            self.org = controller.organigrama_actual.get()[:-1]
        else:
            self.org = controller.organigrama_actual.get()

        self.orgD = self.org + ".db"

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        # botón para ir atrás
        self.imagenatras = tk.PhotoImage(file=controller.imagen_atras.get())
        boton_atras = tk.Button(self,
                                image=self.imagenatras,
                                background=controller.color_botones.get(),
                                command=lambda: controller.show_frame(menu_abrir))

        boton_atras.grid(row=0, column=0, padx=0, pady=0, ipadx=0, ipady=0, sticky="nw")

        titulo = tk.Label(self, text="Modificar dependencia",
                          font=controller.fuente_grande,
                          background=controller.tema.get(),
                          fg=controller.color_letra.get(),
                          justify="center",
                          anchor="center")
        titulo.grid(row=0, column=0, padx=10, pady=10, columnspan=4)

        self.label_cuerpo = tk.Label(self, text="", font=controller.fuente_chica,
                                     background=controller.tema.get(),
                                     fg=controller.color_letra.get(),
                                     justify="center")
        self.label_cuerpo.grid(row=4, column=0, pady=30, padx=10, sticky="w", columnspan=2)

        label_lista = tk.Label(self, text="Dependencia a modificar",
                               font=controller.fuente_chica,
                               fg=controller.color_letra.get(),
                               background=controller.tema.get(), justify="center")
        label_lista.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

        label_error = tk.Label(self, text="",
                               font=controller.fuente_chica,
                               fg=controller.color_letra.get(),
                               background=controller.tema.get(), justify="center")
        label_error.grid(row=4, column=0, padx=10, pady=10, sticky="ew")

        dependencia = tk.StringVar(self)
        dependencia.set("Elegir dependencia")
        input_dependencias = ttk.Combobox(self, textvariable=dependencia, background=controller.tema.get(),
                                          state="readonly", values=controller.lista_dependencias_print, width=50)
        input_dependencias.grid(row=3, column=1)

        cuerpo = tk.Label(self, text=f"¿Qué modificación desea realizar?\n",
                          font=controller.fuente_chica,
                          fg=controller.color_letra.get(),
                          background=controller.tema.get(),
                          justify="center")
        cuerpo.grid(row=5, column=0, padx=10, pady=10, columnspan=2)

        boton_nombre = tk.Button(self, text="Cambiar nombre de la dependencia",
                                 background=controller.color_botones.get(),
                                 fg=controller.color_letra.get(),
                                 command=lambda: abrir_cambiar_nombre_dependencia())
        boton_nombre.grid(row=6, column=0, padx=10, pady=10, ipady=20, sticky="ew", columnspan=2)

        boton_jefe = tk.Button(self, text="Cambiar jefe de la dependencia",
                               background=controller.color_botones.get(),
                               fg=controller.color_letra.get(),
                               command=lambda: abrir_cambiar_jefe_dependencia())
        boton_jefe.grid(row=7, column=0, padx=10, pady=10, ipady=20, sticky="ew", columnspan=2)

        def abrir_cambiar_nombre_dependencia():
            if dependencia.get() == "Elegir dependencia":
                label_error.config(text="Por favor elija una dependencia.")
            else:
                dep = controller.lista_dependencias[input_dependencias.current()]
                controller.dependencia_actual.set(dep)
                controller.show_frame(cambiar_nombre_dependencia)

        def abrir_cambiar_jefe_dependencia():
            if dependencia.get() == "Elegir dependencia":
                label_error.config(text="Por favor elija una dependencia.")
            else:
                dep = controller.lista_dependencias[input_dependencias.current()]
                controller.dependencia_actual.set(dep)
                controller.show_frame(cambiar_jefe_dependencia)


class cambiar_nombre_dependencia(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.config(background=controller.tema.get())

        if controller.organigrama_actual.get()[-1] == "\n":
            self.org = controller.organigrama_actual.get()[:-1]
        else:
            self.org = controller.organigrama_actual.get()

        self.orgD = self.org + ".db"

        if controller.dependencia_actual.get()[-1] == "\n":
            self.dep = controller.dependencia_actual.get()[:-1]
        else:
            self.dep = controller.dependencia_actual.get()

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        # botón para ir atrás
        self.imagenatras = tk.PhotoImage(file=controller.imagen_atras.get())
        boton_atras = tk.Button(self,
                                image=self.imagenatras,
                                background=controller.color_botones.get(),
                                command=lambda: controller.show_frame(modificar_dependencia))

        boton_atras.grid(row=0, column=0, padx=0, pady=0, ipadx=0, ipady=0, sticky="nw")

        titulo = tk.Label(self, text="Modificar dependencia",
                          font=controller.fuente_grande,
                          background=controller.tema.get(),
                          fg=controller.color_letra.get(),
                          justify="center",
                          anchor="center")
        titulo.grid(row=0, column=0, padx=10, pady=10, columnspan=4)

        label_cuerpo = tk.Label(self, text="Nuevo nombre de la dependencia:", font=controller.fuente_chica,
                                fg=controller.color_letra.get(),
                                background=controller.tema.get(), justify="left")
        label_cuerpo.grid(row=2, column=0, padx=10, pady=10)

        campo_nombre = tk.Text(self, height=1, width=10)
        campo_nombre.grid(row=2, column=1, pady=30, ipadx=30, sticky="w")

        self.label_error_nombre = tk.Label(self, text="", font=controller.fuente_chica,
                                           background=controller.tema.get(),
                                           fg=controller.color_letra.get(),
                                           justify="center")
        self.label_error_nombre.grid(row=4, column=0, pady=30, padx=10, sticky="w", columnspan=2)

        boton_confirmar = tk.Button(self, text="Confirmar", background=controller.color_botones.get(),
                                    fg=controller.color_letra.get(),
                                    font=controller.fuente_botones_chicos,
                                    command=lambda: check_input())
        boton_confirmar.grid(row=4, column=3, padx=10, sticky="e")

        def check_input():
            leer = campo_nombre.get("1.0", 'end-1c')
            if len(leer) > 25:
                self.label_error_nombre.config(text="El nombre debe tener\nmenos de 25 caracteres.")
            elif len(leer) < 1:
                self.label_error_nombre.config(text="Por favor ingrese un nombre.")
            elif funct.VerificarExistTabla(self.orgD, leer):
                self.label_error_nombre.config(text="Ese nombre de dependencia ya existe.")
            else:
                self.label_error_nombre.config(text="")
                funct.ModificarDepNombre(self.orgD, self.dep, leer)
                controller.show_frame(exito_operacion)


class cambiar_jefe_dependencia(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.config(background=controller.tema.get())

        if controller.organigrama_actual.get()[-1] == "\n":
            self.org = controller.organigrama_actual.get()[:-1]
        else:
            self.org = controller.organigrama_actual.get()

        self.orgD = self.org + ".db"

        if controller.dependencia_actual.get()[-1] == "\n":
            self.dep = controller.dependencia_actual.get()[:-1]
        else:
            self.dep = controller.dependencia_actual.get()

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        # botón para ir atrás
        self.imagenatras = tk.PhotoImage(file=controller.imagen_atras.get())
        boton_atras = tk.Button(self,
                                image=self.imagenatras,
                                background=controller.color_botones.get(),
                                command=lambda: controller.show_frame(modificar_dependencia))

        boton_atras.grid(row=0, column=0, padx=0, pady=0, ipadx=0, ipady=0, sticky="nw")

        titulo = tk.Label(self, text="Modificar dependencia",
                          font=controller.fuente_grande,
                          background=controller.tema.get(),
                          fg=controller.color_letra.get(),
                          justify="center",
                          anchor="center")
        titulo.grid(row=0, column=0, padx=10, pady=10, columnspan=4)

        label_CI = tk.Label(self, text="Numero de cedula del nuevo jefe:", font=controller.fuente_chica,
                            fg=controller.color_letra.get(),
                            background=controller.tema.get(), justify="left")
        label_CI.grid(row=2, column=0, padx=10, pady=10)

        campo_CI = tk.Text(self, height=1, width=10)
        campo_CI.grid(row=2, column=1, pady=30, ipadx=30, sticky="w")

        self.label_error = tk.Label(self, text="", font=controller.fuente_chica,
                                    background=controller.tema.get(),
                                    fg=controller.color_letra.get(),
                                    justify="center")
        self.label_error.grid(row=4, column=0, pady=30, padx=10, sticky="w", columnspan=2)

        boton_confirmar = tk.Button(self, text="Confirmar", background=controller.color_botones.get(),
                                    fg=controller.color_letra.get(),
                                    font=controller.fuente_botones_chicos,
                                    command=lambda: check_input())
        boton_confirmar.grid(row=4, column=3, padx=10, sticky="e")

        boton_agregar_pers = tk.Button(self, text="Ir a Agregar Personas", background=controller.color_botones.get(),
                                       fg=controller.color_letra.get(),
                                       command=lambda: controller.show_frame(agregar_personas_dep))

        def check_input():
            CI = campo_CI.get("1.0", 'end-1c')
            if funct.ValPersona(self.orgD, CI):
                if funct.ValPersonaArea(self.orgD, self.dep, CI):
                    if funct.ValidarEsJefe(self.orgD, funct.CodigoPersonaSegunCI(self.orgD, CI)):
                        self.label_error.config(text="Esa persona ya es jefe de otro departamento.")
                    else:
                        self.label_error.config(text="")
                        funct.ModificarDepJefe(self.orgD, self.dep, CI)
                        controller.show_frame(exito_operacion)
                else:
                    self.label_error.config(
                        text="La persona que esta intentando asignar como jefe no pertenece a ese departamento.")
            else:
                self.label_error.config(
                    text="La persona ingresada no está en la base de datos aún.\n¿Desea agregarla ahora?")
                boton_agregar_pers.grid(row=5, column=3, padx=10, sticky="ew")


class editar_ubic_dependencia(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.config(background=controller.tema.get())

        if controller.organigrama_actual.get()[-1] == "\n":
            self.org = controller.organigrama_actual.get()[:-1]
        else:
            self.org = controller.organigrama_actual.get()

        self.orgD = self.org + ".db"

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        # botón para ir atrás
        self.imagenatras = tk.PhotoImage(file=controller.imagen_atras.get())
        boton_atras = tk.Button(self,
                                image=self.imagenatras,
                                background=controller.color_botones.get(),
                                command=lambda: controller.show_frame(menu_abrir))

        boton_atras.grid(row=0, column=0, padx=0, pady=0, ipadx=0, ipady=0, sticky="nw")

        titulo = tk.Label(self, text="Editar ubicación de dependencia",
                          font=controller.fuente_grande,
                          background=controller.tema.get(),
                          fg=controller.color_letra.get(),
                          justify="center",
                          anchor="center")
        titulo.grid(row=0, column=0, padx=10, pady=10, columnspan=4)

        self.label_cuerpo = tk.Label(self, text="", font=controller.fuente_chica,
                                     background=controller.tema.get(),
                                     fg=controller.color_letra.get(),
                                     justify="center")
        self.label_cuerpo.grid(row=4, column=0, pady=30, padx=10, sticky="w", columnspan=2)

        label_lista = tk.Label(self,
                               text="Dependencia a la que va a suceder:n",
                               font=controller.fuente_chica,
                               fg=controller.color_letra.get(),
                               background=controller.tema.get(), justify="center")
        label_lista.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

        dependencia_mover = tk.StringVar(self)
        dependencia_mover.set("Elegir dependencia")
        input_dependencia_mover = ttk.Combobox(self, textvariable=dependencia_mover, background=controller.tema.get(),
                                               state="readonly", values=controller.lista_dependencias_print, width=50)
        input_dependencia_mover.grid(row=3, column=1)

        label_lista_2 = tk.Label(self,
                                 text="Dependencia a mover:\nObs: Esta accion moverá todas las "
                                      "dependencias\nsucesoras al nuevo lugar también.",
                                 font=controller.fuente_chica,
                                 fg=controller.color_letra.get(),
                                 background=controller.tema.get(), justify="center")
        label_lista_2.grid(row=4, column=0, padx=10, pady=10, sticky="ew")

        dependencia_parent = tk.StringVar(self)
        dependencia_parent.set("Elegir dependencia")
        input_dependencias = ttk.Combobox(self, textvariable=dependencia_parent, background=controller.tema.get(),
                                          state="readonly", values=controller.lista_dependencias_print, width=50)
        input_dependencias.grid(row=4, column=1)

        label_error = tk.Label(self,
                               text="",
                               font=controller.fuente_chica,
                               fg=controller.color_letra.get(),
                               background=controller.tema.get(), justify="center")
        label_error.grid(row=5, column=0, padx=10, pady=10, sticky="ew")

        boton_confirmar = tk.Button(self, text="Siguiente", background=controller.color_botones.get(),
                                    fg=controller.color_letra.get(),
                                    font=controller.fuente_botones_chicos,
                                    command=lambda: mover_dependencia())
        boton_confirmar.grid(row=5, column=3, padx=10, sticky="e")

        def mover_dependencia():
            if dependencia_mover.get() == "Elegir dependencia" or dependencia_parent.get() == "Elegir dependencia":
                label_error.config(text="Por favor elija una dependencia.")
            else:
                dep = controller.lista_dependencias[input_dependencia_mover.current()]
                dep_parent = controller.lista_dependencias[input_dependencias.current()]
                if funct.EspacioDependencia(self.orgD, dep_parent):
                    if dep != dep_parent:
                        if funct.DependenciaDesciende(self.orgD, dep_parent, dep):
                            label_error.config(
                                text="No puede mover una dependencia a un lugar que sea sucesora a ella.")
                        else:
                            if funct.DependenciaHijo(self.orgD, dep_parent, dep):
                                label_error.config(text="La Dependencia ya sucede de donde trata de mover.")
                            else:
                                funct.MoverDependencia(self.orgD, dep_parent, dep)
                                controller.show_frame(exito_operacion)
                    else:
                        label_error.config(text="Por favor elija otra dependencia.")
                else:
                    label_error.config(text="La dependencia que eligió ya no admite más dependencias.")


class agregar_personas_dep(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.config(background=controller.tema.get())

        if controller.organigrama_actual.get()[-1] == "\n":
            self.org = controller.organigrama_actual.get()[:-1]
        else:
            self.org = controller.organigrama_actual.get()

        self.orgD = self.org + ".db"

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        # botón para ir atrás
        self.imagenatras = tk.PhotoImage(file=controller.imagen_atras.get())
        boton_atras = tk.Button(self,
                                image=self.imagenatras,
                                background=controller.color_botones.get(),
                                command=lambda: controller.show_frame(menu_abrir))

        boton_atras.grid(row=0, column=0, padx=0, pady=0, ipadx=0, ipady=0, sticky="nw")
        titulo = tk.Label(self, text="Agregar personas a una dependencia",
                          font=controller.fuente_grande,
                          background=controller.tema.get(),
                          fg=controller.color_letra.get(),
                          justify="center",
                          anchor="center")
        titulo.grid(row=0, column=0, padx=10, pady=10, columnspan=4)

        label_lista = tk.Label(self, text="Dependencia a la cual va a pertenecer:", font=controller.fuente_chica,
                               fg=controller.color_letra.get(),
                               background=controller.tema.get(), justify="left")
        label_lista.grid(row=1, column=0, padx=10, pady=10)

        dependencia_parent = tk.StringVar(self)
        dependencia_parent.set("Elegir dependencia")
        input_dependencias = ttk.Combobox(self, textvariable=dependencia_parent, background=controller.tema.get(),
                                          state="readonly", values=controller.lista_dependencias_print, width=50)
        input_dependencias.grid(row=1, column=1)

        label_CI = tk.Label(self, text="Cédula de la persona:", font=controller.fuente_chica,
                            fg=controller.color_letra.get(),
                            background=controller.tema.get(), justify="left")
        label_CI.grid(row=2, column=0, padx=10, pady=10)

        campo_CI = tk.Text(self, height=1, width=10)
        campo_CI.grid(row=2, column=1, pady=30, ipadx=30, sticky="w")

        label_nombre = tk.Label(self, text="Nombre de la persona:", font=controller.fuente_chica,
                                fg=controller.color_letra.get(),
                                background=controller.tema.get(), justify="left")
        label_nombre.grid(row=3, column=0, padx=10, pady=10)

        campo_nombre = tk.Text(self, height=1, width=10)
        campo_nombre.grid(row=3, column=1, pady=30, ipadx=30, sticky="w")

        label_apellido = tk.Label(self, text="Apellido de la persona:", font=controller.fuente_chica,
                                  fg=controller.color_letra.get(),
                                  background=controller.tema.get(), justify="left")
        label_apellido.grid(row=4, column=0, padx=10, pady=10)

        campo_apellido = tk.Text(self, height=1, width=10)
        campo_apellido.grid(row=4, column=1, pady=30, ipadx=30, sticky="w")

        label_telefono = tk.Label(self, text="Numero de telefono de la persona:", font=controller.fuente_chica,
                                  fg=controller.color_letra.get(),
                                  background=controller.tema.get(), justify="left")
        label_telefono.grid(row=5, column=0, padx=10, pady=10)

        campo_telefono = tk.Text(self, height=1, width=10)
        campo_telefono.grid(row=5, column=1, pady=30, ipadx=30, sticky="w")

        label_direccion = tk.Label(self, text="Direccion de domicilio de la persona:", font=controller.fuente_chica,
                                   fg=controller.color_letra.get(),
                                   background=controller.tema.get(), justify="left")
        label_direccion.grid(row=6, column=0, padx=10, pady=10)

        campo_direccion = tk.Text(self, height=1, width=10)
        campo_direccion.grid(row=6, column=1, pady=30, ipadx=30, sticky="w")

        label_salario = tk.Label(self, text="Apellido de la persona:", font=controller.fuente_chica,
                                 fg=controller.color_letra.get(),
                                 background=controller.tema.get(), justify="left")
        label_salario.grid(row=7, column=0, padx=10, pady=10)

        campo_salario = tk.Text(self, height=1, width=10)
        campo_salario.grid(row=7, column=1, pady=30, ipadx=30, sticky="w")

        self.label_error = tk.Label(self, text="", font=controller.fuente_chica,
                                    background=controller.tema.get(),
                                    fg=controller.color_letra.get(),
                                    justify="center")
        self.label_error.grid(row=8, column=0, pady=30, padx=10, sticky="w", columnspan=2)

        boton_confirmar = tk.Button(self, text="Confirmar", background=controller.color_botones.get(),
                                    fg=controller.color_letra.get(),
                                    font=controller.fuente_botones_chicos,
                                    command=lambda: check_input())
        boton_confirmar.grid(row=8, column=3, padx=10, sticky="e")

        def check_input():
            if funct.ValPersona(self.orgD, campo_CI.get("1.0", 'end-1c')):
                self.label_error.config(text="Ya existe esa persona en la base de datos.")
            else:
                persAux = clases.Personas
                persAux.DOC = campo_CI.get("1.0", 'end-1c')
                persAux.NOM = campo_nombre.get("1.0", 'end-1c')
                persAux.APE = campo_apellido.get("1.0", 'end-1c')
                persAux.TEL = campo_telefono.get("1.0", 'end-1c')
                persAux.DIR = campo_direccion.get("1.0", 'end-1c')
                persAux.DEP = controller.lista_dependencias[input_dependencias.current()]
                persAux.SAL = campo_salario.get("1.0", 'end-1c')
                funct.IngresarPersonas(self.orgD, persAux.DEP, persAux)
                controller.show_frame(exito_operacion)


class modificar_persona(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.config(background=controller.tema.get())

        if controller.organigrama_actual.get()[-1] == "\n":
            self.org = controller.organigrama_actual.get()[:-1]
        else:
            self.org = controller.organigrama_actual.get()

        self.orgD = self.org + ".db"

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(2, pad=30)
        # titulo principal
        titulo = tk.Label(self, text="Modificar Persona", background=controller.tema.get(),
                          fg=controller.color_letra.get(),
                          font=controller.fuente_grande, justify="center")
        titulo.grid(row=0, column=0, padx=10, pady=10, columnspan=4)

        # para este programa se usa una grilla para ubicar los objetos

        # botones
        # botón para ir atrás
        self.imagenatras = tk.PhotoImage(file=controller.imagen_atras.get())
        boton_atras = tk.Button(self,
                                image=self.imagenatras,
                                background=controller.color_botones.get(),
                                command=lambda: controller.show_frame(menu_abrir))

        boton_atras.grid(row=0, column=0, padx=0, pady=0, ipadx=0, ipady=0, sticky="nw")

        # campos de texto
        # campo para el nombre de organigrama
        label_CI = tk.Label(self, text="Cedula de la persona:", background=controller.tema.get(),
                            fg=controller.color_letra.get(),
                            font=controller.fuente_chica, justify="left")
        label_CI.grid(row=2, column=0, pady=10)

        campo_CI = tk.Text(self, height=1, width=10)
        campo_CI.grid(row=2, column=1, pady=30, ipadx=50, sticky="w")

        # Si hay algun error se modifica esta etiqueta para indicar cuál era el error
        self.label_error = tk.Label(self, font=controller.fuente_chica,
                                    background=controller.tema.get(),
                                    fg=controller.color_letra.get(),
                                    justify="center")
        self.label_error.grid(row=4, column=1, pady=30, padx=10, sticky="w", columnspan=2)

        boton_confirmar = tk.Button(self, text="Confirmar", background=controller.color_botones.get(),
                                    fg=controller.color_letra.get(),
                                    font=controller.fuente_botones_chicos,
                                    command=lambda: check_input())
        boton_confirmar.grid(row=4, column=2, padx=10, sticky="e")

        boton_ir_a_agregar_pers = tk.Button(self, text="Ir a Añadir Persona", background=controller.color_botones.get(),
                                            fg=controller.color_letra.get(),
                                            command=lambda: ir_a_agregar_pers())

        def check_input():
            if funct.ValPersona(self.orgD, campo_CI.get("1.0", 'end-1c')):
                controller.cedula_actual.set(campo_CI.get("1.0", 'end-1c'))
                controller.show_frame(modificar_persona_val)
            else:
                self.label_error.config(text="Esa persona no está en la base de datos.")
                boton_ir_a_agregar_pers.grid(row=5, column=0, padx=10, sticky="e")

        def ir_a_agregar_pers():
            # cargar las dependencias del organigrama actual
            controller.lista_dependencias = funct.DependenciasTodas(self.orgD, "Principal")
            controller.lista_dependencias_print = []

            self.aux = 0
            self.aux_str = ""
            self.rango = len(controller.lista_dependencias)
            for i in range(0, self.rango, 1):
                self.aux = funct.NivelDependencia(self.orgD, controller.lista_dependencias[i])
                self.aux_str = ("   " * self.aux) + controller.lista_dependencias[i]
                controller.lista_dependencias_print.append(self.aux_str)

            controller.show_frame(agregar_personas_dep)


class modificar_persona_val(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.config(background=controller.tema.get())

        if controller.organigrama_actual.get()[-1] == "\n":
            self.org = controller.organigrama_actual.get()[:-1]
        else:
            self.org = controller.organigrama_actual.get()

        self.orgD = self.org + ".db"

        if controller.cedula_actual.get()[-1] == "\n":
            self.cedula = controller.cedula_actual.get()[:-1]
        else:
            self.cedula = controller.cedula_actual.get()

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        # botón para ir atrás
        self.imagenatras = tk.PhotoImage(file=controller.imagen_atras.get())
        boton_atras = tk.Button(self,
                                image=self.imagenatras,
                                background=controller.color_botones.get(),
                                command=lambda: controller.show_frame(menu_abrir))

        boton_atras.grid(row=0, column=0, padx=0, pady=0, ipadx=0, ipady=0, sticky="nw")
        titulo = tk.Label(self, text="Modificar Persona",
                          font=controller.fuente_grande,
                          background=controller.tema.get(),
                          fg=controller.color_letra.get(),
                          justify="center",
                          anchor="center")
        titulo.grid(row=0, column=0, padx=10, pady=10, columnspan=4)

        cuerpo = tk.Label(self,
                          text=f"¿Qué datos desea cambiar de {funct.NombreApellidoPersonaCI(self.orgD, self.cedula)}?"
                               "\nObs: Para dejarlo igual, deje el campo vacío.",
                          font=controller.fuente_chica,
                          background=controller.tema.get(),
                          fg=controller.color_letra.get(),
                          justify="center",
                          )
        cuerpo.grid(row=1, column=0, padx=10, pady=5, columnspan=4, sticky="n")

        label_CI = tk.Label(self, text="Cedula de la persona:", background=controller.tema.get(),
                            fg=controller.color_letra.get(),
                            font=controller.fuente_chica, justify="left")
        label_CI.grid(row=2, column=0, pady=10)

        campo_CI = tk.Text(self, height=1, width=10)
        campo_CI.grid(row=2, column=1, pady=30, ipadx=50, sticky="w")

        label_nombre = tk.Label(self, text="Nombre de la persona:", font=controller.fuente_chica,
                                fg=controller.color_letra.get(),
                                background=controller.tema.get(), justify="left")
        label_nombre.grid(row=3, column=0, padx=10, pady=10)

        campo_nombre = tk.Text(self, height=1, width=10)
        campo_nombre.grid(row=3, column=1, pady=30, ipadx=30, sticky="w")

        label_apellido = tk.Label(self, text="Apellido de la persona:", font=controller.fuente_chica,
                                  fg=controller.color_letra.get(),
                                  background=controller.tema.get(), justify="left")
        label_apellido.grid(row=4, column=0, padx=10, pady=10)

        campo_apellido = tk.Text(self, height=1, width=10)
        campo_apellido.grid(row=4, column=1, pady=30, ipadx=30, sticky="w")

        label_telefono = tk.Label(self, text="Numero de telefono de la persona:", font=controller.fuente_chica,
                                  fg=controller.color_letra.get(),
                                  background=controller.tema.get(), justify="left")
        label_telefono.grid(row=5, column=0, padx=10, pady=10)

        campo_telefono = tk.Text(self, height=1, width=10)
        campo_telefono.grid(row=5, column=1, pady=30, ipadx=30, sticky="w")

        label_direccion = tk.Label(self, text="Direccion de domicilio de la persona:", font=controller.fuente_chica,
                                   fg=controller.color_letra.get(),
                                   background=controller.tema.get(), justify="left")
        label_direccion.grid(row=6, column=0, padx=10, pady=10)

        campo_direccion = tk.Text(self, height=1, width=10)
        campo_direccion.grid(row=6, column=1, pady=30, ipadx=30, sticky="w")

        label_salario = tk.Label(self, text="Apellido de la persona:", font=controller.fuente_chica,
                                 fg=controller.color_letra.get(),
                                 background=controller.tema.get(), justify="left")
        label_salario.grid(row=7, column=0, padx=10, pady=10)

        campo_salario = tk.Text(self, height=1, width=10)
        campo_salario.grid(row=7, column=1, pady=30, ipadx=30, sticky="w")

        self.label_error = tk.Label(self, text="", font=controller.fuente_chica,
                                    background=controller.tema.get(),
                                    fg=controller.color_letra.get(),
                                    justify="center")
        self.label_error.grid(row=8, column=0, pady=30, padx=10, sticky="w", columnspan=2)

        boton_confirmar = tk.Button(self, text="Confirmar", background=controller.color_botones.get(),
                                    fg=controller.color_letra.get(),
                                    font=controller.fuente_botones_chicos,
                                    command=lambda: check_input())
        boton_confirmar.grid(row=8, column=3, padx=10, sticky="e")

        def check_input():
            if funct.ValPersona(self.orgD, campo_CI.get("1.0", 'end-1c')):
                self.label_error.config(text="No se puede repetir la cédula de otra persona.")
            else:
                if (campo_CI.get("1.0", 'end-1c') == "") is False:
                    funct.ModificarCedulaPersona(self.orgD, self.cedula, campo_CI.get("1.0", 'end-1c'))

                if (campo_nombre.get("1.0", 'end-1c') == "") is False:
                    funct.ModificarNombrePersona(self.orgD, self.cedula, campo_nombre.get("1.0", 'end-1c'))

                if (campo_apellido.get("1.0", 'end-1c') == "") is False:
                    funct.ModificarApellidoPersona(self.orgD, self.cedula, campo_apellido.get("1.0", 'end-1c'))

                if (campo_telefono.get("1.0", 'end-1c') == "") is False:
                    funct.ModificarTelefonoPersona(self.orgD, self.cedula, campo_telefono.get("1.0", 'end-1c'))

                if (campo_direccion.get("1.0", 'end-1c') == "") is False:
                    funct.ModificarDireccionPersona(self.orgD, self.cedula, campo_direccion.get("1.0", 'end-1c'))

                if (campo_salario.get("1.0", 'end-1c') == "") is False:
                    funct.ModificarSalarioPersona(self.orgD, self.cedula, campo_salario.get("1.0", 'end-1c'))

                controller.show_frame(exito_operacion)


class copiar_organigrama(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.config(background=controller.tema.get())

        if controller.organigrama_actual.get()[-1] == "\n":
            self.org = controller.organigrama_actual.get()[:-1]
        else:
            self.org = controller.organigrama_actual.get()

        self.orgD = self.org + ".db"

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(2, pad=30)
        # titulo principal
        titulo = tk.Label(self, text="Copiar organigrama", background=controller.tema.get(),
                          fg=controller.color_letra.get(),
                          font=controller.fuente_grande, justify="center")
        titulo.grid(row=0, column=0, padx=10, pady=10, columnspan=4)

        # para este programa se usa una grilla para ubicar los objetos

        # botones
        # botón para ir atrás
        self.imagenatras = tk.PhotoImage(file=controller.imagen_atras.get())
        boton_atras = tk.Button(self,
                                image=self.imagenatras,
                                background=controller.color_botones.get(),
                                command=lambda: controller.show_frame(menu_abrir))

        boton_atras.grid(row=0, column=0, padx=0, pady=0, ipadx=0, ipady=0, sticky="nw")

        cuerpo = tk.Label(self, text="Esta función copia la estructura de un organigrama sin las personas",
                          font=controller.fuente_chica,
                          background=controller.tema.get(),
                          fg=controller.color_letra.get(),
                          justify="center",
                          )
        cuerpo.grid(row=1, column=0, padx=10, pady=5, columnspan=4, sticky="n")

        label_nombre = tk.Label(self, text="Nombre para el nuevo organigrama:", background=controller.tema.get(),
                                fg=controller.color_letra.get(),
                                font=controller.fuente_chica, justify="left")
        label_nombre.grid(row=2, column=0, pady=10)

        campo_nombre = tk.Text(self, height=1, width=10)
        campo_nombre.grid(row=2, column=1, pady=30, ipadx=50, sticky="w")

        # Si hay algun error se modifica esta etiqueta para indicar cuál era el error
        self.label_error = tk.Label(self, font=controller.fuente_chica,
                                    background=controller.tema.get(),
                                    fg=controller.color_letra.get(),
                                    justify="center")
        self.label_error.grid(row=4, column=1, pady=30, padx=10, sticky="w", columnspan=2)

        boton_confirmar = tk.Button(self, text="Confirmar", background=controller.color_botones.get(),
                                    fg=controller.color_letra.get(),
                                    font=controller.fuente_botones_chicos,
                                    command=lambda: check_input())
        boton_confirmar.grid(row=4, column=2, padx=10, sticky="e")

        def check_input():
            nombre = campo_nombre.get("1.0", 'end-1c')
            ruta = nombre + ".db"
            if nombre == "":
                self.label_error.config(text="Por favor ingrese un nombre.")
            elif len(nombre) > 25:
                self.label_error.config(text="El nombre debe tener menos de 25 caracteres.")
            elif os.path.exists(ruta):
                self.label_error.config(text="Ya existe una base de datos con ese nombre")
            else:
                self.label_error.config(text="")
                funct.CopiarOrg(self.orgD, nombre)
                controller.show_frame(exito_operacion)


class graficar_organigrama(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.config(background=controller.tema.get())

        if controller.organigrama_actual.get()[-1] == "\n":
            self.org = controller.organigrama_actual.get()[:-1]
        else:
            self.org = controller.organigrama_actual.get()

        self.orgD = self.org + ".db"

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(2, pad=30)

        self.imagenatras = tk.PhotoImage(file=controller.imagen_atras.get())
        boton_atras = tk.Button(self,
                                image=self.imagenatras,
                                background=controller.color_botones.get(),
                                command=lambda: controller.show_frame(menu_abrir))

        boton_atras.grid(row=0, column=0, padx=0, pady=0, ipadx=0, ipady=0, sticky="nw")

        # titulo principal
        titulo = tk.Label(self, text="Graficar Organigrama", background=controller.tema.get(),
                          fg=controller.color_letra.get(),
                          font=controller.fuente_grande, justify="center")
        titulo.grid(row=0, column=0, padx=10, pady=10, columnspan=4)

        boton_completo = tk.Button(self, text="Organigrama completo", background=controller.color_botones.get(),
                                   fg=controller.color_letra.get(),
                                   font=controller.fuente_chica, justify="center",
                                   command=lambda: graficar_org_completo())
        boton_completo.grid(row=1, column=0, padx=10, pady=10, columnspan=2, sticky="ew")

        boton_parcial = tk.Button(self, text="Organigrama parcial", background=controller.color_botones.get(),
                                  fg=controller.color_letra.get(),
                                  font=controller.fuente_chica, justify="center",
                                  command=lambda: funct_graficar_org_parcial())
        boton_parcial.grid(row=2, column=0, padx=10, pady=10, columnspan=2, sticky="ew")

        def graficar_org_completo():
            funct.GraficarOrganigrama(self.orgD, "Principal")
            controller.show_frame(exito_operacion)

        def funct_graficar_org_parcial():
            # cargar las dependencias del organigrama actual
            controller.lista_dependencias = funct.DependenciasTodas(self.orgD, "Principal")
            controller.lista_dependencias_print = []

            self.aux = 0
            self.aux_str = ""
            self.rango = len(controller.lista_dependencias)
            for i in range(0, self.rango, 1):
                self.aux = funct.NivelDependencia(self.orgD, controller.lista_dependencias[i])
                self.aux_str = ("   " * self.aux) + controller.lista_dependencias[i]
                controller.lista_dependencias_print.append(self.aux_str)

            controller.show_frame(graficar_org_parcial)


class graficar_org_parcial(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.config(background=controller.tema.get())

        if controller.organigrama_actual.get()[-1] == "\n":
            self.org = controller.organigrama_actual.get()[:-1]
        else:
            self.org = controller.organigrama_actual.get()

        self.orgD = self.org + ".db"

        self.imagenatras = tk.PhotoImage(file=controller.imagen_atras.get())
        boton_atras = tk.Button(self,
                                image=self.imagenatras,
                                background=controller.color_botones.get(),
                                command=lambda: controller.show_frame(menu_abrir))

        boton_atras.grid(row=0, column=0, padx=0, pady=0, ipadx=0, ipady=0, sticky="nw")

        titulo = tk.Label(self, text="Graficar Organigrama", background=controller.tema.get(),
                          fg=controller.color_letra.get(),
                          font=controller.fuente_grande, justify="center")
        titulo.grid(row=0, column=0, padx=10, pady=10, columnspan=4)

        self.label_cuerpo = tk.Label(self, text="¿Desde qué dependencia se va a graficar?",
                                     font=controller.fuente_chica,
                                     background=controller.tema.get(),
                                     fg=controller.color_letra.get(),
                                     justify="center")
        self.label_cuerpo.grid(row=4, column=0, pady=30, padx=10, sticky="w", columnspan=2)

        label_lista = tk.Label(self, text="Dependencia",
                               font=controller.fuente_chica,
                               fg=controller.color_letra.get(),
                               background=controller.tema.get(), justify="center")
        label_lista.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

        label_error = tk.Label(self, text="",
                               font=controller.fuente_chica,
                               fg=controller.color_letra.get(),
                               background=controller.tema.get(), justify="center")
        label_error.grid(row=4, column=0, padx=10, pady=10, sticky="ew")

        dependencia = tk.StringVar(self)
        dependencia.set("Elegir dependencia")
        input_dependencias = ttk.Combobox(self, textvariable=dependencia, background=controller.tema.get(),
                                          state="readonly", values=controller.lista_dependencias_print, width=50)
        input_dependencias.grid(row=3, column=1)

        boton_confirmar = tk.Button(self, text="Confirmar", background=controller.color_botones.get(),
                                    fg=controller.color_letra.get(),
                                    font=controller.fuente_botones_chicos,
                                    command=lambda: imprimir_org_parcial())
        boton_confirmar.grid(row=8, column=3, padx=10, sticky="e")

        def imprimir_org_parcial():
            if dependencia.get() == "Elegir dependencia":
                label_error.config(text="Por favor elija una dependencia.")
            else:
                dep = controller.lista_dependencias[input_dependencias.current()]
                funct.GraficarOrganigrama(self.orgD, dep)
                controller.show_frame(exito_operacion)


# esta pantalla se utiliza para confirmar éxito de todas las operaciones de menu_abrir
class exito_operacion(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.config(background=controller.tema.get())

        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=0)

        """titulo = tk.Label(self, text="Eliminar organigrama", font=controller.fuente_grande,
                          background=controller.tema.get(),
                          fg=controller.color_letra.get(),
                          justify="center", anchor="center")
        titulo.grid(row=0, column=1, padx=10, pady=10)"""

        cuerpo = tk.Label(self, text=f"Operación realizada con éxito",
                          font=controller.fuente_chica,
                          fg=controller.color_letra.get(),
                          background=controller.tema.get(),
                          justify="center")
        cuerpo.grid(row=2, column=1, padx=10, pady=10)

        boton_volver = tk.Button(self, text="Volver",
                                 background=controller.color_botones.get(),
                                 fg=controller.color_letra.get(),
                                 command=lambda: controller.show_frame(menu_abrir))
        boton_volver.grid(row=4, column=0, padx=10, ipady=20, sticky="ew", columnspan=2)


class eliminar_organigrama(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.config(background=controller.tema.get())

        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=0)

        titulo = tk.Label(self, text="Eliminar organigrama", font=controller.fuente_grande,
                          background=controller.tema.get(),
                          fg=controller.color_letra.get(),
                          justify="center", anchor="center")
        titulo.grid(row=0, column=1, padx=10, pady=10)

        # putting the button in its place by
        # using grid
        # botón para ir atrás
        self.imagenatras = tk.PhotoImage(file=controller.imagen_atras.get())
        boton_atras = tk.Button(self,
                                image=self.imagenatras, background=controller.color_botones.get(),
                                fg=controller.color_letra.get(),
                                command=lambda: controller.show_frame(principal))

        boton_atras.grid(row=0, column=0, padx=0, pady=0, ipadx=0, ipady=0, sticky="nw")

        cuerpo = tk.Label(self, text="Seleccionar organigrama a eliminar", font=controller.fuente_chica,
                          fg=controller.color_letra.get(),
                          background=controller.tema.get(),
                          justify="center")
        cuerpo.grid(row=2, column=1, padx=10, pady=10)

        self.archivo = open("Nombres_Organigrama.txt")
        lista = []
        for objeto in self.archivo:
            lista.append(objeto)

        lista_organigramas = tk.Variable(value=lista)
        listbox_organigramas = tk.Listbox(self, listvariable=lista_organigramas, width=100)
        scroll = tk.Scrollbar(self, orient=tk.VERTICAL, command=listbox_organigramas.yview,
                              background=controller.tema.get(), highlightcolor="black")
        listbox_organigramas.config(yscrollcommand=scroll.set)
        listbox_organigramas.grid(row=3, column=1, sticky="e")
        scroll.grid(row=3, column=2, sticky="w", ipady=55)

        boton_confirmar = tk.Button(self, text="Confirmar", background=controller.color_botones.get(),
                                    fg=controller.color_letra.get(),
                                    font=controller.fuente_botones_chicos,
                                    command=lambda: funcion_abrir())
        boton_confirmar.grid(row=4, column=2, padx=10, sticky="e")

        self.label_error = tk.Label(self, text="", font=controller.fuente_chica,
                                    background=controller.tema.get(),
                                    fg=controller.color_letra.get(),
                                    justify="center")
        self.label_error.grid(row=4, column=1, pady=30, padx=10, sticky="w", columnspan=2)

        def funcion_abrir():
            # tomar el nombre de archivo abierto y guardarlo en organigrama_actual
            selec = listbox_organigramas.curselection()
            if selec == ():
                self.label_error.config(text="Por favor seleccione una base.")
            else:
                leer = listbox_organigramas.get(selec)
                controller.organigrama_actual.set(leer)
                controller.show_frame(confirmar_eliminacion)


class confirmar_eliminacion(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.config(background=controller.tema.get())

        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=0)

        titulo = tk.Label(self, text="Eliminar organigrama", font=controller.fuente_grande,
                          background=controller.tema.get(),
                          fg=controller.color_letra.get(),
                          justify="center", anchor="center")
        titulo.grid(row=0, column=1, padx=10, pady=10)

        # putting the button in its place by
        # using grid
        # botón para ir atrás
        self.imagenatras = tk.PhotoImage(file=controller.imagen_atras.get())
        boton_atras = tk.Button(self,
                                image=self.imagenatras, background=controller.color_botones.get(),
                                fg=controller.color_letra.get(),
                                command=lambda: controller.show_frame(principal))

        boton_atras.grid(row=0, column=0, padx=0, pady=0, ipadx=0, ipady=0, sticky="nw")
        if controller.organigrama_actual.get()[-1] == "\n":
            self.org = controller.organigrama_actual.get()[:-1]
        else:
            self.org = controller.organigrama_actual.get()

        cuerpo = tk.Label(self, text=f"¿Seguro que desea eliminar el organigrama {self.org}?",
                          font=controller.fuente_chica,
                          fg=controller.color_letra.get(),
                          background=controller.tema.get(),
                          justify="center")
        cuerpo.grid(row=2, column=1, padx=10, pady=10)

        boton_confirmar = tk.Button(self, text="Eliminar", background=controller.color_botones.get(),
                                    fg=controller.color_letra.get(),
                                    font=controller.fuente_botones_chicos,
                                    command=lambda: funcion_eliminar())
        boton_confirmar.grid(row=4, column=0, padx=10, ipady=20, sticky="ew", columnspan=2)

        def funcion_eliminar():
            self.orgD = self.org + ".db"
            funct.EliminarOrg(self.orgD)
            funct.EliminarNombres(self.org)
            controller.organigrama_actual.set("")
            controller.show_frame(exito_eliminar)


class exito_eliminar(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.config(background=controller.tema.get())

        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=0)

        titulo = tk.Label(self, text="Eliminar organigrama", font=controller.fuente_grande,
                          background=controller.tema.get(),
                          fg=controller.color_letra.get(),
                          justify="center", anchor="center")
        titulo.grid(row=0, column=1, padx=10, pady=10)

        cuerpo = tk.Label(self, text=f"Organigrama eliminado exitosamente.",
                          font=controller.fuente_chica,
                          fg=controller.color_letra.get(),
                          background=controller.tema.get(),
                          justify="center")
        cuerpo.grid(row=2, column=1, padx=10, pady=10)

        boton_volver = tk.Button(self, text="Volver al menú principal",
                                 background=controller.color_botones.get(),
                                 fg=controller.color_letra.get(),
                                 command=lambda: controller.show_frame(principal))
        boton_volver.grid(row=4, column=0, padx=10, ipady=20, sticky="ew", columnspan=2)


# Driver Code
app = tkinterApp()
centrar_ventana(app, 700, 500)
app.resizable(False, False)
"""imgfondotemp = tk.Image("fondo.jpg")
img2 = imgfondotemp.re"""
app.title("Programa de organigramas")
app.mainloop()

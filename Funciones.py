from Clases import *
import os
import sqlite3
import shutil
import graphviz as gv

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
"""
Indice de Funciones
"""
def Menu(Base):
    print("""Bienvenido al Organigrama""",Base,"""
1-Crear Dependencia
2-Eliminar Dependencia (Falta tambien eliminar las personas de dichas dependencias)
3-Modificar Dependencia 
4-Editar Ubicacion de Dependencia
5-Agregar Personas Dependencia 
6-Eliminar Persona 
7-Modificar Persona
8-Asignar Persona a Dependencia
9-Asignar personas a dependencia en masa
10-Generar Informe (En curso)
11-Copiar Organigrama 
12-Graficar Organigrama 
13-Eliminar Organigrama
14-Salir""")

#Funcion que imprime todos los nombres del txt Nombres_Organigramas
def ImprimirNombres():
    archivo=open('Nombres_Organigrama.txt','r')
    x=1
    for Linea in archivo:
        print(x,"-",Linea,end="")
        x+=1

    archivo.close()

#Funcion que elimina un nombre del archivo de txt Nombre_organigramas
def EliminarNombres(Base):
    archivo = open('Nombres_Organigrama.txt', 'r')
    Lineas=archivo.readlines()
    Base2=Base+"\n"
    if Base2 in Lineas:
        Lineas.remove(Base2)
    archivo.close()
    archivo = open('Nombres_Organigrama.txt', 'w')
    for dato in Lineas:
        archivo.write(dato)
    archivo.close()

#Funcion que escribe un nuevo nombre de una base de datos en el txt Nombre_organigramas
def AgregarNombres(Base):
    archivo = open('Nombres_Organigrama.txt', 'a')
    archivo.write(Base+"\n")
    archivo.close()

#Funcion que Crea una base de datos nueva
def CrearOrg(ORG_AUX):

    #Se procede a crear una tabla principal para guardar los datos de codigo, nombre y fecha
    ruta = ORG_AUX.ORG + ".db"
    conexion = sqlite3.connect(ruta)
    cursor=conexion.cursor()
    CodAux=CodigoLibreOrg()
    CodAux2=str(CodAux)

    while len(CodAux2)!=5:
        CodAux2="0"+CodAux2

    cursor.execute("CREATE TABLE Principal (COD TEXT , ORG TEXT, FEC TEXT, DepPadre TEXT, Dep1 TEXT, Dep2 TEXT, Dep3 TEXT, Dep4 TEXT, Dep5 TEXT, Nivel INTEGER)")
    cursor.execute("INSERT INTO Principal (COD, ORG, FEC, Nivel ) VALUES ( ?, ?, ?, ?)",(CodAux2 , ORG_AUX.ORG , ORG_AUX.FEC, 0))
    #Se Procede a crear otra tabla principal con los datos de todos los empleados de la empresa
    cursor.execute("CREATE TABLE Personas (COD TEXT, DOC TEXT , APE TEXT, NOM TEXT, TEL TEXT, DIR TEXT, DEP TEXT, SAL INTEGER, Jefe INTEGER)")
    #Anadimos al archivo txt de los codigos el codigo que acabamos de ingresar al organigrama
    AgregarCodOrg(CodAux)
    AgregarNombres(ORG_AUX.ORG)
    #Se guarda y despues se cierra la conexion con la base de datos
    conexion.commit()
    conexion.close()
    return ORG_AUX.ORG

#Funcion que devuelve True si es que se llego al maximo numero de Organigramas a crear
def CodigoLibreOrgVer():
    archivo=open('Codigo_actual.txt','r')
    Numeros=archivo.readlines()
    bool=False
    if 100000>len(Numeros):
            bool=True
    return bool

# Funcion que devuelve el primer numero disponible que encuentre en el TXT Codigo_actual
def CodigoLibreOrg():
    archivo = open('Codigo_actual.txt', 'r')
    NumerosTxt = archivo.readlines()
    Numeros=[]
    x=0
    for x in NumerosTxt:
        Numeros.append(int(x))

    for x in range(100000):
        if x not in Numeros:
            break

    return x

#Funcion que actualiza el archivo Codigo_Actual dependiendo de cual base es la que se esta modificando para mantener hasta 100000 organigramas
def EliminarCodOrg(Numero):
    archivo = open('Codigo_actual.txt', 'r')
    Lineas = archivo.readlines()
    Numero2 = str(Numero) + "\n"
    if Numero2 in Lineas:
        Lineas.remove(Numero2)
    archivo.close()
    archivo = open('Codigo_actual.txt', 'w')
    for dato in Lineas:
        archivo.write(dato)
    archivo.close()
    return True

def AgregarCodOrg(Numero):
    archivo = open('Codigo_actual.txt', 'a')
    archivo.write(str(Numero)+"\n")
    archivo.close()

#Funcion que verifica si es que existe espacio en la dependencia ingresada
def EspacioDependencia(Base,Tabla):
    conexion = sqlite3.connect(Base)
    cursor = conexion.cursor()
    Data = cursor.execute(f'SELECT Dep1, Dep2, Dep3, Dep4, Dep5 FROM "{Tabla}"')
    dato=Data.fetchone()
    bool=False

    if dato[0]==None:
        bool=True

    if dato[1] == None:
        bool = True

    if dato[2] == None:
        bool = True

    if dato[3] == None:
        bool = True

    if dato[4] == None:
        bool = True

    conexion.close()
    return bool

#Funcion que devuelve un numero que este disponible para la tabla
def CodigoParaTabla(Base):
    conexion = sqlite3.connect(Base)
    cursor = conexion.cursor()
    Dependencias=DependenciasCasiTodas(Base,'Principal')
    codigos=[]
    for Dep in Dependencias:
        Data=cursor.execute(f'SELECT COD FROM "{Dep}"')
        dato=Data.fetchone()
        codigos.append(int(dato[0]))

    NuevoCod=1
    while True:
        if NuevoCod not in codigos:
            break
        else:
            NuevoCod+=1

    NuevoCodL=str(NuevoCod)
    while len(NuevoCodL)<3:
        NuevoCodL="0"+NuevoCodL
    conexion.close()
    return NuevoCodL

#Funcion que crea una nueva dependencia en una base de datos X dependiendo de los datos ingresados
def CrearDep(Base,Tabla,Dep):
    conexion=sqlite3.connect(Base)
    cursor=conexion.cursor()
    Data=cursor.execute(f'SELECT Dep1 ,Dep2, Dep3, Dep4, Dep5, Nivel FROM "{Tabla}"')
    #Verificar que la Dependencia que se esta intentando ingresar no Exista

    #Verificacion de que a la tabla X aun se le pueden asignar dependencias subsecuentes
    dato=Data.fetchone()
    DepP=Dep+"P"
    while True:

        if dato[0]==None :
            cursor.execute(f'UPDATE "{Tabla}" SET Dep1= (?) ',(Dep,))
            cursor.execute(f'CREATE TABLE "{Dep}" (COD TEXT , NOM TEXT, CODRES TEXT, DepPadre TEXT, Dep1 TEXT, Dep2 TEXT, Dep3 TEXT, Dep4 TEXT, Dep5 TEXT, Nivel INTEGER)')
            cursor.execute(f'INSERT INTO "{Dep}" (COD, NOM, DepPadre, Nivel) VALUES ( ? , ? , ? , ?)',(CodigoParaTabla(Base),Dep,Tabla,dato[5]+1 ))
            cursor.execute(f'CREATE TABLE "{DepP}" (COD TEXT, DOC TEXT , APE TEXT, NOM TEXT, TEL TEXT, DIR TEXT, DEP  TEXT, SAL REAL, Jefe INTEGER)')
            print("Dependencia creada con exito!")
            break

        if dato[1]==None :
            cursor.execute(f'UPDATE "{Tabla}" SET Dep2= (?) ', (Dep,))
            cursor.execute(f'CREATE TABLE "{Dep}" (COD REAL , NOM TEXT, CODRES TEXT, DepPadre TEXT, Dep1 TEXT, Dep2 TEXT, Dep3 TEXT, Dep4 TEXT, Dep5 TEXT, Nivel INTEGER)')
            cursor.execute(f'INSERT INTO "{Dep}" (COD, NOM, DepPadre, Nivel) VALUES ( ? , ? , ? , ?)',(CodigoParaTabla(Base),Dep,Tabla,dato[5]+1 ))
            cursor.execute(f'CREATE TABLE "{DepP}" (COD TEXT, DOC TEXT , APE TEXT, NOM TEXT, TEL TEXT, DIR TEXT, DEP  TEXT, SAL REAL, Jefe INTEGER)')
            print("Dependencia creada con exito!")
            break

        if dato[2]==None :
            cursor.execute(f'UPDATE "{Tabla}" SET Dep3= (?) ', (Dep,))
            cursor.execute(f'CREATE TABLE "{Dep}" (COD REAL , NOM TEXT, CODRES TEXT, DepPadre TEXT, Dep1 TEXT, Dep2 TEXT, Dep3 TEXT, Dep4 TEXT, Dep5 TEXT, Nivel INTEGER)')
            cursor.execute(f'INSERT INTO "{Dep}" (COD, NOM, DepPadre, Nivel) VALUES ( ? , ? , ? , ?)',(CodigoParaTabla(Base),Dep,Tabla,dato[5]+1 ))
            cursor.execute(f'CREATE TABLE "{DepP}" (COD TEXT, DOC TEXT , APE TEXT, NOM TEXT, TEL TEXT, DIR TEXT, DEP  TEXT, SAL REAL, Jefe INTEGER)')
            print("Dependencia creada con exito!")
            break

        if dato[3]==None :
            cursor.execute(f'UPDATE "{Tabla}" SET Dep4= (?) ', (Dep,))
            cursor.execute(f'CREATE TABLE "{Dep}" (COD REAL , NOM TEXT, CODRES TEXT, DepPadre TEXT, Dep1 TEXT, Dep2 TEXT, Dep3 TEXT, Dep4 TEXT, Dep5 TEXT, Nivel INTEGER)')
            cursor.execute(f'INSERT INTO "{Dep}" (COD, NOM, DepPadre, Nivel) VALUES ( ? , ? , ? , ?)',(CodigoParaTabla(Base),Dep,Tabla,dato[5]+1 ))
            cursor.execute(f'CREATE TABLE "{DepP}" (COD TEXT, DOC TEXT , APE TEXT, NOM TEXT, TEL TEXT, DIR TEXT, DEP  TEXT, SAL REAL, Jefe INTEGER)')
            print("Dependencia creada con exito!")
            break

        if dato[4]==None :
            cursor.execute(f'UPDATE "{Tabla}" SET Dep5= (?) ', (Dep,))
            cursor.execute(f'CREATE TABLE "{Dep}" (COD REAL , NOM TEXT, CODRES TEXT, DepPadre TEXT, Dep1 TEXT, Dep2 TEXT, Dep3 TEXT, Dep4 TEXT, Dep5 TEXT, Nivel INTEGER)')
            cursor.execute(f'INSERT INTO "{Dep}" (COD, NOM, DepPadre, Nivel) VALUES ( ? , ? , ? , ?)',(CodigoParaTabla(Base),Dep,Tabla,dato[5]+1 ))
            cursor.execute(f'CREATE TABLE "{DepP}" (COD TEXT, DOC TEXT , APE TEXT, NOM TEXT, TEL TEXT, DIR TEXT, DEP  TEXT, SAL REAL, Jefe INTEGER)')
            print("Dependencia creada con exito!")
            break

        print("No se pueden asignar mas Dependencias a ",Tabla)
        break

    conexion.commit()
    conexion.close()
    return True

#Funcion que verifica si es que exise una tabla dada en la base de datos
def VerificarExistTabla(Base,Tabla):
    conexion = sqlite3.connect(Base)
    cursor = conexion.cursor()
    tabla = cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    bool=False
    for x in tabla:
        if x[0]==Tabla:
            bool=True

    conexion.close()
    return bool

#Funcion que modifica los datos de un departamento X, Cambia el nombre
def ModificarDepNombre(Base,Dep,nombre):
    conexion=sqlite3.connect(Base)
    cursor=conexion.cursor()
    Data=cursor.execute(f'SELECT COD, NOM, CODRES, DepPadre FROM "{Dep}"')
    dato=Data.fetchone()
    #Cambiamos el nombre que hay en la tabla
    cursor.execute(f'UPDATE "{Dep}" SET NOM="{nombre}"')

    #Cambiamos el nombre en las dependencias Sucesoras
    Data3= cursor.execute(f'SELECT Dep1 ,Dep2, Dep3, Dep4, Dep5 FROM "{Dep}"')
    dato3=Data3.fetchone()
    if dato3[0]!=None:
        cursor.execute(f'UPDATE "{dato3[0]}" SET DepPadre= "{nombre}" ')

    if dato3[1] != None:
        cursor.execute(f'UPDATE "{dato3[1]}" SET DepPadre= "{nombre}" ')

    if dato3[2] != None:
        cursor.execute(f'UPDATE "{dato3[2]}" SET DepPadre= "{nombre}" ')

    if dato3[3] != None:
        cursor.execute(f'UPDATE "{dato3[3]}" SET DepPadre= "{nombre}" ')

    if dato3[4] != None:
        cursor.execute(f'UPDATE "{dato3[4]}" SET DepPadre= "{nombre}" ')

    # Cambiamos el nombre de la Tabla
    DepP=Dep+"P"
    nombreP=nombre+"P"

    cursor.execute(f'ALTER TABLE "{Dep}" RENAME TO "{nombre}"')
    cursor.execute(f'ALTER TABLE "{DepP}" RENAME TO "{nombreP}"')

    #Actualizamos el nombre del departamento en departamento padre
    Data = cursor.execute(f'SELECT Dep1 ,Dep2, Dep3, Dep4, Dep5 FROM "{dato[3]}"')
    dato2 = Data.fetchone()

    if dato2[0] == Dep:
        cursor.execute(f'UPDATE "{dato[3]}" SET Dep1= "{nombre}" ')

    if dato2[1] == Dep:
        cursor.execute(f'UPDATE "{dato[3]}" SET Dep2= "{nombre}" ')

    if dato2[2] == Dep:
        cursor.execute(f'UPDATE "{dato[3]}" SET Dep3= "{nombre}" ')

    if dato2[3] == Dep:
        cursor.execute(f'UPDATE "{dato[3]}" SET Dep4= "{nombre}" ')

    if dato2[4] == Dep:
        cursor.execute(f'UPDATE "{dato[3]}" SET Dep5= "{nombre}" ')

    print("El nombre del departamento ha sido cambiado con exito!")

    conexion.commit()
    cursor.close()

#Funcion que devielve el codigo de una persona segun la cedula ingresada
def CodigoPersonaSegunCI(Base,CI):
    conexion = sqlite3.connect(Base)
    cursor = conexion.cursor()
    Data=cursor.execute(f'SELECT COD FROM Personas WHERE DOC="{CI}"')
    Cod=Data.fetchone()
    conexion.close()
    return Cod[0]

# Funcion que valida si un empleado es un jefe de algun area, validandolo segun su codigo
def ValidarEsJefe(Base,Cod):
    conexion = sqlite3.connect(Base)
    cursor = conexion.cursor()
    Data=cursor.execute(f'SELECT Jefe FROM Personas WHERE COD="{Cod}"')
    dato=Data.fetchone()

    if int(dato[0])==0:
        bool=False
    else:
        bool=True

    conexion.close()
    return bool

#Funcion que verifica que la CI ingresada pertenezca a alguien de esa dependencia
def ValPersonaArea(Base,Tabla,CI):
    conexion = sqlite3.connect(Base)
    cursor = conexion.cursor()
    Data=cursor.execute(f'SELECT DEP FROM Personas WHERE DOC="{CI}"')
    dato=Data.fetchone()
    if dato[0]==Tabla:
        bool=True
    else:
        bool=False

    return bool

#Funcion que modifica los datos de un departamento X, Cambia Jefe
def ModificarDepJefe(Base,Dep,CI):
    conexion=sqlite3.connect(Base)
    cursor=conexion.cursor()
    Data=cursor.execute(f'SELECT CODRES FROM "{Dep}"')
    dato=Data.fetchone()
    cursor.execute(f'UPDATE Personas SET Jefe=0 WHERE COD="{dato[0]}"')
    cursor.execute(f'UPDATE Personas SET Jefe=1 WHERE DOC="{CI}"')
    DepP=Dep+"P"
    cursor.execute(f'UPDATE "{DepP}" SET Jefe=0 WHERE COD="{dato[0]}"')
    cursor.execute(f'UPDATE "{DepP}" SET Jefe=1 WHERE DOC="{CI}"')

    COD=CodigoPersonaSegunCI(Base,CI)
    cursor.execute(f'UPDATE "{Dep}" SET CODRES="{COD}"')
    conexion.commit()
    conexion.close()

#Funcion que verifica si alguna de las dependencias es sucesora de la otra
def DependenciaHijo(Base,Dep1,Dep2):
    conexion = sqlite3.connect(Base)
    cursor = conexion.cursor()
    bool=False
    Data=cursor.execute(f'SELECT Dep1, Dep2, Dep3, Dep4, Dep5 FROM "{Dep1}"')
    dato=Data.fetchone()
    if dato[0]==Dep1:
        bool=True

    if dato[1] == Dep1:
        bool=True

    if dato[2] == Dep1:
        bool=True

    if dato[3] == Dep1:
        bool=True

    if dato[4] == Dep1:
        bool=True

    Data = cursor.execute(f'SELECT Dep1, Dep2, Dep3, Dep4, Dep5 FROM "{Dep2}"')
    dato = Data.fetchone()
    if dato[0] == Dep2:
        bool = True

    if dato[1] == Dep2:
        bool = True

    if dato[2] == Dep2:
        bool = True

    if dato[3] == Dep2:
        bool = True

    if dato[4] == Dep2:
        bool = True
    return bool

#Funcion Recursiva que verifica si es que Dep2 esta en algun lugar de las Dependencias sucesoras de Dep1
def DependenciaDesciende(Base,Dep1,Dep2):
    conexion = sqlite3.connect(Base)
    cursor = conexion.cursor()
    Data = cursor.execute(f'SELECT Dep1, Dep2, Dep3, Dep4, Dep5 FROM "{Dep1}"')
    dato=Data.fetchone()
    bool=False

    while True:

        if (dato[0]!=None):
            if (dato[0]==Dep2):
                bool=True
                break
            boolAux = DependenciaDesciende(Base,dato[0],Dep2)
            if boolAux:
                bool=True
                break

        if (dato[1] != None):
            if dato[1] == Dep2:
                bool = True
                break
            boolAux = DependenciaDesciende(Base, dato[1], Dep2)
            if boolAux:
                bool = True
                break

        if (dato[2] != None):
            if dato[2] == Dep2:
                bool = True
                break
            boolAux = DependenciaDesciende(Base, dato[2], Dep2)

            if boolAux:
                bool = True
                break

        if (dato[3] != None):
            if dato[3] == Dep2:
                bool = True
                break

            boolAux = DependenciaDesciende(Base, dato[3], Dep2)
            if boolAux:
                bool = True
                break

        if (dato[4] != None):
            if dato[4] == Dep2:
                bool = True
                break

            boolAux = DependenciaDesciende(Base, dato[4], Dep2)
            if boolAux:
                bool = True
                break

        break

    return bool

#funcion que mueve la dependencia 1 para que sea sucesora de la dependencia 2
def MoverDependencia(Base,Dep1,Dep2):
    conexion = sqlite3.connect(Base)
    cursor = conexion.cursor()
    #Primero lo que hacemos es modificar la dependencia padre del primero para eliminarla del lugar
    Data=cursor.execute(f'SELECT DepPadre FROM "{Dep1}"')
    DepPadre=Data.fetchone()
    Data=cursor.execute(f'SELECT Dep1, Dep2, Dep3, Dep4, Dep5 FROM "{DepPadre[0]}"')
    dato=Data.fetchone()

    if dato[0]==Dep1:
        cursor.execute(f'UPDATE "{DepPadre[0]}" SET Dep1=NULL')

    if dato[1] == Dep1:
        cursor.execute(f'UPDATE "{DepPadre[0]}" SET Dep2=NULL')

    if dato[2] == Dep1:
        cursor.execute(f'UPDATE "{DepPadre[0]}" SET Dep3=NULL')

    if dato[3] == Dep1:
        cursor.execute(f'UPDATE "{DepPadre[0]}" SET Dep4=NULL')

    if dato[4] == Dep1:
        cursor.execute(f'UPDATE "{DepPadre[0]}" SET Dep5=NULL')

    #luego lo que hacemos es Asignarle al primer departamento el segundo como padre

    cursor.execute(f'UPDATE "{Dep1}" SET DepPadre="{Dep2}"')

    #Por ultimo le asignamos al segundo departamenteo su nueva decendencia
    Data=cursor.execute(f'SELECT Dep1, Dep2, Dep3, Dep4, Dep5 FROM "{Dep2}"')
    dato=Data.fetchone()
    while True:

        if dato[0]==None:
            cursor.execute(f'UPDATE "{Dep2}" SET Dep1="{Dep1}"')
            break

        if dato[1]== None:
            cursor.execute(f'UPDATE "{Dep2}" SET Dep2="{Dep1}"')
            break

        if dato[2]== None:
            cursor.execute(f'UPDATE "{Dep2}" SET Dep3="{Dep1}"')
            break

        if dato[3]== None:
            cursor.execute(f'UPDATE "{Dep2}" SET Dep4="{Dep1}"')
            break

        if dato[4]== None:
            cursor.execute(f'UPDATE "{Dep2}" SET Dep5="{Dep1}"')
            break

    conexion.commit()
    conexion.close()

    #Luego de mover y guardar actualizamos los niveles de las dependencias que movimos}
    ActualizarNiveles(Base,Dep1)


#Funcion que luego de un movimiento actualiza todos los campos de niveles de la dependencia movida
def ActualizarNiveles(Base,Tabla):
    conexion = sqlite3.connect(Base)
    cursor = conexion.cursor()
    Data=cursor.execute(f'SELECT DepPadre FROM "{Tabla}"')
    dato=Data.fetchone()
    Data=cursor.execute(f'SELECT Nivel FROM "{dato[0]}"')
    dato2=Data.fetchone()
    NuevNivel=dato2[0]+1
    cursor.execute(f'UPDATE "{Tabla}" SET Nivel="{NuevNivel}"')
    Data=cursor.execute(f'SELECT Dep1, Dep2, Dep3, Dep4, Dep5 FROM "{Tabla}"')
    dato3=Data.fetchone()
    if dato3[0] != None:
        ActualizarNiveles(Base,dato3[0])

    if dato3[1] != None:
        ActualizarNiveles(Base,dato3[1])

    if dato3[2] != None:
        ActualizarNiveles(Base,dato3[2])

    if dato3[3] != None:
        ActualizarNiveles(Base,dato3[3])

    if dato3[4] != None:
        ActualizarNiveles(Base,dato3[4])
    conexion.commit()
    conexion.close()


#Funcion que verifica si es que la dependencia tiene dependencias sucesoras
def DescendenciaDepExist(Base,Dep):
    conexion=sqlite3.connect(Base)
    cursor=conexion.cursor()
    Data = cursor.execute(f'SELECT Dep1 ,Dep2, Dep3, Dep4, Dep5 FROM "{Dep}"')
    dato=Data.fetchone()
    bool=False
    if dato[0] != None:
        bool=True

    if dato[1] != None:
        bool=True

    if dato[2] != None:
        bool=True

    if dato[3] != None:
        bool=True

    if dato[4] != None:
        bool=True

    conexion.close()
    return bool


def DescendenciaDepImp(Base,Dep):
    conexion = sqlite3.connect(Base)
    cursor = conexion.cursor()
    Data = cursor.execute(f'SELECT Dep1 ,Dep2, Dep3, Dep4, Dep5 FROM "{Dep}"')
    dato = Data.fetchone()

    if dato[0] != None:
        print(dato[0])
        DescendenciaDepImp(Base,dato[0])

    if dato[1] != None:
        print(dato[1])
        DescendenciaDepImp(Base,dato[1])

    if dato[2] != None:
        print(dato[2])
        DescendenciaDepImp(Base,dato[2])

    if dato[3] != None:
        print(dato[3])
        DescendenciaDepImp(Base,dato[3])

    if dato[4] != None:
        print(dato[4])
        DescendenciaDepImp(Base,dato[4])
    conexion.close()

#Imprime todas las dependencias de una base de datos
def ImprimirDepTodas(Base,Tabla):
    if Tabla=="Principal":
        print("Principal")

    conexion=sqlite3.connect(Base)
    cursor=conexion.cursor()
    datos=cursor.execute(f'SELECT Dep1 ,Dep2, Dep3, Dep4, Dep5, Nivel FROM "{Tabla}"')
    dato=datos.fetchone()
    if dato[0] != None:
        for x in range(dato[5]+1):
            print("\t",end="")

        print(dato[0])
        ImprimirDepTodas(Base,dato[0])

    if dato[1] != None:
        for x in range(dato[5]+1):
            print("\t", end="")

        print(dato[1])
        ImprimirDepTodas(Base,dato[1])

    if dato[2] != None:
        for x in range(dato[5]+1):
            print("\t", end="")

        print(dato[2])
        ImprimirDepTodas(Base,dato[2])

    if dato[3] != None:
        for x in range(dato[5]+1):
            print("\t", end="")

        print(dato[3])
        ImprimirDepTodas(Base,dato[3])

    if dato[4] != None:
        for x in range(dato[5]+1):
            print("\t", end="")

        print(dato[4])
        ImprimirDepTodas(Base,dato[4])
    conexion.close()

#Funcion que elimina una dependencia y todas sus dependencias sucesoras
def EliminarDep(Base,Dep):
    conexion=sqlite3.connect(Base)
    cursor=conexion.cursor()
    Data = cursor.execute(f'SELECT Dep1 ,Dep2, Dep3, Dep4, Dep5, DepPadre FROM "{Dep}"')
    dato=Data.fetchone()
    #Verifica y halla cuales son las dependencias sucesoras de la base de datos
    if dato[0] != None:
        EliminarDep(Base,dato[0])

    if dato[1] != None:
        EliminarDep(Base,dato[1])

    if dato[2] != None:
        EliminarDep(Base,dato[2])

    if dato[3] != None:
        EliminarDep(Base,dato[3])

    if dato[4] != None:
        EliminarDep(Base,dato[4])
    DepP=Dep+"P"
    cursor.execute(f'DROP TABLE IF EXISTS "{DepP}"')
    cursor.execute(f'DROP TABLE IF EXISTS "{Dep}"')
    cursor.execute(f'DELETE FROM Personas WHERE DEP="{Dep}"')
    Data=cursor.execute(f'SELECT Dep1 ,Dep2, Dep3, Dep4, Dep5 FROM "{dato[5]}"')
    dato2=Data.fetchone()
    print(dato[5])
    for x in dato2:
        print(x)

    if dato2[0]==Dep:
        cursor.execute(f'UPDATE "{dato[5]}" SET Dep1= NULL ')

    if dato2[1]==Dep:
        cursor.execute(f'UPDATE "{dato[5]}" SET Dep2= NULL ')

    if dato2[2]==Dep:
        cursor.execute(f'UPDATE "{dato[5]}" SET Dep3= NULL ')

    if dato2[3]==Dep:
        cursor.execute(f'UPDATE "{dato[5]}" SET Dep4= NULL ')

    if dato2[4]==Dep:
        cursor.execute(f'UPDATE "{dato[5]}" SET Dep5= NULL ')

    conexion.commit()
    conexion.close()
    return dato[5]


#Funcion que copia una estructura de un organigrama, copiando todas las dependencias que existen en un organigrama pero sin ninguno de los datos de las personas que hay en ellas
def CopiarOrg(Base,Nombre):
    ArchivoOriginal = os.getcwd() + "\\" + Base
    ArchivoCopia=os.getcwd() + "\\" + Nombre +".db"
    shutil.copy2(ArchivoOriginal,ArchivoCopia)
    conexion = sqlite3.connect(Nombre+".db")
    cursor = conexion.cursor()
    cursor.execute(f'UPDATE Principal SET ORG="{Nombre}"')
    Data=cursor.execute(f'SELECT Dep1, Dep2, Dep3, Dep4, Dep5 FROM Principal')
    dato = Data.fetchone()

    if dato[0]!=None:
        cursor.execute(f'UPDATE "{dato[0]}" SET DepPadre="{Nombre}"')

    if dato[1] != None:
        cursor.execute(f'UPDATE "{dato[1]}" SET DepPadre="{Nombre}"')

    if dato[2] != None:
        cursor.execute(f'UPDATE "{dato[2]}" SET DepPadre="{Nombre}"')

    if dato[3] != None:
        cursor.execute(f'UPDATE "{dato[3]}" SET DepPadre="{Nombre}"')

    if dato[4] != None:
        cursor.execute(f'UPDATE "{dato[4]}" SET DepPadre="{Nombre}"')

    cursor.execute(f'DROP TABLE IF EXISTS Personas')
    cursor.execute("CREATE TABLE Personas (COD INTEGER, DOC TEXT , APE TEXT, NOM TEXT, TEL TEXT, DIR TEXT, DEP  TEXT, SAL INTEGER)")
    conexion.commit()
    conexion.close()
    AgregarNombres(Nombre)

#Funcion que elimina la base de datos de la ruta
def EliminarOrg(Base):
    conexion = sqlite3.connect(Base)
    cursor = conexion.cursor()
    Data=cursor.execute(f'SELECT COD FROM Principal')
    dato=Data.fetchone()
    EliminarCodOrg(int(dato[0]))
    conexion.close()
    ruta_archivo=os.getcwd() + "\\" + Base

    if os.path.isfile(ruta_archivo):
        os.remove(ruta_archivo)

#Funcion que devuelve un nuevo codigo para la persona que va a ingresar, el codigo sera 1 mas que la persona con mayor codigo
def CODPersonaNueva(Base):
    conexion = sqlite3.connect(Base)
    cursor = conexion.cursor()
    Data=cursor.execute("SELECT COD FROM Personas")
    mayor=1

    for x in Data:
        if mayor<int(x[0]):
            mayor=x[0]

    mayorL=str(mayor)

    while len(mayorL)<4:
        mayorL="0"+mayorL
    conexion.close()
    return mayorL

#Funcion que recibe la CI de una persona y la base de datos a la cual pertenece para verificar si este existe en la base
def ValPersona(Base,CIPersona):
    conexion = sqlite3.connect(Base)
    cursor = conexion.cursor()
    #Agarramos todas las CI que estan en la base de datos y las verificamos con la que ingresamos, si esta devolvemos True, sino false
    Data=cursor.execute(f'SELECT DOC FROM Personas')
    bool=False
    for x in Data:
        if (x[0]==CIPersona):
            bool=True
            break
    conexion.close()
    return bool

#Funcion que recibe la Cedula de una persona y devuelve el nombre de esta
def NombreApellidoPersonaCI(Base,CIPersona):
    conexion = sqlite3.connect(Base)
    cursor = conexion.cursor()
    Data=cursor.execute(f'SELECT NOM, APE FROM Personas WHERE DOC="{CIPersona}"')
    dato=Data.fetchone()
    NombreYApellido=dato[0]+" "+dato[1]
    conexion.close()
    return NombreYApellido

#funcion que recibe el codigo de una persona y te devuelve el nombre y apellido de esta
def NombreApellidoPersonaCOD(Base,CODPersona):
    conexion = sqlite3.connect(Base)
    cursor = conexion.cursor()
    Data=cursor.execute(f'SELECT NOM, APE FROM Personas WHERE COD="{CODPersona}"')
    dato=Data.fetchone()
    NombreYApellido=dato[0]+" "+dato[1]
    conexion.close()
    return NombreYApellido

def ModificarCedulaPersona(Base,CIPersona,CIPersonaN):
    conexion = sqlite3.connect(Base)
    cursor = conexion.cursor()
    cursor.execute(f'UPDATE Personas SET DOC="{CIPersonaN}" WHERE DOC="{CIPersona}"')
    conexion.commit()
    conexion.close()

def ModificarApellidoPersona(Base,CIPersona,Apellido):
    conexion = sqlite3.connect(Base)
    cursor = conexion.cursor()
    cursor.execute(f'UPDATE Personas SET APE="{Apellido}" WHERE DOC="{CIPersona}"')
    conexion.commit()
    conexion.close()

def ModificarNombrePersona(Base,CIPersona,Nombre):
    conexion = sqlite3.connect(Base)
    cursor = conexion.cursor()
    cursor.execute(f'UPDATE Personas SET NOM="{Nombre}" WHERE DOC="{CIPersona}"')
    conexion.commit()
    conexion.close()

def ModificarTelefonoPersona(Base,CIPersona,Telefono):
    conexion = sqlite3.connect(Base)
    cursor = conexion.cursor()
    cursor.execute(f'UPDATE Personas SET TEL="{Telefono}" WHERE DOC="{CIPersona}"')
    conexion.commit()
    conexion.close()

def ModificarDireccionPersona(Base,CIPersona,Direccion):
    conexion = sqlite3.connect(Base)
    cursor = conexion.cursor()
    cursor.execute(f'UPDATE Personas SET DIR="{Direccion}" WHERE DOC="{CIPersona}"')
    conexion.commit()
    conexion.close()

def ModificarSalarioPersona(Base,CIPersona,Salario):
    conexion = sqlite3.connect(Base)
    cursor = conexion.cursor()
    cursor.execute(f'UPDATE Personas SET SAL="{Salario}" WHERE DOC="{CIPersona}"')
    conexion.commit()
    conexion.close()

#Funcion que modifica la dependencia de una persona segun su cedula
def ModificarDependenciaPersona(Base,CIPersona,Dependencia):
    conexion = sqlite3.connect(Base)
    cursor = conexion.cursor()
    cursor.execute(f'UPDATE Personas SET DEP="{Dependencia}" WHERE DOC="{CIPersona}"')
    conexion.commit()
    conexion.close()

#Funcion que modifica la dependencia de una persona segun la dependencia a la que pertenece
def MoverPersonasMasa(Base,Dep1,Dep2):
    conexion = sqlite3.connect(Base)
    cursor = conexion.cursor()
    cursor.execute(f'UPDATE Personas SET DEP="{Dep2}" WHERE DEP="{Dep1}"')
    conexion.commit()
    conexion.close()

#Funcion que devuelve el nivel en el cual se encuentra una dependencia
def NivelDependencia(Base,Dep):
    conexion = sqlite3.connect(Base)
    cursor = conexion.cursor()
    Data=cursor.execute(f'SELECT Nivel FROM "{Dep}"')
    dato=Data.fetchone()
    conexion.close()
    return dato[0]

#Funcion que devuelve todas las dependencias, menos la principal o la que elijas
def DependenciasCasiTodas(Base,Dep):
    conexion=sqlite3.connect(Base)
    cursor=conexion.cursor()
    Dependencias=[]
    Data=cursor.execute(f'SELECT Dep1, Dep2, Dep3, Dep4, Dep5 FROM "{Dep}"')
    dato=Data.fetchone()
    if dato[0]!=None :
        Dependencias.append(dato[0])
        if len(DependenciasCasiTodas(Base,dato[0]))!=0:
            DependenciasAux=DependenciasCasiTodas(Base,dato[0])
            for x in DependenciasAux:
                Dependencias.append(x)
                
    if dato[1] != None:
        Dependencias.append(dato[1])
        if len(DependenciasCasiTodas(Base, dato[1])) != 0:
            DependenciasAux = DependenciasCasiTodas(Base, dato[1])
            for x in DependenciasAux:
                Dependencias.append(x)

    if dato[2] != None:
        Dependencias.append(dato[2])
        if len(DependenciasCasiTodas(Base, dato[2])) != 0:
            DependenciasAux = DependenciasCasiTodas(Base, dato[2])
            for x in DependenciasAux:
                Dependencias.append(x)

    if dato[3] != None:
        Dependencias.append(dato[3])
        if len(DependenciasCasiTodas(Base, dato[3])) != 0:
            DependenciasAux = DependenciasCasiTodas(Base, dato[3])
            for x in DependenciasAux:
                Dependencias.append(x)

    if dato[4] != None:
        Dependencias.append(dato[4])
        if len(DependenciasCasiTodas(Base, dato[4])) != 0:
            DependenciasAux = DependenciasCasiTodas(Base, dato[4])
            for x in DependenciasAux:
                Dependencias.append(x)

    return Dependencias

#Funcion recursiva que devuelve todas las dependencias que hay en el organigrama, comenzando con la dependencia 'Principal'
def DependenciasTodas(Base,Dep):
    conexion=sqlite3.connect(Base)
    cursor=conexion.cursor()
    Dependencias=[]
    Data=cursor.execute(f'SELECT Dep1, Dep2, Dep3, Dep4, Dep5 FROM "{Dep}"')
    dato=Data.fetchone()
    Dependencias.append(Dep)

    if dato[0]!=None :
        if len(DependenciasTodas(Base,dato[0]))!=0:
            DependenciasAux=DependenciasTodas(Base,dato[0])
            for x in DependenciasAux:
                Dependencias.append(x)

    if dato[1] != None:
        if len(DependenciasTodas(Base, dato[1])) != 0:
            DependenciasAux = DependenciasTodas(Base, dato[1])
            for x in DependenciasAux:
                Dependencias.append(x)

    if dato[2] != None:
        if len(DependenciasTodas(Base, dato[2])) != 0:
            DependenciasAux = DependenciasTodas(Base, dato[2])
            for x in DependenciasAux:
                Dependencias.append(x)

    if dato[3] != None:
        if len(DependenciasTodas(Base, dato[3])) != 0:
            DependenciasAux = DependenciasTodas(Base, dato[3])
            for x in DependenciasAux:
                Dependencias.append(x)

    if dato[4] != None:
        if len(DependenciasTodas(Base, dato[4])) != 0:
            DependenciasAux = DependenciasTodas(Base, dato[4])
            for x in DependenciasAux:
                Dependencias.append(x)

    return Dependencias

#Funcion que ingresa a una persona a la base de datos dependiendo de los datos Base=Base a ingresar; Dep:Dependencia a ingresar y Persona: Clase persona a ingresar
def IngresarPersonas(Base,Dep,persona):
    conexion=sqlite3.connect(Base)
    cursor=conexion.cursor()

    DepP=Dep+"P"
    cursor.execute(f'INSERT INTO "{DepP}" (COD , DOC , APE , NOM , TEL , DIR , DEP , SAL,jefe) VALUES ( ? , ? , ? , ? , ? , ? , ? ,?,?)',(persona.COD, persona.DOC, persona.APE, persona.NOM, persona.TEL, persona.DIR, persona.DEP, persona.SAL,persona.JEF ))
    cursor.execute(f'INSERT INTO Personas (COD , DOC , APE , NOM , TEL , DIR , DEP , SAL,jefe) VALUES ( ? , ? , ? , ? , ? , ? , ? ,?,?)',(persona.COD, persona.DOC, persona.APE, persona.NOM, persona.TEL, persona.DIR, persona.DEP, persona.SAL,persona.JEF ))
    conexion.commit()
    conexion.close()

#Funcion que te devuelve el nombre del jefe asignado a un departamento
def JefeDependencia(Base,Dep):
    conexion = sqlite3.connect(Base)
    cursor = conexion.cursor()
    Data = cursor.execute(f'SELECT CODRES FROM "{Dep}"')
    dato=Data.fetchone()
    Data=cursor.execute(f'SELECT NOM, APE FROM Personas WHERE COD="{dato[0]}"')
    dato=Data.fetchone()
    NombreYApellido=dato[0]+" "+dato[1]
    return NombreYApellido

#Funcion que lo que hace es recorrer la base de datos y encontrar todos los departamentos y devolverlos en el formato necesrio para graficarlo
def DevolverElementosMatriz(Base,Dep):
    conexion = sqlite3.connect(Base)
    cursor = conexion.cursor()

    if Dep=="Principal":
        Data=cursor.execute(f'SELECT ORG, Dep1, Dep2, Dep3, Dep4, Dep5 FROM "{Dep}"')
        dato = Data.fetchone()
        Nombre=dato[0]
    else:
        Data = cursor.execute(f'SELECT NOM, Dep1, Dep2, Dep3, Dep4, Dep5, CODRES FROM "{Dep}"')
        dato = Data.fetchone()
        if dato[6]!=None:
            Nombre=dato[0]+"\n"+"\n"+NombreApellidoPersonaCOD(Base,dato[6])
        else:
            Nombre=dato[0]

    VectorNombres=[]
    Vaux=[]
    Vaux.append(Nombre)
    VectorNombres.append(Vaux)

    if dato[1]!=None:
        Vaux=DevolverElementosMatriz(Base,dato[1])
        VectorNombres.append(Vaux)

    if dato[2] != None:
        Vaux = DevolverElementosMatriz(Base, dato[2])
        VectorNombres.append(Vaux)

    if dato[3] != None:
        Vaux = DevolverElementosMatriz(Base, dato[3])
        VectorNombres.append(Vaux)

    if dato[4] != None:
        Vaux = DevolverElementosMatriz(Base, dato[4])
        VectorNombres.append(Vaux)

    if dato[5] != None:
        Vaux = DevolverElementosMatriz(Base, dato[5])
        VectorNombres.append(Vaux)

    return VectorNombres

#Funcion que elimina una persona de la base de datos segun su Cedula de identidad
def EliminarPersonas(Base,CI):
    conexion = sqlite3.connect(Base)
    cursor = conexion.cursor()
    cursor.execute(f'DELETE FROM Personas WHERE DOC="{CI}"')
    conexion.commit()
    conexion.close()

def ImprimirDepDatos(Base):
    conexion=sqlite3.connect(Base)
    cursor=conexion.cursor()
    Data=cursor.execute(f'SELECT * FROM "{Base}"')
    Datos=Data.fetchone()
    for Dato in Datos:
        print(Dato)

    conexion.close()

def GenerarInformeUnitario(Base,Dep):
    conexion=sqlite3.connect(Base)
    cursor=conexion.cursor()
    Data=cursor.execute(f'SELECT COD, DOC, NOM, APE, DEP  FROM Personas WHERE DEP="{Dep}"')
    print(Data)

def GraficarOrganigrama(Base, Dep, colorCuadro, ColorTexto):
    G = gv.Graph()
    G.graph_attr["layout"] = "dot"

    G.node_attr["shape"] = "box"
    G.node_attr["style"] = "filled"
    G.node_attr["fillcolor"] = colorCuadro
    print(colorCuadro)
    G.node_attr["regular"] = "True"
    G.node_attr["fontname"] = "Verdana"  # Cambiar el tipo de letra
    G.node_attr["fontcolor"] = ColorTexto
    Organigrama = DevolverElementosMatriz(Base, Dep)
    crearEdges(G, Organigrama)  # Pasar el objeto G como parámetro
    FILE = "file"
    G.view(FILE)
    return G  # Devolver el objeto G

def crearEdges(G, M):  # Pasar el objeto G como parámetro
    for i in range(len(M)):
        if len(M[i]) == 1:
            if i == 0:
                PADRE = str(M[i][0])
                G.node(PADRE, group=("group" + PADRE))
                PADRE2 = PADRE + str(i)
                if len(M) == 2:
                    G.node(PADRE2, shape="point", height="0.01", width="0.01", constraint="false",
                           group=("group" + PADRE))
                else:
                    G.node(PADRE2, shape="point", constraint="false", group=("group" + PADRE))
                G.edge(PADRE, PADRE2)
                for j in range(1, len(M), 1):
                    tipo1 = str(type(M[j][0]))
                    if tipo1 == "<class 'list'>":
                        HIJO = str(M[j][0][0])
                    else:
                        HIJO = str(M[j][0])
                    if len(M) == 2:
                        G.node(HIJO, group=("group" + PADRE))
                    G.edge(PADRE2, HIJO)
        else:
            crearEdges(G, M[i])


def informe_pdf(database, tabla, columnas_mostrar, nombres_columnas, nombre_pdf):
    conexion = sqlite3.connect(database)
    cursor = conexion.cursor()

    # Obtiene los nombres de las columnas disponibles en la tabla
    cursor.execute('PRAGMA table_info("{}")'.format(tabla))
    columnas_disponibles = [columna[1] for columna in cursor.fetchall()]

    # Verifica que las columnas especificadas para mostrar estén disponibles en la tabla
    columnas_validas = [columna for columna in columnas_mostrar if columna in columnas_disponibles]
    if not columnas_validas:
        print("No se encontraron columnas válidas para mostrar.")
        conexion.close()
        return

    # Verifica si se especificaron nombres personalizados para las columnas
    if nombres_columnas:
        # Verifica que la cantidad de nombres personalizados sea igual a la cantidad de columnas
        if len(nombres_columnas) != len(columnas_validas):
            print("La cantidad de nombres de columna no coincide con la cantidad de columnas a mostrar.")
            conexion.close()
            return
    else:
        # Si no se especificaron nombres personalizados, utiliza los nombres de columna disponibles
        nombres_columnas = columnas_validas

    # Genera la consulta SQL con las columnas seleccionadas
    consulta_sql = 'SELECT {} FROM "{}"'.format(", ".join(columnas_validas), tabla)
    cursor.execute(consulta_sql)
    datos = cursor.fetchall()

    # Crea el documento PDF
    doc = SimpleDocTemplate(nombre_pdf, pagesize=letter)

    # Crea la tabla con los datos obtenidos de la base de datos, incluyendo los nombres de las columnas
    tabla = Table([nombres_columnas] + datos)

    # Define el estilo de la tabla
    estilo_tabla = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # Color de fondo para la primera fila (encabezado)
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),  # Color del texto para la primera fila (encabezado)
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Alineación del texto al centro en todas las celdas
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Fuente en negrita para la primera fila (encabezado)
        ('FONTSIZE', (0, 0), (-1, 0), 12),  # Tamaño de fuente para la primera fila (encabezado)
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Espaciado inferior para la primera fila (encabezado)
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),  # Color de fondo para las filas restantes
        ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Agrega líneas de borde a todas las celdas
    ])
    tabla.setStyle(estilo_tabla)

    # Agrega la tabla al contenido del documento y genera el PDF
    contenido = [tabla]
    doc.build(contenido)

    conexion.close()

    # Obtener la ruta completa del PDF generado
    ruta_pdf = os.path.abspath(nombre_pdf)

    # Verificar si el archivo PDF existe
    if os.path.isfile(ruta_pdf):
        # Abrir el archivo PDF con el visor predeterminado
        os.startfile(ruta_pdf)
    else:
        print("No se encontró el archivo PDF.")

    return doc



def exportar_tablas_pdf(base_datos, columnas, nombres_columnas, nombre_pdf, tablas):
    # Establecer conexión con la base de datos
    conexion = sqlite3.connect(base_datos)
    cursor = conexion.cursor()

    # Crear el objeto PDF
    doc = SimpleDocTemplate(nombre_pdf, pagesize=letter)
    elements = []

    # Recorrer las tablas y exportar cada una en una tabla separada en el PDF
    for tabla in tablas:
        # Verificar si la tabla existe en la base de datos
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (tabla,))
        resultado = cursor.fetchone()

        if resultado is not None:
            # Obtener los datos de la tabla desde la base de datos

            cursor.execute(f"SELECT {', '.join(columnas)} FROM '{tabla}'")
            datos_tabla = cursor.fetchall()

            # Verificar si la tabla tiene datos antes de exportarla
            if datos_tabla:
                # Crear la tabla con los datos y los nombres de las columnas
                tabla_pdf = Table([nombres_columnas] + datos_tabla)

                # Aplicar estilo a la tabla

                tabla_pdf.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # Color de fondo para la primera fila (encabezado)
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    # Color del texto para la primera fila (encabezado)
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Alineación del texto al centro en todas las celdas
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    # Fuente en negrita para la primera fila (encabezado)
                    ('FONTSIZE', (0, 0), (-1, 0), 12),  # Tamaño de fuente para la primera fila (encabezado)
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Espaciado inferior para la primera fila (encabezado)
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),  # Color de fondo para las filas restantes
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Agrega líneas de borde a todas las celdas
                                                ]))

                elements.append(tabla_pdf)
                elements.append(Spacer(1, 12))
        else:
            print(f"La tabla '{tabla}' no existe en la base de datos.")

    # Cerrar la conexión a la base de datos
    conexion.close()

    # Generar el PDF con las tablas
    doc.build(elements)
    print(f"Se ha exportado correctamente el PDF: {nombre_pdf}")

    # Obtener la ruta completa del PDF generado
    ruta_pdf = os.path.abspath(nombre_pdf)

    # Verificar si el archivo PDF existe
    if os.path.isfile(ruta_pdf):
        # Abrir el archivo PDF con el visor predeterminado
        os.startfile(ruta_pdf)
    else:
        print("No se encontró el archivo PDF.")


#funcion que verifica si la base no tiene personas aun
def ExistePersona(Base):
    conexion = sqlite3.connect(Base)
    cursor = conexion.cursor()
    #Agarramos todas las CI que estan en la base de datos y las verificamos con la que ingresamos, si esta devolvemos True, sino false
    Data=cursor.execute(f'SELECT DOC FROM Personas')
    bool=False
    for x in Data:
        if x[0] is not None:
            bool = True
            break
    conexion.close()
    return bool

#funcion que verifica si la tabla no tiene personas aun
def ExistePersonaDep(Base, Tabla):
    conexion = sqlite3.connect(Base)
    cursor = conexion.cursor()
    #Agarramos todas las CI que estan en la base de datos y las verificamos con la que ingresamos, si esta devolvemos True, sino false
    Data=cursor.execute(f'SELECT DOC FROM Personas WHERE DEP="{Tabla}"')
    dato = Data.fetchone()
    bool=False
    if dato is not None:
        bool = True
    conexion.close()
    return bool
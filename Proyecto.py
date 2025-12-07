from Funciones import *
from Clases import *
import sqlite3
import os

print("Bienvenido al programa de organigramas!")
men=0
persAux = Personas
while True:

    print("""Que es lo que desea hacer?
1-Crear un Organigrama
2-Abrir un Organigrama
3-Eliminar un Organigrama
4-Salir""")
    Selec = int(input())
    while True:

        if Selec==1 :
            if CodigoLibreOrgVer():
                ORG_AUX = Organigrama
                # Crea una base de datos segun un nombre ingresado por el usuario
                while True:
                    ORG_AUX.ORG = input("Ingrese el nombre del organigrama: ")
                    ruta=ORG_AUX.ORG+".db"
                    # Si el nombre para la base de datos ya existe no se crea la base de datos
                    if os.path.exists(ruta):
                        print("Ya existe una base de datos con ese nombre ")
                    else:
                        break

                print("Ingrese la fecha de vigencia del programa en formato DD/MM/AAAA")
                ORG_AUX.FEC = input()

                #CrearOrg Necesita que se le ingrese un dato de tipo "Organigrama"
                Base=CrearOrg(ORG_AUX)
                BaseD=Base+".db"
                print("Organigrama Creado con exito!")
                print("Ingrese el nombre de la primera dependencia que desea agregar: ",end="")
                while True:
                    Dep = input()
                    if CrearDep(BaseD,"Principal",Dep):
                        break
                men=1
                break
            else:
                print("Se a llegado al maximo de organigramas posibles, Favor elimine uno antes de crear otro nuevo")

        if Selec==2 :
            print("Ingrese el nombre del organigrama que desea abrir")
            while True:
                ImprimirNombres()
                Base=input()
                archivo=open("Nombres_Organigrama.txt",'r')
                Lineas=archivo.readlines()
                archivo.close()
                Base2=Base+"\n"
                if Base2 not in Lineas:
                    print("El organigrama ingresado no existe")
                    print("Favor ingrese un nombre valido de la lista")
                else:
                    break

            BaseD=Base+".db"
            men=1
            break

        if Selec==3 :
            print("Que organigrama deseas Eliminar?")
            while True:
                ImprimirNombres()
                Base=input()
                archivo = open("Nombres_Organigrama.txt", 'r')
                Lineas = archivo.readlines()
                archivo.close()
                Base2=Base+"\n"
                if Base2 not in Lineas:
                    print("El organigrama ingresado no existe")
                    print("Favor ingrese un nombre valido de la lista")
                else:
                    break

            BaseD=Base+".db"
            EliminarOrg(BaseD)
            EliminarNombres(Base)
            print("Organigrama eliminado con exito!")
            break

        if Selec==4 :
            break

        print("Error, favor elija una opcion")
        break

    while men==1:
        Menu(Base)
        Opcio=int(input())

        if Opcio==1:
            print("Ingrese la tabla de la cual va a descender: ")
            while True:
                ImprimirDepTodas(BaseD,"Principal")
                Tabla=input()
                if Tabla!=None:
                    if VerificarExistTabla(BaseD,Tabla):
                        if EspacioDependencia(BaseD, Tabla):
                            break
                        else:
                            print("La Dependencia ingresada no puede tener mas dependencias sucesoras")
                    else:
                        print("La Dependencia que usted eligio no existe, favor elija otra")
                else:
                    print("Favor elija una dependencia: ")

            print("Ingrese el nombre de la dependencia que va a crear: ")
            while True:
                Dep = input()
                if Dep!=None:
                    if VerificarExistTabla(BaseD,Dep):
                        print("La dependencia ingresada ya existe, favor ingrese otra")
                    else:
                        break
                else:
                    print("Favor elija una dependencia")

            CrearDep(BaseD,Tabla,Dep)

        if Opcio==2:
            print("Ingrese la dependencia a eliminar\nOBS: SE ELIMINARAN TODAS LAS DESCENDENCIAS SUBSECUENTES ")
            while True:
                ImprimirDepTodas(BaseD,"Principal")
                Tabla = input()
                if Tabla!=None:
                    if VerificarExistTabla(BaseD,Tabla):
                        break
                    else:
                        print("La Dependencia que usted eligio no existe, favor elija otra")
                else:
                    print("Favor elija una dependencia: ")
            print("Esta seguro que desea eliminar",Tabla,"?")
            if DescendenciaDepExist(BaseD,Tabla):
                print("Se eliminaran las siguientes Dependencias: ")
                DescendenciaDepImp(BaseD,Tabla)
            print("Y/N")
            validar=input()
            if validar=='Y' or validar=='y':
                EliminarDep(BaseD,Tabla)
                print("Se elimino la Dependencia ",Tabla,"y todas sus dependencias sucesoras ")


        if Opcio==3:
            print("Ingrese la dependencia que desea modificar:")
            while True:
                ImprimirDepTodas(BaseD,"Principal")
                Tabla=input()
                if Tabla!=None:
                    if VerificarExistTabla(BaseD,Tabla):
                        break
                    else:
                        print("La dependencia ingresada no existe, favor ingrese otra")
                else:
                    print("Favor elija una dependencia: ")
            print("Que desea modificar de la dependencia",Tabla, "?")
            while True:
                print("""1-Nombre Dependencia\n2-Codigo del Jefe de la Dependencia""")
                Select=int(input())
                if Select==1:
                    Nombre=input("Ingrese el nuevo nombre de la dependencia: ")
                    ModificarDepNombre(BaseD, Tabla,Nombre)
                    break

                if Select==2:
                    CIJefe=input("Ingrese la cedula del nuevo jefe: ")
                    if ValPersona(BaseD, CIJefe):
                        if ValPersonaArea(BaseD,Tabla,CIJefe):
                            if ValidarEsJefe(BaseD,CodigoPersonaSegunCI(BaseD,CIJefe)):
                                print("Esa persona ya es jefe de otra area, favor seleccione otro empleado")
                            else:
                                ModificarDepJefe(BaseD, Tabla, CIJefe)
                                print("Se ha cambiado con exito el jefe del area!")
                                break
                        else:
                            print("La persona que esta intentando asignar como jefe no pertenece a ese departamento")
                    else:
                        print("La persona ingresada no esta en la base de datos")
                        break

        if Opcio==4:
            print("Seleccione la dependencia que desee mover"
                  "\nOBS:Esta accion movera todas las dependencias sucesoras al nuevo lugar tambien")
            ImprimirDepTodas(BaseD, "Principal")
            while True:
                Tabla = input()
                if Tabla != None:
                    if VerificarExistTabla(BaseD, Tabla):
                        break
                    else:
                        print("La dependencia ingresada no existe, favor ingrese otra")
                else:
                    print("Favor elija una dependencia: ")

            print("Seleccione la nueva dependencia que va a suceder")
            ImprimirDepTodas(BaseD, "Principal")
            while True:
                Mov = input()
                if Tabla != None:
                    if VerificarExistTabla(BaseD, Mov):
                        if EspacioDependencia(BaseD,Mov):
                            if (Mov!=Tabla):
                                if DependenciaDesciende(BaseD,Tabla,Mov):
                                    print("No puede mover una dependencia a un lugar que sea sucesora a ella")
                                else:

                                    if DependenciaHijo(BaseD,Mov,Tabla):
                                        print("La Dependencia ya sucede de donde trata de mover")
                                    else:
                                        MoverDependencia(BaseD,Tabla,Mov)
                                        break
                            else:
                                print("Favor eleija otra dependencia")
                        else:
                            print("La dependencia que eligio ya no admite mas dependencias")
                    else:
                        print("La dependencia ingresada no existe, favor ingrese otra")
                else:
                    print("Favor elija una dependencia: ")
            print("Movimiento realizado con exito!\n")

        #Opcion para poder ingresar Personas a la base de datos
        if Opcio==5:
            print("Ingrese en que dependencia quiere ingresar a la Persona ")
            ImprimirDepTodas(BaseD,"Principal")
            Dep=input()
            print("Ingrese los datos de la persona a ser ingresada: ")
            persAux.COD=CODPersonaNueva(BaseD)

            while True:
                print("Ingrese la cedula de la persona: ")
                persAux.DOC = input()
                if (ValPersona(BaseD,persAux.DOC)):
                    print("Ya existe esa persona en la base de datos, ingrese otra cedula")
                else:
                    break
            persAux.NOM=input("Ingrese el nombre de la persona: ")
            persAux.APE=input("Ingrese el apellido de la persona: ")
            persAux.TEL=input("Ingrese el numero de telefono la persona: ")
            persAux.DIR=input("Ingrese donde vive esa persona: ")
            persAux.DEP=Dep
            persAux.SAL=input("Ingrese el salario neto de la persona: ")
            IngresarPersonas(BaseD,Dep,persAux)
            print("La persona ha sido añadida a ",Dep," exitosamente!")

        #Opcion de Eliminar a una persona de la base de datos
        if Opcio==6:
            print("Ingrese la cedula de la persona a la cual dar de baja")
            CI=input()
            if (ValPersona(BaseD,CI)):
                Nombre=NombreApellidoPersonaCI(BaseD,CI)
                print("Esta seguro que desea eliminar a ",NombreApellidoPersonaCI(BaseD,CI),"?")
                EliminarPersonas(BaseD,CI)
                print(Nombre," ha sido eliminado satisfactoriamente de la base de datos!")
            else:
                print("Esa persona no esta en la base de datos")

        #Opcion para poder modificar los datos de una persona en la base de datos
        if Opcio==7:
            print("Ingrese la cedula de la persona a la cual va a modificar")
            CI = input()
            if (ValPersona(BaseD, CI)):
                print("Que es lo que desea modificar de ",NombreApellidoPersonaCI(BaseD, CI),"?"
                "\n1-Cedula de identidad"
                "\n2-Apellido"
                "\n3-Nombre"
                "\n4-Telefono"
                "\n5-Direccion"
                "\n6-Salario")
                Select=int(input())
                if (Select<1 and Select>6):
                    print("Eleccion de operacion Fallada, volviendo al menu")
                else:
                    if Select==1:
                        print("Ingrese la nueva cedula de ",NombreApellidoPersonaCI(BaseD,CI))
                        while True:
                            if ValPersona(BaseD,CI):
                                print("No se puede repetir la cedula de una persona")
                            else:
                                DatoMod=input()
                                ModificarCedulaPersona(BaseD,CI,DatoMod)
                                break

                    if Select==2:
                        print("Ingrese el nuevo Apellido de ", NombreApellidoPersonaCI(BaseD, CI))
                        DatoMod = input()
                        ModificarApellidoPersona(BaseD, CI, DatoMod)

                    if Select == 3:
                        print("Ingrese el nuevo Nombre de ", NombreApellidoPersonaCI(BaseD, CI))
                        DatoMod = input()
                        ModificarNombrePersona(BaseD, CI, DatoMod)

                    if Select == 4:
                        print("Ingrese el nuevo Telefono de ", NombreApellidoPersonaCI(BaseD, CI))
                        DatoMod = input()
                        ModificarTelefonoPersona(BaseD, CI, DatoMod)

                    if Select == 5:
                        print("Ingrese la nueva Direccion de ", NombreApellidoPersonaCI(BaseD, CI))
                        DatoMod = input()
                        ModificarDireccionPersona(BaseD, CI, DatoMod)

                    if Select == 6:
                        print("Ingrese el nuevo Salario de ", NombreApellidoPersonaCI(BaseD, CI))
                        DatoMod = input()
                        ModificarSalarioPersona(BaseD, CI, DatoMod)

                    print("Modificacion realizada con exito!")

            else:
                print("Esa persona no esta en la base de datos")

        #Opcion donde realiza el movimiento de una dependencia a otra de una persona
        if Opcio==8:
            print("Ingrese la cedula de la persona que desea mover de dependencia")
            CI = input()
            if (ValPersona(BaseD, CI)):

                print("Ingrese la Dependencia a donde movera a ", NombreApellidoPersonaCI(BaseD, CI))
                ImprimirDepTodas(BaseD,"Principal")
                while True:
                    DatoMod=input()
                    if VerificarExistTabla(BaseD,DatoMod):
                        break
                    else:
                        print("La Dependencia que usted eligio no existe, favor elija otra")

                ModificarDependenciaPersona(BaseD,CI,DatoMod)
                print(NombreApellidoPersonaCI(BaseD, CI)," ha sido movido satisfactoriamente de Dependencia!")
            else:
                print("Esa persona no esta en la base de datos")

        # Opcion donde realiza el movimiento de una dependencia a otra en masa
        if Opcio == 9:

            print("Ingrese la Dependencia de la cual desea mover las personas")
            while True:
                ImprimirDepTodas(BaseD,"Principal")
                Dep1 = input()
                if Dep1 != None:
                    if VerificarExistTabla(BaseD, Dep1):
                        break
                    else:
                        print("La dependencia ingresada no existe, favor ingrese otra")
                else:
                    print("Favor elija una dependencia: ")

            print("Ingrese la Dependencia a la cual va a mover las personas")
            while True:
                ImprimirDepTodas(BaseD, "Principal")
                Dep2 = input()
                if Dep2 != None:
                    if VerificarExistTabla(BaseD, Dep2):
                        break
                    else:
                        print("La dependencia ingresada no existe, favor ingrese otra")
                else:
                    print("Favor elija una dependencia: ")

            MoverPersonasMasa(BaseD,Dep1,Dep2)
            print("Se movieron a todas las personas con exito!")

        if Opcio==10:
            print("si")

        #Esta opcion lo que hace es crear un organigrama con la misma estructura que el organigrama actual
        if Opcio==11:
            print("Esta operacion lo que hace es Crear un organigrama con la misma estructura que la seleccionada")
            while True:
                Nombre = input("Ingrese el nombre para el nuevo organigrama\n")
                ruta = Nombre + ".db"
                # Si el nombre para la base de datos ya existe no se crea la base de datos
                if os.path.exists(ruta):
                    print("Ya existe una base de datos con ese nombre ")
                else:
                    break
            CopiarOrg(BaseD, Nombre)
            print("Organigrama Copiado con exito!")

        if Opcio==12:
            GraficarOrganigrama(BaseD,'Principal')

        #Opcion que elimina el organigrama de donde se encuentra
        if Opcio==13:
            print("Esta seguro que desea eliminar este Organigrama?\nNo podra volver a recuperarlo")
            EliminarOrg(BaseD)
            EliminarNombres(Base)
            print("Organigrama eliminado con exito!")
            men=0
            break

        #Esta Opcion sale del menu
        if Opcio==14:
            men=0
            break

        if Opcio==15:
            V=DependenciasTodas(BaseD,"Principal")
            print(V)

            #1-['Gerente G', 'Gerente M', 'Gerente M2', 'Gerente M3', 'Gerente M4', 'Gerente L', 'Gerente P', 'Gerente F', 'abcd', 'aaaa']
    if Selec==4:
        print("Gracias por usar un programa de Martin y Asociados!")
        break
"""
 * Copyright 2020, Departamento de sistemas y Computación
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 """

import sys
sys.setrecursionlimit(10**6) 
import config
from DISClib.ADT import list as lt
from App import controller
from DISClib.ADT import map as m
assert config


"""
La vista se encarga de la interacción con el usuario.
Presenta el menu de opciones  y  por cada seleccion
hace la solicitud al controlador para ejecutar la
operación seleccionada.
"""

# ___________________________________________________
#  Ruta a los archivos
# ___________________________________________________


accidentsfile = 'us_accidents_small.csv'
#accidentsfile = 'US_Accidents_Dec19.csv'



# ___________________________________________________
#  Menu principal
# ___________________________________________________


def printMenu():
    print("\n")
    print("*******************************************")
    print("Bienvenido")
    print("1- Inicializar Analizador")
    print("2- Cargar información de accidentes")
    print("3- Conocer los accidentes en una fecha")
    print("4- Conocer los accidentes anteriores a una fecha")
    print("5- Requerimiento 3")
    print("0- Salir")
    print("*******************************************")


"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n>')

    if int(inputs[0]) == 1:
        print("\nInicializando....")
        # cont es el controlador que se usará de acá en adelante
        cont = controller.init()

    elif int(inputs[0]) == 2:
        print("\nCargando información de accidentes ....")
        controller.loadData(cont,accidentsfile)
        print('Accidentes cargados: ' + str(controller.accidentsSize(cont)))
        print('Altura del arbol: ' + str(controller.indexHeight(cont)))
        print('Elementos en el arbol: ' + str(controller.indexSize(cont)))
        print('Menor Llave: ' + str(controller.minKey(cont)))
        print('Mayor Llave: ' + str(controller.maxKey(cont)))

    elif int(inputs[0]) == 3:
        print("\nBuscando accidentes en una fecha: ")
        initialDate = input("Fecha (YYYY-MM-DD): ")
        lst = controller.getAccidentsByRange(cont, initialDate, initialDate)
        print("\nTotal de accidentes en el dia: " + str(controller.cont_accidents(lst)))
        tabla=controller.severities(lst)
        print(m.get(tabla,"1"))
        print(m.get(tabla,"2"))
        print(m.get(tabla,"3"))
        print(m.get(tabla,"4"))
    elif int(inputs[0]) == 4:
        print("\nBuscando accidentes antes de la fecha: ")
        Date = input("Fecha (YYYY-MM-DD): ")
        lst = controller.getPastAccidents(cont, Date)
        most = controller.mostAccInDate(lst)
        total_acc = lt.size(lst)
        print("\nTotal de accidentes antes de la fecha: " + str(lt.size(lst)))
        print("\nFecha con mas accidentes: " + str(most))
    elif int(inputs[0]) == 5:
        print("\nRequerimiento No 3 del reto 3: ")
        print("\nBuscando accidentes en una fecha: ")
        initialDate = input("Fecha (YYYY-MM-DD): ")
        FinalDate = input("Fecha (YYYY-MM-DD): ")
        lst = controller.getAccidentsByRange(cont, initialDate, FinalDate)
        # print(lst)
        numero_accidentes=(controller.cont_accidents(lst))
        print("el numero de accidentes entre "+ str(initialDate)+" y "+ str(FinalDate)+ " fue: "+str(numero_accidentes))
        hash_t=controller.severities(lst)
        lstValues=m.valueSet(hash_t)
        key_value=controller.getMaxSeverity(lstValues,hash_t)
        print("el mayor grado de severidad fue "+key_value[0]+" con "+str(key_value[1])+" accidentes")

    else:
        sys.exit(0)
sys.exit(0)




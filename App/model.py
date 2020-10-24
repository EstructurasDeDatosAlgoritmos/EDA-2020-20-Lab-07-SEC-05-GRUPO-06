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
import config
from DISClib.ADT import list as lt
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import map as m
from DISClib.DataStructures import listiterator as it
import datetime
assert config

"""
En este archivo definimos los TADs que vamos a usar,
es decir contiene los modelos con los datos en memoria


"""

# -----------------------------------------------------
# API del TAD Catalogo de accidentes
# -----------------------------------------------------
def newAnalyzer():
    """ Inicializa el analizador

    Crea una lista vacia para guardar todos los accidentes
    Se crean indices (Maps) por los siguientes criterios:
    -Fechas

    Retorna el analizador inicializado.
    """
    analyzer = {'accidents': None,
                'dateIndex': None
                }

    analyzer['accidents'] = lt.newList('SINGLE_LINKED', compareIds)
    analyzer['dateIndex'] = om.newMap(omaptype='RBT',
                                      comparefunction=compareDates)
    return analyzer


# Funciones para agregar informacion al catalogo

def addAccident(analyzer, accident):
    """
    """
    lt.addLast(analyzer['accidents'], accident)
    updateDateIndex(analyzer['dateIndex'], accident)
    return analyzer

def updateDateIndex(map, accident):
    """
    Se toma la fecha del acidente y se busca si ya existe en el arbol
    dicha fecha.  Si es asi, se adiciona a su lista de acidentes
    y se actualiza el indice de tipos de crimenes.

    Si no se encuentra creado un nodo para esa fecha en el arbol
    se crea y se actualiza el indice de tipos de acidentes
    """
    occurreddate = accident['Start_Time']
    accidentdate = datetime.datetime.strptime(occurreddate, '%Y-%m-%d %H:%M:%S')
    entry = om.get(map, accidentdate.date())
    if entry is None:
        datentry = newDataEntry(accident)
        om.put(map, accidentdate.date(), datentry)
    else:
        datentry = me.getValue(entry)
    addDateIndex(datentry, accident)
    return map


def newDataEntry(accident):
    """
    Crea una entrada en el indice por fechas, es decir en el arbol
    binario.
    """
    entry = {'severityIndex': None, 'lstaccidents': None}
    entry['severityIndex'] = m.newMap(numelements=100,
                                     maptype='PROBING',#probar 
                                     comparefunction=compareSeverities)
    entry['lstaccidents'] = lt.newList('SINGLE_LINKED', compareDates)
    return entry

def addDateIndex(datentry, accident):
    """
    Actualiza un indice de tipo de crimenes.  Este indice tiene una lista
    de crimenes y una tabla de hash cuya llave es el tipo de crimen y
    el valor es una lista con los crimenes de dicho tipo en la fecha que
    se está consultando (dada por el nodo del arbol)
    """
    lst = datentry['lstaccidents']
    lt.addLast(lst, accident)
    severityIndex = datentry['severityIndex']
    seventry = m.get(severityIndex, accident['Severity'])
    if (seventry is None):
        entry = newSeverityEntry(accident['Severity'], accident)
        lt.addLast(entry['lstseverities'], accident)
        m.put(severityIndex, accident['Severity'], entry)
    else:
        entry = me.getValue(seventry)
        lt.addLast(entry['lstseverities'], accident)
    return datentry

def newSeverityEntry(severitygrp, accident):
    """
    Crea una entrada en el indice por tipo de crimen, es decir en
    la tabla de hash, que se encuentra en cada nodo del arbol.
    """
    seventry = {'severity': None, 'lstseverities': None}
    seventry['severity'] = severitygrp
    seventry['lstseverities'] = lt.newList('SINGLELINKED', compareSeverities)
    return seventry
# ==============================
# Funciones de consulta
# ==============================

def accidentsSize(analyzer):
    """
    Número de libros en el catago
    """
    return lt.size(analyzer['accidents'])

def indexHeight(analyzer):
    """Numero de autores leido
    """
    return om.height(analyzer['dateIndex'])
def indexSize(analyzer):
    """Numero de autores leido
    """
    return om.size(analyzer['dateIndex'])


def minKey(analyzer):
    """Numero de autores leido
    """
    return om.minKey(analyzer['dateIndex'])


def maxKey(analyzer):
    """Numero de autores leido
    """
    return om.maxKey(analyzer['dateIndex'])

def getAccidentsByRange(analyzer, initialDate, finalDate):
    """
    Retorna el numero de crimenes en un rago de fechas.
    """
    lst = om.values(analyzer['dateIndex'], initialDate, finalDate)
    return lst



#requerimiento 1

def cont_accidents(lst):
    iterator=it.newIterator(lst)
    sum_accidents=0
    while it.hasNext(iterator):
        date=it.next(iterator)
        sum_accidents=lt.size(date["lstaccidents"])+ sum_accidents
    return sum_accidents

def severities(lst):
    severities=m.newMap(5,
                                   maptype='CHAINING',
                                   loadfactor=0.7,
                                   comparefunction=compareSeverities)
    iterator=it.newIterator(lst)
    while it.hasNext(iterator):
        date=it.next(iterator)
        it2=it.newIterator(date["lstaccidents"])
        while it.hasNext(it2):
            accident=it.next(it2)
            addSeverity(severities,accident)
    return(severities)

def addSeverity(map, severity):
    """
    Esta función adiciona una pelicula a la lista de peliculas publicadas
    por una compañia.
    Cuando se adiciona la pelicula se actualiza el promedio de dicha compañia
    """
    existseverity = m.contains(map, severity["Severity"])
    if existseverity:
         entry = m.get(map, severity["Severity"])
         key=me.getKey(entry)
         suma = me.getValue(entry)
         m.put(map,key,int(suma)+1)
    else:
        m.put(map, severity["Severity"],1)


def getMaxSeverity(lst,hash_t):
    max_value=0
    iterador=it.newIterator(lst)
    while it.hasNext(iterador):
        severidad_Value=it.next(iterador)
        if severidad_Value>max_value:
            max_value=severidad_Value
    maxKey=None
    key=0
    while maxKey==None:
        key=key+1
        existentry=m.contains(hash_t,str(key))
        if existentry:
            entry=m.get(hash_t,str(key))
            if me.getValue(entry)==max_value:
                maxKey=me.getKey(entry)
    return (maxKey,max_value)








# ==============================
# Funciones de Comparacion
# ==============================
def compareIds(id1, id2):
    """
    Compara dos accidentes
    """
    if (id1 == id2):
        return 0
    elif id1 > id2:
        return 1
    else:
        return -1
        
def compareDates(date1, date2):
    """
    Compara dos ids de libros, id es un identificador
    y entry una pareja llave-valor
    """
    if (date1 == date2):
        return 0
    elif (date1 > date2):
        return 1
    else:
        return -1
def compareSeverities(severity1, severity2):
    """
    Compara dos ids de libros, id es un identificador
    y entry una pareja llave-valor
    """
    severity = me.getKey(severity2)
    if (severity1 == severity):
        return 0
    elif (severity1 > severity):
        return 1
    else:
        return -1

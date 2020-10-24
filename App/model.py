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
from DISClib.DataStructures import arraylistiterator as it
from DISClib.ADT import map as m
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

    analyzer['accidents'] = m.newMap(numelements=999,
                                 prime=109345121, 
                                 maptype="CHAINING", 
                                 loadfactor=1.0, 
                                 comparefunction=comparer)
    analyzer['dateIndex'] = om.newMap(omaptype='RBT ',
                                      comparefunction=compareDates) 
    
    return analyzer

def convert_date (x):
    accidentdate = datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S')
    return accidentdate.date()
def convert_date_1 (x):
    accidentdate = datetime.datetime.strptime(x, '%Y-%m-%d')
    return accidentdate.date()

# Funciones para agregar informacion al catalogo

def id (analyzer, accident):
    lis = analyzer["accidents"]
    index = analyzer["dateIndex"]
    date = convert_date(accident["Start_Time"])
    m.put(lis, accident["ID"], accident)
    if om.contains(index, date)==True:
        addId(index, accident, date)
    else:
        addDate(index, accident, date) 

def addId(index, accident, date):
    x = om.get(index, date)
    y = me.getValue(x)
    lt.addLast(y, accident["ID"])

def addDate(index, accident, date):
    z = lt.newList(datastructure="ARRAY_LIST")
    lt.addLast(z, accident["ID"])
    om.put(index, date, z)

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

def por_estado (date1,date2,analyzer):

    date = convert_date_1(date1)
    date3 = convert_date_1(date2)
    
    respuesta = {'total': 0, 'Estado': None}
    Estados = lt.newList ("ARRAY_LIST")
    i = 0
    llaves = om.keys (analyzer['dateIndex'],date,date3)
    iterador = llaves ['first']
    
    
    date_F = iterador ['info']    
    total = lt.size(me.getValue(om.get (analyzer['dateIndex'], date_F)))
    respuesta['total'] +=  total
    accidentes = me.getValue(om.get (analyzer['dateIndex'], date_F))    
    totalx = it.newIterator(accidentes)    
    while it.hasNext(totalx):        
        r = it.next(totalx)        
        rta = m.get(analyzer["accidents"], r)        
        gg = me.getValue(rta)
        lt.addLast(Estados,gg['State'])
    
    while iterador['next'] != None:        
        iterador = iterador ['next']
        llave = iterador ['info']
     
        acc = me.getValue(om.get (analyzer['dateIndex'], llave))
        size = lt.size (acc) 
        respuesta['total'] +=  size
        c = it.newIterator(acc)
        if size > total:
            date_F = llave
            total= size
        while it.hasNext(c):
            n = it.next(c)        
            A = m.get(analyzer["accidents"], n)        
            B = me.getValue(A)
            lt.addLast(Estados,B['State'])                       
    print (lt.size (Estados))
    respuesta["total"] = lt.size (Estados)
    for estado in Estados ['elements']:
        if Estados ['elements'].count(estado) > i:
            i = Estados ['elements'].count(estado)
            respuesta['Estado'] = estado
        
    return respuesta

# ==============================
# Funciones de Comparacion
# ==============================

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

def comparer(value1, value2):
    este = me.getKey(value2)
    if (value1 == este):
        return 0
    elif (value1 > este):
        return 1
    else:
        return -1

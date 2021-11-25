"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import sys
import controller
from DISClib.ADT import list as lt
assert cf

default_limit = 1000
sys.setrecursionlimit(default_limit*10)
######################################################################################################################
# Exposición de Resultados
######################################################################################################################

def PrintLoadingInfo(loading_info):
    print('')
    num_airports = loading_info[0]
    num_routes = loading_info[1]
    num_cities = loading_info[2]
    first_airport_info = loading_info[3]
    last_city_info = loading_info[4]
    print('Información de carga:')
    print('Se cargaron dos grafos en los cuales los vértices son los aeropuertos y los arcos son las rutas aéreas.')
    print('Los pesos de los arcos representan las distancias recorridas en cada ruta.')
    print('Uno de los gráfos cargados es dirigido y el otro es no dirigido.')
    print('Existen', num_airports, 'aeropuertos en el grafo difigido y no dirigido.')
    print('Existen', num_routes, 'rutas en el grafo difigido y no dirigido.')
    print('Existen', num_cities, 'ciudades registradas tanto en "worldcities.csv" como en "airports_full.csv".')
    print('')
    airport_name = first_airport_info['Name']
    airport_city = first_airport_info['City']
    airport_country = first_airport_info['Country']
    airport_latitude = first_airport_info['Latitude']
    airport_longitude = first_airport_info['Longitude']
    print('=============== Primer Aeropuerto Cargado ===============')
    print('+' + 26*'-' + '+' + 26*'-' + '+' + 26*'-'+ '+' + 26*'-' + '+' + 26*'-' + '+')
    print('| {:^25}| {:^25}| {:^25}| {:^25}| {:^25}|'.format('Nombre', 'Ciudad', 'País', 'Latitud', 'Longitud'))
    print('+' + 26*'=' + '+' + 26*'=' + '+' + 26*'='+ '+' + 26*'=' + '+' + 26*'=' + '+')
    print('| {:^25}| {:^25}| {:^25}| {:^25}| {:^25}|'.format(airport_name, airport_city, airport_country, 
                                                                            airport_latitude, airport_longitude))
    print('+' + 26*'-' + '+' + 26*'-' + '+' + 26*'-'+ '+' + 26*'-' + '+' + 26*'-' + '+')
    print('')
    city_name = last_city_info['city']
    city_population = last_city_info['population']
    city_latitude = last_city_info['lat']
    city_longitude = last_city_info['lng']
    print('================= última Ciudad Cargada =================')
    print('+' + 26*'-' + '+' + 26*'-' + '+' + 26*'-'+ '+' + 26*'-' + '+')
    print('| {:^25}| {:^25}| {:^25}| {:^25}|'.format('Nombre', 'Población', 'Latitud', 'Longitud'))
    print('+' + 26*'=' + '+' + 26*'=' + '+' + 26*'='+ '+' + 26*'=' + '+')
    print('| {:^25}| {:^25}| {:^25}| {:^25}|'.format(city_name, city_population, city_latitude, 
                                                                                                city_longitude))
    print('+' + 26*'-' + '+' + 26*'-' + '+' + 26*'-'+ '+' + 26*'-' + '+')

######################################################################################################################
# Menú
######################################################################################################################

def printMenu():
    print('')
    print('Bienvenido')
    print('0- Cargar información en el catálogo')
    print('1- (Req 1) Encontrar puntos de interconexión aérea')
    print('2- (Req 2) Encontrar clústeres de tráfico aéreo')
    print('3- (Req 3) Encontrar la ruta más corta entre ciudades')
    print('4- (Req 4) Utilizar las millas de viajero')
    print('5- (Req 5) Cuantificar el efecto de un aeropuerto cerrado')
    print('6- (Req 6) Comparar con servicio WEB externo')
    print('7- Salir')

######################################################################################################################

def UserProgram():
    printMenu()
    inputs = input('Seleccione una opción para continuar:\n>')
    while int(inputs[0]) != 7:

        if int(inputs[0]) == 0:
            print('Existen 92605 rutas registradas en el archivo "routes_full.csv".')
            routes_sample = int(input('Ingrese el número de rutas aéreas que deasea cargar: '))
            print('Creando catálogo ....')
            catalog = controller.Initialization()
            print('Cargando información de los archivos ....')
            loading_info = controller.LoadData(catalog, routes_sample)
            PrintLoadingInfo(loading_info)

        elif int(inputs[0]) == 1:
            print('Requerimiento 1')

        elif int(inputs[0]) == 2:
            print('Requerimiento 2')

        elif int(inputs[0]) == 3:
            print('Requerimiento 3')

        elif int(inputs[0]) == 4:
            print('Requerimiento 4')

        elif int(inputs[0]) == 5:
            print('Requerimiento 5')

        elif int(inputs[0]) == 6:
            print('Requerimiento 6')

        else:
            print('Ingrese una opción válida.')

        printMenu()
        inputs = input('Seleccione una opción para continuar\n')
    print('')
    print('Gracias por utilizar mi programa...')
    print('')


UserProgram()
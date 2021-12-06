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
import controller
import sys
assert cf

default_limit = 1000
sys.setrecursionlimit(default_limit*10)

######################################################################################################################
# Exposición de Resultados
######################################################################################################################

def PrintLoadingInfo(loading_info):
    num_cities = loading_info[1]
    num_airports = loading_info[2]
    num_routes_graph = loading_info[3]
    num_routes_digraph = loading_info[4]
    airports_info_list = loading_info[5]
    cities_info_list = loading_info[6]
    
    print('=== Airports-Routes DiGraph ===')
    print('Nodes:', num_airports, 'loaded airports.')
    print('Edges:', num_routes_digraph, 'loaded routes.')
    print('')
    print('=== Airports-Routes Graph ===')
    print('Nodes:', num_airports, 'loaded airports.')
    print('Edges:', num_routes_graph, 'loaded routes.')
    print('')
    print('=== First & Last Airport loaded in the Graph and Digraph ===')
    print('+' + 8*'-' + '+' + 51*'-' + '+' + 31*'-'+ '+' + 31*'-' + '+' + 15*'-' + '+' + 15*'-' + '+')
    print('| {:<7}| {:<50}| {:<30}| {:<30}| {:<14}| {:<14}|'.format('IATA', 'Name', 'City', 'Country',
                                                                                        'Latitude', 'Longitude'))
    print('+' + 8*'=' + '+' + 51*'=' + '+' + 31*'='+ '+' + 31*'=' + '+' + 15*'=' + '+' + 15*'=' + '+')
    for airport in airports_info_list:
        IATA = airport['IATA']
        name = airport['Name']
        city = airport['City']
        country = airport['Country']
        lat = airport['Latitude']
        lon = airport['Longitude']
        print('| {:<7}| {:<50}| {:<30}| {:<30}| {:<14}| {:<14}|'.format(IATA, name, city, country, lat, lon))
        print('+' + 8*'-' + '+' + 51*'-' + '+' + 31*'-'+ '+' + 31*'-' + '+' + 15*'-' + '+' + 15*'-' + '+')
    print('')
    print('== City Network ==')
    print('The number of cities are:', num_cities)
    print('First and Last City loaded in data structure.')
    print('+' + 51*'-' + '+' + 31*'-' + '+' + 21*'-' + '+' + 21*'-' + '+' + 21*'-' + '+')
    print('| {:<50}| {:<30}| {:>20}| {:>20}| {:>20}|'.format('city', 'country', 'lat', 'lon', 'population'))
    print('+' + 51*'=' + '+' + 31*'=' + '+' + 21*'=' + '+' + 21*'=' + '+' + 21*'=' + '+')
    for city in cities_info_list:
        lat = city['lat']
        lon = city['lng']
        name = city['city_ascii']
        country = city['country']
        population = city['population']
        print('| {:<50}| {:<30}| {:>20}| {:>20}| {:>20}|'.format(name, country, lat, lon, population))
        print('+' + 51*'-' + '+' + 31*'-' + '+' + 21*'-' + '+' + 21*'-' + '+' + 21*'-' + '+')

######################################################################################################################

def PrintRequirement1(requirement_list, num_airports):
    print('====== Aeropuertos por Número de Interconexiones ======')
    print('')
    print('Los primeros', num_airports, 'aeropuertos ordenados por número de interconexiones son:')
    print('+' + 17*'-' + '+' + 6*'-'+ '+' + 71*'-' + '+' + 36*'-' + '+' + 36*'-' + '+')
    print('| {:^16}| {:^5}| {:^70}| {:^35}| {:^35}|'.format('Interconexiones', 'IATA', 'Nombre', 'Ciudad', 'País'))
    for airport in requirement_list:
        num_interconnections = airport[0]
        info_airport = airport[1]
        country = info_airport['Country']
        name = info_airport['Name']
        IATA = info_airport['IATA']
        city = info_airport['City']
        print('+' + 17*'=' + '+' + 6*'='+ '+' + 71*'=' + '+' + 36*'=' + '+' + 36*'=' + '+')
        print('| {:<16}| {:<5}| {:<70}| {:<35}| {:<35}|'.format(num_interconnections, IATA, name,
                                                                                                city, country))

    print('+' + 17*'-' + '+' + 6*'-'+ '+' + 71*'-' + '+' + 36*'-' + '+' + 36*'-' + '+')

######################################################################################################################

def PrintCitiesOptions(origin_options_list, destiny_options_list):
    print('')
    print('=================== Opciones de Origen ===================')
    print('')
    origin_options_dict = {}
    counter = 1
    print('+' + 9*'-' + '+' + 25*'-' + '+' + 25*'-' + '+' + 25*'-'+ '+' + 25*'-' + '+' + 25*'-' + '+' + 25*'-' + '+')
    print('| {:^8}| {:^24}| {:^24}| {:^24}| {:^24}| {:^24}| {:^24}|'.format('Opción', 'Nombre', 'Provincia/Estado', 'País',  
                                                                                            'Longitud', 'Latitud', 'ID'))
    for origin_option in origin_options_list:
        state_province = information['admin_name']
        information = origin_option['info']
        country = information['country']
        city_id = information['id']
        name = information['city']
        lat = information['lat']
        lon = information['lng']
        
        print('+' + 9*'=' + '+' + 25*'=' + '+' + 25*'=' + '+' + 25*'='+ '+' + 25*'=' + '+' + 25*'=' + '+' + 25*'=' + '+')
        print('| {:^8}| {:^24}| {:^24}| {:^24}| {:^24}| {:^24}| {:^24}|'.format(counter, name, state_province, country, 
                                                                                        lon,  lat, city_id))
    
        origin_options_dict[counter] = origin_option
        counter += 1
    print('+' + 9*'-' + '+' + 25*'-' + '+' + 25*'-' + '+' + 25*'-'+ '+' + 25*'-' + '+' + 25*'-' + '+' + 25*'-' + '+')
    
    origin_choise = int(input('Ingrese la ciudad que desea considerar como origen: '))
    choosen_origin = origin_options_dict[origin_choise]
    print('')
    print('=================== Opciones de Destino ===================')
    destiny_options_dict = {}
    counter = 1
    print('+' + 9*'-' + '+' + 25*'-' + '+' + 25*'-' + '+' + 25*'-'+ '+' + 25*'-' + '+' + 25*'-' + '+' + 25*'-' + '+')
    print('| {:^8}| {:^24}| {:^24}| {:^24}| {:^24}| {:^24}| {:^24}|'.format('Opción', 'Nombre', 'Provincia/Estado', 'País',  
                                                                                            'Longitud', 'Latitud', 'ID'))
    for destiny_option in destiny_options_list:
        information = destiny_option['info']
        state_province = information['admin_name']
        country = information['country']
        longitude = information['lng']
        latitude = information['lat']
        city_id = information['id']
        name = information['city']
        
        print('+' + 9*'=' + '+' + 25*'=' + '+' + 25*'=' + '+' + 25*'='+ '+' + 25*'=' + '+' + 25*'=' + '+' + 25*'=' + '+')
        print('| {:^8}| {:^24}| {:^24}| {:^24}| {:^24}| {:^24}| {:^24}|'.format(counter, name, state_province, country, 
                                                                                        longitude,  latitude, city_id))
        
        destiny_options_dict[counter] = destiny_option
        counter += 1
    print('+' + 9*'-' + '+' + 25*'-' + '+' + 25*'-' + '+' + 25*'-'+ '+' + 25*'-' + '+' + 25*'-' + '+' + 25*'-' + '+')
    
    destiny_choise = int(input('Ingrese la ciudad que desea considerar como destino: '))
    choosen_destiny = destiny_options_dict[destiny_choise]

    return choosen_origin, choosen_destiny


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
    print('')
    while int(inputs[0]) != 7:

        if int(inputs[0]) == 0:
            print('Existen 92605 rutas registradas en "routes_full.csv".')
            routes_sample = int(input('Ingrese el número de rutas aéreas que deasea cargar: '))
            print('Creando catálogo ....')
            initialization_info = controller.Initialization()
            time_initialization = initialization_info[0]
            catalog = initialization_info[1]
            print('Cargando información de los archivos ....')
            loading_info = controller.LoadData(catalog, routes_sample)
            time_loading = loading_info[0]
            time = time_initialization + time_loading
            print('')
            print('El carge de datos tardó', time, 'mseg en ejecutarse')
            print('')
            PrintLoadingInfo(loading_info)

        elif int(inputs[0]) == 1:
            num_airports = int(input('Elija el número de aeropuertos que desea ver: '))
            print('Cargando resultados...')
            requirement_info = controller.Requirement1(catalog, num_airports)
            requirement_list = requirement_info[1]
            time = requirement_info[0]
            print('')
            print('El requerimiento tardó', time, 'mseg en ejecutarse')
            print('')
            PrintRequirement1(requirement_list, num_airports)

        elif int(inputs[0]) == 2:
            print('Requerimiento 2')

        elif int(inputs[0]) == 3:
            origin = input('Ingrese la ciudad de origen (sin signos de puntuación): ')
            destiny = input('Ingrese la ciudad de destino (sin signos de puntuación): ')
            cities_options = controller.GetCitiesOptions(origin, destiny, catalog)
            origin_options_list = cities_options[0]
            destiny_options_list = cities_options[1]
            choosen_cities = PrintCitiesOptions(origin_options_list, destiny_options_list)
            choosen_origin = choosen_cities[0]
            choosen_destiny = choosen_cities[1]
            #controller.Requirement3(choosen_origin, choosen_destiny, catalog)
            

        elif int(inputs[0]) == 4:
            print('Requerimiento 4')

        elif int(inputs[0]) == 5:
            print('Requerimiento 5')

        elif int(inputs[0]) == 6:
            print('Requerimiento 6')

        else:
            print('')
            print('Ingrese una opción válida.')

        printMenu()
        inputs = input('Seleccione una opción para continuar\n')
        print('')
        
    print('Gracias por utilizar mi programa...')
    print('')

UserProgram()
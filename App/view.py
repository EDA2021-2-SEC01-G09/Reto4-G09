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
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import map as mp
import folium as fl
import controller
import sys
assert cf

default_limit = 10000
sys.setrecursionlimit(default_limit*10)

###################################################################################################################################
# Exposición de Resultados
###################################################################################################################################
def PrintCities(cities_list):
    print('+' + 51*'-' + '+' + 31*'-' + '+' + 21*'-' + '+' + 21*'-' + '+' + 21*'-' + '+')
    print('| {:<50}| {:<30}| {:>20}| {:>20}| {:>20}|'.format('city', 'country', 'latitude', 'longitude', 'population'))
    print('+' + 51*'=' + '+' + 31*'=' + '+' + 21*'=' + '+' + 21*'=' + '+' + 21*'=' + '+')
    for city in cities_list:
        lat = city['lat']
        lon = city['lng']
        name = city['city_ascii']
        country = city['country']
        population = city['population']
        print('| {:<50}| {:<30}| {:>20}| {:>20}| {:>20}|'.format(name, country, lat, lon, population))
        print('+' + 51*'-' + '+' + 31*'-' + '+' + 21*'-' + '+' + 21*'-' + '+' + 21*'-' + '+')

###################################################################################################################################
def PrintAirports(airports_list):
    print('+' + 8*'-' + '+' + 51*'-' + '+' + 31*'-'+ '+' + 31*'-' + '+' + 15*'-' + '+' + 15*'-' + '+')
    print('| {:<7}| {:<50}| {:<30}| {:<30}| {:<14}| {:<14}|'.format('IATA', 'Name', 'City', 'Country',
                                                                                        'Latitude', 'Longitude'))
    print('+' + 8*'=' + '+' + 51*'=' + '+' + 31*'='+ '+' + 31*'=' + '+' + 15*'=' + '+' + 15*'=' + '+')
    for airport in airports_list:
        IATA = airport['IATA']
        name = airport['Name']
        city = airport['City']
        country = airport['Country']
        lat = airport['Latitude']
        lon = airport['Longitude']
        print('| {:<7}| {:<50}| {:<30}| {:<30}| {:<14}| {:<14}|'.format(IATA, name, city, country, lat, lon))
        print('+' + 8*'-' + '+' + 51*'-' + '+' + 31*'-'+ '+' + 31*'-' + '+' + 15*'-' + '+' + 15*'-' + '+')

###############################################################################################################################
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
    PrintAirports(airports_info_list)
    print('')
    print('== City Network ==')
    print('The number of cities are:', num_cities)
    print('First and Last City loaded in data structure.')
    PrintCities(cities_info_list)

###################################################################################################################################

def PrintRequirement1(catalog, loading_info, requirement_info):
    airports_map = catalog['airports_map']
    num_connected_airports = requirement_info[2]
    requirement_list = requirement_info[1]
    num_airports = loading_info[2]
    airport_coordinates = requirement_info[3]
    adjacent_airports_list = requirement_info[4]
    print('=============== Req No. 1 Inputs ===============')
    print('Most connectected airports in network (TOP 5)')
    print('Number of airports in network:', num_airports)
    print('')
    print('=============== Req No. 1 Answer ===============')
    print('Connected airports inside network:', num_connected_airports)
    print('Top 5 most connected airports...')
    for airport in requirement_list:
        info_airport = airport[0]
        country = info_airport['Country']
        name = info_airport['Name']
        IATA = info_airport['IATA']
        city = info_airport['City']
        num_interconnections = airport[1]
        num_inbound = airport[2]
        num_outbound = airport[3]  
        print('+' + 51*'='+ '+' + 31*'=' + '+' + 31*'=' + '+' + 8*'=' + '+' + 16*'=' + '+' + 11*'=' + '+' + 11*'=' + '+')
        print('| {:<50}| {:<30}| {:<30}| {:<7}| {:>15}| {:>10}| {:>10}|'.format(name, city, country, IATA, 
                                                                    num_interconnections, num_inbound, num_outbound))
    print('+' + 51*'-'+ '+' + 31*'-' + '+' + 31*'-' + '+' + 8*'-' + '+' + 16*'-' + '+' + 11*'-' + '+' + 11*'-' + '+')

    requirement_map = fl.Map(location=airport_coordinates)

    for adj_airport_IATA in adjacent_airports_list:
        adj_airport_info_key_value = mp.get(airports_map, adj_airport_IATA)
        adj_airport_info = me.getValue(adj_airport_info_key_value)
        adj_airport_latitude = adj_airport_info['Latitude']
        adj_airport_longitude = adj_airport_info['Longitude']
        loc = [ airport_coordinates,
                (adj_airport_latitude, adj_airport_longitude)]

        fl.PolyLine(loc,
                color='green',
                weight=15,
                opacity=0.9).add_to(requirement_map)
    requirement_map.save('Requirement_1.html')

###################################################################################################################################

def PrintRequirement2(requirement_info, airport_1, airport_2):
    airports_info_list = requirement_info[1]
    num_SCC = requirement_info[2]
    answer = requirement_info[3]

    print('=============== Req No. 2 Inputs ===============')
    print('Airport-1 IATA code:', airport_1)
    print('Airport-2 IATA code:', airport_2)
    print('')
    airports_names = []
    for info_airport in airports_info_list:
        country = info_airport['Country']
        name = info_airport['Name']
        IATA = info_airport['IATA']
        city = info_airport['City']
        print('+++ Airport IATA code:', IATA, '+++')
        print('+' + 8*'-'+ '+' + 51*'-' + '+' + 31*'-' + '+' + 31*'-' + '+')
        print('| {:>7}| {:>50}| {:>30}| {:>30}|'.format('IATA', 'Name', 'City', 'Country'))
        print('+' + 8*'='+ '+' + 51*'=' + '+' + 31*'=' + '+' + 31*'=' + '+')
        print('| {:>7}| {:>50}| {:>30}| {:>30}|'.format(IATA, name, city, country))
        print('+' + 8*'-'+ '+' + 51*'-' + '+' + 31*'-' + '+' + 31*'-' + '+')
        airports_names.append(name)
    print('')
    print('- Numbre of SCC in Airport-Route network:', num_SCC)
    print("- Does the '" + airports_names[0] + "' and the '" + airports_names[1], "' belong together?")
    print('- ANS:', answer)

###################################################################################################################################

def PrintCitiesOptionsRequirement3(origin_options_list, destiny_options_list):
    origin_options_dict = {}
    counter = 1
    print('=================== Departure Options ===================')
    print('')
    print('+' + 9*'-' + '+' + 25*'-' + '+' + 25*'-' + '+' + 25*'-'+ '+' + 25*'-' + '+' + 25*'-' + '+' + 25*'-' + '+')
    print('| {:^8}| {:^24}| {:^24}| {:^24}| {:^24}| {:^24}| {:^24}|'.format('Option', 'Name', 'Province/State',
                                                                        'Country', 'Longitude', 'Latitude', 'ID'))
    for origin_option in origin_options_list:
        information = origin_option['info']
        state_province = information['admin_name']
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
    
    origin_choise = int(input('Enter the departure city option: '))
    choosen_origin = origin_options_dict[origin_choise]
    print('')
    print('=================== Destination Options ===================')
    destiny_options_dict = {}
    counter = 1
    print('+' + 9*'-' + '+' + 25*'-' + '+' + 25*'-' + '+' + 25*'-'+ '+' + 25*'-' + '+' + 25*'-' + '+' + 25*'-' + '+')
    print('| {:^8}| {:^24}| {:^24}| {:^24}| {:^24}| {:^24}| {:^24}|'.format('Option', 'Name', 'Province/State',
                                                                        'Country', 'Longitude', 'Latitude', 'ID'))
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
    
    destiny_choise = int(input('Enter the destination city option: '))
    choosen_destiny = destiny_options_dict[destiny_choise]

    return choosen_origin, choosen_destiny

###################################################################################################################################

def PrintRequirement3(origin, destiny, requirement_info):
    origin_airport_info = requirement_info[1]
    destiny_airport_info = requirement_info[2]
    distance = requirement_info[3]
    trip_path_list = requirement_info[4]
    trip_path_airports_list = requirement_info[5]
    print('=============== Req No. 3 Inputs ===============')
    print('Departure city:', origin)
    print('Arrival city:', destiny)
    print('')
    print('=============== Req No. 3 Answer ===============')
    print('+++ The departure airport in', origin, 'is +++')
    country = origin_airport_info['Country']
    name = origin_airport_info['Name']
    IATA = origin_airport_info['IATA']
    city = origin_airport_info['City']
    print('+' + 8*'-'+ '+' + 51*'-' + '+' + 31*'-' + '+' + 31*'-' + '+')
    print('| {:>7}| {:>50}| {:>30}| {:>30}|'.format('IATA', 'Name', 'City', 'Country'))
    print('+' + 8*'='+ '+' + 51*'=' + '+' + 31*'=' + '+' + 31*'=' + '+')
    print('| {:>7}| {:>50}| {:>30}| {:>30}|'.format(IATA, name, city, country))
    print('+' + 8*'-'+ '+' + 51*'-' + '+' + 31*'-' + '+' + 31*'-' + '+')
    print('')
    print('+++ The arrival airport in', destiny, 'is +++')
    country = destiny_airport_info['Country']
    name = destiny_airport_info['Name']
    IATA = destiny_airport_info['IATA']
    city = destiny_airport_info['City']
    print('+' + 8*'-'+ '+' + 51*'-' + '+' + 31*'-' + '+' + 31*'-' + '+')
    print('| {:>7}| {:>50}| {:>30}| {:>30}|'.format('IATA', 'Name', 'City', 'Country'))
    print('+' + 8*'='+ '+' + 51*'=' + '+' + 31*'=' + '+' + 31*'=' + '+')
    print('| {:>7}| {:>50}| {:>30}| {:>30}|'.format(IATA, name, city, country))
    print('+' + 8*'-'+ '+' + 51*'-' + '+' + 31*'-' + '+' + 31*'-' + '+')
    print('')
    print('Dijkstra´s trip detatails +++')
    print('- Total distance:', distance)    
    print('- Trip path: ')
    print('+' + 15*'-'+ '+' + 15*'-' + '+' + 15*'-' + '+' + 15*'-' + '+')
    print('| {:<14}| {:<14}| {:<14}| {:>14}|'.format('Airline', 'Departure', 'Destination', 'distance_km'))
    for path_info in trip_path_list:
        airline = path_info['Airline']
        departure = path_info['Departure']
        destination = path_info['Destination']
        distance = path_info['distance_km']
        print('+' + 15*'='+ '+' + 15*'=' + '+' + 15*'=' + '+' + 15*'=' + '+')
        print('| {:<14}| {:<14}| {:<14}| {:>14}|'.format(airline, departure, destination, distance))
    print('+' + 15*'-'+ '+' + 15*'-' + '+' + 15*'-' + '+' + 15*'-' + '+')
    print('- Trip Stops:')
    print('+' + 8*'-'+ '+' + 51*'-' + '+' + 31*'-' + '+' + 31*'-' + '+')
    print('| {:>7}| {:>50}| {:>30}| {:>30}|'.format('IATA', 'Name', 'City', 'Country'))        
    for airport_info in trip_path_airports_list:
        country = airport_info['Country']
        name = airport_info['Name']
        IATA = airport_info['IATA']
        city = airport_info['City']
        print('+' + 8*'='+ '+' + 51*'=' + '+' + 31*'=' + '+' + 31*'=' + '+')
        print('| {:>7}| {:>50}| {:>30}| {:>30}|'.format(IATA, name, city, country))
    print('+' + 8*'-'+ '+' + 51*'-' + '+' + 31*'-' + '+' + 31*'-' + '+')

###################################################################################################################################

def PrintCitiesOptionsRequirement4(cities_options):
    city_options_dict = {}
    counter = 1
    print('=================== City Options ===================')
    print('')
    print('+' + 9*'-' + '+' + 25*'-' + '+' + 25*'-' + '+' + 25*'-'+ '+' + 25*'-' + '+' + 25*'-' + '+' + 25*'-' + '+')
    print('| {:^8}| {:^24}| {:^24}| {:^24}| {:^24}| {:^24}| {:^24}|'.format('Option', 'Name', 'Province/State',
                                                                        'Country', 'Longitude', 'Latitude', 'ID'))
    for city_option in cities_options:
        information = city_option['info']
        state_province = information['admin_name']
        country = information['country']
        city_id = information['id']
        name = information['city']
        lat = information['lat']
        lon = information['lng']
        print('+' + 9*'=' + '+' + 25*'=' + '+' + 25*'=' + '+' + 25*'='+ '+' + 25*'=' + '+' + 25*'=' + '+' + 25*'=' + '+')
        print('| {:^8}| {:^24}| {:^24}| {:^24}| {:^24}| {:^24}| {:^24}|'.format(counter, name, state_province, country, 
                                                                                        lon,  lat, city_id))
    
        city_options_dict[counter] = city_option
        counter += 1
    print('+' + 9*'-' + '+' + 25*'-' + '+' + 25*'-' + '+' + 25*'-'+ '+' + 25*'-' + '+' + 25*'-' + '+' + 25*'-' + '+')
    
    city_choise = int(input('Enter the departure city option: '))
    choosen_city = city_options_dict[city_choise]

    return choosen_city

###################################################################################################################################

def PrintRequirement4(choosen_city, miles, requirement_info):
    airport_info = requirement_info[1]
    routes_path_list = requirement_info[2]
    num_possible_airports = requirement_info[3]
    max_traveling_distance = requirement_info[4]
    longest_path_distance = requirement_info[5]
    miles_need = requirement_info[6]
    country = airport_info['Country']
    name = airport_info['Name']
    IATA = airport_info['IATA']
    city = airport_info['City']
    print('=============== Req No. 4 Inputs ===============')
    print('City choise:', choosen_city['info']['city'])
    print('Departure IATA code:', IATA)
    print('AVaible Travel Miles:', miles)
    print('')
    print('=============== Req No. 4 Answer ===============')
    print('+++ Departure Airport for IATA code:', IATA, '+++')
    print('+' + 8*'-'+ '+' + 51*'-' + '+' + 31*'-' + '+' + 31*'-' + '+')
    print('| {:>7}| {:>50}| {:>30}| {:>30}|'.format('IATA', 'Name', 'City', 'Country'))
    print('+' + 8*'='+ '+' + 51*'=' + '+' + 31*'=' + '+' + 31*'=' + '+')
    print('| {:>7}| {:>50}| {:>30}| {:>30}|'.format(IATA, name, city, country))
    print('+' + 8*'-'+ '+' + 51*'-' + '+' + 31*'-' + '+' + 31*'-' + '+')
    print('')
    print('- Number of possible airports:', num_possible_airports, '.')
    print('- Max traveling distance between airports:', max_traveling_distance, '(km).')
    print('- Passenger avalaible traveling miles:', miles*1.6, '(km).')
    print('')
    print("+++ Longest possible route with airport '" + IATA + "' +++")
    print('- Longest possible path distance:', longest_path_distance, ' (km).')
    print('- Longest possible path details:')
    print('+' + 15*'-'+ '+' + 15*'-' + '+' + 15*'-' + '+' + 15*'-' + '+')
    print('| {:<14}| {:<14}| {:<14}| {:>14}|'.format('Airline', 'Departure', 'Destination', 'distance_km'))
    for path_info in routes_path_list:
        airline = path_info['Airline']
        departure = path_info['Departure']
        destination = path_info['Destination']
        distance = path_info['distance_km']
        print('+' + 15*'='+ '+' + 15*'=' + '+' + 15*'=' + '+' + 15*'=' + '+')
        print('| {:<14}| {:<14}| {:<14}| {:>14}|'.format(airline, departure, destination, distance))
    print('+' + 15*'-'+ '+' + 15*'-' + '+' + 15*'-' + '+' + 15*'-' + '+')
    print('-----')
    print('The passenger needs', miles_need, 'miles to complete the trip.')
    print('-----')

###################################################################################################################################

def PrintRequirement5(IATA, loading_info, requirement_info):
    num_airports = loading_info[2]
    num_routes_graph = loading_info[3]
    num_routes_digraph = loading_info[4]
    effected_airports_list = requirement_info[1]
    resulting_num_routes_digraph = requirement_info[2]
    resulting_num_routes_graph = requirement_info[3]
    affected_airports = requirement_info[4]
    print('=============== Req No. 5 Inputs ===============')
    print('Closing the airport with IATA code:', IATA)
    print('')
    print('--- Airports-Routes DiGraph ---')
    print('Original number of Airports:', num_airports, 'and Routes:', num_routes_digraph)
    print('--- Airports-Routes Graph ---')
    print('Original number of Airports:', num_airports, 'and Routes:', num_routes_graph)
    print('')
    print('+++ Removing Airports with IATA:', IATA, '+++')
    print('')
    print('--- Airports-Routes DiGraph ---')
    print('Resulting number of Airports:', num_airports - 1, 'and Routes:', num_routes_digraph - resulting_num_routes_digraph)
###################################################################################################################################
    print('--- Airports-Routes Graph ---')
    print('Resulting number of Airports:', num_airports - 1, 'and Routes:', num_routes_graph - resulting_num_routes_graph)
    print('')
    print('=============== Req No. 5 Answer ===============')
    print('There are', affected_airports, 'Airports affected by the removal of', IATA)
    print('The first & last 3 Airports affected are:')
    print('+' + 8*'-'+ '+' + 51*'-' + '+' + 31*'-' + '+' + 31*'-' + '+')
    print('| {:>7}| {:>50}| {:>30}| {:>30}|'.format('IATA', 'Name', 'City', 'Country'))     
    for airport_info in effected_airports_list:
        country = airport_info['Country']
        name = airport_info['Name']
        IATA = airport_info['IATA']
        city = airport_info['City']
        print('+' + 8*'='+ '+' + 51*'=' + '+' + 31*'=' + '+' + 31*'=' + '+')
        print('| {:>7}| {:>50}| {:>30}| {:>30}|'.format(IATA, name, city, country))
    print('+' + 8*'-'+ '+' + 51*'-' + '+' + 31*'-' + '+' + 31*'-' + '+')


###################################################################################################################################
# Menú
###################################################################################################################################

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

###################################################################################################################################

def UserProgram():
    printMenu()
    inputs = int(input('Seleccione una opción para continuar:\n>'))
    print('')
    while inputs != 7:
        if inputs == 0:
            print('There exist 92605 routes registred in "routes_full.csv".')
            routes_sample = int(input('Enter the number of routes to load: '))
            print('Creating catalog ....')
            initialization_info = controller.Initialization()
            time_initialization = initialization_info[0]
            catalog = initialization_info[1]
            print('Loading information from files ....')
            loading_info = controller.LoadData(catalog, routes_sample)
            time_loading = loading_info[0]
            time = time_initialization + time_loading
            print('')
            print('Loading data took', time, 'mseg')
            print('')
            PrintLoadingInfo(loading_info)

        elif inputs == 1:
            print('Loading result...')
            requirement_info = controller.Requirement1(catalog)
            time = requirement_info[0]
            print('')
            print('The requirement took', time, 'mseg')
            print('')
            PrintRequirement1(catalog, loading_info, requirement_info)

        elif inputs == 2:
            airport_1 = input('Enter the IATA code of the first airport: ')
            airport_2 = input('Enter the IATA code of the second airport: ')
            print('Loading results...')
            requirement_info = controller.Requirement2(catalog, airport_1, airport_2)
            time = requirement_info[0]
            print('')
            print('The requirement took', time, 'mseg')
            print('')
            PrintRequirement2(requirement_info, airport_1, airport_2)

        elif inputs == 3:
            origin = input('Enter the departure city: ')
            destiny = input('Enter the destination city: ')
            print('Loading results...')
            cities_options = controller.GetCitiesOptionsRequirement3(catalog, origin, destiny)
            origin_options_list = cities_options[0]
            destiny_options_list = cities_options[1]
            choosen_cities = PrintCitiesOptionsRequirement3(origin_options_list, destiny_options_list)
            requirement_info = controller.Requirement3(catalog, choosen_cities)
            time = requirement_info[0]
            print('')
            print('The requirement took', time, 'mseg')
            print('')
            PrintRequirement3(origin, destiny, requirement_info)

        elif inputs == 4:
            city = input('Enter the city: ')
            miles = int(input('Enter the number of miles avaible: '))
            print('Loading results...')
            cities_options = controller.GetCitiesOptionsRequirement4(catalog, city)
            choosen_city = PrintCitiesOptionsRequirement4(cities_options)
            requirement_info = controller.Requirement4(catalog, choosen_city, miles)
            time = requirement_info[0]
            print('')
            print('The requirement took', time, 'mseg')
            print('')
            PrintRequirement4(choosen_city, miles, requirement_info)

        elif inputs == 5:
            IATA = input('Enter the IATA code of the airport: ')
            print('Loading results...')
            requirement_info = controller.Requirement5(catalog, IATA)
            print('')
            print('The requirement took', time, 'mseg')
            print('')
            PrintRequirement5(IATA, loading_info, requirement_info)

        elif inputs == 6:
            print('Requerimiento 6')

        else:
            print('')
            print('Ingrese una opción válida.')

        printMenu()
        inputs = int(input('Seleccione una opción para continuar\n>'))
        print('')
        
    print('Gracias por utilizar mi programa...')
    print('')

UserProgram()
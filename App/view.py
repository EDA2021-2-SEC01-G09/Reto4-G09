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

default_limit = 10000
sys.setrecursionlimit(default_limit*10)

###########################################################################
# Exposición de Resultados
###########################################################################
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

###########################################################################
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

###########################################################################

def PrintRoutes(routes_list):
    print('+' + 15*'-'+ '+' + 15*'-' + '+' + 15*'-' + '+' + 15*'-' + '+')
    print('| {:<14}| {:<14}| {:<14}| {:>14}|'.format('Airline', 'Departure', 'Destination', 'distance_km'))
    print('+' + 15*'='+ '+' + 15*'=' + '+' + 15*'=' + '+' + 15*'=' + '+')
    for path_info in routes_list:
        airline = path_info['Airline']
        departure = path_info['Departure']
        destination = path_info['Destination']
        distance = path_info['distance_km']
        print('| {:<14}| {:<14}| {:<14}| {:>14}|'.format(airline, departure, destination, distance))
        print('+' + 15*'-'+ '+' + 15*'-' + '+' + 15*'-' + '+' + 15*'-' + '+')

###########################################################################

def PrintCitiesOptions(city_options_list, test):
    if test:
        city_options_dict = {}
        counter = 1
        for city_option in city_options_list:
            city_options_dict[counter] = city_option
            counter += 1
        choosen_city = city_options_dict[1]
    else:
        city_options_dict = {}
        counter = 1
        print('+' + 9*'-' + '+' + 25*'-' + '+' + 25*'-' + '+' + 25*'-'+ '+' + 25*'-' + '+' + 25*'-' + '+' + 25*'-' + '+')
        print('| {:^8}| {:^24}| {:^24}| {:^24}| {:^24}| {:^24}| {:^24}|'.format('Option', 'Name', 'Province/State',
                                                                            'Country', 'Longitude', 'Latitude', 'ID'))
        for city_option in city_options_list:
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

###########################################################################
def PrintLoadingInfo(loading_info):
    num_cities = loading_info[1]
    num_airports = loading_info[2]
    num_routes_digraph = loading_info[3]
    num_routes_graph = loading_info[4]
    num_edges_digraph = loading_info[5]
    num_edges_graph = loading_info[6]
    airports_list = loading_info[7]
    cities_list = loading_info[8]
    
    print('=== Airports-Routes DiGraph ===')
    print(num_airports, 'loaded airports.')
    print(num_routes_digraph, 'loaded routes.')
    print('Nodes:', num_airports, '& Edges:', num_edges_digraph)
    print('')
    print('=== Airports-Routes Graph ===')
    print(num_airports, 'loaded airports.')
    print(num_routes_graph, 'loaded routes.')
    print('Nodes:', num_airports, '& Edges:', num_edges_graph)
    print('')
    print('=== First & Last Airport loaded in the Graph and Digraph ===')
    PrintAirports(airports_list)
    print('')
    print('== City Network ==')
    print('The number of cities are:', num_cities)
    print('First and Last City loaded in data structure.')
    PrintCities(cities_list)

###########################################################################

def PrintRequirement1(loading_info, requirement_info):
    num_connected_airports = requirement_info[2]
    requirement_list = requirement_info[1]
    num_airports = loading_info[2]
    print('=============== Req No. 1 Inputs ===============')
    print('Most connectected airports in network (TOP 5)')
    print('Number of airports in network:', num_airports)
    print('')
    print('=============== Req No. 1 Answer ===============')
    print('Connected airports inside network:', num_connected_airports)
    print('Top 5 most connected airports...')
    print('+' + 51*'-'+ '+' + 31*'-' + '+' + 31*'-' + '+' + 8*'-' + '+' + 16*'-' + '+' + 11*'-' + '+' + 11*'-' + '+')
    print('| {:<50}| {:<30}| {:<30}| {:<7}| {:>15}| {:>10}| {:>10}|'.format('Name', 'City', 'Country', 'IATA', 
                                                                                    'connections', 'inbound', 'outbound'))
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
    print('')

###########################################################################

def PrintRequirement2(requirement_info, airport_1, airport_2):
    airports_list = requirement_info[1]
    num_SCC = requirement_info[2]
    answer = requirement_info[3]
    print('=============== Req No. 2 Inputs ===============')
    print('Airport-1 IATA code:', airport_1)
    print('Airport-2 IATA code:', airport_2)
    print('')
    print('=============== Req No. 2 Answer ===============')
    PrintAirports(airports_list)
    print('')
    print('- Numbre of SCC in Airport-Route network:', num_SCC)
    print('- Does the', airport_1, 'and the', airport_2, 'belong together?')
    print('- ANS:', answer)
 
###########################################################################

def PrintCitiesOptionsRequirement3(origin_options_list, destiny_options_list):
    print('=================== Departure Options ===================')
    choosen_origin = PrintCitiesOptions(origin_options_list, False)
    print('')
    print('=================== Destination Options ===================')
    choosen_destiny = PrintCitiesOptions(destiny_options_list, False)

    return choosen_origin, choosen_destiny

###########################################################################

def PrintRequirement3(origin, destiny, requirement_info):
    end_airports_list = requirement_info[1]
    distance = requirement_info[2]
    routes_list = requirement_info[3]
    routes_airports_list = requirement_info[4]
    print('=============== Req No. 3 Inputs ===============')
    print('Departure city:', origin)
    print('Arrival city:', destiny)
    print('')
    print('=============== Req No. 3 Answer ===============')
    print('+++ The departure airport in', origin, 'and the arrival airport in', destiny, 'are:')
    PrintAirports(end_airports_list)
    print('')
    print('Dijkstra´s trip detatails +++')
    print('- Total distance:', distance)    
    print('- Trip path: ')
    PrintRoutes(routes_list)
    print('- Trip Stops:')
    PrintAirports(routes_airports_list)
    
###########################################################################

def PrintCitiesOptionsRequirement4(cities_options):
    print('=================== City Options ===================')
    choosen_city = PrintCitiesOptions(cities_options, False)

    return choosen_city

###########################################################################

def PrintRequirement4(choosen_city, miles, requirement_info):
    airport_list = requirement_info[1]
    routes_list = requirement_info[2]
    num_possible_airports = requirement_info[3]
    max_traveling_distance = requirement_info[4]
    longest_path_distance = requirement_info[5]
    miles_need = requirement_info[6]

    city_name = choosen_city['info']['city']
    print('=============== Req No. 4 Inputs ===============')
    print('City choise:', city_name)
    print('AVaible Travel Miles:', miles)
    print('')
    print('=============== Req No. 4 Answer ===============')
    print('+++ Departure Airport for the city', city_name, '+++')
    PrintAirports(airport_list)
    print('')
    print('- Number of possible airports:', num_possible_airports, '.')
    print('- Max traveling distance between airports:', round(max_traveling_distance, 2), '(km).')
    print('- Passenger avalaible traveling miles:', miles*1.6, '(km).')
    print('')
    print('- Longest possible path distance:', round(longest_path_distance, 2), ' (km).')
    print('When there exist two paths of equal length (equal number of edges), we choose the one with lesser miles.')
    print('- Longest possible path details:')
    PrintRoutes(routes_list)
    print('-----')
    print('The passenger needs', round(miles_need, 2), 'miles to complete the trip.')
    print('-----')

###########################################################################

def PrintRequirement5(IATA, loading_info, requirement_info):
    num_airports = loading_info[2]
    num_routes_digraph = loading_info[3]
    num_routes_graph = loading_info[4]
    airports_list = requirement_info[1]
    resulting_num_routes_digraph = requirement_info[2]
    resulting_num_routes_graph = requirement_info[3]
    num_affected_airports = requirement_info[4]
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
    print('--- Airports-Routes Graph ---')
    print('Resulting number of Airports:', num_airports - 1, 'and Routes:', num_routes_graph - resulting_num_routes_graph)
    print('')
    print('=============== Req No. 5 Answer ===============')
    print('There are', num_affected_airports, 'Airports affected by the removal of', IATA)
    print('The first & last 3 Airports affected are:')
    PrintAirports(airports_list)

###########################################################################
# Menú
###########################################################################

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

###########################################################################

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
            PrintRequirement1(loading_info, requirement_info)

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
            time = requirement_info[0]
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

def TestProgram(inputs, catalog, input_1, input_2):
    if inputs == 0:
        initialization_info = controller.Initialization()
        catalog = initialization_info[1]
        controller.LoadData(catalog, input_1)
        return catalog

    elif inputs == 1:
        requirement_info = controller.Requirement1(catalog)
        return requirement_info[0]
            
    elif inputs == 2:
        requirement_info = controller.Requirement2(catalog, input_1, input_2)
        return requirement_info[0]

    elif inputs == 3:
        cities_options = controller.GetCitiesOptionsRequirement3(catalog, input_1, input_2)
        origin_options_list = cities_options[0]
        destiny_options_list = cities_options[1]
        choosen_origin = PrintCitiesOptions(origin_options_list, True)
        choosen_destiny = PrintCitiesOptions(destiny_options_list, True)
        requirement_info = controller.Requirement3(catalog, (choosen_origin, choosen_destiny))
        return requirement_info[0]     

    elif inputs == 4:
        cities_options = controller.GetCitiesOptionsRequirement4(catalog, input_1)
        choosen_city = PrintCitiesOptions(cities_options, True)
        requirement_info = controller.Requirement4(catalog, choosen_city, input_2)
        return requirement_info[0]

    elif inputs == 5:
        requirement_info = controller.Requirement5(catalog, input_1)
        return requirement_info[0]

UserProgram()
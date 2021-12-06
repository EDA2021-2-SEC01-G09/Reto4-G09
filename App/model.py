"""
 * Copyright 2020, Departamento de sistemas y Computación,
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
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """

import config as cf
from haversine import haversine
from DISClib.ADT import map as mp
from DISClib.ADT import list as lt
from DISClib.ADT import graph as gp
from DISClib.DataStructures import rbt
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Trees.traversal import inorder
assert cf

######################################################################################################################
# Construccion de modelos
######################################################################################################################

def Initialization():
    catalog = { 'graph': None,
                'digraph': None,
                'cities_map': None,
                'airports_map': None,
                'airports_list': None}

    catalog['graph'] = gp.newGraph(datastructure='ADJ_LIST',
                                            directed=False,
                                            size=9075,
                                            comparefunction=None)

    catalog['digraph'] = gp.newGraph(datastructure='ADJ_LIST',
                                             directed=True,
                                             size=9075,
                                             comparefunction=None)

    catalog['cities_map'] = mp.newMap(42739, maptype='PROBING', loadfactor=0.5)
    catalog['airports_map'] = mp.newMap(9075, maptype='PROBING', loadfactor=0.5)
    catalog['airports_list'] = lt.newList('ARRAY_LIST')

    return catalog

######################################################################################################################
# Funciones para agregar informacion al catalogo
######################################################################################################################

def AddCity(catalog, city):
    city_RBT = rbt.newMap(minorcmpFunction)
    cities_map = catalog['cities_map']
    city_name = city['city']
    city_value = {  'info': city,
                    'RBT': city_RBT}

    if mp.contains(cities_map, city_name):
        city_key_values_list = mp.get(cities_map, city_name)
        city_values_list = me.getValue(city_key_values_list)
        lt.addLast(city_values_list, city_value)
    else:
        city_values_list = lt.newList('ARRAY_LIST')
        lt.addLast(city_values_list, city_value)
        mp.put(cities_map, city_name, city_values_list)

######################################################################################################################

def AddAirport(catalog, airport):
    airports_list = catalog['airports_list'] 
    airports_map = catalog['airports_map']
    cities_map = catalog['cities_map']  
    digraph = catalog['digraph']
    graph = catalog['graph']

    airport_IATA = airport['IATA']
    airport_city_name = airport['City']
    airport_city_country = airport['Country']

    airport_lat = float(airport['Latitude'])
    airport_lon = float(airport['Longitude'])
    if mp.contains(cities_map, airport_city_name):
        city_key_list_values = mp.get(cities_map, airport_city_name)
        city_list_values = me.getValue(city_key_list_values)

        nearest_city = None
        min_distance = 5*(10**7)
        for city in lt.iterator(city_list_values):
            city_info = city['info']
            city_lat = float(city_info['lat'])
            city_lon = float(city_info['lng'])

            airport_coordinates = (airport_lat, airport_lon)
            city_coordinates = (city_lat, city_lon)
            distance = haversine(airport_coordinates, city_coordinates)
            if distance < min_distance:
                min_distance = distance
                nearest_city = city
        
        nearest_city_RBT = nearest_city['RBT']
        rbt.put(nearest_city_RBT, distance, airport)

    else:
        city = {'city': airport_city_name,
                'city_ascii': airport_city_name,
                'lat': airport_lat,
                'lng': airport_lon,
                'country': airport_city_country,
                'iso2': 'Not Available',
                'iso3': 'Not Available',
                'admin_name': airport_city_name,
                'capital': airport_city_name,
                'population': 'Not Available',
                'id': 'Not Available'}
        AddCity(catalog, city)
        city_key_list_values = mp.get(cities_map, airport_city_name)
        city_list_values = me.getValue(city_key_list_values)
        city = lt.getElement(city_list_values, 1)
        city_RBT = city['RBT']
        rbt.put(city_RBT, 0, airport)

    element = (airport_IATA, airport)
    lt.addLast(airports_list, element)
    mp.put(airports_map, airport_IATA, airport)
    gp.insertVertex(digraph, airport_IATA)
    gp.insertVertex(graph, airport_IATA)

######################################################################################################################

def AddRoute(catalog, route, undirected_routes_map):
    digraph = catalog['digraph']
    graph = catalog['graph']

    departure_IATA = route['Departure']
    destination_IATA = route['Destination']
    distance = float(route['distance_km'])

    gp.addEdge(digraph, departure_IATA, destination_IATA, distance)
    gp.addEdge(graph, destination_IATA, departure_IATA, distance)      

    forward_route = mp.get(undirected_routes_map, departure_IATA + destination_IATA)
    backward_route = mp.get(undirected_routes_map, destination_IATA + departure_IATA)
    if forward_route == None:
        if backward_route != None:
            backward_route_value = me.getValue(backward_route)
            if backward_route_value >= 1:
                mp.put(undirected_routes_map, destination_IATA + departure_IATA, backward_route_value - 1)
                add_num_routes_graph = 1
            else:
                mp.put(undirected_routes_map, departure_IATA + destination_IATA, 1)
                add_num_routes_graph = 1
        else:
            mp.put(undirected_routes_map, departure_IATA + destination_IATA, 1)
            add_num_routes_graph = 0       
    else:
        forward_route_value = me.getValue(forward_route)
        if backward_route != None:
            backward_route_value = me.getValue(backward_route)
            if backward_route_value >= 1 and forward_route_value >= 1:
                mp.put(undirected_routes_map, destination_IATA + departure_IATA, backward_route_value - 1)
                mp.put(undirected_routes_map, departure_IATA + destination_IATA, forward_route_value - 1)
                add_num_routes_graph = 1
            else:
                mp.put(undirected_routes_map, departure_IATA + destination_IATA, forward_route_value + 1)
                add_num_routes_graph = 0
        else:
            mp.put(undirected_routes_map, departure_IATA + destination_IATA, forward_route_value + 1)
            add_num_routes_graph = 0  

    return add_num_routes_graph 
                

######################################################################################################################
# Funciones para creacion de datos
######################################################################################################################

def GetCitiesOptions(origin, destiny, catalog):
    cities_map = catalog['cities_map']
    
    origin_options_key_value = mp.get(cities_map, origin)
    destiny_options_key_value = mp.get(cities_map, destiny)
    origin_options_value = me.getValue(origin_options_key_value)
    destiny_options_value = me.getValue(destiny_options_key_value)
    origin_options_list = lt.iterator(origin_options_value)
    destiny_options_list = lt.iterator(destiny_options_value)

    return origin_options_list, destiny_options_list

######################################################################################################################
# Funciones de consulta
######################################################################################################################

def Requirement1(catalog, num_airports):
    digraph = catalog['digraph']
    airports_list = catalog['airports_list']
    interconnections_RBT = rbt.newMap(Requirement1cmpFunction)

    num_connected_airports = 0
    for airport in lt.iterator(airports_list):
        information = airport[1]
        IATA = airport[0]
        airport_indegre = gp.indegree(digraph, IATA)
        airport_outdegree = gp.outdegree(digraph, IATA)
        num_interconnections = airport_indegre + airport_outdegree
        element = information, num_interconnections, airport_indegre, airport_outdegree
        rbt.put(interconnections_RBT, (num_interconnections, airport_indegre, airport_outdegree), element)
        if num_interconnections > 0:
            num_connected_airports += 1

    initial_requirement_list = inorder(interconnections_RBT)
    final_requirement_list = lt.subList(initial_requirement_list, 1, num_airports)
    requirement_list = lt.iterator(final_requirement_list)

    return requirement_list, num_connected_airports
    
######################################################################################################################
# Funciones utilizadas para comparar elementos dentro de una lista
######################################################################################################################

def minorcmpFunction(key_1, key_2):
    if key_1 >= key_2:
        return 1
    else:
        return -1

######################################################################################################################

def majorcmpFunction(key_1, key_2):
    if key_1 <= key_2:
        return 1
    else:
        return -1

######################################################################################################################

def Requirement1cmpFunction(key_1, key_2):
    num_interconnections_1 = key_1[0]
    num_interconnections_2 = key_2[0]
    airport_indegre_1 = key_1[1]
    airport_indegre_2 = key_2[1]
    airport_outdegree_1 = key_1[2]
    airport_outdegree_2 = key_2[2]
    if num_interconnections_1 < num_interconnections_2:
        return 1
    elif num_interconnections_1 == num_interconnections_2:
        if airport_indegre_1 < airport_indegre_2:
            return 1
        elif airport_indegre_1 == airport_indegre_2:
            if airport_outdegree_1 <= airport_outdegree_2:
                return 1
            else:
                return -1
        else:
            return -1
    else:
        return -1

######################################################################################################################
# Funciones de ordenamiento
######################################################################################################################
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
    catalog = { 'directed_graph': None,
                'undirected_graph': None,
                'cities_map': None,
                'airports_map': None}

    catalog['directed_graph'] = gp.newGraph(datastructure='ADJ_LIST',
                                            directed=True,
                                            size=9075,
                                            comparefunction=None)

    catalog['undirected_graph'] = gp.newGraph(datastructure='ADJ_LIST',
                                             directed=False,
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
    cities_map = catalog['cities_map']
    city_RBT = rbt.newMap(minorcmpFunction)
    city_key = city['city_ascii']
    city_value = {  'info': city,
                    'RBT': city_RBT}

    if mp.contains(cities_map, city_key):
        city_key_list_values = mp.get(cities_map, city_key)
        city_list_values = me.getValue(city_key_list_values)
        lt.addLast(city_list_values, city_value)
    else:
        city_list_values = lt.newList('ARRAY_LIST')
        lt.addLast(city_list_values, city_value)
        mp.put(cities_map, city_key, city_list_values)

######################################################################################################################

def AddAirport(catalog, airport):
    undirected_graph = catalog['undirected_graph']
    directed_graph = catalog['directed_graph']
    airports_list = catalog['airports_list'] 
    airports_map = catalog['airports_map']
    cities_map = catalog['cities_map']  
    additional_cities = 0

    airport_IATA = airport['IATA']
    airport_city_name = airport['City']
    airport_city_country = airport['Country']

    airport_latitude = float(airport['Latitude'])
    airport_longitude = float(airport['Longitude'])
    if mp.contains(cities_map, airport_city_name):
        city_key_list_values = mp.get(cities_map, airport_city_name)
        city_list_values = me.getValue(city_key_list_values)

        nearest_city = None
        min_distance = 5*(10**7)
        for city in lt.iterator(city_list_values):
            city_info = city['info']
            city_latitude = float(city_info['lat'])
            city_longitude = float(city_info['lng'])

            airport_coordinates = (airport_latitude, airport_longitude)
            city_coordinates = (city_latitude, city_longitude)
            distance = haversine(airport_coordinates, city_coordinates)
            if distance < min_distance:
                min_distance = distance
                nearest_city = city
        
        nearest_city_RBT = nearest_city['RBT']
        rbt.put(nearest_city_RBT, distance, airport)
        city = {'info': None}

    else:
        city = {'city': airport_city_name,
                'city_ascii': airport_city_name,
                'lat': airport_latitude,
                'lng': airport_longitude,
                'country': airport_city_country,
                'iso2': 'Desconocida',
                'iso3': 'Desconocida',
                'admin_name': airport_city_name,
                'capital': airport_city_name,
                'population': 'Desconocida',
                'id': 'Desconocida'}
        AddCity(catalog, city)
        city_key_list_values = mp.get(cities_map, airport_city_name)
        city_list_values = me.getValue(city_key_list_values)
        city = lt.getElement(city_list_values, 1)
        city_RBT = city['RBT']
        rbt.put(city_RBT, 0, airport)
        additional_cities += 1

    element = (airport_IATA, airport)
    lt.addLast(airports_list, element)
    mp.put(airports_map, airport_IATA, airport)
    gp.insertVertex(directed_graph, airport_IATA)
    gp.insertVertex(undirected_graph, airport_IATA)

    return additional_cities, city['info']

######################################################################################################################

def AddRoute(catalog, route):
    directed_graph = catalog['directed_graph']
    undirected_graph = catalog['undirected_graph']

    departure_IATA = route['Departure']
    destination_IATA = route['Destination']
    distance = float(route['distance_km'])


    if gp.getEdge(directed_graph, departure_IATA, destination_IATA) != None:
        num_added_edges_directed_graph = 0
        if gp.getEdge(directed_graph, destination_IATA, departure_IATA) != None:
            if gp.getEdge(undirected_graph, departure_IATA, destination_IATA) == None:
                gp.addEdge(undirected_graph, departure_IATA, destination_IATA, distance)
                num_added_edges_undirected_graph = 1
            else:
                num_added_edges_undirected_graph = 0
        else:
            num_added_edges_undirected_graph = 0
    else:
        gp.addEdge(directed_graph, departure_IATA, destination_IATA, distance)
        num_added_edges_directed_graph = 1
        if gp.getEdge(directed_graph, destination_IATA, departure_IATA) != None:
            if gp.getEdge(undirected_graph, departure_IATA, destination_IATA) == None:
                gp.addEdge(undirected_graph, departure_IATA, destination_IATA, distance)
                num_added_edges_undirected_graph = 1
            else:
                num_added_edges_undirected_graph = 0
        else:
            num_added_edges_undirected_graph = 0
    
    return num_added_edges_directed_graph, num_added_edges_undirected_graph

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
    directed_graph = catalog['directed_graph']
    airports_list = catalog['airports_list']
    interconnections_RBT = rbt.newMap(majorcmpFunction)

    for airport in lt.iterator(airports_list):
        information = airport[1]
        IATA = airport[0]
        list_interconnections = gp.adjacents(directed_graph, IATA)
        num_interconnections = lt.size(list_interconnections)
        element = num_interconnections, information
        rbt.put(interconnections_RBT, num_interconnections, element)

    initial_requirement_list = inorder(interconnections_RBT)
    final_requirement_list = lt.subList(initial_requirement_list, 1, num_airports)
    requirement_list = lt.iterator(final_requirement_list)

    return requirement_list
    
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
# Funciones de ordenamiento
######################################################################################################################
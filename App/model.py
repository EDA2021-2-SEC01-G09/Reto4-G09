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
from math import inf
from haversine import haversine
from DISClib.ADT import map as mp
from DISClib.ADT import list as lt
from DISClib.ADT import graph as gp
from DISClib.ADT import queue as qu
from DISClib.DataStructures import rbt
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import prim
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Trees.traversal import inorder
from DISClib.Algorithms.Graphs.dijsktra import Dijkstra
assert cf

###########################################################################
# Construccion de modelos
###########################################################################

def Initialization():
    catalog = { 'graph': None,
                'digraph': None,
                'compl_graph': None,
                'cities_map': None,
                'airports_map': None,
                'routes_map': None,
                'airports_list': None}

    catalog['graph'] = gp.newGraph(datastructure='ADJ_LIST',
                                            directed=False,
                                            size=9075,
                                            comparefunction=None)

    catalog['digraph'] = gp.newGraph(datastructure='ADJ_LIST',
                                             directed=True,
                                             size=9075,
                                             comparefunction=None)

    catalog['compl_graph'] = gp.newGraph(datastructure='ADJ_LIST',
                                            directed=False,
                                            size=9075,
                                            comparefunction=None)

    catalog['cities_map'] = mp.newMap(42739)
    catalog['airports_map'] = mp.newMap(9075)
    catalog['routes_map'] = mp.newMap(92605)
    catalog['airports_list'] = lt.newList('ARRAY_LIST')

    return catalog

###########################################################################
# Funciones para agregar informacion al catalogo
###########################################################################

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

###########################################################################

def AddAirport(catalog, airport):
    airports_list = catalog['airports_list'] 
    airports_map = catalog['airports_map']
    compl_graph = catalog['compl_graph']
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
        RBT_element = airport, distance
        rbt.put(nearest_city_RBT, distance, RBT_element)

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
        RBT_element = airport, 0
        rbt.put(city_RBT, 0, RBT_element)

    lt.addLast(airports_list, airport)
    mp.put(airports_map, airport_IATA, airport)
    gp.insertVertex(compl_graph, airport_IATA)
    gp.insertVertex(digraph, airport_IATA)
    gp.insertVertex(graph, airport_IATA)

###########################################################################

def AddRoute(catalog, route, undirected_routes_map):
    compl_graph = catalog['compl_graph']
    routes_map = catalog['routes_map']
    digraph = catalog['digraph']
    graph = catalog['graph']

    departure_IATA = route['Departure']
    distance = float(route['distance_km'])
    destination_IATA = route['Destination']

    if gp.getEdge(digraph, departure_IATA, destination_IATA) == None:
        if gp.getEdge(digraph, destination_IATA, departure_IATA) != None:
            if gp.getEdge(graph, destination_IATA, departure_IATA) == None:
                add_num_edges_digraph = 1
                add_num_edgees_graph = 1
            else:
                add_num_edges_digraph = 1
                add_num_edgees_graph = 0
        else:
            add_num_edges_digraph = 1
            add_num_edgees_graph = 0
    else:
        if gp.getEdge(digraph, destination_IATA, departure_IATA) != None:
            if gp.getEdge(graph, destination_IATA, departure_IATA) == None:
                add_num_edges_digraph = 0
                add_num_edgees_graph = 1
            else:
                add_num_edges_digraph = 0
                add_num_edgees_graph = 0
        else:
            add_num_edges_digraph = 0
            add_num_edgees_graph = 0

    forward_key = departure_IATA + destination_IATA
    backward_key = destination_IATA + departure_IATA

    mp.put(routes_map, forward_key, route)
    gp.addEdge(digraph, departure_IATA, destination_IATA, distance)
    gp.addEdge(compl_graph, departure_IATA, destination_IATA, distance)   

    forward_route = mp.get(undirected_routes_map, departure_IATA + destination_IATA)
    backward_route = mp.get(undirected_routes_map, destination_IATA + departure_IATA)

    if forward_route == None:
        if backward_route != None:
            backward_route_value = me.getValue(backward_route)
            if backward_route_value >= 1:
                mp.put(undirected_routes_map, backward_key, backward_route_value - 1)
                gp.addEdge(graph, destination_IATA, departure_IATA, distance)
            else:
                mp.put(undirected_routes_map, forward_key, 1)
                gp.addEdge(graph, destination_IATA, departure_IATA, distance)
        else:
            mp.put(undirected_routes_map, forward_key, 1)   
    else:
        forward_route_value = me.getValue(forward_route)
        if backward_route != None:
            backward_route_value = me.getValue(backward_route)
            if backward_route_value >= 1 and forward_route_value >= 1:
                mp.put(undirected_routes_map, backward_key, backward_route_value - 1)
                mp.put(undirected_routes_map, forward_key, forward_route_value - 1)
                gp.addEdge(graph, destination_IATA, departure_IATA, distance)
            else:
                mp.put(undirected_routes_map, forward_key, forward_route_value + 1)
        else:
            mp.put(undirected_routes_map, forward_key, forward_route_value + 1)

    return add_num_edges_digraph, add_num_edgees_graph

###########################################################################
# Funciones para creacion de datos
###########################################################################

def GetCitiesOptions(catalog, city):
    cities_map = catalog['cities_map']

    cities_options_key_value = mp.get(cities_map, city)
    cities_options_value = me.getValue(cities_options_key_value)
    cities_options_list = lt.iterator(cities_options_value)

    return cities_options_list

###########################################################################
# Funciones de consulta
###########################################################################

def Requirement1(catalog):
    airports_list = catalog['airports_list']
    digraph = catalog['digraph']
    interconnections_RBT = rbt.newMap(Requirement1cmpFunction)

    num_connected_airports = 0
    for airport in lt.iterator(airports_list):
        IATA = airport['IATA']
        airport_indegre = gp.indegree(digraph, IATA)
        airport_outdegree = gp.outdegree(digraph, IATA)
        num_interconnections = airport_indegre + airport_outdegree
        element = airport, num_interconnections, airport_indegre, airport_outdegree
        rbt.put(interconnections_RBT, (num_interconnections, airport_indegre, airport_outdegree), element)
        if num_interconnections > 0:
            num_connected_airports += 1

    requirement_list = inorder(interconnections_RBT)
    requirement_list = lt.subList(requirement_list, 1, 5)

    return lt.iterator(requirement_list), num_connected_airports
    
###########################################################################

def Requirement2(catalog, airport_1, airport_2):
    digraph = catalog['digraph']
    airports_map = catalog['airports_map']

    airports_info_list = lt.newList('ARRAY_LIST')
    for airport in [airport_1, airport_2]:
        airport_key_value = mp.get(airports_map, airport)
        aiport_info = me.getValue(airport_key_value)
        lt.addLast(airports_info_list, aiport_info)
    airports_info_list = lt.iterator(airports_info_list)

    SCC = scc.KosarajuSCC(digraph)
    num_SCC = scc.connectedComponents(SCC)
    answer = scc.stronglyConnected(SCC, airport_1, airport_2)

    return airports_info_list, num_SCC, answer

###########################################################################

def Requirement3(catalog, choosen_cities):
    digraph = catalog['digraph']
    routes_map = catalog['routes_map']
    airports_map = catalog['airports_map']
    
    origin_city = choosen_cities[0]
    destiny_city = choosen_cities[1]

    oringin_RBT = origin_city['RBT']
    destiny_RBT = destiny_city['RBT']

    origin_airport_list = inorder(oringin_RBT)
    destiny_airport_list = inorder(destiny_RBT)

    origin_airport_list_size = lt.size(origin_airport_list)
    destiny_airport_list_size = lt.size(destiny_airport_list)
    path = False
    index_1 = 1
    while path == False and index_1 <= origin_airport_list_size:
        origin_airport = lt.getElement(origin_airport_list, index_1)
        origin_airport_info = origin_airport[0]
        origin_airport_IATA = origin_airport_info['IATA']
        Dijkstra_path = Dijkstra(digraph, origin_airport_IATA)
        index_2 = 1
        while path == False and index_2 <= destiny_airport_list_size:
            destiny_airport = lt.getElement(destiny_airport_list, index_2)
            destiny_airport_info = destiny_airport[0]
            destiny_airport_IATA = destiny_airport_info['IATA']
            path_key_value = mp.get(Dijkstra_path['visited'], destiny_airport_IATA)
            path = me.getValue(path_key_value)
            distance = path['distTo']

            if distance != inf:
                path == True
            else:
                index_2 += 1
        index_1 += 1

    if path:  
        routes_airports_list = lt.newList('ARRAY_LIST')
        routes_list = lt.newList('ARRAY_LIST')

        destiny_airport_info_key_value = mp.get(airports_map, destiny_airport_IATA)
        destiny_airport_info = me.getValue(destiny_airport_info_key_value)
        lt.addLast(routes_airports_list, destiny_airport_info)

        route = path['edgeTo']
        while route != None:
            departure = route['vertexA']
            destination = route['vertexB']
            route_key = departure + destination
            route_info_key_value = mp.get(routes_map, route_key)
            route_info = me.getValue(route_info_key_value)
            lt.addLast(routes_list, route_info)

            departure_airport_info_key_value = mp.get(airports_map, departure)
            departure_airport_info = me.getValue(departure_airport_info_key_value)
            lt.addLast(routes_airports_list, departure_airport_info)
            
            path_key_value = mp.get(Dijkstra_path['visited'], departure)
            path = me.getValue(path_key_value)
            route = path['edgeTo']
    else:
        distance = 0
        routes_list = lt.newList('ARRAY_LIST')
        routes_airports_list = lt.newList('ARRAY_LIST')

    end_airports_list = lt.newList('ARRAY_LIST')
    lt.addLast(end_airports_list, origin_airport_info)
    lt.addLast(end_airports_list, destiny_airport_info)
        
    return lt.iterator(end_airports_list), distance, lt.iterator(routes_list), lt.iterator(routes_airports_list)

###########################################################################

def Requirement4(catalog, choosen_city, miles):
    routes_map = catalog['routes_map']
    city_RBT = choosen_city['RBT']
    graph= catalog['graph']
    airports_list_city = inorder(city_RBT)
    airport_info = lt.getElement(airports_list_city, 1)[0]
    IATA = airport_info['IATA']

    airport_list = lt.newList('ARRAY_LIST')
    lt.addLast(airport_list, airport_info)

    search = prim.initSearch(graph)
    prim_structure = prim.prim(graph, search, IATA)
    max_traveling_distance = prim.weightMST(graph, search)
    airports_list = prim_structure['pq']['elements']
    edge_To_map = prim_structure['edgeTo']
    mp.put(edge_To_map, IATA, {'vertexA': None, 'vertexB': IATA, 'weight': 0})

    major_leaf = IATA
    num_possible_airports = lt.size(airports_list)
    airports_path_map = mp.newMap(num_possible_airports)
    mp.put(airports_path_map, major_leaf, (0,0))

    longest_path = 0
    for airport in lt.iterator(airports_list):
        airport_IATA = airport['key']
        
        if airport_IATA != IATA:
            queue = qu.newQueue()
            current_path_key_value = mp.get(edge_To_map, airport_IATA)
            current_path_info = me.getValue(current_path_key_value)
            current_node = airport_IATA
            father_node = current_path_info['vertexA']
            route_distance = current_path_info['weight']

            counter = 0
            total_distance = 0
            current_node_key_value = None
            while current_node_key_value == None:
                total_distance += route_distance
                        
                qu.enqueue(queue, current_node)
                current_path_key_value = mp.get(edge_To_map, father_node)
                current_path_info = me.getValue(current_path_key_value)
                current_node = father_node
                father_node = current_path_info['vertexA']
                route_distance = current_path_info['weight']
                current_node_key_value = mp.get(airports_path_map, current_node)
                counter += 1

            additional_values = me.getValue(current_node_key_value)
            additional_count = additional_values[0]
            additional_distance = additional_values[1]
            counter += additional_count
            total_distance += additional_distance
            
            if counter > longest_path:
                longest_path = counter
                major_leaf = airport_IATA
                major_distance_path = total_distance
            elif counter == longest_path:
                if total_distance < major_distance_path:
                    major_leaf = airport_IATA
                    major_distance_path = total_distance

            num_elements_queue = lt.size(queue)
            for i in range(num_elements_queue):
                airport_path_IATA = qu.dequeue(queue)
                mp.put(airports_path_map, airport_path_IATA, (counter, total_distance))
                counter -= 1

    routes_list = lt.newList('ARRAY_LIST')
    current_node = major_leaf
    current_path_key_value = mp.get(edge_To_map, current_node)
    current_path_info = me.getValue(current_path_key_value)
    father_node = current_path_info['vertexA']
    route_distance = current_path_info['weight']

    longest_path_distance = 0
    while father_node != None:
        route_key = father_node + current_node
        route_info_key_value = mp.get(routes_map, route_key)
        route_info = me.getValue(route_info_key_value)
        lt.addLast(routes_list, route_info)
        longest_path_distance += route_distance
        current_path_key_value = mp.get(edge_To_map, father_node)
        current_path_info = me.getValue(current_path_key_value)
        current_node = father_node
        father_node = current_path_info['vertexA']
        route_distance = current_path_info['weight']

    miles_need = (5/8)*(longest_path_distance*2 - miles*1.6)

    return lt.iterator(airport_list), lt.iterator(routes_list), num_possible_airports, max_traveling_distance, longest_path_distance, miles_need

###########################################################################

def Requirement5(catalog, IATA):
    airports_map = catalog['airports_map']
    compl_graph = catalog['compl_graph']
    graph = catalog['graph']
    digraph = catalog['digraph']

    digraph_airport_indegre = gp.indegree(digraph, IATA)
    digraph_airport_outdegree = gp.outdegree(digraph, IATA)
    resulting_num_routes_digraph = digraph_airport_indegre + digraph_airport_outdegree
    
    resulting_num_routes_graph = gp.degree(graph, IATA)

    effected_airports_IATA_list = gp.adjacents(compl_graph, IATA)
    possible_affected_airports = lt.size(effected_airports_IATA_list)
    airports_list = lt.newList('ARRAY_LIST')
    effected_airports_map = mp.newMap(possible_affected_airports)
    for airport_IATA in lt.iterator(effected_airports_IATA_list):
        airport_key_value = mp.get(airports_map, airport_IATA)
        airport_info = me.getValue(airport_key_value)
        if mp.get(effected_airports_map, airport_IATA) == None:
            lt.addLast(airports_list, airport_info)
            mp.put(effected_airports_map, airport_IATA, 0)

    num_affected_airports = lt.size(airports_list)

    if num_affected_airports > 6:
        definitive_airports_list = lt.subList(airports_list, 1, 3)
        last_airports_list = lt.subList(airports_list, num_affected_airports - 2, 3)
        for airport in lt.iterator(last_airports_list):
            lt.addLast(definitive_airports_list, airport)
    else:
        definitive_airports_list = airports_list
#
    return lt.iterator(definitive_airports_list), resulting_num_routes_digraph, resulting_num_routes_graph, num_affected_airports

###########################################################################
# Funciones utilizadas para comparar elementos dentro de una lista
###########################################################################

def minorcmpFunction(key_1, key_2):
    if key_1 >= key_2:
        return 1
    else:
        return -1

###########################################################################

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
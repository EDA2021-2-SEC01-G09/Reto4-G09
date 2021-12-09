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
 """
 
import config as cf
from DISClib.ADT import map as mp
from DISClib.ADT import list as lt
from DISClib.ADT import graph as gp
import model
import time
import csv

###########################################################################
# Inicialización del Catálogo
###########################################################################

def Initialization():
    start_time = time.process_time()

    catalog = model.Initialization()

    stop_time = time.process_time()
    elapsed_time = (stop_time - start_time)*1000 

    return elapsed_time, catalog

###########################################################################
# Funciones para la carga de datos
###########################################################################

def LoadData(catalog, routes_sample):
    start_time = time.process_time()

    info_cities = LoadCities(catalog)
    cities_info_list = info_cities[0]
    num_cities = info_cities[1]

    airports_info_list = LoadAirports(catalog)
    
    routes_info_list = LoadRoutes(catalog, routes_sample)
    num_edges_digraph = routes_info_list[0]
    num_edges_graph = routes_info_list[1]

    digraph = catalog['digraph']
    graph = catalog['graph']
    num_airports = gp.numVertices(graph)
    num_routes_graph = gp.numEdges(graph)
    num_routes_digraph = gp.numEdges(digraph)

    stop_time = time.process_time()
    elapsed_time = (stop_time - start_time)*1000 
  
    return elapsed_time, num_cities, num_airports, num_routes_digraph, num_routes_graph, num_edges_digraph, num_edges_graph, airports_info_list, cities_info_list
###########################################################################

def LoadCities(catalog):
    cities_data = cf.data_dir + 'Data/worldcities-utf8.csv'
    input_file = csv.DictReader(open(cities_data, encoding="utf-8"), delimiter=",")
    file = list(input_file)

    first_city = file[0]
    cities_info_list = lt.newList('ARRAY_LIST')
    lt.addLast(cities_info_list, first_city)

    num_cities = 0
    for city in file:
        model.AddCity(catalog, city)
        num_cities += 1

    lt.addLast(cities_info_list, city)
    
    return lt.iterator(cities_info_list), num_cities

###########################################################################

def LoadAirports(catalog):
    airports_data = cf.data_dir + 'Data/airports-utf8-large.csv'
    input_file = csv.DictReader(open(airports_data, encoding="utf-8"), delimiter=",")
    file = list(input_file)

    first_airport = file[0]
    airports_info_list = lt.newList('ARRAY_LIST')
    lt.addLast(airports_info_list, first_airport)
    
    for airport in file:
        model.AddAirport(catalog, airport)

    lt.addLast(airports_info_list, airport)

    return lt.iterator(airports_info_list)

###########################################################################

def LoadRoutes(catalog, routes_sample):
    routes_data = cf.data_dir + 'Data/routes-utf8-large.csv'
    input_file = csv.DictReader(open(routes_data, encoding="utf-8"), delimiter=",")
    reduced_list = list(input_file)[:routes_sample]
    undirected_routes_map = mp.newMap(routes_sample)

    num_edges_digraph = 0
    num_edges_graph = 0

    for route in reduced_list:
        route_info = model.AddRoute(catalog, route, undirected_routes_map)
        add_num_edges_digraph = route_info[0]
        add_num_edgees_graph = route_info[1]
        num_edges_digraph += add_num_edges_digraph
        num_edges_graph += add_num_edgees_graph

    return num_edges_digraph, num_edges_graph

###########################################################################
# Funciones para creacion de datos
###########################################################################

def GetCitiesOptionsRequirement3(catalog, origin, destiny):
    origin_options_list = model.GetCitiesOptions(catalog, origin)
    destiny_options_list = model.GetCitiesOptions(catalog, destiny)

    return origin_options_list, destiny_options_list

###########################################################################

def GetCitiesOptionsRequirement4(catalog, city):
    return model.GetCitiesOptions(catalog, city)

###########################################################################
# Funciones de consulta sobre el catálogo
###########################################################################

def Requirement1(catalog):

    start_time = time.process_time()

    requirement_info = model.Requirement1(catalog)
    requirement_list = requirement_info[0]
    num_connected_airports = requirement_info[1]

    stop_time = time.process_time()
    elapsed_time = (stop_time - start_time)*1000 

    return elapsed_time, requirement_list, num_connected_airports

###########################################################################

def Requirement2(catalog, airport_1, airport_2):

    start_time = time.process_time()

    requirement_info = model.Requirement2(catalog, airport_1, airport_2)
    airports_info_list = requirement_info[0]
    num_SCC = requirement_info[1]
    answer = requirement_info[2]

    stop_time = time.process_time()
    elapsed_time = (stop_time - start_time)*1000 

    return elapsed_time, airports_info_list, num_SCC, answer

###########################################################################

def Requirement3(catalog, choosen_cities):
    start_time = time.process_time()

    requirement_info = model.Requirement3(catalog, choosen_cities)
    end_airports_list = requirement_info[0]
    distance = requirement_info[1]
    routes_list = requirement_info[2]
    routes_airports_list = requirement_info[3]

    stop_time = time.process_time()
    elapsed_time = (stop_time - start_time)*1000 

    return elapsed_time, end_airports_list, distance, routes_list, routes_airports_list

###########################################################################

def Requirement4(catalog, choosen_city, miles):
    start_time = time.process_time()

    requirement_info = model.Requirement4(catalog, choosen_city, miles)
    airport_list = requirement_info[0]
    routes_list = requirement_info[1]
    num_possible_airports = requirement_info[2]
    max_traveling_distance = requirement_info[3]
    longest_path_distance = requirement_info[4]
    miles_need = requirement_info[5]

    stop_time = time.process_time()
    elapsed_time = (stop_time - start_time)*1000 

    return elapsed_time, airport_list, routes_list, num_possible_airports, max_traveling_distance, longest_path_distance, miles_need

###########################################################################

def Requirement5(catalog, IATA):
    start_time = time.process_time()

    requirement_info = model.Requirement5(catalog, IATA)
    airports_list = requirement_info[0]
    resulting_num_routes_digraph = requirement_info[1]
    resulting_num_routes_graph = requirement_info[2]
    num_affected_airports = requirement_info[3]
    stop_time = time.process_time()
    elapsed_time = (stop_time - start_time)*1000 

    return elapsed_time, airports_list, resulting_num_routes_digraph, resulting_num_routes_graph, num_affected_airports
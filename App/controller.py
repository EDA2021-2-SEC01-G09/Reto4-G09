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

######################################################################################################################
# Inicialización del Catálogo
######################################################################################################################

def Initialization():
    start_time = time.process_time()

    catalog = model.Initialization()

    stop_time = time.process_time()
    elapsed_time = (stop_time - start_time)*1000 

    return elapsed_time, catalog

######################################################################################################################
# Funciones para la carga de datos
######################################################################################################################

def LoadData(catalog, routes_sample):
    start_time = time.process_time()

    info_cities = LoadCities(catalog)
    cities_info_list = info_cities[0]
    num_cities = info_cities[1]

    airports_info_list = LoadAirports(catalog)
    
    routes_info = LoadRoutes(catalog, routes_sample)


    graph = catalog['graph']
    num_airports = gp.numVertices(graph)
    num_routes_graph = routes_info[0]
    num_routes_digraph = routes_info[1]

    stop_time = time.process_time()
    elapsed_time = (stop_time - start_time)*1000 
  
    return elapsed_time, num_cities, num_airports, num_routes_graph, num_routes_digraph, lt.iterator(airports_info_list), lt.iterator(cities_info_list)
######################################################################################################################

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
    
    return cities_info_list, num_cities

######################################################################################################################

def LoadAirports(catalog):
    airports_data = cf.data_dir + 'Data/airports-utf8-small.csv'
    input_file = csv.DictReader(open(airports_data, encoding="utf-8"), delimiter=",")
    file = list(input_file)

    first_airport = file[0]
    airports_info_list = lt.newList('ARRAY_LIST')
    lt.addLast(airports_info_list, first_airport)
    
    for airport in file:
        model.AddAirport(catalog, airport)

    lt.addLast(airports_info_list, airport)

    return airports_info_list

######################################################################################################################

def LoadRoutes(catalog, routes_sample):
    routes_data = cf.data_dir + 'Data/routes-utf8-small.csv'
    input_file = csv.DictReader(open(routes_data, encoding="utf-8"), delimiter=",")
    reduced_list = list(input_file)[:routes_sample]
    undirected_routes_map = mp.newMap(routes_sample, loadfactor=0.5)

    num_routes_graph = 0
    num_routes_digraph = 0
    for route in reduced_list:
        add_num_routes_graph = model.AddRoute(catalog, route, undirected_routes_map)
        num_routes_graph += add_num_routes_graph
        num_routes_digraph += 1

    return num_routes_graph, num_routes_digraph

######################################################################################################################
# Funciones para creacion de datos
######################################################################################################################

def GetCitiesOptions(origin, destiny, catalog):
    return model.GetCitiesOptions(origin, destiny, catalog)

######################################################################################################################
# Funciones de consulta sobre el catálogo
######################################################################################################################

def Requirement1(catalog, num_airports):

    start_time = time.process_time()

    requirement_list = model.Requirement1(catalog, num_airports)

    stop_time = time.process_time()
    elapsed_time = (stop_time - start_time)*1000 

    return elapsed_time, requirement_list
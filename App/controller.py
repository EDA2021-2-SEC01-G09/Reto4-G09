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

    num_cities = LoadCities(catalog)
    info_airports = LoadAirports(catalog)
    info_routes = LoadRoutes(catalog, routes_sample)
    
    num_airports = info_airports[0]
    total_additional_cities = info_airports[1]
    first_airport_info = info_airports[2]
    last_city_info = info_airports[3]
    total_num_cities = num_cities + total_additional_cities

    num_routes_directed_graph = info_routes[0]
    num_routes_undirected_graph = info_routes[1]

    stop_time = time.process_time()
    elapsed_time = (stop_time - start_time)*1000 
    
    return elapsed_time, total_num_cities, num_airports, num_routes_directed_graph, num_routes_undirected_graph, first_airport_info, last_city_info

######################################################################################################################

def LoadCities(catalog):
    cities_data = cf.data_dir + 'Data/worldcities.csv'
    input_file = csv.DictReader(open(cities_data, encoding="utf-8"), delimiter=",")

    num_cities = 0
    for city in input_file:
        model.AddCity(catalog, city)
        num_cities += 1
    
    return num_cities

######################################################################################################################

def LoadAirports(catalog):
    airports_data = cf.data_dir + 'Data/airports_full.csv'
    input_file = csv.DictReader(open(airports_data, encoding="utf-8"), delimiter=",")
    
    num_airports = 0
    total_additional_cities = 0
    for airport in input_file:
        airport_output = model.AddAirport(catalog, airport)
        additional_cities = airport_output[0]
        city_info = airport_output[1]
        if city_info != None:
            last_city_info = city_info
        if num_airports == 0:
            first_airport_info = airport
        num_airports += 1
        total_additional_cities += additional_cities

    return num_airports, total_additional_cities, first_airport_info, last_city_info

######################################################################################################################

def LoadRoutes(catalog, routes_sample):
    routes_data = cf.data_dir + 'Data/routes_full.csv'
    input_file = csv.DictReader(open(routes_data, encoding="utf-8"), delimiter=",")
    reduced_list = list(input_file)[:routes_sample]

    num_routes_directed_graph = 0
    num_routes_undirected_graph = 0
    for route in reduced_list:
        num_added_edges_info = model.AddRoute(catalog, route)
        num_added_edges_directed_graph = num_added_edges_info[0]
        num_added_edges_undirected_graph = num_added_edges_info[1]
        num_routes_directed_graph += num_added_edges_directed_graph
        num_routes_undirected_graph += num_added_edges_undirected_graph

    return num_routes_directed_graph, num_routes_undirected_graph

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
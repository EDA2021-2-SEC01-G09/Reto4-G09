import config as cf
from haversine import haversine
from DISClib.ADT import map as mp
from DISClib.ADT import list as lt
from DISClib.ADT import graph as gp
from DISClib.Algorithms.Graphs.dijsktra import Dijkstra
from DISClib.Algorithms.Graphs.prim import PrimMST
from DISClib.DataStructures import bst as bst
from DISClib.DataStructures import mapentry as me
assert cf

graph = gp.newGraph(directed=False)
gp.insertVertex(graph, '1')
gp.insertVertex(graph, '2')
gp.insertVertex(graph, '3')
gp.insertVertex(graph, '4')
gp.insertVertex(graph, '5')
gp.insertVertex(graph, '6')
gp.insertVertex(graph, '7')
gp.insertVertex(graph, '8')
gp.insertVertex(graph, '9')


gp.addEdge(graph, '1', '5', 4)
gp.addEdge(graph, '2', '9', 4)
gp.addEdge(graph, '2', '4', 1)
gp.addEdge(graph, '3', '1', 2)
gp.addEdge(graph, '4', '8', 3)
gp.addEdge(graph, '5', '2', 8)
gp.addEdge(graph, '5', '4', 8)
gp.addEdge(graph, '5', '6', 5)
gp.addEdge(graph, '5', '7', 5)
gp.addEdge(graph, '6', '3', 6)
gp.addEdge(graph, '6', '4', 4)
gp.addEdge(graph, '6', '8', 6)
gp.addEdge(graph, '7', '1', 10)
gp.addEdge(graph, '7', '2', 1)
gp.addEdge(graph, '7', '9', 6)
gp.addEdge(graph, '8', '3', 4)
gp.addEdge(graph, '9', '1', 4)

print(mp.get(PrimMST(graph)['distTo'], '1'))
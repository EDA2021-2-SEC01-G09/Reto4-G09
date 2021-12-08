from math import inf
import config as cf
from haversine import haversine
from DISClib.ADT import map as mp
from DISClib.ADT import list as lt
from DISClib.ADT import graph as gp
from DISClib.Algorithms.Graphs import prim
from DISClib.Algorithms.Graphs import dijsktra
from DISClib.DataStructures import bst as bst
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Trees.traversal import inorder
assert cf

def cmpFunction(key_1, key_2):
    if key_1 > key_2:
        return 1
    elif key_1 < key_2:
        return -1
    else:
        return 0

BST = bst.newMap(cmpFunction)
bst.put(BST, 1, 'a')
bst.put(BST, 2, 'b')


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


gp.addEdge(graph, '1', '2', 1)
gp.addEdge(graph, '2', '3', 4)
gp.addEdge(graph, '1', '4', 2)
gp.addEdge(graph, '1', '5', 4)
gp.addEdge(graph, '1', '3', 4)
gp.addEdge(graph, '3', '7', 4)
gp.addEdge(graph, '7', '8', 4)
search = prim.initSearch(graph)
Prim = prim.prim(graph, search, '1')
mp.get(Prim['edgeTo'], '1')
print(lt.size(Prim['pq']['elements']))

print(mp.get(Prim['edgeTo'], '2'))

for element in lt.iterator(Prim['pq']['elements']):
    print(element)

'''
search = initSearch(graph)
prim_graph = prim(graph, search, '1')
print(mp.get(prim_graph['edgeTo'], '3'))
'''

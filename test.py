import networkx as nx
import pandas as pd
import numpy as np
from functools import reduce

#
# a = pd.DataFrame(np.zeros(shape=(4,4)))
# print(a)
# print(a.loc[[2,3], :])
# G = nx.DiGraph()
# G.add_node('1', r={'a':3, 'b':2})
# G.add_edge('1', '1', w=1)
# G.add_edge('1', '3', weight=1)
# G.add_edge('2', '3', weight=1)
# G.add_edge('3', '1', weight=1)
# G.add_edge('2', '4', weight=1)
# print(np.mean(list(G.out_degree().values())))
# # print(G.neighbors('1'))
# a = {'a':2, 'b':3, 'c':4,'d':2}
# print(reduce(lambda x,y: x*y, a.values()))
a = np.loadtxt('data/3_mv_scoring1.txt', dtype='int')
b = np.loadtxt('data/3_mv_scoring2.txt', dtype='int')
for i in range(len(a)):
    for j in range(3):
        if a[i, j] != b[i, j]:
            print('~~~~')

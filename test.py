import networkx as nx
import pandas as pd
import numpy as np

# a = pd.DataFrame(np.zeros(shape=(4,4)))
# print(a)
# print(a.loc[[2,3], :])
# G = nx.DiGraph()
# G.add_node('6', rak=123)
# G.add_edge('1', '2', w=1)
# G.add_edge('1', '3', weight=1)
# G.add_edge('2', '3', weight=1)
# G.add_edge('3', '1', weight=1)
# G.add_edge('2', '4', weight=1)
# print(G.node['6'])
# a = set([1,2,3])
# b = set([1])
# c = set(2)
# print(c)
a = {'a':0.8,'b':0.5,'c':0.5}
print(sum(a.values()))
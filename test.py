import networkx as nx
import pandas as pd
import numpy as np

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

a = {'a':3, 'b':4, 'c':1}
a.pop('a')
print(a)

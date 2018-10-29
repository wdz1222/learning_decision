import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import networkx as nx
np.set_printoptions(suppress=True)

def draw_M_and_T():
    M = np.loadtxt('data/3_M1.txt', dtype='int')
    T = np.loadtxt('data/3_T1.txt', dtype='int')
    plt.figure(1, figsize=(14,12))
    cmap = sns.cubehelix_palette(start=1.5, rot=3, gamma=0.8, as_cmap=True)
    ax = sns.heatmap(M, linewidths=0.1, square=True, linecolor='white', annot=True, cmap=cmap,
                xticklabels=[6119,6068,12105], yticklabels=[6068,12105,7584], fmt='d', annot_kws={'fontsize':30})
    plt.show()

def basic_info():
    G = nx.read_gpickle('./data/4-network.gpickle')
    print(G.number_of_edges())
    print(G.number_of_nodes())

def draw_vi():
    # x = [1, 2, 3]
    # y1 = [0.98867, 0.00053, 0.01125]
    # y2 = [0.1403, 0.0356, 0.8233]
    # y1 = [0.00011, 0.00219, 0.99773]
    # y2 = [0.4277, 0.1767, 0.3966]
    x = [1, 2, 3, 4]
    y1 = [0.92179, 3.92E-11, 6.09E-06, 0.07879]
    y2 = [0.61134, 0.21051, 0.056066, 0.12115]
    plt.figure(1)
    l1, = plt.plot(x[0], y1[0], 'ro', markersize=10)
    plt.plot(x[0], y2[0], 'ro', markersize=10)
    l2, = plt.plot(x[1], y1[1], 'go', markersize=10)
    plt.plot(x[1], y2[1], 'go', markersize=10)
    l3, = plt.plot(x[2], y1[2], 'bo', markersize=10)
    plt.plot(x[2], y2[2], 'bo', markersize=10)
    l4, = plt.plot(x[3], y1[3], 'yo', markersize=10)
    plt.plot(x[3], y2[3], 'yo', markersize=10)
    plt.plot(x, y1, '-')
    plt.plot(x, y2, '--')
    plt.legend([l1, l2, l3, l4], ['6119', '6068', '12105', '7584'], loc=1)
    plt.show()

draw_M_and_T()
# basic_info()
# draw_vi()
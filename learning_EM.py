import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from file_treatment import FileUtil


class EM():

    def __init__(self, G_path, k):
        self.k = k
        self.G = nx.read_gpickle(G_path)
        self.top_k_movies = FileUtil.build_candidate_set(k)

    # def EM_algorithm(self):


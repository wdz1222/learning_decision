import networkx as nx
import numpy as np
import matplotlib.pyplot as plt


class Network:


    @staticmethod
    def build_network(trust_path, user_saw_k_movies_dic_path, user_saw_movies_dic_path, k):
        with open(user_saw_k_movies_dic_path, 'r') as f:
            user_saw_k_movies_dic = eval(f.read())
        with open(user_saw_movies_dic_path, 'r') as f:
            user_saw_movies_dic = eval(f.read())
        trusts = np.loadtxt(trust_path, dtype='str', delimiter=',')
        G = nx.DiGraph()
        k_user_ids = list(user_saw_k_movies_dic.keys())
        user_ids = list(user_saw_movies_dic.keys())
        for rel in trusts:
            if rel[0] not in k_user_ids and rel[1] not in k_user_ids:
                continue
            else:
                if rel[0] in user_ids and rel[0] in k_user_ids:
                    if not G.has_node(rel[0]):
                        G.add_node(rel[0], ratings=user_saw_k_movies_dic[rel[0]])
                elif rel[0] in user_ids and rel[0] not in k_user_ids:
                    if not G.has_node(rel[0]):
                        G.add_node(rel[0], ratings=list())
                if rel[1] in user_ids and rel[1] in k_user_ids:
                    if not G.has_node(rel[1]):
                        G.add_node(rel[1], ratings=user_saw_k_movies_dic[rel[1]])
                elif rel[1] in user_ids and rel[1] not in k_user_ids:
                    if not G.has_node(rel[1]):
                        G.add_node(rel[1], ratings=list())
                if G.has_node(rel[0]) and G.has_node(rel[1]):
                    G.add_edge(rel[0], rel[1], trust=Network.build_trust(user_saw_movies_dic[rel[0]],
                                                                         user_saw_movies_dic[rel[1]]))
        for user_id in G.nodes():
            out_degree = G.out_degree(user_id, weight='trust')
            if out_degree == 0:
                continue
            else:
                neighbors = G.neighbors(user_id)
                for neighbor in neighbors:
                    G[user_id][neighbor]['trust'] = G[user_id][neighbor]['trust'] / out_degree
        nx.write_gpickle(G, 'data/'+str(k)+'-network.gpickle')

    @staticmethod
    def build_trust(movies1, movies2):
        movies1 = set([list(mv.keys())[0] for mv in movies1])
        movies2 = set([list(mv.keys())[0] for mv in movies2])
        return len(movies1.intersection(movies2))

    @staticmethod
    def draw_network(network_path):
        G = nx.read_gpickle(network_path)
        plt.figure(figsize=(8, 8))
        nx.draw_spring(G, node_size=7, linewidths=0.1, arrows=False)
        # nx.draw_random(G, node_size=10, linewidths=0.3, arrows=False)
        plt.show()

    @staticmethod
    def basic_network_infomation(network_path):
        G = nx.read_gpickle(network_path)
        print(G.number_of_nodes())
        print(G.number_of_edges())
        print(np.mean(list(G.out_degree().values())))
        print(np.mean(list(G.in_degree().values())))


# trust_path = 'data/trusts.txt'
# user_saw_k_movies_dic_path = 'data/user_saw_3_movies_dic.txt'
# user_saw_movies_dic_path = 'data/user_saw_movies_dic.txt'
# k = 3
# Network.build_network(trust_path, user_saw_k_movies_dic_path, user_saw_movies_dic_path, k)

network_path = 'data/3-network.gpickle'
Network.basic_network_infomation(network_path)
# Network.draw_network(network_path)

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from file_treatment import FileUtil
from scipy.special import comb
np.set_printoptions(suppress=True)


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
                for i in range(2):
                    if rel[i] in user_ids and rel[i] in k_user_ids:
                        if not G.has_node(rel[i]):
                            G.add_node(rel[i], ratings=user_saw_k_movies_dic[rel[i]])
                            G.add_edge(rel[i], rel[i], trust=1)
                    elif rel[i] in user_ids and rel[i] not in k_user_ids:
                        if not G.has_node(rel[i]):
                            G.add_node(rel[i], ratings=dict())
                            G.add_edge(rel[i], rel[i], trust=1)
                if G.has_node(rel[0]) and G.has_node(rel[1]):
                    G.add_edge(rel[0], rel[1], trust=Network.build_trust(user_saw_movies_dic[rel[0]],
                                                                         user_saw_movies_dic[rel[1]]))
                    G.add_edge(rel[0], rel[0], trust=Network.build_distrust(G, rel[0], user_saw_movies_dic[rel[0]],
                                                                            user_saw_movies_dic[rel[1]]))
        for user_id in G.nodes():
            out_degree = G.out_degree(user_id)
            if out_degree != 0:
                G[user_id][user_id]['trust'] = G[user_id][user_id]['trust'] / G.out_degree(user_id)
        for user_id in G.nodes():
            out_degree = G.out_degree(user_id)
            out_degree_trust = G.out_degree(user_id, weight='trust')
            if out_degree == 0:
                continue
            else:
                neighbors = G.neighbors(user_id)
                G[user_id][user_id]['trust'] = G[user_id][user_id]['trust'] / G.out_degree(user_id)
                for neighbor in neighbors:
                    G[user_id][neighbor]['trust'] = G[user_id][neighbor]['trust'] / out_degree_trust
        G = Network.build_spearman(G, k)
        G = Network.build_kendall(G, k)
        nx.write_gpickle(G, 'data/'+str(k)+'-network.gpickle')

    @staticmethod
    def build_kendall(G, k):
        nf = comb(k, 2)
        for rel in G.edges():
            user1 = rel[0]
            user2 = rel[1]
            if user1 == user2:
                continue
            else:
                kd = Network.kendall(G.node[user1]['ratings'], G.node[user2]['ratings'], k)
                if kd == 0:
                    G[user1][user2]['kendall'] = 0
                else:
                    G[user1][user2]['kendall'] = kd/nf
        return G

    @staticmethod
    def kendall(rating1, rating2, k):
        if len(rating1) == 0 or len(rating2) == 0:
            return 0
        top_k_movies = FileUtil.build_candidate_set(k)
        rating1 = rating1.copy()
        rating2 = rating2.copy()
        for movie in top_k_movies:
            if movie not in rating1.keys():
                rating1[movie] = 0
            if movie not in rating2.keys():
                rating2[movie] = 0
        kd = 0
        for m1 in top_k_movies:
            for m2 in top_k_movies:
                if m1 == m2:
                    continue
                else:
                    if Network.sgn(rating1[m1]-rating1[m2]) != Network.sgn(rating2[m1]-rating2[m2]):
                        kd = kd + 1
        return kd

    @staticmethod
    def sgn(x):
        if x > 0:
            return 1
        elif x == 0:
            return 0
        else:
            return -1

    @staticmethod
    def build_spearman(G, k):
        sk = np.power(k, 2)/2
        for rel in G.edges():
            user1 = rel[0]
            user2 = rel[1]
            if user1 == user2:
                continue
            else:
                s = Network.spearman(G.node[user1]['ratings'], G.node[user2]['ratings'])
                if s == 0:
                    G[user1][user2]['spearman'] = 0
                else:
                    G[user1][user2]['spearman'] = s/sk
        return G

    @staticmethod
    def spearman(rating1, rating2):
        if len(rating1) == 0 or len(rating2) == 0:
            return 0
        rating1 = rating1.copy()
        rating2 = rating2.copy()
        rating1_num = dict()
        rating2_num = dict()
        rating1_tr = sorted(rating1.items(), key=lambda x: x[1], reverse=True)
        rating2_tr = sorted(rating2.items(), key=lambda x: x[1], reverse=True)
        num1 = 0
        num2 = 0
        rating1_num[rating1_tr[0][0]] = num1
        rating2_num[rating2_tr[0][0]] = num2
        sp = 0
        if len(rating1_tr) != 1:
            for i in range(1, len(rating1_tr)):
                if rating1_tr[i][1] < rating1_tr[i-1][1]:
                    num1 = num1 + 1
                rating1_num[rating1_tr[i][0]] = num1
        if len(rating2_tr) != 1:
            for i in range(1, len(rating2_tr)):
                if rating2_tr[i][1] < rating2_tr[i-1][1]:
                    num2 = num2 + 1
                rating2_num[rating2_tr[i][0]] = num2
        for movie in rating1.keys():
            if movie in rating2.keys():
                sp = sp + abs(rating1_num[movie]-rating2_num[movie])
                rating2.pop(movie)
        return sp



    @staticmethod
    def build_distrust(G, id, movies1, movies2):
        movies1 = set([list(mv.keys())[0] for mv in movies1])
        movies2 = set([list(mv.keys())[0] for mv in movies2])
        return G[id][id]['trust'] + 1 - (len(movies1.intersection(movies2)) / len(movies2))

    @staticmethod
    def build_trust(movies1, movies2):
        movies1 = set([list(mv.keys())[0] for mv in movies1])
        movies2 = set([list(mv.keys())[0] for mv in movies2])
        return len(movies1.intersection(movies2)) / len(movies2)

    @staticmethod
    def draw_network(network_path):
        G = nx.read_gpickle(network_path)
        plt.figure(figsize=(8, 8))
        nx.draw_spring(G, node_size=7, linewidths=0.1, arrows=False)
        # nx.draw_random(G, node_size=10, linewidths=0.3, arrows=False)
        plt.show()

    @staticmethod
    def basic_network_infomation(network_path, k):
        G = nx.read_gpickle(network_path)
        top_k_movies = FileUtil.build_candidate_set(k)
        dist = np.empty(shape=(G.number_of_edges(), 3))
        mv_rating1 = np.empty(shape=(G.number_of_edges(), k))
        mv_scoring1 = np.empty(shape=(G.number_of_edges(), k))
        mv_rating2 = np.empty(shape=(G.number_of_edges(), k))
        mv_scoring2 = np.empty(shape=(G.number_of_edges(), k))
        i = 0
        for edge in G.edges():
            user1 = edge[0]
            user2 = edge[1]
            if user1 != user2:
                neighbor1 = set(G.neighbors(user1))
                neighbor2 = set(G.neighbors(user2))
                common_friends = neighbor1.intersection(neighbor2)
                value = 0
                for friend in common_friends:
                    value = G[user1][friend]['trust']*G[user2][friend]['trust']+value
                dist[i, 0] = value
                dist[i, 1] = G[user1][user2]['spearman']
                dist[i, 2] = G[user1][user2]['kendall']

                rating1 = G.node[user1]['ratings'].copy()
                rating2 = G.node[user2]['ratings'].copy()
                for mv in top_k_movies:
                    if mv not in rating1.keys():
                        rating1[mv] = 0
                    if mv not in rating2.keys():
                        rating2[mv] = 0
                rating1_tr = sorted(rating1.items(), key=lambda x: x[1], reverse=True)
                rating2_tr = sorted(rating1.items(), key=lambda x: x[1], reverse=True)
                for j in range(k):
                    mv_rating1[i, j] = np.argwhere(top_k_movies == rating1_tr[j][0])[0][0]
                    mv_rating2[i, j] = np.argwhere(top_k_movies == rating2_tr[j][0])[0][0]
                    mv_scoring1[i, j] = rating1_tr[j][1]
                    mv_scoring2[i, j] = rating2_tr[j][1]
                i = i + 1
        np.savetxt('data/' + str(k) + '_dist.txt', dist)
        np.savetxt('data/' + str(k) + '_mv_rating1.txt', mv_rating1, fmt='%d')
        np.savetxt('data/' + str(k) + '_mv_rating2.txt', mv_rating2, fmt='%d')
        np.savetxt('data/' + str(k) + '_mv_scoring1.txt', mv_scoring1, fmt='%d')
        np.savetxt('data/' + str(k) + '_mv_scoring2.txt', mv_scoring2, fmt='%d')

#
trust_path = 'data/trusts.txt'
user_saw_k_movies_dic_path = 'data/user_saw_3_movies_dic.txt'
user_saw_movies_dic_path = 'data/user_saw_movies_dic.txt'
k = 3
Network.build_network(trust_path, user_saw_k_movies_dic_path, user_saw_movies_dic_path, k)

network_path = 'data/3-network.gpickle'
Network.basic_network_infomation(network_path, k)

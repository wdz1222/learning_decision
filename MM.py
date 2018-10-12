import networkx as nx
import numpy as np
import pandas as pd
from file_treatment import FileUtil

class MM:

    def __init__(self, network_path, k):
        self.k = k
        self.network = nx.read_gpickle(network_path)
        self.k_top_movies = FileUtil.build_candidate_set(k)

    def MM_algorithm(self):
        M, T = self.build_M_and_T_matrix()
        print(M)
        print(T)
        gamma = dict()
        for movie_id in self.k_top_movies:
            gamma[movie_id] = 1/self.k
        theta = 0
        gamma_new = self.compute_gamma(M, T, theta, gamma)
        theta_new = self.compute_theta(M, T, gamma_new, theta)
        while abs(theta_new-theta) > 1e-6:
            theta = theta_new
            gamma = gamma_new
            gamma_new = self.compute_gamma(M, T, theta, gamma)
            theta_new = self.compute_theta(M, T, gamma_new, theta)
            print(gamma)

    def compute_gamma(self, M, T, theta, gamma):
        gamma_new = dict()
        for movie_id in self.k_top_movies:
            movie_id_loc = np.argwhere(self.k_top_movies == movie_id)
            op_movie_ids = np.delete(self.k_top_movies, movie_id_loc)
            g = 0
            for op_movie_id in op_movie_ids:
                g = g + ((M.loc[movie_id, op_movie_id]+M.loc[op_movie_id, movie_id]+T.loc[movie_id, op_movie_id])*\
                    (2+theta*np.sqrt(gamma[op_movie_id]/gamma[movie_id])))/(gamma[movie_id]+gamma[op_movie_id]+theta*
                    np.sqrt(gamma[op_movie_id]*gamma[movie_id]))
            gamma_new[movie_id] = (2*M.loc[movie_id, :].sum()+T.loc[movie_id, :].sum()) / g
        for movie_id in self.k_top_movies:
            gamma_new[movie_id] = gamma_new[movie_id] / sum(gamma_new.values())
        return gamma_new

    def compute_theta(self, M, T, gamma_new, theta):
        T_sum = T.sum().sum()
        t = 0
        for i in self.k_top_movies:
            for j in self.k_top_movies:
                if i == j:
                    continue
                t = t + (2*M.loc[i, j]+T.loc[i, j])*(gamma_new[i]+gamma_new[j])/\
                        (gamma_new[i]+gamma_new[j]+theta*np.sqrt(gamma_new[i]*gamma_new[j]))
        theta_new = 4*T_sum*t
        return theta_new

    def build_M_and_T_matrix(self):
        M = pd.DataFrame(np.zeros(shape=(self.k, self.k)), index=self.k_top_movies, columns=self.k_top_movies)
        T = pd.DataFrame(np.zeros(shape=(self.k, self.k)), index=self.k_top_movies, columns=self.k_top_movies)
        for user_id in self.network.nodes():
            movies_ratings = self.network.node[user_id]['ratings']
            saw_number = len(movies_ratings)
            if saw_number != 0:
                movies_ratings = list(self.network.node[user_id]['ratings'].items())
                movies_ratings_ids = list(self.network.node[user_id]['ratings'].keys())
            if saw_number == 0:
                T = T + 1
                continue
            elif saw_number == 1:
                movie_id = movies_ratings[0][0]
                M.loc[movie_id, :] = M.loc[movie_id, :] + 1
            else:
                for i in range(saw_number-1):
                    for j in range(i+1, saw_number):
                        if movies_ratings[i][1] > movies_ratings[j][1]:
                            M.loc[movies_ratings[i][0], movies_ratings[j][0]] = M.loc[movies_ratings[i][0],
                                                                                      movies_ratings[j][0]] + 1
                        elif movies_ratings[i][1] < movies_ratings[j][1]:
                            M.loc[movies_ratings[j][0], movies_ratings[i][0]] = M.loc[movies_ratings[j][0],
                                                                                      movies_ratings[i][0]] + 1
                        else:
                            T.loc[movies_ratings[i][0], movies_ratings[j][0]] = T.loc[movies_ratings[i][0],
                                                                                      movies_ratings[j][0]] + 1
                            T.loc[movies_ratings[j][0], movies_ratings[i][0]] = T.loc[movies_ratings[i][0],
                                                                                      movies_ratings[j][0]]
            tie_movie_id = list(set(self.k_top_movies).difference(movies_ratings_ids))
            tie_num = len(tie_movie_id)
            for i in range(tie_num - 1):
                for j in range(i + 1, tie_num):
                    T.loc[tie_movie_id[i], tie_movie_id[j]] = T.loc[tie_movie_id[i], tie_movie_id[j]] + 1
                    T.loc[tie_movie_id[j], tie_movie_id[i]] = T.loc[tie_movie_id[i], tie_movie_id[j]]
        for i in range(self.k):
            M.iloc[i, i] = 0
            T.iloc[i, i] = 0
        # print(M)
        # print(T)
        return M, T



# network_path = 'data/10-network.gpickle'
# k = 10
# mm = MM(network_path, k)
# mm.build_M_and_T_matrix()
# mm.MM_algorithm()
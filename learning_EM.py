import networkx as nx
import numpy as np
from functools import reduce
from file_treatment import FileUtil
from scipy.optimize import minimize


class EM:

    def __init__(self, G_path, k, dis_name):
        self.k = k
        self.G = nx.read_gpickle(G_path)
        self.top_k_movies = FileUtil.build_candidate_set(k)
        self.dis_name = dis_name

    def EM_algorithm(self):
        a = 0.5
        b = 1
        alpha = 2.5
        v = dict()
        for movie_id in self.top_k_movies:
            v[movie_id] = np.random.uniform(low=0.0, high=1.0)
            # v[movie_id] = 1/self.k
        for movie_id in self.top_k_movies:
            v[movie_id] = v[movie_id] / np.sum(list(v.values()))
        scp, fcp = self.build_condi_prob(a, b, alpha, v)
        print(scp)
        print(fcp)
        bnds = list()
        for i in range(self.k):
            bnds.append((0.001, 0.999))
        bnds.append((0.1, 3))
        bnds.append((0.1, 3))
        bnds.append((0.1, 10))
        cons = dict()
        cons['type'] = 'eq'
        cons['fun'] = lambda x: np.sum(x[0:self.k])
        x0 = list(v.values())
        x0.append(a)
        x0.append(b)
        x0.append(alpha)
        res = minimize(lambda x: self.obj(x, succ_condi_prob=scp, fail_condi_prob=fcp), x0=x0, constraints=cons,
                       bounds=bnds, method='SLSQP')
        print(res.fun)
        print(res.success)
        print(res.message)
        print(res.x)

    def obj(self, x, succ_condi_prob, fail_condi_prob):
        print(x)
        v = dict()
        for i in range(self.k):
            v[self.top_k_movies[i]] = x[i]
        a = x[self.k]
        b = x[self.k+1]
        alpha = x[self.k+2]
        temp1 = 0
        temp2 = 0
        for rel in self.G.edges():
            user1 = rel[0]
            user2 = rel[1]
            if user1 != user2:
                temp1 = temp1 + np.log(self.build_meeting_prob(a, b, user1, user2)) + \
                        np.log(self.build_decision_prob(alpha, v, user1, user2))
                temp2 = temp2 + np.log(self.build_meeting_prob(a, b, user1, user2)) + \
                        np.log(1 - self.build_decision_prob(alpha, v, user1, user2))
        return -(succ_condi_prob*temp1+fail_condi_prob*temp2)

    def build_condi_prob(self, a, b, alpha, v):
        succ_condi_prob = 1
        fail_condi_prob = 1
        for rel in self.G.edges():
            user1 = rel[0]
            user2 = rel[1]
            if user1 != user2:
                meeting_prob = self.build_meeting_prob(a, b, user1, user2)
                decision_prob = self.build_decision_prob(alpha, v, user1, user2)
                succ_condi_prob = np.log(meeting_prob*decision_prob/
                                   (meeting_prob*decision_prob+meeting_prob*(1-decision_prob)))+succ_condi_prob
                fail_condi_prob = np.log(meeting_prob*(1-decision_prob)/
                                   (meeting_prob*decision_prob+meeting_prob*(1-decision_prob)))+fail_condi_prob
        return succ_condi_prob, fail_condi_prob

    def build_meeting_prob(self, a, b, user1, user2):
        neighbor1 = set(self.G.neighbors(user1))
        neighbor2 = set(self.G.neighbors(user2))
        common_friends = neighbor1.intersection(neighbor2)
        value = 0
        for friend in common_friends:
            value = self.G[user1][friend]['trust']*self.G[user2][friend]['trust']+value
        return np.exp(b*value)/(a+np.exp(b*value))

    def build_decision_prob(self, alpha, v, user1, user2):
        rating1 = self.G.node[user1]['ratings']
        rating2 = self.G.node[user2]['ratings']
        prob_rating1 = self.build_rating_prob(v, rating1)
        prob_rating2 = self.build_rating_prob(v, rating2)
        value = prob_rating1*prob_rating2*self.sim(user1, user2, alpha)
        return np.exp(value)/(1+np.exp(value))

    def sim(self, user1, user2, alpha):
        mean_degree = np.mean(list(self.G.out_degree().values()))
        dis = self.G[user1][user2][self.dis_name]
        return np.power(1+dis/mean_degree, -alpha)

    def build_rating_prob(self, v, rating):
        if len(rating) == 0:
            return reduce(lambda x, y: x*y, list(v.values()))/np.power(np.sum(list(v.values())), self.k)
        else:
            rating = rating.copy()
            for mv in self.top_k_movies:
                if mv not in rating.keys():
                    rating[mv] = 0
            rating_tr = sorted(rating.items(), key=lambda x: x[1], reverse=True)
            prob = dict()
            prob[rating_tr[0][0]] = v[rating_tr[0][0]]/np.sum(list(v.values()))
            for i in range(1, len(rating)):
                if rating_tr[i][1] == rating_tr[i-1][1]:
                    prob[rating_tr[i][0]] = prob[rating_tr[i-1][0]]
                else:
                    prob[rating_tr[i][0]] = v[rating_tr[i][0]]/np.sum([v[vt[0]] for vt in rating_tr[i:]])
        return reduce(lambda x, y: x*y, list(prob.values()))


G_path = 'data/3-network.gpickle'
k = 3
dis_name = 'spearman'
em = EM(G_path, k, dis_name)
em.EM_algorithm()
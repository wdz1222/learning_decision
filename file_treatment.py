import numpy as np


class FileUtil:

    def __init__(self, trusts_path, movie_ratings_paths):
        self.trusts_path = trusts_path
        self.movie_ratings_paths = movie_ratings_paths

    def top_k_movies(self, k):
        '''
        Statistic the top-K movies
        :param k: The number of the topest movies
        :return:
        Save the top-K movies as 'top-k-movies.txt'
        '''
        movie_dic = dict()
        with open(self.movie_ratings_paths, 'r') as f:
            for line in f.readlines():
                line = line.strip('\n')
                contents = line.split(',')
                movie_id = contents[1]
                if movie_id not in movie_dic.keys():
                    movie_dic[movie_id] = 1
                else:
                    movie_dic[movie_id] = movie_dic[movie_id] + 1
        movie_sorted_dic = sorted(movie_dic.items(), key=lambda x:x[1], reverse=True)
        with open('data/top_'+str(k)+'_movies.txt', 'a+') as f:
            for i in range(k):
                f.writelines(movie_sorted_dic[i][0]+' '+str(movie_sorted_dic[i][1])+'\n')

    def user_saw_movies(self):
        """
        Build the dictionary that contains movie ids and rating whose user saw movies
        The dict construction is as follows:
        {user_id : [{movie1:rating1]}, {movie2:rating3}, ...], ...}
        :return:
        Save the dictionary as a txt document named 'user_saw_movies_dic.txt'
        """
        user_saw_movies_dic = dict()
        with open(self.movie_ratings_paths, 'r') as f:
            for line in f.readlines():
                line = line.strip('\n')
                contents = line.split(',')
                user_id = contents[0]
                movie_id = contents[1]
                movie_rating = int(contents[4])
                if user_id not in user_saw_movies_dic.keys():
                    user_saw_movies_dic[user_id] = list()
                    user_saw_movies_dic[user_id].insert(0, {movie_id : movie_rating})
                else:
                    user_saw_movies_dic[user_id].insert(0, {movie_id: movie_rating})
        with open('data/user_saw_movies_dic.txt', 'w') as f:
            f.write(str(user_saw_movies_dic))

    def user_saw_k_movies_dic(self, k):
        """
        Statistic the dictionary that user's movies ranking for the top-K movies
        :param k: The number of the topest movies
        :return:
        Save the dictionary as a txt document named 'user_saw_k_movies_dic.txt'
        """
        k_top_movies = self.build_candidate_set(k)
        with open('data/user_saw_movies_dic.txt', 'r') as f:
            user_saw_movies_dic = eval(f.read())
        user_saw_k_movies_dic = dict()
        for user_id in user_saw_movies_dic.keys():
            user_saw_movies = user_saw_movies_dic[user_id]
            for movie in user_saw_movies:
                movie_id = list(movie.keys())[0]
                if movie_id in k_top_movies:
                    if user_id not in user_saw_k_movies_dic:
                        user_saw_k_movies_dic[user_id] = list()
                        user_saw_k_movies_dic[user_id].insert(0, movie)
                    else:
                        flag = True
                        for mv in user_saw_k_movies_dic[user_id]:
                            mv_id = list(mv.keys())[0]
                            if mv_id == movie_id:
                                flag = False
                                if movie[movie_id] >= mv[mv_id]:
                                    mv[mv_id] = movie[movie_id]
                                break
                        if flag:
                            user_saw_k_movies_dic[user_id].insert(0, movie)
        with open('data/user_saw_'+str(k)+'_movies_dic.txt', 'w') as f:
            f.write(str(user_saw_k_movies_dic))

    @staticmethod
    def build_candidate_set(k):
        k_top_movies_path = 'data/top_'+str(k)+'_movies.txt'
        k_top_movies = np.loadtxt(k_top_movies_path, dtype='str')
        return k_top_movies[:, 0]


# trusts_path = 'data/trusts.txt'
# movie_ratings_paths = 'data/movie-ratings.txt'
# fu = FileUtil(trusts_path, movie_ratings_paths)
# fu.top_k_movies(3)
# fu.build_candidate_set(3)
# fu.user_saw_movies()
# fu.user_saw_k_movies_dic(3)
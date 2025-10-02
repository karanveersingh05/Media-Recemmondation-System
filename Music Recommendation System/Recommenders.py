import numpy as np
import pandas

class popularity_recommender_py():
    def __init__(self):
        self.my_data = None
        self.uid = None
        self.iid = None
        self.pop_recs = None
        
    def create(self, my_data, uid, iid):
        self.my_data = my_data
        self.uid = uid
        self.iid = iid

        data_grouped = my_data.groupby([self.iid]).agg({self.uid: 'count'}).reset_index()
        data_grouped.rename(columns = {'user_id': 'score'},inplace=True)
        
        data_sort = data_grouped.sort_values(['score', self.iid], ascending = [0,1])
        
        data_sort['Rank'] = data_sort['score'].rank(ascending=0, method='first')
        
        self.pop_recs = data_sort.head(10)

    def recommend(self, uid):    
        my_recs = self.pop_recs
        
        my_recs['user_id'] = uid
        
        cols = my_recs.columns.tolist()
        cols = cols[-1:] + cols[:-1]
        my_recs = my_recs[cols]
        
        return my_recs

class item_similarity_recommender_py():
    def __init__(self):
        self.data = None
        self.u = None
        self.i = None
        self.co_matrix = None
        self.songs_dict = None
        self.rev_songs_dict = None
        self.item_sim_recs = None
        
    def create(self, data, u, i):
        self.data = data
        self.u = u
        self.i = i

    def get_user_items(self, user):
        user_d = self.data[self.data[self.u] == user]
        user_i = list(user_d[self.i].unique())
        
        return user_i
        
    def get_item_users(self, item):
        item_d = self.data[self.data[self.i] == item]
        item_u = set(item_d[self.u].unique())
            
        return item_u
        
    def get_all_items_train_data(self):
        all_i = list(self.data[self.i].unique())
            
        return all_i
        
    def construct_cooccurence_matrix(self, u_songs, all_songs):
        
        u_songs_users = []        
        for i in range(0, len(u_songs)):
            u_songs_users.append(self.get_item_users(u_songs[i]))
            
        co_matrix = np.matrix(np.zeros(shape=(len(u_songs), len(all_songs))), float)
           
        for i in range(0,len(all_songs)):
            songs_i_data = self.data[self.data[self.i] == all_songs[i]]
            users_i = set(songs_i_data[self.u].unique())
            
            for j in range(0,len(u_songs)):       
                users_j = u_songs_users[j]
                users_intersection = users_i.intersection(users_j)
                
                if len(users_intersection) != 0:
                    users_union = users_i.union(users_j)
                    
                    co_matrix[j,i] = float(len(users_intersection))/float(len(users_union))
                else:
                    co_matrix[j,i] = 0
                    
        return co_matrix

    def generate_top_recommendations(self, user, co_matrix, all_songs, u_songs):
        print("Non zero values in cooccurence_matrix :%d" % np.count_nonzero(co_matrix))
        
        user_sim_scores = co_matrix.sum(axis=0)/float(co_matrix.shape[0])
        user_sim_scores = np.array(user_sim_scores)[0].tolist()
 
        sort_index = sorted(((e,i) for i,e in enumerate(list(user_sim_scores))), reverse=True)
    
        columns = ['user_id', 'song', 'score', 'rank']
        df = pandas.DataFrame(columns=columns)
         
        rank = 1 
        for i in range(0,len(sort_index)):
            if ~np.isnan(sort_index[i][0]) and all_songs[sort_index[i][1]] not in u_songs and rank <= 10:
                df.loc[len(df)]=[user,all_songs[sort_index[i][1]],sort_index[i][0],rank]
                rank = rank+1
        
        if df.shape[0] == 0:
            print("The current user has no songs for training the item similarity based recommendation model.")
            return -1
        else:
            return df
 
    def recommend(self, user):
        
        u_songs = self.get_user_items(user)    
        
        print("No. of unique songs for the user: %d" % len(u_songs))
        
        all_songs = self.get_all_items_train_data()
        
        print("no. of unique songs in the training set: %d" % len(all_songs))
         
        co_matrix = self.construct_cooccurence_matrix(u_songs, all_songs)
        
        df_recs = self.generate_top_recommendations(user, co_matrix, all_songs, u_songs)
                
        return df_recs
    
    def get_similar_items(self, item_list):
        
        u_songs = item_list
        
        all_songs = self.get_all_items_train_data()
        
        print("no. of unique songs in the training set: %d" % len(all_songs))
         
        co_matrix = self.construct_cooccurence_matrix(u_songs, all_songs)
        
        user = ""
        df_recs = self.generate_top_recommendations(user, co_matrix, all_songs, u_songs)
         
        return df_recs

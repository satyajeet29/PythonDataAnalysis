import pandas as pd
import warnings
from tabulate import tabulate
path = "//Users//satyajeetpradhan//DataAnalysisRepo//pydata-book//datasets//movielens//"

# Read data files
warnings.filterwarnings("ignore") # ignore warning message
unames = ['user_id', 'gender','age','occupation','zip']
users = pd.read_table(path+"users.dat",sep='::',header=None, names=unames)
rnames = ['user_id', 'movie_id','rating','timestamp']
ratings = pd.read_table(path+"ratings.dat",sep='::',header=None, names=rnames)
mnames = ['movie_id', 'title','genres']
movies = pd.read_table(path+"movies.dat",sep='::',header=None, names=mnames)

# Explore datasets
def printHead(tableName):
    print(tabulate(tableName.head(), headers='keys', tablefmt='psql'))
#printHead(users)
#printHead(ratings)
#printHead(movies)

#merging/joining dataframes
data = pd.merge(movies, pd.merge(ratings,users, left_on='user_id', right_on='user_id'), left_on='movie_id', right_on='movie_id')
mean_ratings = data.pivot_table('rating', index = 'title', columns ='gender', aggfunc = 'mean') # changed rows to index, correction
printHead(mean_ratings[:5])

ratings_by_title = data.groupby('title').size()
print(ratings_by_title[:10])
print(ratings_by_title.dtypes)

active_titles = ratings_by_title.index[ratings_by_title  >= 250]
print("\n\n")
print(active_titles)

mean_ratings = mean_ratings.ix[active_titles]
print("\n\n")
print(mean_ratings)

top_female_ratings =  mean_ratings.sort_index(by='F', ascending = False)
print("\n\n")
print(top_female_ratings[:10])

mean_ratings['diff'] = mean_ratings['M'] - mean_ratings['F']
sorted_by_diff = mean_ratings.sort_index(by='diff')
print("\n\n")
print(sorted_by_diff[:15])

#Reverse order of rows to take first 15 rows
print("\n\n")
print(sorted_by_diff[::-1][:15])

rating_std_by_title = data.groupby('title')['rating'].std()
print("\n\n")
print(rating_std_by_title)

rating_std_by_title = rating_std_by_title.ix[active_titles]
print("\n\n")
print(rating_std_by_title)

print("\n\n")
print(rating_std_by_title.sort_values(ascending=False)[:10]) #.order replace with .sort_values
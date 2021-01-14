import pandas as pd
path = "//Users//satyajeetpradhan//DataAnalysisRepo//pydata-book//datasets//movielens//"

unames = ['user_id', 'gender','age','occupation','zip']
users = pd.read_table(path+"users.dat",sep='::',header=None, names=unames)

rnames = ['user_id', 'movie_id','rating','timestamp']
ratings = pd.read_table(path+"ratings.dat",sep='::',header=None, names=unames)

mnames = ['movie_id', 'title','genres']
movies = pd.read_table(path+"movies.dat",sep='::',header=None, names=unames)

print(ratings.head())

data = pd.merge(pd.merge(ratings, users), movies)
print(data.ix[0])


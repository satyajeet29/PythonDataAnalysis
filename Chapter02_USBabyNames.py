import pandas as pd
import warnings
from tabulate import tabulate
import os
import numpy as np
path = "//Users//satyajeetpradhan//DataAnalysisRepo//pydata-book//datasets//babynames//"

names1880 = pd.read_csv(path+'yob1880.txt', names = ['name','sex','births'])
print(names1880)

print(names1880.groupby('sex').births.sum())

years = range(1880,2011)
columns = ['name','sex','births']
pieces = []
for year in years:
    file = path+'yob%d.txt' %year
    frame = pd.read_csv(file,names=columns)

    frame['year'] = year
    pieces.append(frame)

names = pd.concat(pieces, ignore_index=True)
def printHead(tableName):
    print(tabulate(tableName.head(), headers='keys', tablefmt='psql'))
printHead(names)

total_births = names.pivot_table('births', index = 'year', columns = 'sex', aggfunc=sum)
def add_prop(group):
    # Integer division floors
    births = group.births.astype(float)

    group['prop'] = births /births.sum()
    return group
names = names.groupby(['year','sex']).apply(add_prop)

np.allclose(names.groupby(['year','sex']).prop.sum(),1)

def get_top1000(group):
    return group.sort_index(by='births', ascending=False)[:1000]

grouped = names.groupby(['year','sex'])
top1000 = grouped.apply(get_top1000)

pieces=[]
for year, group in names.groupby(['year','sex']):
    pieces.append(group.sort_index(by='births', ascending = False)[:1000])

top1000 = pd.concat(pieces, ignore_index=True)

print(top1000)

boys = top1000[top1000.sex  == 'M']
girls = top1000[top1000.sex  == 'F']

total_births = top1000.pivot_table('births',index ='year',columns ='name',aggfunc=sum)
print(total_births)

subset = total_births[['John','Harry','Mary','Marilyn']]
subset.plot(subplots = True, figsize = (12,10), grid = False, title = "Number of births per year")

table = top1000.pivot_table('prop',index ='year',columns ='name',aggfunc=sum)
#table.plot(titles = 'Sum of table1000.prop by year and sex', yticks = np.linspace(0,1.2,13), xticks = range(1880,2020,10))

df = boys[boys.year==2010]
printHead(df)

prop_cumsum = df.sort_values(by = 'prop', ascending=False).prop.cumsum()

df = boys[boys.year==1900]
in1900 = df.sort_values(by = 'prop', ascending=False).prop.cumsum()
in1900.searchsorted(0.5) + 1

def get_quantile_count(group, q=0.5):
    group = group.sort_values(by = 'prop', ascending=False)
    return group.prop.cumsum().searchsorted(q) + 1

diversity = top1000.groupby(['year','sex']).apply(get_quantile_count)
diversity = diversity.unstack('sex')
print(diversity.head())

# Print last letter revolution
get_last_letter = lambda x: x[-1]
last_letters = names.name.map(get_last_letter)
last_letters.name = 'last_letter'

table = names.pivot_table('births', index = last_letters, columns = ['sex','year'], aggfunc=sum)

subtable = table.reindex(columns = [1910,1960,2010],level = 'year')
print(subtable.head())
print(subtable.sum())

letter_prop = subtable/subtable.sum().astype(float)
import matplotlib.pyplot as plt
fig, axes = plt.subplots(2,1,figsize = (10,8))
letter_prop['M'].plot(kind = 'bar', rot = 0, ax=axes[0], title = 'Male')
letter_prop['F'].plot(kind = 'bar', rot = 0, ax=axes[0], title = 'Male')


letter_prop = table/table.sum().astype(float)
dny_ts = letter_prop.ix[['d','n','y'],'M'].T
print(dny_ts.head())

dny_ts.plot()

all_names = top1000.name.unique()
mask = np.array(['les1' in x.lower() for x in all_names])
lesley_like = all_names[mask]
lesley_like
#array([Leslie, Lesley, Leslee, Lesli, Lesly], dtype = object)
filtered = top1000[top1000.name.isin(lesley_like)]
filtered.groupby('name').births.sum()

table = filtered.pivot_table('births', index ='year',columns = 'sex', aggfunc = 'sum')
table = table.div(table.sum(1),axis=0)
print(table.tail())

#table.plot(style={'M':'k-','F':'k--'})

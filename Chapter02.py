path = "//Users//satyajeetpradhan//DataAnalysisRepo//pydata-book//datasets//bitly_usagov//example.txt"
#print(open(path).readline())

import json
records = [json.loads(line) for line in  open(path)]

print(records[0])
print(records[0]['tz'])
timeZones = [rec['tz'] for rec in records] # would fail as 'tz' isn't present in all rows

def get_counts(sequence):
    counts = {}
    for x in sequence:
        if x in counts:
            counts[x]+=1
        else:
            counts[x] = 1
    return counts

from collections import defaultdict
def get_counts2(sequence):
    counts = defaultdict(int)
    for x in sequence:
        counts[x] +=1
    return counts

counts = get_counts(timeZones)
print(counts)
print(len(timeZones))

# get top 10 counts
def top_counts(count_dict, n=10):
    value_key_pairs = [(count,tz) for  tz, count in count_dict.items()]
    value_key_pairs.sort()
    return value_key_pairs[-n:]

#Counting time zones with pandas:
from pandas import DataFrame, Series
import pandas as pd; import numpy as np
frame = DataFrame(records)
frame

tz_counts = frame['tz'].value_counts() # obtains value counts by a given value

#plot the given results
clean_tz = frame['tz'].fillna('Missing')
clean_tz[clean_tz == ''] = 'Unknown'
tz_counts = clean_tz.value_counts()

results = Series([x.split()[0] for x in frame.a.dropna()])

cframe = frame[frame.a.notnull()]
operating_system = np.where/(cframe['a'].str.contains('Windows'),'Windows','Not Windows')
by_tz_os = cframe.groupby(['tz',operating_system])

agg_counts = by_tz_os.size().unstack().fillna(0)
indexer = agg_counts.sum(1).argsort()
count_subset = agg_counts.take(indexer)[-10:]

normed_subset = count_subset.div(count_subset.sum(1), axis=0)

normed_subset.plot(kind = 'barh', stacked = True)

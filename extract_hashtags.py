import sqlite3 as db
import pandas as pd
from ttp import ttp
p = ttp.Parser()

def get_hashtags(tweet):
	parsed_tweet = p.parse(tweet)
	return parsed_tweet.tags

database = "all_data"
type_data = "cc"
table_from = type_data
#table_to = "cc_counts"

con = db.connect(database)
c = con.cursor()
df = pd.read_sql("SELECT * from " + table_from, con)

hashtags = df['tweet'].apply(get_hashtags).apply(pd.Series).stack().reset_index(drop=True)

h_counts = hashtags.value_counts()

print(h_counts[0:100])

h_counts[0:100].to_csv(type_data + "_hashtag_counts.csv")



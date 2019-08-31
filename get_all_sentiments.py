import pandas as pd 
import sqlite3 as db
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
import sent_analysis

database = "all_data"
#type of the data is always cc (#commoncore) or ccr ("college and career readiness")
type_data = "ccr"
table_from = type_data
table_to = type_data + "_sampled"

#connect to database
con = db.connect(database)
c = con.cursor()
big_df = pd.read_sql("SELECT * from " + table_from, con)

#take out deleted tweets
big_df = big_df[big_df['deleted'] == 0]

#samples 100 tweets from the table and extracts just the sentiment scores
df = big_df.sample(n=100)[['tweet', 'sentiment_corenlp', 'sentiment_textblob']]

#filled in by a human later
df.insert(1, 'hand_rated',0)

#apply the various algorithms for sentiment scores: 
#(re applying textblob because there was a slight change to the algorithm)
#checkout sent analysis for more detailed explanations on the programs

df['sentiment_textblob'] = df['tweet'].apply(sent_analysis.get_sentiment_textblob)

df['sentiment_vader'] = df['tweet'].apply(sent_analysis.get_sentiment_vader)

df['sentiment_textblob_NB'] = df['tweet'].apply(sent_analysis.get_sentiment_textblob_NB)

df['sentiment_textblob_NB_weighted'] = df['tweet'].apply(sent_analysis.get_sentiment_textblob_NB_weighted)

df['sentiment_textblob_weighted'] = df['tweet'].apply(sent_analysis.get_sentiment_textblob_weighted)

#then normalize them to be -1 to 1

df['sentiment_corenlp'] = (df['sentiment_corenlp'] / 2) - 1

df['sentiment_textblob_NB'] = (df['sentiment_textblob_NB'] * 2) - 1

df['sentiment_textblob_NB_weighted'] = (df['sentiment_textblob_NB_weighted'] * 2) - 1

df.to_sql(table_to, con, index = False)

con.close()



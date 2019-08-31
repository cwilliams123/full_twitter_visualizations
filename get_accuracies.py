import pandas as pd 
import sqlite3 as db
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
import sent_analysis

database = "all_data"
#type of the data is always cc (#commoncore) or ccr ("college and career readiness")
type_data = "ccr"
table_from = type_data + "_sampled"

#connect to database and get the sampled data
con = db.connect(database)
c = con.cursor()
df = pd.read_sql("SELECT * from " + table_from, con)


#gets the sum of the absolute value differences between the hand rated score and the algorithms' scores
#and averages them over the total, 100

diff_textblob = (df['sentiment_textblob'] - df['hand_rated']).abs().sum() / 100
diff_textblob_weighted = (df['sentiment_textblob_weighted'] - df['hand_rated']).abs().sum() / 100
diff_textblob_NB = (df['sentiment_textblob_NB'] - df['hand_rated']).abs().sum() / 100
diff_textblob_NB_weighted = (df['sentiment_textblob_NB_weighted'] - df['hand_rated']).abs().sum() / 100
diff_corenlp = (df['sentiment_corenlp'] - df['hand_rated']).abs().sum() / 100
diff_vader = (df['sentiment_vader'] - df['hand_rated']).abs().sum() / 100

print("textblob: " + str(diff_textblob))
print("textblob weighted: " + str(diff_textblob_weighted))
print("textblob NB: " + str(diff_textblob_NB))
print("textblob NB weighted: " + str(diff_textblob_NB_weighted))
print("textblob corenlp: " + str(diff_corenlp))
print("vader: " + str(diff_vader))

con.close()

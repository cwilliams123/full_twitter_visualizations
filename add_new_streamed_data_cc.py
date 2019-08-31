import sqlite3 as db
import clean_streamed_data as csd
import sent_analysis

#scp cwilli22@bsn01:/data/cwilli22/streaming/common_core/new_cc_tweets.db .

#to start NLP server: (should be done before this program starts on a different terminal, inside the stanford folder)
#java -mx6g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -timeout 5000 

consumer_key = 'TpFFRQhpLU6xB8Ju48XVprWMg'
consumer_secret = 'KMi4t6ciEISo23rxJxltJ4bvt6MdQg1sipCt2TnnOluGN295qq'
access_token= '1135946096449138689-RNoNCILwV70CGX0aHBWTDXoshkCIqH'
access_secret= 'WIckI9PXgskqN1H8gW3B1QgFZAqG8bYGqDHN4gOHPzMo1'

database_from = "new_cc_tweets.db"

database_to = "all_data"

original_table = "tweets"

cleaned_table = "clean"

sentiment_table = "with_sentiment"

full_table = "cc"

#clean new data:
csd.clean_streamed_data(consumer_key, consumer_secret, access_token, access_secret, database_from, original_table, cleaned_table)

#sentiment analysis of new data (stored as a dataframe):
sent_analysis.add_col_w_sentiment(database_from, cleaned_table, sentiment_table)

#insert new data into old db:
con = db.connect(database_to)

c = con.cursor()

c.execute("ATTACH DATABASE \'" + database_from + "\' as new_db")

c.execute("INSERT INTO \'" + full_table + '''\' SELECT id,
	created_at,
	time_downloaded,
	deleted,
	screenname,
	user_description,
	user_location,
	isRetweet,
	favoriteCount,
	retweetCount,
	state,
	geo,
	coordinates,
	tweet,
	sentiment_corenlp,
	sentiment_textblob,
	subjectivity,
	source FROM new_db.''' + sentiment_table)

con.commit()

con.close()










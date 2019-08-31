import sqlite3 as db
import clean_streamed_data as csd
import sent_analysis

#scp cwilli22@bsn01:/data/cwilli22/streaming/college_career_readiness/new_ccr_tweets.db .

#to start NLP server: (should be done before this program starts on a different terminal, inside the stanford folder)
#java -mx6g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -timeout 5000 


consumer_key = 'f0RtjQ2jcq9ZNw1jOprB3EVeC'
consumer_secret = '5YjR83H05slPnaDVl1KNafonWU36ewtQAb2JNMOpLZeMJipSn4'
access_token = '1136378599227953152-Xqn4sl2Fa7X4ycvP5pFUlTte7iT1v2'
access_secret = 'UdRdEBiUxgpCa2fJibcA1S5uzz4NxJRC4Di5cc9uaMyuv'

database_from = "new_ccr_tweets.db"

database_to = "all_data"

original_table = "tweets"

cleaned_table = "clean"

sentiment_table = "with_sentiment"

full_table = "ccr"

#clean new data:
csd.clean_streamed_data(consumer_key, consumer_secret, access_token, access_secret, database_from, original_table, cleaned_table)

#sentiment analysis of new data:
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









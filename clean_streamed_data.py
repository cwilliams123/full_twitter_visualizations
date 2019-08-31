import sqlite3 as db
import tweepy 
import json
import datetime as dt
import sys
import pandas as pd
import numpy as np
import us
import nltk
import time
import cleaning_functions

def clean_streamed_data(consumer_key, consumer_secret, access_token, access_secret, database, table_from, table_to):
	#connect to database and make it a pandas dataframe:
	con = db.connect(database)
	c = con.cursor()
	df = pd.read_sql("SELECT * from " + table_from, con)

	#authorize
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret) 
	auth.set_access_token(access_token, access_secret)
	api = tweepy.API(auth)

	#make isRetweet a boolean for ease of use
	df['isRetweet'] = df['isRetweet'] == 1

	#add a column for the state the tweet was from, according to the user_location
	df['state'] = np.nan
	df['state'] = df['user_location'].apply(cleaning_functions.get_state)

	#add in any geotagging and save full (not truncated) text as well as if the tweet's a retweet
	df = cleaning_functions.fix_geo_text_and_retweet(df, api)

	df['source'] = 'streamed'

	#drop old table to make way for the new
	c.execute("DROP TABLE IF EXISTS %s" % table_to)
	df.to_sql(table_to, con)

	con.close()

def main():
	consumer_key = 'f0RtjQ2jcq9ZNw1jOprB3EVeC'
	consumer_secret = '5YjR83H05slPnaDVl1KNafonWU36ewtQAb2JNMOpLZeMJipSn4'
	access_token = '1136378599227953152-Xqn4sl2Fa7X4ycvP5pFUlTte7iT1v2'
	access_secret = 'UdRdEBiUxgpCa2fJibcA1S5uzz4NxJRC4Di5cc9uaMyuv'

	database = "cc_streamed_download1.db"

	table_from = "tweets"

	table_to = "clean"

	clean_streamed_data(consumer_key, consumer_secret, access_token, access_secret, database, table_from, table_to)


if __name__ == "__main__":
	main()

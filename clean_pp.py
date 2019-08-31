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

def clean_pp_data(consumer_key, consumer_secret, access_token, access_secret, database, table_from, table_to):
	#connect to database and make it a pandas dataframe:
	con = db.connect(database)
	c = con.cursor()
	df = pd.read_sql("SELECT * from " + table_from, con)

	#authorize--used to connect to twitter
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret) 
	auth.set_access_token(access_token, access_secret)

	#"api" is our connection to twitter data
	api = tweepy.API(auth)

	#don't know the exact time downloaded so this is our closest estimation:
	df['time_downloaded'] = df['created_at']

	#make isRetweet a bool for ease of use
	df['isRetweet'] = df['isRetweet'] == 'TRUE'

	#add a column for the state the tweet was from, according to the user_location
	df['state'] = df['user_location'].apply(cleaning_functions.get_state)

	#add in any geotagging and save full (not truncated) text
	df = cleaning_functions.fix_geo_and_text(df, api)

	#drop any old table to make way for the new
	c.execute("DROP TABLE IF EXISTS %s" % table_to)
	df.to_sql(table_to, con)


def main():
	consumer_key = 'f0RtjQ2jcq9ZNw1jOprB3EVeC'
	consumer_secret = '5YjR83H05slPnaDVl1KNafonWU36ewtQAb2JNMOpLZeMJipSn4'
	access_token = '1136378599227953152-Xqn4sl2Fa7X4ycvP5pFUlTte7iT1v2'
	access_secret = 'UdRdEBiUxgpCa2fJibcA1S5uzz4NxJRC4Di5cc9uaMyuv'

	database = "ccr_pp.db"

	table_from = "tweets"

	table_to = "clean1"

	clean_pp_data(consumer_key, consumer_secret, access_token, access_secret, database, table_from, table_to)


main()
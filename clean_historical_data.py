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

def clean_historical_data(consumer_key, consumer_secret, access_token, access_secret, database, table_from, table_to):
	#connect to database and make it a pandas dataframe:
	con = db.connect(database)
	c = con.cursor()
	df = pd.read_sql("SELECT * from " + table_from, con)

	#authorize
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret) 
	auth.set_access_token(access_token, access_secret)
	api = tweepy.API(auth)

	#initialize all the necessary cols
	df['isRetweet'] = np.nan
	df['favoriteCount'] = np.nan
	df['retweetCount'] = np.nan
	df['screenname'] = np.nan
	df['user_description'] = np.nan
	df['user_location'] = np.nan
	df['time_downloaded'] = df['created_at'] #cause this was streamed so that's a safe bet
	df['geo'] = np.nan
	df['coordinates'] = np.nan
	df['deleted'] = False
	df['id'] = np.nan
	df['state'] = df['state'].apply(cleaning_functions.get_state)

	#to protect against twitter rate limiting
	tweets_remaining = json.dumps(api.rate_limit_status()['resources']['statuses']['/statuses/show/:id']['remaining'])
	print("tweets remaining before program: "+ tweets_remaining)

	tweets_remaining = int(tweets_remaining)

	for index, row in df.iterrows():
		if tweets_remaining <= 0:
			print("had to pause for rate limiting")
			time.sleep(900)
			tweets_remaining += 900
		#the id might not be linked to a tweet anymore (if it's been deleted) 
		#so we just move on if that's the case
		try:
			tweets_remaining -= 1
			user = api.get_user(row['userid'])

			#gets the info we can from the tweets; since this data set contains no valid tweet ids, we
			#can't get more info on retweets or favorites; but the user ids are correct so we can get more
			#info there:
			df.loc[index, 'screenname'] = user.screen_name
			df.loc[index, 'user_description'] = user.description
			df.loc[index, 'user_location']= user.location

			#if we can't get the data from twitter, that means it doesn't exits (the tweets has been deleted)
		except:
		 	df.loc[index, 'deleted'] = True

	print("remaining after program: " + str(tweets_remaining))


	#drop old table to make way for the new
	c.execute("DROP TABLE IF EXISTS %s" % table_to)
	df.to_sql(table_to, con)


def main():
	consumer_key = 'TpFFRQhpLU6xB8Ju48XVprWMg'
	consumer_secret = 'KMi4t6ciEISo23rxJxltJ4bvt6MdQg1sipCt2TnnOluGN295qq'
	access_token= '1135946096449138689-RNoNCILwV70CGX0aHBWTDXoshkCIqH'
	access_secret= 'WIckI9PXgskqN1H8gW3B1QgFZAqG8bYGqDHN4gOHPzMo1'

	database = "historical_data.db"

	table_from = "cc"

	table_to = "clean_cc"

	clean_historical_data(consumer_key, consumer_secret, access_token, access_secret, database, table_from, table_to)


main()

import sqlite3 as db
import json
import datetime
import pandas as pd
from twython import Twython
import numpy as np
import time

#this is what makes the new data table with the updated counts to add to the big data table
#df only has ids of all the tweets to update in it
def make_new_data_table(consumer_key, consumer_secret, access_token, access_secret, df):
	#used a different twitter package here because it gets more accurate retweet/favorite counts
	twitter = Twython(consumer_key, consumer_secret,
	                  access_token, access_secret)

	#tracking the things that change over time (and saving them with their time downloaded):
	df['retweet_count'] = np.nan
	df['favorite_count'] = np.nan
	df['deleted'] = False
	df['time_downloaded'] = np.nan

	#check for rate limiting
	tweets_remaining = json.dumps(twitter.get_application_rate_limit_status()['resources']['statuses']['/statuses/show/:id']['remaining'])
	print("tweets remaining before program: "+ tweets_remaining)

	tweets_remaining = int(tweets_remaining)

	for index, row in df.iterrows():
		if tweets_remaining <= 0:
			string_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
			print("had to pause for rate limiting. time: " + string_time)
			while(tweets_remaining == 0):
				time.sleep(15)
				tweets_remaining = int(json.dumps(twitter.get_application_rate_limit_status()['resources']['statuses']['/statuses/show/:id']['remaining']))
		try:
			tweets_remaining -= 1

			tweet = twitter.show_status(id=row['id'])

			df.loc[index, 'retweet_count'] = tweet['retweet_count']
			df.loc[index, 'favorite_count'] = tweet['favorite_count']

			now = datetime.datetime.now()
			formatted_time = now.strftime("%Y-%m-%d %H:%M")
			df.loc[index, 'time_downloaded'] = formatted_time
			

		except:
			#if we can't find the tweet that means its been deleted
			df.loc[index, 'deleted'] = True
			now = datetime.datetime.now()
			formatted_time = now.strftime("%Y-%m-%d %H:%M")
			df.loc[index, 'time_downloaded'] = formatted_time

	return df

	
#adds new data pulled above
def append_new_data(consumer_key, consumer_secret, access_token, access_secret, database, all_data_table, updates_data_table):
	con = db.connect(database)
	c = con.cursor()
	id_df = pd.read_sql("SELECT id, created_at from " + all_data_table + " WHERE id IS NOT NULL", con)
	big_df = pd.read_sql("SELECT * from " + updates_data_table, con)

	new_data = make_new_data_table(consumer_key, consumer_secret, access_token, access_secret, id_df)

	new_data.to_sql(updates_data_table, con, index = False, if_exists='append')

	con.close()




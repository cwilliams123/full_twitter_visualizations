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

#used to extract any mention of a state from user location
def get_state(location):
	if(location == None):
		return None
	#tokenize words in location string
	location_tokens = nltk.word_tokenize(location)
	#only use words, not numbers or symbols
	location_tokens = [word for word in location_tokens if word.isalpha()]
	for word in location_tokens:
		#check if us.states can find a matching state (either by acronym or full name)
		s = us.states.lookup(word)
		#if it does then s will have something in it, and that's the state we've pulled
		if s != None:
			return str(s)
	#otherwise we return nothing
	return None

#pulls any geotagging data and the full text of the tweet
def fix_geo_and_text(df, api):
	#placeholders where location info (if available) will be stored
	df['geo'] = np.nan
	df['coordinates'] = np.nan
	df['deleted'] = False

	#check for rate limiting--Twitter only allows us 900 tweets per 15 minutes
	tweets_remaining = json.dumps(api.rate_limit_status()['resources']['statuses']['/statuses/show/:id']['remaining'])
	print("tweets remaining before program: "+ tweets_remaining)

	tweets_remaining = int(tweets_remaining)

	for index, row in df.iterrows():
		if tweets_remaining <= 0:
			print("had to pause for rate limiting")
			#if we exceed the number of tweets then we wait 15 minutes
			time.sleep(900)
			tweets_remaining += 900
		#the id might not be linked to a tweet anymore (if it's been deleted) 
		#so we just move on and record that if that's the case
		try:
			tweets_remaining -= 1
			status = api.get_status(id = row['id'], tweet_mode = 'extended')
			#below ensures text is full -- twitter's default is to truncate
			#if it's a retweet the full text of the tweet is stored in a different place than if its not
			if row['isRetweet']:
				df.loc[index, 'tweet'] = status.retweeted_status._json['full_text']
			else:
				df.loc[index, 'tweet'] = status._json['full_text']

			#check if there's any geotagging goin on--saves those as strings
			coordinates = status.coordinates
			geo = status.geo

			if geo is not None:
				geo = json.dumps(geo)

			if coordinates is not None:
				coordinates = json.dumps(coordinates)

			df.loc[index, 'geo'] = geo
			df.loc[index, 'coordinates'] = coordinates

		except:
		 	df.loc[index, 'deleted'] = True

	print("remaining after program: " + str(tweets_remaining))
	return df


def fix_geo_text_and_retweet(df, api):
	#placeholders where location info (if available) will be stored
	df['geo'] = np.nan
	df['coordinates'] = np.nan
	df['isRetweet'] = np.nan
	df['deleted'] = False

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
			status = api.get_status(id = row['id'], tweet_mode = 'extended')
			#below ensures text is full -- twitter's default is to truncate

			#check if the tweets a retweet
			try:
				status.retweeted_status
				df.loc[index, 'isRetweet'] = True
				retBool = True

			except AttributeError:
				df.loc[index, 'isRetweet'] = False
				retBool = False

			if retBool:
				df.loc[index, 'tweet'] = status.retweeted_status._json['full_text']
			else:
				df.loc[index, 'tweet'] = status._json['full_text']

			#check if there's any geotagging goin on--saves those as strings
			coordinates = status.coordinates
			geo = status.geo

			if geo is not None:
				geo = json.dumps(geo)

			if coordinates is not None:
				coordinates = json.dumps(coordinates)

			df.loc[index, 'geo'] = geo
			df.loc[index, 'coordinates'] = coordinates

		except:
		 	df.loc[index, 'deleted'] = True

	print("remaining after program: " + str(tweets_remaining))
	return df


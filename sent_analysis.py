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
import preprocessor as p
from textblob import TextBlob
from textblob import Blobber
from textblob.sentiments import NaiveBayesAnalyzer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


#set up CoreNLP server, Texblob and VADER (last line) -- three sentiment packages
from pycorenlp import StanfordCoreNLP
nlp = StanfordCoreNLP('http://localhost:9000')
tb = Blobber(analyzer=NaiveBayesAnalyzer())
analyzer = SentimentIntensityAnalyzer()

def clean_tweet(tweet):
	#clean the tweet: (takes out url's and mentions)
	p.set_options(p.OPT.URL, p.OPT.MENTION)
	return p.clean(tweet)

def get_sentiment_corenlp(tweet):
	cleaned_tweet = clean_tweet(tweet)
	#get the sentiment of each sentence:
	result = nlp.annotate(cleaned_tweet,
                   properties={
                       'annotators': 'sentiment',
                       'outputFormat': 'json',
                       'timeout': 5000,
                   })
	#if it's empty, return nothing
	if(len(result['sentences']) == 0):
		return None
	#otherwise, get the sentiment of each sentence and average normally
	average_sentiment = 0
	for s in result["sentences"]:
		average_sentiment += int(s["sentimentValue"])
	return average_sentiment / len(result['sentences'])

#weighted = instead of a normal average, the average is weighted by
#number of words in each sentence--this performs very similarly
#to the normal averaging, so it's not used in the visualization
def get_sentiment_textblob_weighted(tweet):
	cleaned_tweet = clean_tweet(tweet)
	blob = TextBlob(cleaned_tweet)
	if(len(blob.sentences) == 0):
			return None
	average_sentiment = 0
	total_words = sum(map(lambda x: len(x.split()), blob.sentences))
	for s in blob.sentences:
		average_sentiment += (s.sentiment.polarity * len(s.split()))
	return average_sentiment / total_words

#since the normal textblob algorithm is word by word, we decided to
#just treat the whole tweet as one giant sentence
def get_sentiment_textblob(tweet):
	cleaned_tweet = clean_tweet(tweet)
	no_periods = cleaned_tweet.replace(".", "")
	blob = TextBlob(cleaned_tweet)
	if(len(blob.sentences) == 0):
			return None
	average_sentiment = 0
	for s in blob.sentences:
		average_sentiment += s.sentiment.polarity
	return average_sentiment / len(blob.sentences)

#NB = Naive Bayes, the alternative textblob algorithm
def get_sentiment_textblob_NB(tweet):
	cleaned_tweet = clean_tweet(tweet)
	blob = tb(cleaned_tweet)
	if(len(blob.sentences) == 0):
			return None
	average_sentiment = 0
	for s in blob.sentences:
		average_sentiment += s.sentiment.p_pos
	return average_sentiment / len(blob.sentences)

def get_sentiment_textblob_NB_weighted(tweet):
	cleaned_tweet = clean_tweet(tweet)
	blob = tb(cleaned_tweet)
	if(len(blob.sentences) == 0):
			return None
	average_sentiment = 0
	total_words = sum(map(lambda x: len(x.split()), blob.sentences))
	for s in blob.sentences:
		average_sentiment += (s.sentiment.p_pos * len(s.split()))
	return average_sentiment / total_words

#The normal textblob algorithm also offers a "subjectivity" score
def get_subjectivity_textblob(tweet):
	cleaned_tweet = clean_tweet(tweet)
	blob = TextBlob(cleaned_tweet)
	if(len(blob.sentences) == 0):
			return None
	average_subjectivity = 0
	#weighted average of sentiment:
	for s in blob.sentences:
		average_subjectivity += s.sentiment.subjectivity
	return average_subjectivity / len(blob.sentences)

#VADER does it's processing by paragraph (not sentence)
def get_sentiment_vader(tweet):
	cleaned_tweet = clean_tweet(tweet)
	return analyzer.polarity_scores(tweet)['compound']


#applies the algorithms we originally used; all the algorithms are applied in test.py
def add_col_w_sentiment(database, table_from, table_to):
	con = db.connect(database)
	c = con.cursor()
	df = pd.read_sql("SELECT * from " + table_from, con)

	df['sentiment_corenlp'] = df['tweet'].apply(get_sentiment_corenlp)
	#df['sentiment_textblob_weighted_average'] = df['tweet'].apply(get_sentiment_textblob_weighted)
	df['sentiment_textblob'] = df['tweet'].apply(get_sentiment_textblob)

	df['subjectivity'] = df['tweet'].apply(get_subjectivity_textblob)

	c.execute("DROP TABLE IF EXISTS %s" % table_to)
	df.to_sql(table_to, con)

	con.close()

def main():
	database = "all_data"
	table_from = 'cc'
	table_to = "sentiment_cc_weighted_average"

	add_col_w_sentiment(database, table_from, table_to)

if __name__ == "__main__":
	main()



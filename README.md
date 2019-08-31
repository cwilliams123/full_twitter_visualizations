# ReadMe for “Twitter Data Analysis to Track the Spread of Ideas”

This is the readme for the twitter sentiment analysis and visualization project conducted by Cori Williams and Grace Fan, under the supervision of Professor Susan Moffit, Cadence Willse, and Professor Ugur Centintemel. It tracks two key phrases: “#commoncore” (AKA cc) and “college and career readiness” (AKA ccr) to analyze how the public opinion on both topics has changed over time and throughout the country. 


Full abstract: 

Our work has focused on the spread of ideas related to instructional practice and content (such as sharing ideas and resources on how to teach math) and the spread of populist ideas about education standards as a vehicle for federal government control of local public schools.  Our analysis has focused on tweets from 2012-2018, using basic text analysis and sentiment analysis to assess the systematic differences between tweets referencing the Common Core (i.e. the Common Core State Standards Initiative in education) and those referencing college and career readiness standards. We have been examining how the former term has become a target and vehicle for populist antipathy and the latter term has become a vehicle for sharing information on.

Link to the live visualization: http://twtr.cs.brown.edu/


Folder Breakdown

Other Scripts: (not used in directly live visualization)
•	Testing 
o	get_all_sentiments.py – Brings in a few new sentiment algorithms to use on sampled data (100 tweets) and normalizes them to a scale of -1 (very negative) to 1 (very positive).
o	get_accuracies: tests the accuracy of each algorithm from get_all_sentiments.py, used to find the best algorithm for the visualization (TextBlob). 
•	extract_hashtags.py – Extracts the 100 most common hashtags from each category of tweets
•	Cleaning Scripts – includes the cleaning scripts for all three data sources and pulls what’s necessary for each of them from the Twitter API (eg full tweet text, retweet count, geotag) as well as cleans up some other pieces
o	Clean_pp.py – Cleans the data collected by the public policy RA from 2016-2018
o	Clean_historical_data.py – Cleans Professor Steve Reiss’ historical data (from 2012-2019)
o	Clean_streamed_data.py – Cleans newly streamed data from this summer
o	The outputs are then analyzed with the various sentiment models and aggregated into the database “all_data”

Server Scripts

•	all_data: database everything is stored in; in the home directory I have this database with all these tables in it as well as all the tables separate as CSV’s; on the github the database file is too large to upload, so only the CSV’s are available.
o	cc / ccr : main tables that everything else either reorganizes or updates;
Some info on a few columns:
	id = id of tweet (we don’t have them for the historical data)
	time_downloaded = this is normally created_at and is really only relevant for the update tables in which we pull data on the tweet periodically
	deleted = whether or not tweet has been deleted from Twitter
	state = any mention of a state taken from the user inputted location
	geo / coordinates = geotag data from Twitter (very rare)
	sentiments = explained in the sentiment analysis section
	source = streamed, public policy, or historical
o	cc/ccr_reorganized : data for each state aggregated by time; sentiments are just averages of the available data for that month; used in heatmap visualization
o	cc/ccr_time_aggregated : data used in sentiment over time graph
o	cc/ccr_sampled : used in testing (see test.py)
o	cc/ccr_with_updates : contains the id, time created and some time-sensitive data (retweet_count, favorite_count, deleted) pulled from Twitter at time_downloaded;
I tried to do this weekly but did not always have time

•	Streaming scripts: 
o	These take data from the database that’s constantly collecting new tweets and upload them to the big database
o	add_new_streamed_data_cc.py – uploads data from common core stream
o	add_new_streamed_data_ccr.py – uploads data from college and career readiness stream
o	cleaning_functions.py, clean_streamed_data.py, and sent_analysis.py are the programs used to clean and process the newly streamed data before it’s uploaded to the main database

•	Updating
o	In the database there’s also tables reserved for keeping track of the features of tweets that change over time (ie number of retweets and favorites) so these scripts update that table
o	Update_functions.py – include the functions used in update_cc and update_ccr that pull the required data and save them to the main table

•	Data organizing
o	Organize_for_heatmap.py – reorganizes data for the two heatmap visualizations
o	Organize_for_overtime_graph.py – reorganizes data for the sentiment over time visualization (aggregates by month for each state)

Explanation of Sentiment Analysis Algorithms:

Sentiment_textblob and subjectivity both come from a python library called texblob, which performs sentiment analysis word by word. The algorithm's pretty basic: it looks up every word and adds it's polarity score (if it exists) to the overall score and averages. If it's a negating word, it'll multiply the next word's score by a negative number. If it's a modifying work (like "very") it's multiply the next word's score by the intensity score of that word. Subjectivity is handled in a similar manner, it basically averages the "subjectivity" score of each word in the sentence. Both algorithms take in sentences as input, so to get the sentiment of the whole tweet, we averaged the sentiments together (with different weights). This model, plus plain averaging across sentences, was the most accurate according to the testing method described below. Textblob also has a feature that will perform Naïve Bayes on a text to find the probability it is positive, this is denoted as “textblob NB.” More info here: 
https://textblob.readthedocs.io/en/dev/quickstart.html

Sentiment_corenlp is from a Stanford natural language processing library called CoreNLP. They use a tree model to represent the sentences and neural networks to output a sentiment score. It also works on the sentence level, so we had to average those to get a full score. I honestly know the least about this library, because it's pretty complicated, but I thought it'd be good to include because it handles sentence structure in a more sophisticated way than the other algorithms. More info here: https://nlp.stanford.edu/sentiment/

VADER also goes word by word, but has more data on emojis and emoticons and other social media/slang specific attributes, as it is built to analyze social media. It takes in paragraphs, so there was no need to average over sentences. It was created by MIT. More info here: https://github.com/cjhutto/vaderSentiment


Testing

I tested the three sentiment analysis algorithms (as well as different weights on each sentence where it applied) to see which was the most accurate to use in the visualizations. I hand labelled 100 tweets on a scale of -1 to 1, picked randomly from each set of data, and then took the absolute value of the differences between my sentiment score and each algorithm’s (normalized) sentiment score. Then I averaged those differences to find which algorithm was closest to the hand labelled data. 

Here are the results of those tests:

College and Career Readiness:
textblob: 0.17603400936447813
textblob weighted*: 0.1870950449017832
textblob NB: 0.5466461398905628
textblob NB weighted*: 0.5635235468496349
textblob corenlp: 1.5675714285714286
vader: 0.406187

Common Core:
textblob: 0.5595773418710919
textblob weighted*: 0.5507194311330924
textblob NB: 0.8811572974088273
textblob NB weighted*: 0.8889673946180687
textblob corenlp: 1.6263333333333336
vader: 0.534081

*weighted = weighted by the number of words in each sentence; these scores were never different enough from the original normal averaging to apply them to the visualization

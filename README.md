# Twitter-Sentiment-Analysis

Problem Statement:
	Sentiment Analysis
	Tweets from a particular topic were taken and an analysis on the sentiment of the respective tweets was done. The topic chosen was 'Article 370'

My Approach:
	This was my first experience with any sort of Machine Learning Project. 
	So, after referring through a lot of medium blogs and tutorials, I got a rough idea as to what to do.

	1. Collect tweets about the given topic
		This required a developer account and corresponding tokens and keys. Using Twitter's restful API, this was easily done.
	
	2.The next task was to build a training set.I took a training DataSet of 10,000 movie reviews.
And a test Data Set of 3000 tweets. The dataset file for the same is attached. Only the required sentiment and the text of the review was stored in a different file tweetdatafile.csv

	3.The next task was to preprocess all tweets/reviews. Using the nltk library functions, stop words were discarded, punctuations, usernames, and hashtags were removed. AND the text was tokenised i.e was split into tokens.

	4.Next task was to build the vocabulary i.e bag of words and form the word feature vectors. 
	5.Using Naive Baye's Classification Algorithm, each token from the test data set is checked with the vector, and a sentiment is assigned based on the same, either high or low.
 
Tools Used: I used google Collab as my environment. Libraries mainly used were nltk , twitter , csv.
Also, generated a wordCloud from these 3000 tweets, after preprocessing them using the wordcloud library. One can get the most frequently used words from the distribution table in the build Vocabulary function.

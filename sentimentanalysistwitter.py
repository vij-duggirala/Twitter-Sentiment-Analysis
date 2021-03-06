# -*- coding: utf-8 -*-
"""SentimentAnalysisTwitter.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ALdQxGbu-HZ1PK1-iK723oWKu3RBcZGZ
"""

import pandas
!pip install python-twitter

import csv
import time

!pip install --user -U nltk

import twitter
! git clone git://github.com/bear/python-twitter.git

!cd python-twitter
!make dev

import twitter
api = twitter.Api(consumer_key='XX4dHeBBBT08WOGDOgi4nvhCp',
                      consumer_secret='wiiYxsWYlRU0FNYBTg3CUlXFdRbs9IzvRjj01F0OcH2fz2oadf',
                      access_token_key='2510807773-QExVZEIM1B7L1JUpPmSKo1a2KV4KwODmbHVW81v',
                      access_token_secret='uam2zq0DDrAbKDcZCth74sIDF2Qqe5mLfXN8g6gWyE5y2')
print(api.VerifyCredentials())

def buildTestSet(search, tid):
    try:
        tweets_fetched = api.GetSearch(search,max_id=tid,  count=100)
        
        print("Fetched " + str(len(tweets_fetched)) + " tweets for the term " + search)
        
        return [{"text":status.text, "label":None, "id":status.id} for status in tweets_fetched]
    except:
        print("Unfortunately, something went wrong..")
        return None

search = input("Enter a search keyword:")
testDataSet=buildTestSet(search, 99999999999999999999)
print(testDataSet[0:4])
testData=[]
for i in range(0,30):
    max=0
    for row in testDataSet:
      testData.append({"text":row["text"],"label":row["label"],"id":row["id"]  })
      tid=row["id"]
      if(tid>max):
          max=tid
    print (tid)
    testDataSet=buildTestSet(search, tid)
    print(testDataSet[0:1])
    
print (testData)
i=0
for row in testData:
  i+=1
print ("Number of tweets fetched on Article 370:")
print (i)

import nltk
nltk.download('stopwords')
nltk.download('punkt')
import re
from nltk.tokenize import word_tokenize
from string import punctuation 
from nltk.corpus import stopwords 

def buildTrainingSet2(corpusFile):
  
    
    corpus = []
    
    with open(corpusFile,'r') as fin:
        lineReader = csv.reader(fin,delimiter='\t', quotechar="\"")
        i=0
        for row in lineReader:
            if(i<10000):
              corpus.append({"tweet_id":row[0], "label":row[1], "text":row[2]})
              print(i)
            else:
              break
            i+=1
    
    trainingDataSet = []
    for tweet in corpus:      
              trainingDataSet.append(tweet)
                            
            
   
    return trainingDataSet
  
corpusFile2="/content/labeledTrainData.tsv"
trainingData2=buildTrainingSet2(corpusFile2)

class PreProcessTweets:
    def __init__(self):
        self._stopwords = set(stopwords.words('english') + ['AT_USER','URL','.',',', '&', ';','\'','\\','\"'])
        
    def processTweets(self, list_of_tweets):
        processedTweets=[]
        for tweet in list_of_tweets:
            processedTweets.append((self._processTweet(tweet["text"]),tweet["label"]))
        return processedTweets
    
    def _processTweet(self, tweet):
        tweet = tweet.lower()
        tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))', 'URL', tweet) 
        tweet = re.sub('@[^\s]+', 'AT_USER', tweet) 
        tweet = re.sub(r'#([^\s]+)', r'\1', tweet) 
        tweet = word_tokenize(tweet) 
        return [word for word in tweet if word not in self._stopwords]

tweetProcessor = PreProcessTweets()
preprocessedTrainingSet = tweetProcessor.processTweets(trainingData2)
preprocessedTestSet = tweetProcessor.processTweets(testData)
print(preprocessedTrainingSet[0:5])
print(preprocessedTestSet[0:5])

def buildVocabulary(preprocessedTrainingData):
    all_words = []
    
    for (words, sentiment) in preprocessedTrainingData:
        all_words.extend(words)

    wordlist = nltk.FreqDist(all_words)
    word_features = wordlist.keys()
    
    return word_features

def extract_features(tweet):
    tweet_words = set(tweet)
    features = {}
    for word in word_features:
        features['contains(%s)' % word] = (word in tweet_words)
    return features

word_features = buildVocabulary(preprocessedTrainingSet)
trainingFeatures = nltk.classify.apply_features(extract_features, preprocessedTrainingSet)
NBayesClassifier = nltk.NaiveBayesClassifier.train(trainingFeatures)

word_features2=buildVocabulary(preprocessedTestSet)
trainingFeatures2=nltk.classify.apply_features(extract_features, preprocessedTestSet)
NBayesClassifier2=nltk.NaiveBayesClassifier.train(trainingFeatures2)



NBayesClassifier.show_most_informative_features(20)

NBResultLabels = [NBayesClassifier.classify(extract_features(tweet[0])) for tweet in preprocessedTestSet]
print("positive:", NBResultLabels.count('1'),"\tNegative:", NBResultLabels.count('0'))
if NBResultLabels.count('1') > NBResultLabels.count('0'):
    print("Overall Positive Sentiment")
else: 
    print("Overall Negative Sentiment")

if NBResultLabels.count('1') > NBResultLabels.count('0'):
    print("Percentage of Positive Tweets:", NBResultLabels.count('1')/(NBResultLabels.count('1')+NBResultLabels.count('0'))*100)
else: 
    print("Percentage of Negative Tweets:", NBResultLabels.count('0')/(NBResultLabels.count('1')+NBResultLabels.count('0'))*100)

from google.colab import drive
drive.mount('/content/drive')

!git clone https://github.com/amueller/word_cloud.git

# Commented out IPython magic to ensure Python compatibility.
# %cd word_cloud
!pip install .

!pwd

import numpy as np
import pandas as pd
from os import path
from PIL import Image
from wordcloud import WordCloud,ImageColorGenerator
import matplotlib.pyplot as plt

i=0
for tweet in preprocessedTestSet:
  print(tweet[0])
  i+=1
  print(i)

b = [i for sub in preprocessedTestSet for i in sub[0]]
print (b)
text=",".join(b)
print (text)

mask=np.array(Image.open("/content/ind.png"))

print(mask)

def transform_format(val):
    if val == 0:
        return 255
    else:
       return val
#trans_mask = np.ndarray((mask.shape[0],mask.shape[1]), np.int32)
#for i in range(len(mask)):
#    trans_mask[i] = list(map(transform_format, mask[i]))  
wordcloud=WordCloud(background_color="white", mode="RGBA", max_words=3000, mask=mask).generate(text)



image_colors=ImageColorGenerator(mask)
plt.figure(figsize=[7,7])
plt.imshow(wordcloud.recolor(color_func=image_colors), interpolation="bilinear")
plt.axis("off")

plt.savefig("wordcloud.png", format="png")
plt.show()

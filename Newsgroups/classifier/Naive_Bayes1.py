import re
import numpy as np 
import pandas as pd 

from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import LabelEncoder

import pickle


def normalize_text(s):
    s = s.lower()
    
    # remove punctuations
    s = re.sub('\s\W',' ',s)
    s = re.sub('\W\s',' ',s)
    
    # no double spaces
    s = re.sub('\s+',' ',s)
    
    return s

def train_model(input_data):
	# get data
	news = pd.read_csv(input_data)
	news['TEXT'] = [normalize_text(s) for s in news['TITLE']]

	# makes whole words lowercase, removes duplicates, and removes single word characters
	vectorizer = CountVectorizer()
	x = vectorizer.fit_transform(news['TEXT'])

	encoder = LabelEncoder()
	y = encoder.fit_transform(news['CATEGORY'])

	# split into train and test sets
	x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)

	# Naive Bayes Classifier
	nb = MultinomialNB()
	nb.fit(x_train, y_train)

	model = open('../Models/naive_bayes1.pickle', 'wb')
	pickle.dump(nb, model)
	pickle.dump(vectorizer, model)
	model.close()

	print(nb.score(x_test, y_test))

	# predictions = nb.predict(x_test)

	# These are which words are characteristic of each category
	# coefs = nb.coef_
	# print(coefs.shape)
	# print(coefs)


if __name__ == '__main__':
	Train_Data = "../TrainingData/uci-news-aggregator.csv"
	train_model(Train_Data)





Detect bias in articles with machine learning

Dataset: https://www.kaggle.com/snapcrack/all-the-news


Description
===========
Trained to recognize opinions, sentiment, bias in news articles


Outline:
=======
1. Process the data, extract features of interest
2. Implement multilayer perception that takes n grams
3. Figure out how to parse out keywords, significant phrases, get rid of rest. 





Application to Stocks
=====================
Use a web scraper to get news articles for each of the stocks in the S&P 500 over a few years, and for each news article we can label the sentiment by running our stocktool scripts to see how the stock changed in the days around the date of publication. After we successfully label the effect/sentiment of each news article, we can run text classification on that training set to teach an algorithm how to predict it

For stock market, maybe use SEC 8-K dataset instead of news dataset
https://towardsdatascience.com/using-nlp-and-deep-learning-to-predict-the-stock-market-64eb9229e102
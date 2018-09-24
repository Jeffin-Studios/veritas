import re
import pickle
from sklearn.feature_extraction.text import CountVectorizer

def normalize_text(s):
    s = s.lower()
    
    # remove punctuations
    s = re.sub('\s\W',' ',s)
    s = re.sub('\W\s',' ',s)
    
    # no double spaces
    s = re.sub('\s+',' ',s)
    
    return s

file = open("../Models/naive_bayes1.pickle", "rb")
classifier = pickle.load(file)
vectorizer = pickle.load(file)
file.close()

# This classifier is now deserialized, so we can use it as an object, just as before
headline = ["Crisis in the White House: Trump Rejects Vital Government Healthcare Bill.", "Apple Company Stock Rises, Good Market in Tech Industry"]
headline = [normalize_text(s) for s in headline]
# makes whole words lowercase, removes duplicates, and removes single word characters
x = vectorizer.transform(headline)

label = classifier.predict(x)

print(label)


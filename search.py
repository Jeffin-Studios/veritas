from googlesearch import search
import requests as req
import re
from lxml import html
from bs4 import BeautifulSoup

query = "NIO Stock Rating"

def fetch(query):
	results = []
	for result in search(query, tld="co.in", num=10, stop=1, pause=2): 
		results.append(result)

	resp = req.get(results[0])
	content = resp.text 
	stripped = re.sub('<[^<]+?>', '', content)

	file = open('test.txt','w') 
	file.write(stripped) 
	file.close() 
	return results

def fetch2(query):
	results = []
	file = open('test.txt','w') 
	for result in search(query, tld="co.in", num=1, stop=1, pause=2): 
		results.append(result)
		resp = req.get(result)
		content = BeautifulSoup(resp.content, 'html.parser')
		for i, p in enumerate(content.select('p')):
			file.write(p.text) 

	file.close() 
	return results


def verify(url):
	# Determines if source is credible and recent. Discards those that do not meet criteria
	return

if __name__ == '__main__':
	query = "NIO Stock Rating"
	fetch2(query)



# from googlesearch.googlesearch import GoogleSearch
# response = GoogleSearch().search("NIO Stock Rating")
# for result in response.results:
#     print("Title: " + result.title)
#     print("Content: " + result.getText())
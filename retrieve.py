from googlesearch import search
query = "NIO Stock Rating"
  
for result in search(query, tld="co.in", num=10, stop=1, pause=2): 
    print(result) 


# Determines if source is credible and recent. Discards those that do not meet criteria
# def filter():


# from googlesearch.googlesearch import GoogleSearch
# response = GoogleSearch().search("NIO Stock Rating")
# for result in response.results:
#     print("Title: " + result.title)
#     print("Content: " + result.getText())
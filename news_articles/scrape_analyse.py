import time

import requests
from bs4 import BeautifulSoup
from analyzer import Analyzer



Base_url = "http://www.moneycontrol.com"

# Build a dictionary of companies and their abbreviated names
companies = { 'cadilahealthcare': 'CHC', 'piramalenterprises': 'PH05',
             'glenmarkpharma': 'GP08', 'glaxosmithklinepharmaceuticals': 'GSK',
             'sunpharmaceuticalindustries': 'SPI', 'lupinlaboratories': 'LL',
             'cipla': 'C', 'aurobindopharma': 'AP',
             'drreddyslaboratories': 'DRL', 'divislaboratories': 'DL03'}

# Create a list of the news section urls of the respective companies
master_list =[]

for k, v in companies.items():
    url = 'http://www.moneycontrol.com/company-article/{}/news/{}#{}'.format(k, v, v)
    company = k
    abbr = v
    master_list.append({"coy":k, "abbr": v, "url":url})

print(master_list)
# Create an empty list which will contain the selected news articles
List_of_links = []

# Extract the relevant news articles weblinks from the news section of selected companies
for item in master_list:
   html = requests.get(item['url'])
   # Create a BeautifulSoup object
   soup = BeautifulSoup(html.text, 'html.parser')

   # Retrieve a list of all the links and the titles for the respective links
   word1, word2, word3 = "US", "USA", "USFDA"

   sub_links = soup.find_all('a', class_='arial11_summ')
   for links in sub_links:
      # first convert into a string
      sp = BeautifulSoup(str(links), 'html.parser')
      tag = sp.a
      if word1 in tag['title'] or word2 in tag['title'] or word3 in tag['title']:
          category_links = Base_url + tag["href"]
          List_of_links.append({'coy': item['coy'], 'link':category_links})
          time.sleep(3)

# Print the select list of news articles weblinks
#final_list = list(set(List_of_links))

data = []
analyzer = Analyzer()

for item in List_of_links:
    res = requests.get(item['link'])
    soup = BeautifulSoup(res.content, 'lxml')
    article = soup.find("div", {"class": "arti-flow"})
    if article:
        content = article.find_all('p')
        lines = [item.text for item in content]
        paragraph = ' '.join(lines)
        vader_score = analyzer.vader_analyze(paragraph)
        corpus_score = analyzer.analyze(paragraph)
        #print("{:-<40} {}".format(link, str(vader_score)))
        #print(vader_score['compound'])
        data.append({"coy": item['coy'], "neg":vader_score['neg'],"neu":vader_score['neu'],"pos":vader_score['pos'],"compound":vader_score['compound'], "corpus":corpus_score})
    else:
        print("No article")
        continue

for entry in data:
    print(entry)





import urllib2
from bs4 import BeautifulSoup as soup
import requests, json, os 
import  re
import csv
from datetime import datetime
from elasticsearch import Elasticsearch




url = 'https://health.usnews.com/doctors/city-index/new-jersey'

page = requests.get(url,headers={'User-Agent':'Mozilla/5.0'})

#html parser
data = page.text
html_soup = soup(data,"html.parser")
containers =  html_soup.findAll("li",{"class":"index-item"})

links_list_city = [ ]
doctors_list = [ ]

##Below will give the  links of cities and name of the cities in New-Jersey

for i in containers:
	city_name =i.a.text.strip().lower().replace(' ','-')
	
	links_cities  = i.a['href']
	links = 'https://health.usnews.com'+'/'+links_cities
	links_list_city.append(links)
# ###################################Converting to text##############################################################
#         with open('Data.txt', 'a') as the_file:
#              the_file.write(city_name+ "\n")
#	print(city_name)

##################################implementing elasticsearch############################################################

res = requests.get('http://localhost:9200')
print (res.content)
es = Elasticsearch([{'host': 'localhost', 'port': '9200'}])

i = 1

for filename in ("Data.json"):
	f= open("Data.json")
	docket_content = f.read()

es.index(index='us_news', ignore=400, doc_type='docket', id=i, body=json.loads(docket_content))

i = i + 1



	
for i in links_list_city:
	url2 = requests.get(i,headers={'User-Agent':'Mozilla/5.0'})
	data_links = url2.text
	html_soup2 = soup(data_links,"html.parser")
	find_links = html_soup2.findAll("li",{"class":"index-item"})

	for k in find_links:
	 	doctor_name = k.a.text.strip().lower().replace(' ','-')
		links_connect = k.a['href']
		links2 = links_connect.replace("specialists-index",links_connect)
	 	links3 = 'https://health.usnews.com' + links2 
		doctors_list.append(links3)



    ################################
		#print (doctors_list)

with open('Data2.txt', 'a') as the_file:
	the_file.write(doctor_name+ "\n")



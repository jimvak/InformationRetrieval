from elasticsearch import Elasticsearch, helpers

import csv

#sindesi me tin elasticsearch
es = Elasticsearch(host = "localhost", port = 9200)

#anoigma tou arxeiou csv gia diavasma
with open('BX-Books.csv', encoding = 'utf8') as f:
   #diavazetai to periexomenou tou arxeiou 
    reader = csv.DictReader(f)
    #anevasma tou arxeio stin elasticsearch kai dimiouegeitai to index me to onoma 'evretirio'
    helpers.bulk(es, reader, index='evretirio')
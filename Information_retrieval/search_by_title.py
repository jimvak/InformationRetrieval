from elasticsearch import helpers, Elasticsearch
import csv

#sindesi me tin elasticsearch
es=Elasticsearch([{'host':'localhost','port':9200}])


#dinoume titlo tou vivliou
x=input("Enter a book title: ")


#edo ektelei to query to opoio kanei matching me ton titlo

#sto res apothikevontai ta apotelesmata pou epsitrefei i mixani 
res= es.search(index='evretirio',body={'query':{'match':{'book_title':x}}})

#sto all results krataei ta apotelesmata pou exoun epistrafei (mono ayta ta opoia xreiazomaste)
all_results = res['hits']['hits']


#diatrexoume ta apotelesmata
for  i in range(len(all_results)):
    
    #ektyponoume tis plirofories
    print(all_results[i]['_source'])

    #ektyponoume to score pou exei dosei to elasticsearch
    print("Score: "+str(all_results[i]['_score']))
    



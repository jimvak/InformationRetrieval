from gensim.models import word2vec
import csv
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split

from sklearn.cluster import KMeans

import matplotlib.pyplot as plt

from sklearn import preprocessing 

import math

#anoigoume to arxeio Books.csv gia diavasma
mydata = pd.read_csv('BX-Books.csv')

#edo kratao tis perilipseis twn vivliwn
summaries= mydata['summary']


#edo krataw ta isbns twn vivliwn
isbns = mydata['isbn']

#apo kai sto eksis efarmozetai mia diadikasia i opoia 

#exei efarmostei kai se proigoumena erotimata 

#efarmozoume diadikasia vectorization panw sta summaries twn vivliwn 

summary_split=[]

#lista apo listes ( kathe epimrous lista periexei tous orous tis perilipsis)
for summary in summaries:
    summary_split.append(str(summary).split())
    
model = word2vec.Word2Vec(summary_split, min_count=1)

summary_vectors= []

final_summaries = []

for j in range(len(summary_split)):
    vector_summary = []
    for y in summary_split[j]:
        vector_summary.append(model.wv[y])
    summary_vectors.append(vector_summary)
    
for x in summary_vectors:
    final_summaries.append(np.average(x, axis=0))
    
    
final_summaries = np.array(final_summaries)

#kanoume normalize ta data etsi wste na leitourgei me omoiomotita

#sinimitonou o kmeans ( mathimatika apodedeigmeno)

final_summaries = preprocessing.normalize(final_summaries)

#edo trexei o kmeans, o opoios dimiouegei 10 clusters apo vivlia

kmeans = KMeans(n_clusters=10, init='random').fit(final_summaries)

#lista apo listes ( kathe lista tha periexei to isbn tou vivliou kai to id tou cluster)
clustered_books = []

#gia kathe ena apo ta apotelesmata 
for i in range(len(kmeans.labels_)):

   #dmiourgoume mia temp lista
    temp_list = []
    #mpainei to isbn
    temp_list.append(isbns[i])
    
    #mpainei to id tou cluter 
    temp_list.append(kmeans.labels_[i])
    
    #enimeronetai i teliki lista 
    clustered_books.append(temp_list)
    
####################################################################
#apo edo kai pera ginetai to cluster twn users me vasi ta dimografika 

#tous xaraktiristika

#anoigoume to arxeio me ta stoixeia twn xristwn gia diavasma
mydata = pd.read_csv('BX-Users.csv')


#edo kratame ta ids twn xristwn
user_id = mydata['uid']

#edo kratame to location twn xristwn
user_location = mydata['location']

#edo kratame tin ilikia twn xristwn 
user_age = mydata['age']

#apo edo kai sto eksis  efarmozetai diadikasia vectorization panw 

#sta locations 

location_split=[]

for location in user_location:
    location_split.append(str(location).split())
    
model = word2vec.Word2Vec(location_split, min_count=1)

location_vectors= []

final_locations = []


for j in range(len(location_split)):
    vector_location = []
    for y in location_split[j]:
        vector_location.append(model.wv[y])
    location_vectors.append(vector_location)
    
for x in location_vectors:
    final_locations.append(np.average(x, axis=0))
    
    
final_locations = np.array(final_locations)

#edo dimiourgeitai to input gia ton kmeans 
final_input = []

for i in range(len(final_locations)):
    temp_list = []
    #edo mpainei to id tou xristi 
    temp_list.append(user_id[i])
    
    #meta mpainei i ilikia(kai an i ilikia den einai simpliromeni tote mpainei i timi 0)
    if math.isnan(user_age[i]):
        temp_list.append(0)
    else:
     #diaforetika mpainei kanonika i timi tis ilikias
        temp_list.append(user_age[i])
    
    #mpainoun ta stoixeia tou dianismatos pou antistoixei sto location 
    for x in final_locations[i]:
        temp_list.append(x)
     
    #enimeronetai i teliki lista
    final_input.append(temp_list)
    
    #i lista ginetai np.array gia na mporei na dothei san eisodos ston kmeans 
final_input = np.array(final_input)

#kanonikopoihsh gia na mporei na leitoyegei o kmeans me omoiothta sinimitonou 
final_input = preprocessing.normalize(final_input)

#trexei o kmeans ( 5 clusters gia tous xristes)
kmeans = KMeans(n_clusters=5, init='random').fit(final_input)

# i lista apo listes(kathe lista tha periexei to user id kai to id tou cluster sto opoio anikei o xristis)
clustered_users = []

#gia ola ta apotelesmata 
for i in range(len(kmeans.labels_)):
    temp_list = []
    
    #mpainei to user id
    temp_list.append(user_id[i])
    #mpainei to id tou cluster tou user
    temp_list.append(kmeans.labels_[i])
    clustered_users.append(temp_list)
    

#anoigoume to arxeio me tis vatmolohies 
mydata = pd.read_csv('short.csv')

#ta ids twn users
uid = mydata['uid']

#ta isbns twn vivliwn
isbn = mydata['isbn']


#oi vathmologies 
rating = mydata['rating']


mylist = []


#ftiaxnoume mia lista apo 50 4 ades 

#kathe tetrada tha periexei:
    
#to id tou cluster twn xristwn

#to id tou cluster twn vivliwn

#to athroisma twn vathmwn pou exoun dothei apo tous xristes tou cluster

#sta vivlia tou cluster

#to plithos twn vathmwn


#arxikopoiume tis 4 -ades (kathe mia exei 4-midenika mesa)
for i in range(5):
    for j in range(10):
        temp_list=[]
        temp_list.append(0)
        temp_list.append(0)
        temp_list.append(0)
        temp_list.append(0)
        mylist.append(temp_list)

#tha vroume gia kathe cluster xristwn tin mesi vathmologia 

#pou exei dosei gia kathe cluster vivliwn

#gia kathe enan apo tous clustered users
for i in range(len(clustered_users)):
    #gia kathe ena apo ta clustered books
    for j in range(len(clustered_books)):
        #gia kathe eggrafi tou pinaka me tis vathmologies
        for k in range(len(mydata)):
            #an vroume to user_id kai to isbn tou vivliou
            if clustered_users[i][0] == uid[k] and clustered_books[j][0] == isbn[k]:
                #vriskoume to cluster tou user
                x = clustered_users[i][1]
                #vriskoume to cluster tou book
                y = clustered_books[j][1]
                
                #edo mpainei to id tou cluster tou user
                mylist[x+y][0] = x
                
                #edo mpainei to id tou cluster tou vivliou
                mylist[x+y][1] = y
                
                #edo ayksanetai i vathmologia
                mylist[x+y][2] = mylist[x+y][2]+rating[k]
                
                #ayksanoume to plithos kata 1
                mylist[x+y][3] = mylist[x+y][3]+1
                
    
#lista pou tha apoteleitai apo ypolistes tis morfis

#id cluster twn users

#id cluster twn books

#mesi vathmologia pou exei dothei
mo_final=[]

#ypologismos twn meswn orwn
for i in range(len(mylist)):
    #ypologizetai o mesos oros
    mo = mylist[i][2]/mylist[i][3]
    #mpainei to id tou cluster twn users
    mo_final.append(mylist[i][0])
    #mpainei to id tou cluster twn books
    mo_final.append(mylist[i][1])
    
    #teleytaios mpainei o mesos oros 
    mo_final.append(mo)

from gensim.models import word2vec

from elasticsearch import helpers, Elasticsearch
import csv
import pandas as pd

import numpy as np

from keras.models import Sequential

from keras.layers import Dense

from sklearn.model_selection import train_test_split

from elasticsearch import helpers, Elasticsearch
import csv

import pandas as pd

#sindesi me tin elasticsearch
es=Elasticsearch([{'host':'localhost','port':9200}])

#diavasma tou csv
mydata = pd.read_csv('BX-Books.csv')

#edo diatiroume ta summaries olwn twn vivliwn 
summaries= mydata['summary']

#edo diatiroume ta isbns olwn twn vivliwn
isbns = mydata['isbn'].to_numpy()


#apo edo kai kato ksekinaei i diadikasia tou word embedding,
#etsi oste na metatrpsume tis perilipseis se dianysmata ( vectors)

#voithiki lista 
summary_split=[]


#lista apo listes ( kathe epimrous lista periexei tous orous tis perilipsis)
for summary in summaries:
    #xrisimopoioume tin split etsi wste na spasoume tis tis perilipseis se lekseis 
    summary_split.append(str(summary).split())
 
#dimiourgeitai to modelo word2vec  
model = word2vec.Word2Vec(summary_split, min_count=1)


#anoigoume to short.csv ( mia short ekdoxi tou arxeiou me tis vathmologies)

book_ratings= pd.read_csv('short.csv')

#kratame ta user_ids
book_ratings_uid= book_ratings['uid'].to_numpy()

#ta isbns
book_ratings_isbn= book_ratings['isbn'].to_numpy()


#ratings
book_ratings_rating= book_ratings['rating'].to_numpy()

summary_vectors = []

final_uids = []

final_ratings = []


#gia kathe ena apo ta isbns pou exoun vathmologithei
for i in range(len(book_ratings_isbn)):
    #gia kathe ena apo ta isbns sto arxeio books.csv
    for j in range(len(isbns)):
        #an taytizontai ta isbns
        if book_ratings_isbn[i]==isbns[j]:
        
           #exo ta dianismata olwn twn leksewn tis trexousa perilipsis
            vector_summary = []
            #gia kathe leksi tis perilipsis tou vivliou
            for y in summary_split[j]:
            
              #prostheto sto vector summary to vector pou antistoixei stin leksi tis perilipsis
                vector_summary.append(model.wv[y])
                
             # mpainei stin teliki lista, i opoia tha periexei tis listes twn dianismatwn olwn twn perilipsewn
            summary_vectors.append(vector_summary)
            #se ksexoristi lista mpainei to id tou xristi
            final_uids.append(book_ratings_uid[i])
            #se ksexoristi lista mpainei i vathmologia 
            final_ratings.append(book_ratings_rating[i])

final_summaries=[]

#epeidi kathe perilipsi exei diaforetiko plithos leksewn

#vriskoume ton meso oro twn dianismatwn pou antistoixo se

#kathe perlipsi

#etsi gia kathe perilipsi tha vgei telika ena dianysma 

#to opoio tha einai twn 100 thesewn

for x in summary_vectors:

    final_summaries.append(np.average(x, axis=0))    
                

#to final input gia to nevroniko 
final_input=[]

#to final output gia to nevroniko
final_output=[]

#diatrexoume tin final_summaries 
for i in range(len(final_summaries)):

    #dimiourgoume mia prosorini lista
    temp_list =[]
    #mpainei to id tou user
    temp_list.append(final_uids[i])
    
    #mpainoun kai ta 100 stoixeia tou dianismatos tis perilipsis
    for k in final_summaries[i]:
        temp_list.append(k)
    
    #enimeronetai i teliki lista
    final_input.append(temp_list)
    
    #sto output mpainei i vathmologia
    final_output.append(final_ratings[i])

#metatropi twn listwn se arrays gia na mporoun

#na dothoun san eisodoi sto nevroniko diktyo

final_input = np.array(final_input)


final_output =  np.array(final_output)


#diaxorismos tou siniolikou dataset se train kai test  set 

#75 % trainset   25 % test set

X_train, X_test, y_train, y_test = train_test_split(final_input, final_output, test_size=0.25)

#dimiourgeitai to nevroiniko diktyo
nevroniko = Sequential()

#to input dim prepei na einai 101 ( 100 stoixeia gia tin perilipsei + 1 gia to gia to user_id)
nevroniko.add(Dense(12, input_dim=101, activation='relu'))
nevroniko.add(Dense(101, activation='relu'))
nevroniko.add(Dense(1, activation='sigmoid'))

nevroniko.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])


#to nevroniko diktyo ekpaidetrai me vasi to X_train kai to y_ytain 
nevroniko.fit(X_train, y_train, epochs=20)

#etsi oste na mporei na mas provlepei tis vathmologies pou leipoun

#(tha klithei  i predict argotera  otan xreiastei)

######################################################


#idios kodikas me question2 me kapoies parallages gia na mporoun na ginoun predict 

#oi vathmologies pou leipoun
x=input("Enter a book title: ")


#dinoume ena user_id

user_id = int(input("Enter a user id:"))


#dinoume ta vari 
a = float(input("Give weight of user ratings :"))

b = float(input("Give weight of elastic_search ratings :"))

c = float(input("Give weight of average ratings :"))



#edo ektelei to query to opoio kanei matching me ton titlo
res= es.search(index='evretirio',body={'query':{'match':{'book_title':x}}})

#sto all results krataei ta apotelesmata pou exoun epistrafei
all_results = res['hits']['hits']


result_isbns = []

result_scores = []

result_summaries = []

#diatrexoume ta apotelesmata gia na perasoume stis 2 listes 

#ta apotelesmata pou theloume 
for  i in range(len(all_results)):
    
    result_scores.append(all_results[i]['_score'])

    result_isbns.append(all_results[i]['_source']['isbn'])
    
    result_summaries.append(all_results[i]['_source']['summary'])
    
#edo prepei na kanoume vectorization twn perilipsewn pou exoun epistrafei


#voithitikes listes 
summary_result_split=[]

summary_result_vectors = []

final_result_summaries = []



#kano tin idia diadikasia pou ekana kai prin, alla mono gia tis perilipseis twn vivliwn pou exoun epistrafei
for summary in result_summaries:
   #kalo tin split gia na paro tis lekseis twn perilipsewn 
    summary_result_split.append(str(summary).split())

#edo dimiourgo to summary_result_vectors, to opoio periexei tis listes twn dianismtwn gia kathe leksi 
for j in range(len(summary_result_split)):
    vector_summary = []
    for y in summary_result_split[j]:
        vector_summary.append(model.wv[y])
    summary_result_vectors.append(vector_summary)
  


#pairno ton meso oro , gia na antimetopiso to provlima tou diadoreikou plithos leksewn twn perilipsewn  
for x in summary_result_vectors:

    final_result_summaries.append(np.average(x, axis=0)) 

#i final_result_summaries einai mia lista apo 100ades, opou kathe 100ada antistoixei se mia apo tis perilipseis
#twn vivliwn pou exoun epistrafei 

user_scores = []

average_scores = []

final_scores = []

for i in range(len(all_results)):
    user_scores.append(0)
    average_scores.append(0)
    final_scores.append(0)


#vathmologies pou exei valei o xristis gia kathe ena apo ta vivlia pou exoun

#epistrafei 

#kai mesos oros vathmologias twn bibliwn pou exoun epistrafei

#gia kathe epistrefomeno vivlio
for i in range(len(all_results)):
    book_sum=0
    book_count=0
    #gia kathe vathmologia pou exei dothei sinolika
    for j in range(len(book_ratings)):
    
      #exo mia metavliti pou leitourgei os flag 
      #gia na me enimeroni an o xristis exei vathmologisei to vivlio i oxi 
        flag = 0
        #taysisi tou id tou xristi kai tou isbn tou vivlvuou
        if user_id == book_ratings_uid[j] and result_isbns[i] == book_ratings_isbn[j]:
            #mpainei to antistoixo score
            user_scores[i] = book_ratings_rating[j]
            
            #an to exei vathmologisei tote to flag ginetai iso me to 1
            flag=1
        
        
        if result_isbns[i]==book_ratings_isbn[j]:
            book_sum = book_sum + book_ratings_rating[j]
            book_count = book_count+1
            book_average_rating = book_sum/book_count
            
            if book_count ==0:
                average_scores[i]=0
            
            else:
                average_scores[i]=book_sum/book_count
    
    #ean den exei vathmologisei o user to vivlio 
    
    #tote prepei na kanei predict to nevroniko diktyo
    if flag==0:
    
       #ftiaxnw mia temo lista
        temp_list = []
        
        #prota mpainei to user_id 
        temp_list.append(user_id)
        
        #mpainoun ta 100 stoixeia tou dianismatos tis perilipsis 
        for x in final_result_summaries[i]:
            temp_list.append(x)
        
        
        #kanoume reshape tin pliroforia gia na mporei na ginei apodekti sto 
        
        #nevroniko diktyo 
        final_test = np.array(temp_list)
        
        final_test = final_test.reshape(1,101)
        
        #!!!!!!!edo ginetai to predict etsi wste na provlefthei i vathmologia pou tha edine o sigkekrimenos 
        
        #user sto sigkekrimeno vivlio 
        user_scores[i]=nevroniko.predict(final_test)
        
    
    #ypologismos newn score twn vivliwn
    final_scores[i] = a*user_scores[i] + b*result_scores[i] + c*average_scores[i]
    print(all_results[i]['_source'])
    #ektyponoume to neo scoreo pou ypologistike
    print("Updated Score: "+str(final_scores[i]))
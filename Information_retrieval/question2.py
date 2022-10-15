from elasticsearch import helpers, Elasticsearch
import csv
import pandas as pd
es=Elasticsearch([{'host':'localhost','port':9200}])

#edo ginetai to diavasma tou csv arxeioy me tis aksiologiseis 
book_ratings= pd.read_csv('BX-Book-Ratings.csv')

#edo kratame ta user ids
book_ratings_uid= book_ratings['uid'].to_numpy()

#edo ta isbns twn vivliwn pou exoun vathmologithei
book_ratings_isbn= book_ratings['isbn'].to_numpy()

#edo kratame tis vathmologies 
book_ratings_rating= book_ratings['rating'].to_numpy()


#dinoume titlo
x=input("Enter a book title: ")


#dinoume ena user_id

user_id = int(input("Enter a user id:"))

#dinoume to varos pou theloume na exoyn oi vathmologies tou xristi 
a = float(input("Give weight of user ratings :"))

#dinoume to varos po tha exoun oi vathmologies tis mixanis
b = float(input("Give weight of elastic_search ratings :"))

#dinoume to varos pou tha exei i mesi vathmologia twn xristwn 
c = float(input("Give weight of average ratings :"))



#edo ektelei to query to opoio kanei matching me ton titlo
res= es.search(index='evretirio',body={'query':{'match':{'book_title':x}}})

#sto all results krataei ta apotelesmata pou exoun epistrafei
all_results = res['hits']['hits']


#ayti i lista tha periexei ta isbns twn vivliwn pou exei epistrepsei i mixani
result_isbns = []

#ayti i lista tha periexei ta scores twn vivliwn pou exei epistrepsei i mixani
result_scores = []

#diatrexoume ta apotelesmata gia na perasoume stis 2 listes 

#ta apotelesmata pou theloume 
for  i in range(len(all_results)):
    
    #edo mpainoun ta scores
    result_scores.append(all_results[i]['_score'])

    #edo mpainoun ta isbs twn vivliwn
    result_isbns.append(all_results[i]['_source']['isbn'])
    

# i lista i opoia tha krataei tis vathmologies tou xristi gia ta vlivlia pou exoyn epistrafei
user_scores = []

#i lista i opoia tha periexei tin mesi vathmologia twn xristwn gia ta vivlia pou exoyn epistrafei
average_scores = []

# i lista pou tha periexei ta telika score 
final_scores = []

#arxikopoume tis listes aytes kai pantou pername to 0
for i in range(len(all_results)):
    user_scores.append(0)
    average_scores.append(0)
    final_scores.append(0)



#vathmologies pou exei valei o xristis gia kathe ena apo ta vivlia pou exoun

#epistrafei 

#kai mesos oros vathmologias twn vivliwn pou exoun epistrafei

#gia kathe epistrefomeno vivlio
for i in range(len(all_results)):
   #to athroisma twn vathmologiwn
    book_sum=0
    #to plithos twn vathmologiwn
    book_count=0
    #gia kathe vathmologia pou exei dothei sinolika
    for j in range(len(book_ratings)):
        #taysisi tou id tou xristi, kai tou isbn tou vivliou
        if user_id == book_ratings_uid[j] and result_isbns[i] == book_ratings_isbn[j]:
            #mpainei to antistoixo score stin antistoixi thesi tou user_scores
            user_scores[i] = book_ratings_rating[j]
        #edo ginetai o ypologismos tis mesis vathmologias tou vivliou apo olous tous xristes
        if result_isbns[i]==book_ratings_isbn[j]:
        
           #edo ypologizetai ro athroisma twn vathmologiwn
            book_sum = book_sum + book_ratings_rating[j]
            
            #edo to plithos twn vathmologiwn
            book_count = book_count+1
            
            #edo ypologizetai i mesi vathmolgia gia to vivlio
            book_average_rating = book_sum/book_count
            
            #an den to exei vathmologisei kaneis 
            if book_count ==0:
            #diatiro tin timi sto miden 
                average_scores[i]=0
            
            else:
            #diaforetika vazw stin stin antistoixi thesi ton meso oro pou upologisa
                average_scores[i]=book_sum/book_count
        
    #ypologismos newn score twn vivliwn
    final_scores[i] = a*user_scores[i] + b*result_scores[i] + c*average_scores[i]
    
    #ginetai i ektiposi twn pliroforiwn tou vivliou 
    print(all_results[i]['_source'])
    #ektyponoume to neo scoreo pou ypologistike
    print("Updated Score: "+str(final_scores[i]))
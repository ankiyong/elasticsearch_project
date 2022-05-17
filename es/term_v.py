# from errno import EL
import re
from argon2 import verify_password
from elasticsearch import Elasticsearch,helpers
from pyrsistent import b
import pymysql
import csv

reversed_char = ["+","-","=","&&","||",">","<","!","(",")","{","}","[","]","^",'"',"~","*","?",":","\\","/"]
input = input("검색어를 입력하세요 : ")
for i in reversed_char:
    if i in input:
        print("a")
    else:
        print("b")

es = Elasticsearch("http://192.168.219.196:9200")
# input = input("검색어를 입력하세요 : ")
body = {
    "query" : {
        "query_string" : {
            "default_field" : "title",
            "query" : input
        }
    }
}


# if 
# res = es.search(index="news",body=body)
# print(res)


# body = {
#     "fields" : ["title","text"],
#     "filter" : {
#         "min_word_length" : 2   
#     }
# }



# keywords = []
# for num in range(1,9991):
#     keyword = es.termvectors(index="news_title_auto",id=num,body=body)["term_vectors"]["title"]["terms"].keys()
#     for k in keyword:
#         keywords.append(k)
# print(keywords)




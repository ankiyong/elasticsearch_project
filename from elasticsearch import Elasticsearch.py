from elasticsearch import Elasticsearch
import pymysql

es = Elasticsearch(
    ['https://elastic:123456@192.168.219.141:9200'],

    # # turn on SSL
    # use_ssl=True,
    # # make sure we verify SSL certificates
    # verify_certs=True,
    # # provide a path to CA certs on disk
    # ca_certs='C:\python\ca.p12'


    # SSL을 사용하지만 인증서를 확인하지 않는 설정
    # turn on SSL
    use_ssl=True,
    # no verify SSL certificates
    verify_certs=False,
    # don't show warnings about ssl certs verification
    ssl_show_warn=False
)


print(es.indices.exists(index="news"))


# ## 뉴스 수집시 사용한 검색어(query 필드)
# with open('C:/python/news_query_list.txt', "r") as f:
#     query_lst = f.readlines()

# f.close()

# ## 집계 쿼리
# word_lst = []
# shingle_lst = []

# for query in query_lst:


query = {
    "query": {
        "match_all": {}
    }
}

ids = es.search(index='news', body = query)['hits']['total']['value']
print(ids)
print(type(ids))

mbody ={
  "ids": [str(i) for i in range(1, 10)],
  "parameters": {
    "fields": [
      "title", "text"
    ],
    "offsets" : False,
    "positions" : False,
    "term_statistics" : False,
    "field_statistics" : False,
    "filter": {
    "min_word_length": 2
  }
  }
}

mterm = es.mtermvectors(index='news', body=mbody)



keywords = [] #결과값을 담을 list 선언
for i in mterm['docs']:
    keys = [keys for keys in i['term_vectors']['title']['terms'].keys()] #for 문을 사용해서 json으로 반환된 결과값에서 필요한 단어 값을 dict 형태로 추출한 후 key 값만 남김
    for k in keys: #list로 반환된 key 값들을 list에 저장
        keywords.append(k)        
print(keywords)





conn = pymysql.connect(host='192.168.219.141', #mysql에 접근할 때 필요한 파라미터
                       user='root',
                       password='MySQL2022!',
                       db='article',
                       charset='utf8')


curs = conn.cursor()
sql = "insert into auto_table (auto) values (%s)" #id값은 auto_increment 처리 해두고 

for line in keywords:
    curs.execute(sql,(line))
#for line in rd:
 #   curs.execute(sql, (line[0],line[1],line[2],line[3]))
    
conn.commit()
conn.close()
#f.close
    

'''
import requests
from pandas import DataFrame
from bs4 import BeautifulSoup
import re
from datetime import datetime
import os

date = str(datetime.now())
date = date[:date.rfind(':')].replace(' ', '_')
date = date.replace(':','시') + '분'



query = input('검색 키워드를 입력하세요 : ')
news_num = int(input('총 필요한 뉴스기사 수를 입력해주세요(숫자만 입력) : '))
query = query.replace(' ', '+')


news_url = 'https://search.naver.com/search.naver?where=news&sm=tab_jum&query={}'

req = requests.get(news_url.format(query))
soup = BeautifulSoup(req.text, 'html.parser')


news_dict = {}
idx = 0
cur_page = 1

print()
print('크롤링 중...')

while idx < news_num:
### 네이버 뉴스 웹페이지 구성이 바뀌어 태그명, class 속성 값 등을 수정함(20210126) ###
    
    table = soup.find('ul',{'class' : 'list_news'})
    li_list = table.find_all('li', {'id': re.compile('sp_nws.*')})
    area_list = [li.find('div', {'class' : 'news_area'}) for li in li_list]
    a_list = [area.find('a', {'class' : 'news_tit'}) for area in area_list]
    
    for n in a_list[:min(len(a_list), news_num-idx)]:
        news_dict[idx] = {'title' : n.get('title'),
                          'url' : n.get('href') }
        idx += 1

    cur_page += 1

    pages = soup.find('div', {'class' : 'sc_page_inner'})
    next_page_url = [p for p in pages.find_all('a') if p.text == str(cur_page)][0].get('href')
    
    req = requests.get('https://search.naver.com/search.naver' + next_page_url)
    soup = BeautifulSoup(req.text, 'html.parser')

print('크롤링 완료')

print('데이터프레임 변환')
news_df = DataFrame(news_dict).T

folder_path = os.getcwd()
xlsx_file_name = '네이버뉴스_{}_{}.xlsx'.format(query, date)

news_df.to_excel(xlsx_file_name)

print('엑셀 저장 완료 | 경로 : {}\\{}'.format(folder_path, xlsx_file_name))
os.startfile(folder_path)
'''

import sys, os
import re
from datetime import datetime
import pickle, progressbar, json, glob, time
from tracemalloc import start

import requests
import selenium
from selenium import webdriver
import requests
from pandas import DataFrame
from bs4 import BeautifulSoup
from tqdm import tqdm
import mysql.connector


###### 날짜 저장 ##########
date = str(datetime.now())
date = date[:date.rfind(':')].replace(' ', '_')
date = date.replace(':','시') + '분'

sleep_sec = 0.5


####### 언론사별 본문 위치 태그 파싱 함수 ###########
print('본문 크롤링에 필요한 함수를 로딩하고 있습니다...\n' + '-' * 100)
def crawling_main_text(url):

    req = requests.get(url)
    req.encoding = None
    soup = BeautifulSoup(req.text, 'html.parser')
    text = ''
    news_date = ''
    name = ''
    email = ''
   
    # SBS
    if 'news.sbs' in url:
        try:
            text = soup.find('div', {'itemprop' : 'articleBody'}).text
        except Exception as e:
            print("수집에러 : "+str(e))
    
    # KBS
    elif 'news.kbs' in url:
        try:
            text = soup.find('div', {'id' : 'cont_newstext'}).text

            date_temp = soup.find('span', {'class' : 'txt-info'}).text
            start_idx = date_temp.find('\n')
            end_idx = date_temp.find('\n',start_idx+1)
            news_date = date_temp[start_idx+4:end_idx]
            news_date = news_date.replace('.','-')
            news_date = news_date.replace('(','')
            news_date = news_date.replace(')','')
            print(news_date)
            temp = soup.find('p', {'class' : 'name'}).text
            start_idx = temp.find('\n')
            end_idx = temp.find('\n',start_idx+1)
            name = temp[start_idx+1:end_idx]
            name = name.replace('기자','')
            name = name.strip()            
            start_idx = end_idx+1
            end_idx = temp.find('\n',start_idx+1)
            email = temp[start_idx+1:end_idx]
            
        except Exception as e:
            print("수집에러 : "+str(e))
        
    # JTBC
    elif 'news.jtbc' in url:
        try:
            text = soup.find('div', {'class' : 'article_content'}).text
        except Exception as e:
            print("수집에러 : "+str(e))
        
    # 그 외
    else:
        text == None

    if text is not None:
        return text.replace('\n','').replace('\r','').replace('<br>','').replace('\t',''),news_date,name,email
    else:
        return text,news_date,name,email
    
    
#press_nms = ['KBS','SBS','JTBC']
press_nms = ['KBS']

#print('검색할 언론사 : {}'.format(press_nm))


############### 브라우저를 켜고 검색 키워드 입력 ####################
#query = input('검색할 키워드  : ')
#news_num = int(input('수집 뉴스의 수(숫자만 입력) : '))
#querys = ['윤석렬','이재명','코로나']
querys = ['경기지사','정호영','bts','한덕수','원희룡','금리','물가','여행']
news_num=10

print('\n' + '=' * 100 + '\n')

print('브라우저를 실행시킵니다(자동 제어)\n')

for press_nm in press_nms:
    for query in querys:
        chrome_path = 'c:/chromedriver/chromedriver.exe'
        browser = webdriver.Chrome(chrome_path)

        news_url = 'https://search.naver.com/search.naver?where=news&query={}'.format(query)
        browser.get(news_url)
        time.sleep(sleep_sec)


        ######### 언론사 선택 및 confirm #####################
        print('설정한 언론사를 선택합니다.\n')

        search_opn_btn = browser.find_element_by_xpath('//a[@class="btn_option _search_option_open_btn"]')
        search_opn_btn.click()
        time.sleep(sleep_sec)

        bx_press = browser.find_element_by_xpath('//div[@role="listbox" and @class="api_group_option_sort _search_option_detail_wrap"]//li[@class="bx press"]')

        # 기준 두번 째(언론사 분류순) 클릭하고 오픈하기
        press_tablist = bx_press.find_elements_by_xpath('.//div[@role="tablist" and @class="option"]/a')
        press_tablist[1].click()
        time.sleep(sleep_sec)

        # 첫 번째 것(언론사 분류선택)
        bx_group = bx_press.find_elements_by_xpath('.//div[@class="api_select_option type_group _category_select_layer"]/div[@class="select_wrap _root"]')[0]

        press_kind_bx = bx_group.find_elements_by_xpath('.//div[@class="group_select _list_root"]')[0]
        press_kind_btn_list = press_kind_bx.find_elements_by_xpath('.//ul[@role="tablist" and @class="lst_item _ul"]/li/a')

        for press_kind_btn in press_kind_btn_list:
            
            # 언론사 종류를 순차적으로 클릭(좌측)
            press_kind_btn.click()
            time.sleep(sleep_sec)
            
            # 언론사선택(우측)
            press_slct_bx = bx_group.find_elements_by_xpath('.//div[@class="group_select _list_root"]')[1]
            # 언론사 선택할 수 있는 클릭 버튼
            press_slct_btn_list = press_slct_bx.find_elements_by_xpath('.//ul[@role="tablist" and @class="lst_item _ul"]/li/a')
            # 언론사 이름들 추출
            press_slct_btn_list_nm = [psl.text for psl in press_slct_btn_list]
            
            # 언론사 이름 : 언론사 클릭 버튼 인 딕셔너리 생성
            press_slct_btn_dict = dict(zip(press_slct_btn_list_nm, press_slct_btn_list))
            
            # 원하는 언론사가 해당 이름 안에 있는 경우
            # 1) 클릭하고
            # 2) 더이상 언론사분류선택 탐색 중지
            if press_nm in press_slct_btn_dict.keys():
                print('<{}> 카테고리에서 <{}>를 찾았으므로 탐색을 종료합니다'.format(press_kind_btn.text, press_nm))
                
                press_slct_btn_dict[press_nm].click()
                time.sleep(sleep_sec)
                
                break



        ################ 뉴스 크롤링 ########################

        print('\n크롤링을 시작합니다.')
        # ####동적 제어로 페이지 넘어가며 크롤링
        news_dict = {}
        idx = 1
        cur_page = 1

        pbar = tqdm(total=news_num ,leave = True)
            
        while idx < news_num:

            table = browser.find_element_by_xpath('//ul[@class="list_news"]')
            li_list = table.find_elements_by_xpath('./li[contains(@id, "sp_nws")]')
            area_list = [li.find_element_by_xpath('.//div[@class="news_area"]') for li in li_list]
            a_list = [area.find_element_by_xpath('.//a[@class="news_tit"]') for area in area_list]
        
            for n in a_list[:min(len(a_list), news_num-idx+1)]:
                n_url = n.get_attribute('href')

                text, news_date, name, email = crawling_main_text(n_url)                
                
                news_dict[idx] = {'title' : n.get_attribute('title'), 
                                'url' : n_url,
                                'text' : text,
                                'date' : news_date,
                                'writer' : name,
                                'email' : email,
                                'query' : query
                                }
                
                idx += 1
                pbar.update(1)
                
            if idx < news_num:
                cur_page +=1

                try:
                    pages = browser.find_element_by_xpath('//div[@class="sc_page_inner"]')        
                    next_page_url = [p for p in pages.find_elements_by_xpath('.//a') if p.text == str(cur_page)][0].get_attribute('href')
                    browser.get(next_page_url)
                    time.sleep(sleep_sec)
                except Exception as e:
                    print("수집에러 : "+str(e))
                    idx = news_num
                
            else:
                pbar.close()
                
                print('\n브라우저를 종료합니다.\n' + '=' * 100)
                time.sleep(0.7)
                browser.close()
                break

        #### DB insert ###################################################### 

        print('DB접속')

        try:

            mydb = mysql.connector.connect(
                host='192.168.56.1',
                user='root',
                passwd='595855',
                database='article'
            )

            cur = mydb.cursor(prepared=True)

            print('DB SQL 작성')
            for k,v in news_dict.items():
        
                sql = '''
                insert into news( url,title,text,date,writer,email,content_size,query)
                VALUES(?,?,?,TIMESTAMP(?),?,?,?,?) 
                ON DUPLICATE KEY 
                UPDATE title = ?
                ,text = ?
                ,date = TIMESTAMP(?)
                ,writer = ?
                ,email = ?
                ,content_size = ?
                ,query=?
                '''

                val = (v['url'],v['title'], v['text'], v['date'], v['writer'], v['email'], len(v['text']),v['query'], v['title'], v['text'], v['date'], v['writer'], v['email'], len(v['text']),v['query'])
                cur.execute( sql, val)

        except Exception as e:
            mydb.rollback()
            print(str(e))
        finally:
            mydb.commit()
            cur.close()

        
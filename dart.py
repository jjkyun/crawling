'''
- Dart 제목 Crawling
- 종목코드 Crawling
@ Jae Kyun Kim
'''
import requests
from bs4 import BeautifulSoup
from pprint import pprint

def requestDart():
    URL = "http://dart.fss.or.kr/dsac001/mainAll.do?selectDate=&sort=&series=&mdayCnt=2" 
    ## mdayCnt=1이 당일을 기준이며 2는 하루 전이다. (주말도 Counting 된다)
    
    response = requests.get(URL)
    html = response.text
    parsing = BeautifulSoup(html, 'html.parser')

    parsing.find('div', id ='listContents')
    
    # listContents = soup.find('div', id='listContents') #.find 함수를 써서 테이블 범위를 지정
    # listTr = listContents.div.table.find_all('tr') #점점 좁혀나간다
    # #print(listTr)
    # for tr in listTr:
    #     try: #tr이 없는 경우를 생각해서
    #         time = tr.find('td', class_="cen_txt").get_text().strip() #tr.find는 가장 위에 있는 것만 반환
    #         company = tr.find('span').a.get_text().strip() #회사 이름만 프린트
    #         title = tr.find_all('td')[2].get_text().replace(" ","").strip() #find_all하고 인덱싱으로 원하는 td에 접근
    #         date = tr.find_all('td', class_="cen_txt")[1].get_text()
    #         print(time+' '+company+' '+title+' '+date)
    #     except:
    #         pass
    
requestDart()
'''
requests, bs4 활용해서 dart 제목만 crawling 하기
'''

import requests
from bs4 import BeautifulSoup

def reqDartData():
    URL = "http://dart.fss.or.kr/dsac001/mainAll.do?selectDate=&sort=&series=&mdayCnt=1" 
    response = requests.get(URL)
    html = response.text #text를 html에 담고 
    soup = BeautifulSoup(html,'html.parser') #bs를 통해서 보기 편하게 바꿈
    #파싱은 원하는 데이터를 쪼개는 것

    listContents = soup.find('div', id='listContents') #.find 함수를 써서 테이블 범위를 지정
    listTr = listContents.div.table.find_all('tr') #점점 좁혀나간다
    #print(listTr)
    for tr in listTr:
        try: #tr이 없는 경우를 생각해서
            time = tr.find('td', class_="cen_txt").get_text().strip() #tr.find는 가장 위에 있는 것만 반환
            company = tr.find('span').a.get_text().strip() #회사 이름만 프린트
            title = tr.find_all('td')[2].get_text().replace(" ","").strip() #find_all하고 인덱싱으로 원하는 td에 접근
            date = tr.find_all('td', class_="cen_txt")[1].get_text()
            print(time+' '+company+' '+title+' '+date)
        except:
            pass
    
reqDartData()

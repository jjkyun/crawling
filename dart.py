'''
- Dart 제목 Crawling
- 종목코드 Crawling
@ Jae Kyun Kim
'''
import requests
from bs4 import BeautifulSoup
from pprint import pprint

def getCode(link):
    response = requests.get('https://dart.fss.or.kr/' + link)
    bs = BeautifulSoup(response.text, 'html.parser')
    if bs.find('div', class_="pop_table_B").table.find_all('tr')[3].th.get_text() == '종목코드':
        ## 현재 4번째 tr이 종목코드이지만, 추후 양식이 바뀔 것을 대비해서 '종목코드' 체크
        return bs.find('div', class_="pop_table_B").table.find_all('tr')[3].td.get_text()

def requestDart():
    URL = "http://dart.fss.or.kr/dsac001/mainAll.do?selectDate=&sort=&series=&mdayCnt=2" 
    ## mdayCnt=1이 당일을 기준이며 2는 하루 전이다. (주말도 Counting 된다)
    
    response = requests.get(URL)
    bs = BeautifulSoup(response.text, 'html.parser')

    listContents = bs.find('div', id ='listContents')
    listTr = listContents.div.table.find_all('tr')[1:]

    for tr in listTr:
        time = tr.find('td', class_='cen_txt').get_text().strip()
        market = tr.find('span').img['title']
        name = tr.find('span').a.get_text().strip()
        code = getCode(tr.find('span').a['href'])
        ## code가 None일 경우는 market이 기타인 경우
        title = ''.join(tr.find_all('td')[2].get_text().replace(" ","").split())

        print(time, market, name, code, title)

requestDart()
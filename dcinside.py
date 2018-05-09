import requests
from bs4 import BeautifulSoup

BaseURL = 'http://gall.dcinside.com/board/view/?id=bitcoins&no='
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36'}

latestNum = 4641419 # 가장 최신 게시글 Number
stepSize = 100 # 초기 stepSize 설정
counter = 0 # 날짜별 게시글 수 파악용 counter
dataDict = dict() # 데이터 저장용 Dictionary

def Scraping(currentNum):
    '''현재 게시글의 날짜 및 시간 정보 스크레이핑'''
    global latestNum
    global counter
    try:
        res = requests.get(BaseURL+str(currentNum), headers=headers)
        html = res.text #HTML의 Body 파트를 string타입으로 반환
        bs = BeautifulSoup(html, 'lxml') 
        date = bs.find('div', class_='w_top_right').ul.li.b.get_text().strip()
        return date
    except:
        latestNum -= 1
        counter += 1
        return Scraping(currentNum-1) # 삭제된 게시글이 있을 경우 다음 게시글 재귀, but Network가 끊어져도 카운트가 하나 올라감

def SetStepSize(hour, minute):
    '''현재 시간을 기준으로 다음 stepsize 결정'''
    global stepSize
    if hour > 21: stepSize = 2000
    elif hour > 18 : stepSize = 1000
    elif hour > 12: stepSize = 700
    elif hour > 6: stepSize = 400
    elif hour > 3: stepSize = 300
    elif hour > 0: stepSize = 200
    elif minute > 30: stepSize = 80
    elif minute > 5: stepSize = 30
    else : stepSize = 5

def SaveAndUpdate(date):
    ''' dataDict에 현재 날짜(key)와 해당 날짜에 쓰여진 게시글 수(value) 저장 & 다음 stepsize 결정'''
    global counter
    datelist = date.split() # ex >>> ['2018-02-27', '12:27:38']
    day = datelist[0]
    hour = datelist[1][:2]
    minute = datelist[1][3:5]
    if day in dataDict:
        counter += stepSize
        dataDict[day] = counter
    else:
        counter = 1 # 자정 넘어서 recursive된 counter는 무시
        dataDict[day] = counter
    SetStepSize(int(hour), int(minute))

if __name__=='__main__':
    while latestNum > 0:
        date = Scraping(latestNum)
        SaveAndUpdate(date)
        latestNum -= stepSize
        print(dataDict)
        if len(dataDict) == 180: break

    with open("bitcoin-gall.txt", "w", encoding='UTF-8') as f:
        for date, count in dataDict.items():
            f.write(str(date) + ' : ' + str(count) + '\n')
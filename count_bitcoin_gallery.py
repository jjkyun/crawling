import requests
from bs4 import BeautifulSoup

class EmptyPostError(Exception):
    pass

def SlowDown(step, magnitude=10, method='linear'):
    if method == 'linear':
        if step > magnitude:
            return step - magnitude
        else:
            return step - int(magnitude / 2)
    elif method == 'exponential':
        return int(step / magnitude)

def Accelerate(step, magnitude=10, method='linear'):
    if method == 'linear':
        return step + magnitude
    elif method == 'exponential':
        return step * magnitude

def isNumber(s):
  try:
    float(s)
    return True
  except ValueError:
    return False

def ScrapeBoard(pageNumber):
    customHeaders = {
        'User-Agent': 'Chrome/63.0.3239.132'
    }
    baseURL = 'http://gall.dcinside.com/board/lists/?id=bitcoins&page='
    URL = baseURL + str(pageNumber)
    html = requests.get(URL, headers=customHeaders).text
    return BeautifulSoup(html, 'lxml')
    
def ScrapePost(postNumber):
    customHeaders = {
        'User-Agent': 'Chrome/63.0.3239.132'
    }
    baseURL = 'http://gall.dcinside.com/board/view/?id=bitcoins&no='
    URL = baseURL + str(postNumber)
    html = requests.get(URL, headers=customHeaders).text
    return BeautifulSoup(html, 'lxml')

def GetTimeFromPost(postNumber):
    post = ScrapePost(postNumber)
    try:
        time = post.find('div', class_='w_top_right').ul.li.get_text().split(' ')
        return tuple(time)
    except:
        raise EmptyPostError

def GetTimeFromLatestPost():
    # 비트코인 갤러리의 게시판의 첫 페이지를 긁어온다.
    bitgall = ScrapeBoard(1)

    #가장 첫 글을 긁는다
    date = ''
    latestPostNum = ''

    table = bitgall.find('tbody', class_='list_tbody')
    trs = table.findAll('tr')
    for tr in trs:
        postNumber = tr.find('td', class_='t_notice').get_text()
        if isNumber(postNumber):
            latestPostNum = postNumber
            date = tr.find('td', class_='t_date').get_text().replace('.', '-')
            break

    #오늘 날짜와 최신 글 번호를 반환한다.
    return date, latestPostNum

class PostsInTheDay():
    def __init__(self, date, endPostNumber):
        self.date = date
        self.endPostNumber = int(endPostNumber)
        self.startPostNumber = 0
        self.step = 10
        self.stepCount = 0

    def Count(self):
        return self.endPostNumber - self.startPostNumber + 1
    
    def FindNextDay(self, currentPostNumber):
        print(currentPostNumber, self.step, self.endPostNumber - currentPostNumber + 1)
        nextPostNumber = currentPostNumber - self.step
        
        date = ''
        time = ''
        while True:
            try:
                date, time = GetTimeFromPost(nextPostNumber)
                break
            except:
                nextPostNumber -= 1

        if date != self.date:
            if currentPostNumber - nextPostNumber < 10:
                self.startPostNumber = currentPostNumber
                print(date, str(self.Count()) + '개', str(self.stepCount) + '회 탐색')
                return date, nextPostNumber
            else:
                self.step = SlowDown(self.step, magnitude=2, method='exponential')
                self.stepCount += 1
                return self.FindNextDay(currentPostNumber)

        else:
            self.step = Accelerate(self.step, magnitude=2, method='exponential')
            self.stepCount += 1
            return self.FindNextDay(nextPostNumber)

    
date, latestPostNumber = GetTimeFromLatestPost()
lastDate = '2017-05-31'

PostsInTheDays = dict()
while date != lastDate:
    if date not in PostsInTheDays:
        PostsInTheDays[date] = PostsInTheDay(date, latestPostNumber)

    todayPosts = PostsInTheDays[date]
    date, latestPostNumber = todayPosts.FindNextDay(int(latestPostNumber))
    print(date, latestPostNumber)
import os

from bs4 import BeautifulSoup
from time import sleep
from multiprocessing import Process
from selenium import webdriver

baseURL = 'https://upbit.com/exchange?code=CRIX.UPBIT.KRW-'

def open_window(coin):
    driver = webdriver.Chrome() 
    driver.get(baseURL+coin)
    sleep(10)
    while True:
        soup = BeautifulSoup(driver.page_source, 'lxml')
        soup.child
        table = soup.find_all('table', attrs={'class':'ty01'})[1].tbody
        for trx in table.children:
            print(str(trx.td.p).split(' ')[2])

if __name__ == '__main__':
    coins = ['EOS', 'ETH']
    processes = []

    for index, coin in enumerate(coins):
        process = Process(target=open_window, args=(coin,))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()
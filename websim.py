from selenium import webdriver
import time
import getpass
import datetime
import pandas as pd

driver = webdriver.Chrome()

URL = 'https://websim.worldquantchallenge.com/en/cms/wqc/home/'
driver.get(URL)

driver.maximize_window()

time.sleep(5)
driver.find_element_by_xpath('/html/body/nav/div/div/div/div[2]/a[1]').click() ## login

time.sleep(2)
driver.find_element_by_xpath('//*[@id="EmailAddress"]').send_keys('jaeunit@hanyang.ac.kr') ## email login
driver.find_element_by_xpath('//*[@id="Password"]').send_keys('Jkorea12')
driver.find_element_by_xpath('/html/body/main/article/section/div[1]/div/div[1]/div[2]/div/div/div/div/div/div[1]/div[4]/span[1]/button').click()
time.sleep(40)

## simulate
driver.find_element_by_xpath('//*[@id="websim-navbar-left"]/ul/li[2]/span/a').click() 
driver.find_element_by_xpath('//*[@id="websim-navbar-left"]/ul/li[2]/span/ul/li[1]/a').click()
time.sleep(30)

## alphas
alphas = driver.find_element_by_xpath('//*[@id="code-editor-container"]/div/div[6]/div[1]/div/div/div/div[4]')

# data = ['accounts_payable', 'accum_depre', 'assets', 'assets_curr', 'assets_curr_oth', 'bookvalue_ps']

# for element in data:
#     for element2 in range(1,data:
#         alphas.send_keys(element)
#         alphas.send_keys('+')
#         alphas.send_keys(element2)
#         data.append(element + '+' element2)


alphas.click()
alphas.send_keys('eps')
alphas.send_keys('+')
alphas.send_keys('returns')
driver.find_element_by_xpath('//*[@id="codeForm"]/div[2]/div/div/div[3]/button').click() 
time.sleep(50)

driver.find_element_by_xpath('//*[@id="test-statsBtn"]').click() 
time.sleep(10)

results = []
rank = driver.find_element_by_xpath('//*[@id="percentileStats"]/div/a/h4') 
results.append(rank)

alphas.click()
alphas.clear()

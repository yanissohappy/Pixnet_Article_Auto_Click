import requests
from bs4 import BeautifulSoup
import sys
import re
import time
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

Options.binary_location = "C:\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
webdriver_path = 'C:\\chromedriver.exe'
options = Options()
options.add_argument("--incognito") # 
proxy = "socks5://localhost:9050" # using tor to visit internet
# ua = "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0"
ua = UserAgent(verify_ssl = False) # "verify_ssl = False" must be added, or sth wrong
options.add_argument("user-agent={}".format(ua.random)) # using fake user-agent
options.add_argument('blink-settings=imagesEnabled=false') # no need to load photo 
driver = webdriver.Chrome(executable_path=webdriver_path, options=options)

page = 1
account = sys.argv[1]
account = account.strip() # get rid of whitespace of inputed account
"""
blogLink = "https://" + account + ".pixnet.net/blog/" + str(page)
r = requests.get("https://" + account + ".pixnet.net/blog/" + "/")
soup = BeautifulSoup(r.text,"html.parser")
max_pages = soup.find("div", {"class": "page"})
max_pages = []
max_pages = [page_num.text for page_num in soup.find_all("div", {"class": "page"})]
print(max_pages)
"""

while True:
	blogLink = "https://" + account + ".pixnet.net/blog/" + str(page)
	r = requests.get(blogLink)
	soup = BeautifulSoup(r.text,"html.parser")
	 # using html.parser to parse
	sel = soup.find_all('h2') # get every h2 tag
	sel.pop(0)
	articleLink = []
	for sel_element in sel:
		current_height = 0
		next_height = 100
		url = sel_element.find('a').get('href').split('-',1)[0] # get rid of needless part of a href
		articleLink.append(url) # get href under <h2> tag
		try:
			driver.get("https://" + account + ".pixnet.net/blog/")
			time.sleep(4)
			driver.get(url)
			current_page_height = driver.execute_script("return document.body.scrollHeight")
			while current_height < current_page_height and next_height < current_page_height:
				next_height = current_height + 100
				if next_height > current_page_height:
					break
				else:
					driver.execute_script("window.scrollTo({},{});".format(current_height, next_height))
				current_height += 100	
				time.sleep(0.5)
			driver.close() # close the window 
			ua = UserAgent(verify_ssl = False)
			options.add_argument("user-agent={}".format(ua.random)) # using fake user-agent			
			driver = webdriver.Chrome(executable_path = webdriver_path, options = options) # reopen driver
		except Exception as e:
			print(e.message)	
		print('{A} in page {B}'.format(A = url, B = page))
	if not sel:
		time.sleep(20)
		page = 0
	page += 1
	
driver.close()
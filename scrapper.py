#! /usr/bin/env python3
# coding: utf-8

from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from urllib.request import Request, urlopen
import requests
import random
import requests

from lxml.html import fromstring
import requests
from itertools import cycle
import traceback

# url = 'https://httpbin.org/ip'

# proxies = {"http": 'http://187.17.145.237:33511',
# 			"https": 'http://187.17.145.237:33511'}

# response = requests.get(url,proxies=proxies)
# print (response.json())


def get_proxies():
	ua = UserAgent()
	proxies = []
	proxies_req = Request('https://free-proxy-list.net/')
	proxies_req.add_header('User-Agent', ua.random)
	proxies_doc = urlopen(proxies_req).read().decode('utf8')
	soup = BeautifulSoup(proxies_doc, 'html.parser')
	proxies_table = soup.find(id='proxylisttable')


	for row in proxies_table.tbody.find_all('tr'):
		if row.find_all('td')[6].string == 'yes':
			proxies.append({
				'ip': row.find_all('td')[0].string,
				'port': row.find_all('td')[1].string
			})

	return proxies

def random_index_proxy(proxies):
	return random.randint(0, len(proxies) - 1)

 
def main():


	proxies = get_proxies()
	print(proxies)
	proxy_pool = cycle(proxies)
	
	url = 'https://httpbin.org/ip'
	for i in range(1,len(proxies)):
		proxy = next(proxy_pool)
		print(proxy)
		print("Request #%d"%i)
		try:
			response = requests.get(url,proxies={"http": proxy, "https": proxy})
			print(response.json())
		except:
			#Most free proxies will often get connection errors. You will have retry the entire request using another proxy to work. 
			#We will just skip retries as its beyond the scope of this tutorial and we are only downloading a single url 
			print("Skipping. Connnection error")


	# proxies = get_proxies()
	# print(proxies)
	# proxy_index = random_index_proxy(proxies)
	# proxy = proxies[proxy_index]
	# ua = UserAgent()

	# for n in range(1,100):
	# 	print('Tour de boucle: ',n)
	# 	req = Request('https://icanhazip.com/')
	# 	req.set_proxy(proxy['ip']+':'+proxy['port'],'http')
	# 	req.add_header('User-Agent', ua.random)

	# 	if n % 10 == 0:
	# 		proxy_index = random_index_proxy(proxies)
	# 		proxy = proxies[proxy_index]

	# 	try:
	# 		my_ip = urlopen(req).read().decode('utf8')
	# 		print('#' + str(n) +': ' + my_ip)
	# 	except:
	# 		del proxies[proxy_index]
	# 		print('Proxy ' + proxy['ip'] + ':' + proxy['port'] + ' deleted.')
	# 		proxy_index = random_index_proxy(proxies)
	# 		proxy = proxies[proxy_index]


if __name__=='__main__':
	main()







	# proxies = get_proxies()
# 	print(proxies)
# 	url = 'http://icanhazip.com'

# 	for i in range(0, len(proxies)-1):
# 		proxy_index = random_index_proxy(proxies)
# 		proxy = proxies[proxy_index]
# 		print("Request #%d"%i)
# 		try:
# 			response = requests.get(url,proxies={"http": proxy, "https": proxy})
# 			print(response.json())
# 		except:
# 			print("Skipping. Connnection error")
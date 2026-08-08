'''
XSSCon - 2019/2020
This project was created by Sheikh Sabbir with MCS team. 
Copyright under the MIT license
'''
import requests, json
##### Warna ####### 
N = '\033[0m'
W = '\033[1;37m' 
B = '\033[1;34m' 
M = '\033[1;35m' 
R = '\033[1;31m' 
G = '\033[1;32m' 
Y = '\033[1;33m' 
C = '\033[1;36m' 
##### Styling ######
underline = "\033[4m"
##### Default ######
agent = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'} 
line="—————————————————" 
#####################
def session(proxies,headers,cookie):
	r=requests.Session()
	r.proxies=proxies
	r.headers=headers
	r.cookies.update(json.loads(cookie))
	return r

logo=G+"""   _____  _    __     __  _____   _____   _____ 
  / ____|| |   \ \   / / |  __ \ / ____| / ____|
 | (___  | |    \ \_/ /  | |__) | (___  | (___  
  \___ \ | |     \   /   |  _  /  \___ \  \___ \ 
  ____) || |____  | |    | | \ \  ____) | ____) |
 |_____/ |______| |_|    |_|  \_\|_____/ |_____/ 
                                                   
         SK XSS - Advanced XSS Scanner
         Developer: Sheikh Sabbir
         Version: 1.0 Final
         "Security is not a product, it's a process"
"""

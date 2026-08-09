'''
SK XSS - Helper Module
Developer: Sheikh Sabbir
Version: 1.0 Final
'''
import json
import requests
from lib.helper.log import *  # <- ছোট হাতের log
import re
from urllib.parse import urljoin

# ============ Color Codes ============
W = "\033[93m"
G = "\033[92m"
R = "\033[91m"
B = "\033[94m"
C = "\033[96m"
Y = "\033[93m"
N = "\033[0m"
P = "\033[95m"
M = "\033[1;35m"
# ===================================

# ============ Default User-Agent ============
agent = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
# ===========================================

# ============ SK XSS BANNER ============
SK_BANNER = G + r"""
   _____  _    __     __  _____   _____   _____ 
  / ____|| |   \ \   / / |  __ \ / ____| / ____|
 | (___  | |    \ \_/ /  | |__) | (___  | (___  
  \___ \ | |     \   /   |  _  /  \___ \  \___ \ 
  ____) || |____  | |    | | \ \  ____) | ____) |
 |_____/ |______| |_|    |_|  \_\|_____/ |_____/ 
""" + N + G + """
         SK XSS - Advanced XSS Scanner
         Developer: Sheikh Sabbir
         Version: 1.0 Final
         "Security is not a product, it's a process"
""" + N
# ==========================================

def session(proxy, headers, cookie):
    r = requests.Session()
    if proxy:
        r.proxies = proxy
    r.headers = headers
    if cookie:
        try:
            r.cookies.update(json.loads(cookie))
        except:
            r.cookies.update({'cookie': cookie})
    r.verify = False
    return r

def print_banner():
    print(SK_BANNER)

def extract_links(html, base_url):
    links = set()
    pattern = r'(?:href|src|action)=["\']([^"\']+)["\']'
    for match in re.finditer(pattern, html, re.I):
        link = match.group(1)
        full_url = urljoin(base_url, link)
        if full_url.startswith(('http://', 'https://')):
            links.add(full_url)
    return links

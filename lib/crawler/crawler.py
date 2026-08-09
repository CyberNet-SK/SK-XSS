'''
SK XSS - Crawler Module
Developer: Sheikh Sabbir
Version: 1.0 Final
'''
import requests
from lib.helper.Log import *
from lib.helper.helper import *
from lib.core import *
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from multiprocessing import Process

class crawler:
    
    visited = []
    
    @classmethod
    def getLinks(self, base, proxy, headers, cookie):
        lst = []
        
        try:
            conn = session(proxy, headers, cookie)
            response = conn.get(base, timeout=10)
            text = response.text
            isi = BeautifulSoup(text, "html.parser")
            
            for obj in isi.find_all("a", href=True):
                url = obj["href"]
                
                if urljoin(base, url) in self.visited:
                    continue
                
                if url.startswith("mailto:") or url.startswith("javascript:"):
                    continue
                
                if url.startswith(base) or "://" not in url:
                    full_url = urljoin(base, url)
                    lst.append(full_url)
                    self.visited.append(full_url)
                    
        except Exception as e:
            Log.error(f"Error getting links from {base}: {str(e)}")
            
        return lst

    @classmethod
    def crawl(self, base, depth, proxy, headers, level, method, cookie):
        if depth < 0:
            return
            
        Log.info(f"Crawling depth {depth}: {base}")
        urls = self.getLinks(base, proxy, headers, cookie)
        
        for url in urls:
            if url.startswith("https://") or url.startswith("http://"):
                Log.info(f"Testing URL: {url}")
                p = Process(target=core.main, args=(url, proxy, headers, level, cookie, method))
                p.start()
                p.join()
                
                if depth > 0:
                    self.crawl(url, depth - 1, proxy, headers, level, method, cookie)

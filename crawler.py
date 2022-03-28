# Name: Sai Anish Garapati
# UIN: 650208577

import requests, time
import pickle
import urllib.robotparser
from threading import Thread
from bs4 import BeautifulSoup
from collections import deque
from pageRank import PageRank
from IR_system import text_preprocesser, IR_system

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class web_crawler:
    url_queue = deque([])
    index_table = dict([])
    web_graph = {}
    def __init__(self, base_url, crawl_limit):
        self.base_url = base_url
        self.crawl_limit = crawl_limit
        self.url_queue.append(self.base_url)
        
    def check_URL(self, url):
        # If URL not in UIC domain
        if 'uic.edu' not in url:
            return False
        
        if url in self.index_table:
            return False
        
        if 'http' not in url:
            return False
        
        return True

        
        
    def crawl_web_pages(self):
        text_preprocess = text_preprocesser()
        while len(self.url_queue) != 0 and len(self.index_table) < self.crawl_limit:
            crawl_url = self.url_queue.popleft()
            crawl_url = crawl_url.replace(" ", "%20")
            print(crawl_url, len(self.index_table))
            
            if self.check_URL(crawl_url) == False:
                continue
            
            try:
                req = requests.get(crawl_url, verify=False)
            except Exception:
                continue

            if 'content-type' in req.headers and 'text/html' not in req.headers['content-type']:
                continue
            
            # read lines from robots.txt file of the url
            robotParser = None
            try:
                if requests.head(crawl_url + '/robots.txt', verify=False).status_code < 400:
                    robotParser = urllib.robotparser.RobotFileParser()
                    robotParser.set_url(crawl_url + '/robots.txt')
                    robotParser.read()
            except Exception:
                continue

            page_content = BeautifulSoup(req.text, features='lxml')
            
            if crawl_url not in self.web_graph:
                self.web_graph[crawl_url] = []
            
            self.index_table[crawl_url] = ""
            
            for url in page_content.findAll('a'):
                href = url.get('href')
                title = url.string

                if href == None or title == None or len(href) <= 0 or href[0] == '#':
                    continue

                href = href.split('?', 1)[0]

                # print(crawl_url, href)
                if href[0] == '/':
                    rev = crawl_url.rfind('.edu')
                    href = crawl_url[0:rev + 4] + href

                # print(href)
                if href[-1] == '/':
                    href = href[:-1]
                    
                href = href.replace('http://', 'https://')
                
                if 'uic.edu' not in href or 'http' not in href or href == crawl_url:
                    continue
                  
                if robotParser == None:
                    self.url_queue.append(href)
                    self.web_graph[crawl_url].append(href)
                elif robotParser != None and robotParser.can_fetch('*', href):
                    self.url_queue.append(href)
                    self.web_graph[crawl_url].append(href)

            for content in page_content(['script', 'meta', 'style', 'a']):
                content.decompose()
            page_content = ' '.join(page_content.stripped_strings)

            self.index_table[crawl_url] = text_preprocess.preprocessing(str(page_content))


def main():    
    crawler = web_crawler(base_url='https://cs.uic.edu', crawl_limit=10000)
   
    start_time = time.time()
    crawler.crawl_web_pages()
    
    print('Crawling is done, crawled {} webpages in {} minutes'.format(len(crawler.index_table), (time.time() - start_time) / 60.0))
    
    IR_syst = IR_system()
    IR_syst.build_inverted_index(crawler.index_table)
    IR_syst.compute_webpage_lengths(crawler.index_table)
    
    with open('inverted_index_10k.pickle', 'wb') as file:
        pickle.dump(IR_syst, file, protocol=pickle.HIGHEST_PROTOCOL)

    pageRank = PageRank(epsilon=0.15, max_iterations=50)
    page_rank_scores = pageRank.compute_page_rank_scores(crawler.web_graph, crawler.index_table)
    
    with open('page_rank_scores_10k.pickle', 'wb') as file:
        pickle.dump(page_rank_scores, file, protocol=pickle.HIGHEST_PROTOCOL)
    
  
if __name__ == '__main__':
    main()   

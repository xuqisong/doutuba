#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author：albert time:2019/1/12

#异步爬取
import os
import re
from queue import Queue
from urllib import request
import threading
import requests
from bs4 import BeautifulSoup


class Procuder(threading.Thread):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
    }

    def __init__(self,page_queue,img_queue,*args,**kwargs):
        super(Procuder,self).__init__(*args,**kwargs)
        self.page_queue = page_queue
        self.img_queue = img_queue

    def run(self):
        while True:
            if self.page_queue.empty():
                break
            url = self.page_queue.get()
            self.parser_page(url)

    def parser_page(self,url):
        print(url)
        req = requests.get(url, headers=self.headers)
        text = req.text
        soup = BeautifulSoup(text, 'lxml')
        imgs = soup.find_all(class_="col-xs-6 col-sm-3")
        for img in imgs:
            img_url = img.contents[1].get('data-original')
            if img_url:
                img_name = img.contents[1].get('alt')
                img_name = re.sub(r'[\?？\.，。！!\*]', ' ', img_name)
                suffix = os.path.splitext(img_url)[-1]
                suffix_name = suffix.split('!')[0]
                file_name = img_name + suffix_name
                self.img_queue.put((img_url,file_name))


class Consumer(threading.Thread):
    def __init__(self,page_queue,img_queue,*args,**kwargs):
        super(Consumer,self).__init__(*args,**kwargs)
        self.page_queue = page_queue
        self.img_queue = img_queue

    def run(self):
        while True:
            if self.img_queue.empty() and self.page_queue.empty():
                break
            img_url, file_name = self.img_queue.get()

            request.urlretrieve(img_url, 'images/' + file_name)
            print('%s 下载完成！！！'% file_name)

def main():
    page_queue = Queue(100) # 存储页面的queue
    img_queue = Queue(1000) #存储图片的queue
    for x in range(1,101):
        url = 'http://www.doutula.com/article/list/?page=%d'% x
        page_queue.put(url)
        #parser_page(url)
    for x in range(5):
        t = Procuder(page_queue,img_queue)
        t.start()
    for i in range(5):
        t1 = Consumer(page_queue,img_queue)
        t1.start()


if __name__ == '__main__':
    main()

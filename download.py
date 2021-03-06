import requests
from bs4 import BeautifulSoup
import time
from lxml import etree
import csv
from concurrent.futures import ThreadPoolExecutor

fr_url = 'https://www.htu.edu.cn'
f = open('data.csv', mode='w', encoding='utf-8-sig')
csvwriter = csv.writer(f)

lens = []
def download(url):
    resp = requests.get(url)
    html = etree.HTML(resp.content.decode())
    titles = html.xpath('//*[@id="wp_news_w15"]/ul/li/div[1]/span[2]/a/@title')
    urls = html.xpath('//*[@id="wp_news_w15"]/ul/li/div[1]/span[2]/a/@href')
    times = html.xpath('//*[@id="wp_news_w15"]/ul/li/div[2]/span/text()')
    for title, url, time in zip(titles, urls, times):
        if 'http' in url:
            url = url
        else:
            url = fr_url + url
        txt = [title, url, time]
        print(txt)
        lens.append(txt)
        csvwriter.writerow(txt)


if __name__ == '__main__':
    t1 = time.time() 
    res = requests.get('https://www.htu.edu.cn/8954/list.htm')
    all_pages = int(BeautifulSoup(res.content.decode(), "html.parser").find("em", attrs={"class":"all_pages"}).text)
    with ThreadPoolExecutor(50) as t:
        for i in range(1, all_pages):
            t.submit(download, f'https://www.htu.edu.cn/8954/list{i}.htm')
    t2 = time.time()
    print(f'{len(lens)} 条数据全部下载完毕 共耗时{t2 - t1} s') 

import requests
from lxml import etree
import csv
from concurrent.futures import ThreadPoolExecutor

fr_url = 'https://www.htu.edu.cn'
f = open('data.csv', mode='w', encoding='utf-8')
csvwriter = csv.writer(f)

def download(url):
    resp = requests.get(url)
    html = etree.HTML(resp.content.decode())
    titles = html.xpath('//*[@id="wp_news_w15"]/ul/li/div[1]/span[2]/a/text()')
    urls = html.xpath('//*[@id="wp_news_w15"]/ul/li/div[1]/span[2]/a/@href')
    times = html.xpath('//*[@id="wp_news_w15"]/ul/li/div[2]/span/text()')
    for title, url, time in zip(titles, urls, times):
        if 'http' in url:
            url = url
        else:
            url = fr_url + url
        txt = [title, url, time]
        print(txt)
        csvwriter.writerow(txt)


if __name__ == '__main__':
    with ThreadPoolExecutor(50) as t:
        for i in range(1, 802):
            t.submit(download, f'https://www.htu.edu.cn/8954/list{i}.htm')
    print('全部下载完毕') 

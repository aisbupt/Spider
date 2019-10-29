import requests
from bs4 import BeautifulSoup
import webbrowser
import os
import numpy as np
import json
'''
第一次爬取网页代码 By:Tjw Date:2019-06-17:19:01
'''
class Spider:
    def __init__(self,baseUrl,local_path):
        self.baseUrl = baseUrl
        self.local_path = local_path+'\\'
        self.imgUrl = set([])#保存html页面的url
        self.pageUrl = set([])#保存所有页 html的url  第一 第二 第三
        self.imagesurl = set([])#保存具体的图片url地址
        self.nexturls = set([])#保存下一页地址
        self.nexturl = ""
    def GetHtml(self,url,params={},header={}):
        print("打开网页：",self.baseUrl+url)
        trueurl = self.baseUrl+url
        try:
            r  = requests.get(trueurl,params = params,headers = header)
            #print(r.status_code)
            r.raise_for_status()
            data = r.text
            self.soup = BeautifulSoup(data,'html.parser')
            self.html = r.content
            self.nexturls.add(url)
            self.nexturl = url
            return True
            #print(self.soup.prettify())
        except:
            print('Connection error')
            return False
    def GetAll_Url(self,tag='a',attrs={}):
        print(tag,attrs)
        tags = self.soup.find_all(tag, attrs=attrs)#得到div标签
        #print(tags)
        for tag in tags:
            targets = tag.find_all('a')#得到 a 标签
            for target in targets:
                href = target.get('href')#得到下一页的url
                if not href.find('index'):
                    sub = self.nexturl.split('/')[-1]
                    self.nexturl = self.nexturl.replace(sub,href)
                    print('有index', self.nexturl)
                else:
                    self.nexturl = href[1:]+'index.html'
                    print('没有index', self.nexturl)
                print("下一页Url:",self.baseUrl+self.nexturl)
                #self.next_page.add(url)
                imgs = target.find_all('img')
                for img in imgs:
                    self.DownLoad_Pic(img.get('src'))
        if self.nexturl not in self.nexturls:
            self.GetHtml(self.nexturl)
            self.GetAll_Url(tag='div',attrs=attrs)
    def DownLoad_Pic(self,url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
        }
        pic = requests.get(url)  # 非高清
        #print(url)
        PicName = self.local_path+url.split('/')[-1]
        with open(PicName, 'wb') as p:
            p.write(pic.content)
            # print('DownLoad','https:' + image['src'].replace('pre','pic'))
            print('DownLoad',url,'Name',PicName)
    def GetUrls(self,tag = True,className = ''):
        targets = self.soup.find_all(tag, attrs={'class': className})
        #print(targets)
        for target in targets:
            for tag in target.find_all('a'):
                #print(tag.get('href'))
                self.imgUrl.add(tag.get('href'))
        #print(self.imgUrl)
        if len(self.pageUrl) != 0:
            return
        pages = self.soup.find_all('div',attrs={'class':'pagelist'})
        for page in pages:
            for tag in page.find_all('a'):
                self.pageUrl.add(tag.get('href'))
        #print(self.pageUrl)

    def DownLoad(self):
        # 包含图片的一个html页面 不是最终图片url，有下一张按钮
        for url in self.imgUrl:
            img_url = self.baseUrl+url
            #print(img_url)
            r = requests.get(img_url)
            try:
                r.raise_for_status()
            except:
                print('connection error')
                return
            data = r.text
            soup = BeautifulSoup(data, 'html.parser')
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
            }
            imagesurl = soup.find_all('img',attrs={'id':'imgis'})#保存本页的图片地址
            for image in imagesurl: #具体的图片url
                self.imagesurl.add(image['src'])
                #pic = requests.get('https:' + image['src'].replace('pre','pic')) #高清的url就是把pre 替换为 pic即可
                pic = requests.get('https:' + image['src']) # 非高清
                #print(pic.text)
                PicName = self.local_path + image['src'][15:].split('/')[-1]+'.jpg'
                with open(PicName, 'wb') as p:
                    p.write(pic.content)
                    #print('DownLoad','https:' + image['src'].replace('pre','pic'))
                    print('DownLoad', 'https:' + image['src'])
                ####

    def SaveHtml(self,file_path):
        with open(file_path,'wb') as file:
            file.write(self.html)
            webbrowser.open(file_path)
if __name__ == '__main__':
    #url = 'https://www.baidu.com/s?'
    #params = {'wd': '星系图片'}
    #https://www.ivsky.com/search.php?
    baseUrl = 'https://www.7160.com/'
    page_num = np.linspace(60000,65000,num=50,dtype='str')
    page_num = np.array(page_num).tostring()
    #print(page_num)
    url_pre = 'fengjing/'
    url_tail = '/index.html'
    #file_path = "D:\marker_chart"+url.split('/')[-1]+'.html'
    local_path = "D:\Spider\xingxi"
    if not os.path.exists(local_path):
        os.mkdir(local_path)
    headers = {
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
               }
    attrs = {'class':"picsbox"}
    s = Spider(baseUrl=baseUrl,local_path=local_path)
    for num in range(59459,62700):
        num = str(num)
        print(num)
        url = url_pre+num+url_tail
        # s.GetHtml(url=url, header=headers)
        # s.GetAll_Url(tag='div', attrs=attrs)
        if(s.GetHtml(url=url,header=headers)):
            s.GetAll_Url(tag='div',attrs=attrs)
    print("DownLoad Over")
    exit()
    #s.SaveHtml(file_path)

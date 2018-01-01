import scrapy
import time
import json
import pymysql
import re
import requests
from bs4 import BeautifulSoup
from book_chapter.items import Book_content_Item,BookChapterItem
class chapter_crawler(scrapy.Spider):
    name = "chapter_crawler"  # 爬虫名称
    start_urls = [
        'http://www.baidu.com/']  # 启动网址
    headers = {

        'Upgrade-Insecure-Requests': '1',
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3026.3 Safari/537.36'
    }

    def parse(self, response):

        db = pymysql.connect("106.14.168.122", "bingren11111", "li5266790", "biquge_book", use_unicode=True,
                             charset="utf8")
        # db = pymysql.connect("localhost", "bingren11111", "li5266790", "biquge_book", use_unicode=True,
        #                      charset="utf8")
        cursor = db.cursor()
        cursor.execute('select count(*) from amazing_life_chapter WHERE download_status = 0')
        result = cursor.fetchall()[0][0]  #拿到记录总数
        sql_record_num = int(result/1000)
        cursor.execute('select book_id,chapter_name from amazing_life_chapter where download_status =0;')
        result_ = cursor.fetchall()
        print(result_)
        baseUrl = 'http://www.baidu.com/s?wd={}'

        for record in result_:
            print(record)
            sql_com_line = 'select name from amazing_life_book where id = {}'.format(record[0])
            print(sql_com_line)
            cursor.execute(sql_com_line)
            book_name = cursor.fetchall()[0][0]
            print(book_name)
            baidu_line = '{} {}'.format(book_name,record[1])
            yield scrapy.http.Request(url=baseUrl.format(baidu_line), callback=self.parse_page_index)
    def parse_page_index(self,response):
        pass
        # for i in range(1,sql_record_num):
        #     sql = self.sql_record_fetch(i,sql_record_num)
        #     print(sql)
        #     cursor.execute(sql)
        #     bookRecordList = cursor.fetchall()
        #     print(bookRecordList)
        #     for bookRecord in bookRecordList:
        #         name,author = bookRecord
        #         baseUrl = 'http://www.baidu.com/s?wd={}'
        #         yield scrapy.http.Request(url=baseUrl.format(name),callback=self.parse_page_index)

                # payload = {'searchkey':name.encode('gb2312')}
                # yield scrapy.FormRequest(url=self.baseUrl,headers=self.headers,formdata=payload,callback=self.parse_page_index)


    # def parse_page_index(self,response):
    #     print(response.status)
    #     for i in range(1,10):
    #         cssCom = 'div#{} h3.t a::attr(href)'.format(i)
    #         _url = response.css(cssCom).extract_first()
    #         if ('起点' not in response.css('div#{} h3 a::text'.format(i)).extract_first()):
    #             yield scrapy.Request(url=_url,callback=self.parse_content)
    #             break
    #             print(_url)
    #     for index,chapter_content in enumerate(response.css('div.ml_list li a::text').extract()):
    #         item = Book_content_Item()
    #         item['chapter_id'] = str(index + 1)
    #         item['book_name'] = response.css('div.introduce h1::text').extract_first()
    #         item['chapter_name'] = response.css('div.ml_list li a::text')[index].extract()
    #         chapter_url = ''.join([response.request.url,response.css('div.ml_list li a::attr(href)')[index].extract()])
    #         yield scrapy.Request(url=chapter_url,meta={'key':item},callback=self.parse_page_content)
    # def parse_page_content(self,response):
    #     item = response.meta['key']
    #     item['content'] = ''.join(response.css('div.novelcontent p::text')[3:-2].extract())
    #     yield item

    # def parse_content(self,response):
    #     soup = BeautifulSoup(response.body,'lxml')
    #     br = soup.find('br')
    #     content = br.parent.get_text()
    #     if len(content) > 500:
    #         item = BookChapterItem()
    #
    #         item['content'] = content






    #
    # def sql_record_fetch(self,sql_recod_num,max_sql_num):
    #     i = sql_recod_num
    #     if sql_recod_num != max_sql_num:
    #         sql = 'select name,author from amazing_life_book where id >={} and id < {}'.format((i-1)*1000,i*1000)
    #         return sql
    #     else:
    #         sql = 'select name,author from amazing_life where id >= {}'.format(i * 1000)
    #         return sql
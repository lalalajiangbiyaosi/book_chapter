import scrapy
import time
import json
import pymysql
import re
import requests
from book_chapter.items import Book_content_Item
class chapter_crawler(scrapy.Spider):
    name = "chapter_crawler"  # 爬虫名称
    start_urls = [
        'http://www.wmtxt.com/']  # 启动网址
    baseUrl = 'http://www.wmtxt.com/modules/article/search.php'
    headers = {
        'Host': 'www.wmtxt.com',
        'Referer': 'http://www.wmtxt.com/modules/article/search.php',
        'Upgrade-Insecure-Requests': '1',
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3026.3 Safari/537.36'
    }

    custom_settings = {
    'Host': 'www.wmtxt.com',
    'Referer':'http://www.wmtxt.com/modules/article/search.php',
    'Upgrade-Insecure-Requests':'1',
    'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3026.3 Safari/537.36'
}

    def parse(self, response):

        # db = pymysql.connect("106.14.168.122", "bingren11111", "li5266790", "biquge_book", use_unicode=True,
        #                      charset="utf8")
        db = pymysql.connect("localhost", "bingren11111", "li5266790", "biquge_book", use_unicode=True,
                             charset="utf8")
        cursor = db.cursor()
        cursor.execute('select count(*) from amazing_life_book')
        result = cursor.fetchall()[0][0]  #拿到记录总数
        sql_record_num = int(result/1000)
        for i in range(1,sql_record_num):
            sql = self.sql_record_fetch(i,sql_record_num)
            print(sql)
            cursor.execute(sql)
            bookRecordList = cursor.fetchall()
            print(bookRecordList)
            for bookRecord in bookRecordList:
                name,author = bookRecord
                payload = {'searchkey':name.encode('gb2312')}
                yield scrapy.FormRequest(url=self.baseUrl,headers=self.headers,formdata=payload,callback=self.parse_page_index)


    def parse_page_index(self,response):
        print(response.status)
        for index,chapter_content in enumerate(response.css('div.ml_list li a::text').extract()):
            item = Book_content_Item()
            item['chapter_id'] = str(index + 1)
            item['book_name'] = response.css('div.introduce h1::text').extract_first()
            item['chapter_name'] = response.css('div.ml_list li a::text')[index].extract()
            chapter_url = ''.join([response.request.url,response.css('div.ml_list li a::attr(href)')[index].extract()])
            yield scrapy.Request(url=chapter_url,meta={'key':item},callback=self.parse_page_content)
    def parse_page_content(self,response):
        item = response.meta['key']
        item['content'] = ''.join(response.css('div.novelcontent p::text')[3:-2].extract())
        yield item




    def sql_record_fetch(self,sql_recod_num,max_sql_num):
        i = sql_recod_num
        if sql_recod_num != max_sql_num:
            sql = 'select name,author from amazing_life_book where id >={} and id < {}'.format((i-1)*1000,i*1000)
            return sql
        else:
            sql = 'select name,author from amazing_life where id >= {}'.format(i * 1000)
            return sql
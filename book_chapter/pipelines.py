# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import oss2
import os,sys
import shutil,pymysql
class BookChapterPipeline(object):
    access_key_id = os.getenv('OSS_TEST_ACCESS_KEY_ID', 'LTAIolNYPMt1wbBA')
    access_key_secret = os.getenv('OSS_TEST_ACCESS_KEY_SECRET', '5PvJ6bvVMbZOPLMD2fDlao9fLYGRL9')
    bucket_name = os.getenv('OSS_TEST_BUCKET', 'biquge-test')
    endpoint = os.getenv('OSS_TEST_ENDPOINT', 'https://oss-cn-hangzhou-internal.aliyuncs.com')

    # 确认上面的参数都填写正确了
    def __init__(self):
        super().__init__()

        self.bucket = oss2.Bucket(oss2.Auth(self.access_key_id, self.access_key_secret), self.endpoint, self.bucket_name)
    def process_item(self, item, spider):

        db = pymysql.connect("106.14.168.122", "bingren11111", "li5266790", "biquge_book", use_unicode=True,
                             charset="utf8")
        cursor = db.cursor()

        cursor.execute('select id from amazing_life_book where name = \'{}\''.format(item['book_name']))
        book_id = cursor.fetchall()[0][0]
        print('-----------------------------------------------------------------------')
        print(item['chapter_id'], book_id, item['chapter_name'])
        print(type(item['chapter_id']),type(book_id),type(item['chapter_name']))
        sqlLine = 'INSERT into amazing_life_chapter(chapter_name,chapter_id,book_id) values(\'%s\', %s, %s)' % (item['chapter_name'],item['chapter_id'], book_id, )

        if cursor.execute(sqlLine):
            print('----------输出数据库成功----------，')
        cursor.close()
        db.commit()
        db.close()

        bucket = self.bucket
        command_line = '{}/{}.txt'.format(item['book_name'],item['chapter_name'])
        try:
            result_status =  bucket.put_object(command_line,item['content'])
        except:
            print('上传至oss失败')
            pass
        finally:
            pass
        return item

# -*- coding: utf-8 -*-

import pymysql

db_config = {
    'host':'localhost',
    'user':'root',
    'password':'123456',
    'db':'mydb',
    'charset':'utf8',
}


class NutPipeline(object):
    def __init__(self):
        self.conn = pymysql.Connect(**db_config)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        sql = "insert into db_text(title,content,content_img) values(%s, %s, %s)"
        try:
            self.cursor.execute(sql, (item['title'], item['content'], item['content_img']))
            self.conn.commit()
        except Exception as e:
            print("操作数据库发生异常", e)
            self.conn.rollback()

    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()
        print("数据库资源关闭了！")
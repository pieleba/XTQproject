# -*- coding: utf-8 -*-

import pymysql


db_config = {
    'host': 'localhost',
    'user': 'root',
    'password':  '123456',
    'db': 'msj',
    'charset': 'utf8'
}


class FoodsinfoPipeline(object):
    def __init__(self):
        self.conn = pymysql.Connect(**db_config)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        sql = "insert into foods(fname, fimg, fpopnum, fprice, fcategory, fstorenum) values(%s, %s, %s, %s, %s, %s)"
        try:
            print("pipeline中item的内容是------------>", item)
            self.cursor.execute(sql, (item['fname'], item['fimg'], item['fpopnum'], item['fprice'], item['fcategory'], item['fstorenum']))
            self.conn.commit()
        except Exception as e:
            print("操作数据库发生异常", e)
            self.conn.rollback()

    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()
        print("数据库资源关闭了！")
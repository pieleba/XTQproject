import pymysql

from myjob import settings


def connect2mysql():
    conn = pymysql.connect(**(settings.dbsettings))
    with conn.cursor() as cursor:
        sql = """
                select fname,fpopnum
                from mm_foods
                order by fpopnum desc
              """
        cursor.execute(sql)
        items = cursor.fetchmany(10)  # 获取本店前6条人气数据
    conn.close()
    return items
# -*- coding: utf-8 -*-
from scrapy import log
import MySQLdb

def insert_or_update(cursor,table,where_str,insert_data,update_data,index_key = 'id'):

   """
   :param cursor:
   :type cursor: MySQLdb.cursors.Cursor
   :param table:
   :param where_str:
   :param insert_data:
   :type insert_data dict
   :param update_data:
   :type update_data:dict
   :return:
   """

   try:
       cursor.execute("select * from %s where %s" % (table, where_str))
       check_item = cursor.fetchone()
       if check_item is not None:
           update_sql = "update " + table + " set " + ",".join(
               ["%s = %%d" % (k,) if isinstance(v, int) else "%s = %%s" % (k,) for k, v in
                update_data.items()]) + " where " + where_str
           cursor.execute(update_sql,update_data.values())
           return check_item
       else:
           insert_sql = "insert into " + table + " set " + ",".join(
               ["%s = %%d" % (k,) if isinstance(v, int) else "%s = %%s" % (k,) for k, v in insert_data.items()])
           cursor.execute(insert_sql,insert_data.values())
           insert_id = cursor.connection.insert_id()
           insert_item = insert_data;
           insert_item[index_key] = insert_id;
           return insert_item
   except Exception,e:
    log.msg("error:%s,sql:%s"%(e,insert_sql), level=log.CRITICAL)
    return None



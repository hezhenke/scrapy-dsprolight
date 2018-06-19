# -*- coding: utf-8 -*-


def insert_or_update(cursor,table,where_str,insert_data,update_data):

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
           update_sql = "update " + table + "set " + ",".join(
               ["%s = %s" % (k, v) if isinstance(v, int) else "%s = '%s'" % (k, v) for k, v in
                update_data.items()]) + " where " + where_str
           cursor.execute(update_sql)
           return check_item
       else:
           insert_sql = "insert into " + table + "set " + ",".join(
               ["%s = %s" % (k, v) if isinstance(v, int) else "%s = '%s'" % (k, v) for k, v in insert_data.items()])
           cursor.execute(insert_sql)

           cursor.execute("select * from %s where %s" % (table, where_str))
           insert_item = cursor.fetchone()
           return insert_item
   except:
       return None



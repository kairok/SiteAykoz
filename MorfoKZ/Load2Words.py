
# -*- encoding: utf-8 -*-
__author__ = 'kkairat'

import sys
import os
#sys.path.append("/media/kairat/Windows7_OS/WorkPython/InstituteIPIC/")
#sys.path.append("/WorkPython/InstituteIPIC/")
import re
import mysql.connector


user1='root'
password1='kairat'
database1='morphokz'
cnx = mysql.connector.connect(user=user1, password=password1, database=database1)
cursor = cnx.cursor(buffered=True)
cursor2 = cnx.cursor(buffered=True)

def DeleteSent():
    sql = "delete from words2kai  "
    cursor2.execute(sql)

DeleteSent()
file = open('C:\\Kazyna\\word2kaitap.txt', 'r')
i=1
for line in file:
    if len(line.strip())>0:
        print (str(i)+' '+line)
        add_employee = ("INSERT INTO words2kai "
                        "(name) "
                        "VALUES ('{}')").format(line.strip())
        data_employee = (line.strip())
        #print(data_employee)
        cursor.execute(add_employee)
        i+=1



cnx.commit()
cursor.close()
cursor2.close()
cnx.close()
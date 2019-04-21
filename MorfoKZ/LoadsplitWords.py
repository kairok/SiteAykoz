#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import mysql.connector


user1='root'
password1='kairat'
database1='morphokz'
cnx = mysql.connector.connect(user=user1, password=password1, database=database1)
cursor = cnx.cursor(buffered=True)
cursor2 = cnx.cursor(buffered=True)


'''
def DeleteSent():
    sql = "delete from split115  "
    cursor2.execute(sql)

DeleteSent()
file = open(u'C:\\Kazyna\\СПИСОК СЛИТНЫХ СЛОВ\\1-15.txt', 'r')
i=1
for line in file:
    line = line.replace('|', '').strip()
    if len(line.strip())>0:
        print (str(i)+' '+line)

        add_employee = ("INSERT INTO split115 "
                        "(name) "
                        "VALUES ('{}')").format(line.strip())
        data_employee = (line.strip())
        #print(data_employee)
        cursor.execute(add_employee)
        i+=1

'''
'''
def DeleteSent():
    sql = "delete from splitrus  "
    cursor2.execute(sql)

DeleteSent()
file = open(u'C:\\Kazyna\\СПИСОК СЛИТНЫХ СЛОВ\\rus.txt', 'r')
i=1
for line in file:
    line = line.replace('|', '').strip()
    if len(line.strip())>0:
        print (str(i)+' '+line)

        add_employee = ("INSERT INTO splitrus "
                        "(name) "
                        "VALUES ('{}')").format(line.strip())
        data_employee = (line.strip())
        #print(data_employee)
        cursor.execute(add_employee)
        i+=1

'''
def DeleteSent():
    sql = "delete from splitkaz  "
    cursor2.execute(sql)

DeleteSent()
file = open(u'C:\\Kazyna\\СПИСОК СЛИТНЫХ СЛОВ\\kaz.txt', 'r')
i=1
for line in file:
    line = line.replace('|', '').strip()
    if len(line.strip())>0:
        print (str(i)+' '+line)

        add_employee = ("INSERT INTO splitkaz "
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

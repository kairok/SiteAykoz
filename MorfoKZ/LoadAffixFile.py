#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import mysql.connector
import pickle
import re
from string import printable
import string

'''
user1='root'
password1='kairat'
database1='morphokz'
cnx = mysql.connector.connect(user=user1, password=password1, database=database1)
cursor = cnx.cursor(buffered=True)
cursor2 = cnx.cursor(buffered=True)
'''

'''

def DeleteSent():
    sql = "delete from afikscreate  "
    cursor2.execute(sql)

DeleteSent()
file = open(u'C:\Kazyna\СЛОВООБРАЗОВАТЕЛЬНЫЕ АФФИКСЫ\СЛОВООБРАЗОВАТЕЛЬНЫЕ АФФИКСЫ\\all.txt', 'r')
i=1
for line in file:
    line = line.replace('-', '').strip()

    if len(line.strip())>0:
        print (str(i)+' '+line)
        s = line.split()
        name=s[0]
        if len(s)>2:
            pos=s[1]+s[2]
        else:
            pos=s[1]
        add_employee = ("INSERT INTO afikscreate "
                        "(name, pos) "
                        "VALUES ('{}', '{}')").format(name.strip(), pos.strip())
        #data_employee = (line.strip())
        #print(data_employee)
        cursor.execute(add_employee)
        i+=1
'''

file = open(u'C:\Kazyna\СЛОВООБРАЗОВАТЕЛЬНЫЕ АФФИКСЫ\СЛОВООБРАЗОВАТЕЛЬНЫЕ АФФИКСЫ\\all.txt', 'r')
i=1
slovar={}
for line in file:
    line = line.replace('-', '').strip()

    if len(line.strip())>0:
        #print (str(i)+' '+line)
        s = line.split()
        name=s[0].strip().decode('utf-8')
        text = re.sub(u"[^a-z0-9а-яәіңғүұқөһ]+", "", name, flags=re.IGNORECASE)
        name=text
        #print(repr(name))
        if len(s)>2:
            pos=s[1]+s[2]
        else:
            pos=s[1]
        print (name + ' ' + pos.decode('utf-8'))

        pst=''
        if u'ыр' == name:
            ok=1
        if 'Ес.зт' in pos or 'Зт.рең' in pos or 'Ет.зт' in pos:
            pst='зт'
        if 'Ел.ес' in pos or 'Ел..ет' in pos:
            pst='ел'
        if 'Ес.ет' in pos or 'Ет.ет' in pos  or 'Ел.ет' in pos:
            pst='ет'
        if 'Са.са' in pos or 'Са.зт' in pos  or 'Са.сн' in pos  or 'Са.ет' in pos:
            pst='са'
        if 'Ес.сн' in pos or 'Ет.сн' in pos  or 'Ел.сн' in pos :
            pst='сн'
        if 'Ес.үст' in pos or 'Есімд.үст' in pos  or 'Есімд.үст' in pos :
            pst='үс'

        if len(pst)==0:
            print ('Error!!')
            break

        try:
            # ps=[]
            ps1=slovar[pst]
            anal={'afiks':name.strip(),
                  'analitic':pos.strip().decode('utf-8')}
            ps1.append(anal)
            slovar[pst]=ps1
        except:
            ps=[]
            anal = {'afiks': name.strip(),
                    'analitic': pos.strip().decode('utf-8')}
            ps.append(anal)
            slovar[pst]=ps

        '''
        # prepare query and data
        query = " UPDATE morphokz.word_parts" \
                "                        SET analitic = '{}'" \
                "                        WHERE word like '%{}' and pos = '{}' ".format(pos.strip(), name.strip(), pst)

       # data = (pos.strip(), name.strip(), pst)
        cursor.execute(query)
        cnx.commit()
        '''
        ok=1

file='afikscreate'
output = open(file, 'wb')
pickle.dump(slovar, output)
output.close()
'''
cnx.commit()
cursor.close()
cursor2.close()
cnx.close()
'''
ok=1
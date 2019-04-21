# -*- coding: utf-8 -*-
import pickle
#import pyodbc
import os
#import mysql.connector
#import mysqldb

import pymysql

def AccessToPicle():
    DATA_DIR = os.path.dirname(os.path.realpath(__file__))
    DATA_DIR = os.path.join(DATA_DIR, 'data')
    #rule = LoadRuleMdb(r'C:\lingvobaze\kazyna.mdb')
    #slovar = LoadSlovarMdb(r'C:\lingvobaze\kazyna.mdb')
    #afix = LoadAfixMdb(r'C:\lingvobaze\kazyna.mdb')
    #fio = LoadFioMdb(r'C:\lingvobaze\kazyna.mdb')
    #geo = LoadGeoMdb(r'C:\lingvobaze\kazyna.mdb')
    #endChar = LoadEndCharMdb(r'C:\lingvobaze\kazyna.mdb')
    #rashifr = LoadRashifrMdb(r'C:\lingvobaze\kazyna.mdb')
    rule, slovar, afix, fio, geo, endChar, rashifr = LoadSQL()
    saveslovar(slovar, os.path.join(DATA_DIR,'slovar'))
    saveafix(afix, os.path.join(DATA_DIR,'afix'))
    saverule(rule, os.path.join(DATA_DIR,'rule'))
    savefio(fio, os.path.join(DATA_DIR,'fio'))
    savegeo(geo, os.path.join(DATA_DIR,'geo'))
    saveEndchar(endChar, os.path.join(DATA_DIR,'Endchar'))
    saverashifr(rashifr, os.path.join(DATA_DIR,'rashifr'))


def LoadPikl():
    DATA_DIR = os.path.dirname(os.path.realpath(__file__))
    DATA_DIR = os.path.join(DATA_DIR, 'data')
   #print DATA_DIR
    rule = loadrule(os.path.join(DATA_DIR, 'rule'))
    slovar = loadslovar(os.path.join(DATA_DIR, 'slovar'))
    afix = loadafix(os.path.join(DATA_DIR, 'afix'))
    fio = loadfio(os.path.join(DATA_DIR, 'fio'))
    geo = loadgeo(os.path.join(DATA_DIR, 'geo'))
    endChar = loadendChar(os.path.join(DATA_DIR, 'Endchar'))
    rashifr = loadrashifr(os.path.join(DATA_DIR, 'rashifr'))
    word2 = loadrashifr(os.path.join(DATA_DIR, 'word2'))
    word2kai = loadrashifr(os.path.join(DATA_DIR, 'word2kai'))
    split115 = loadrashifr(os.path.join(DATA_DIR, 'split115'))
    splitrus = loadrashifr(os.path.join(DATA_DIR, 'splitrus'))
    splitkaz = loadrashifr(os.path.join(DATA_DIR, 'splitkaz'))
    afikscreate = loadrashifr(os.path.join(DATA_DIR, 'afikscreate'))
    verb2words = loadverb2word(os.path.join(DATA_DIR, 'verb2words'))

    return rule, slovar, afix, fio, geo, endChar, rashifr, word2, word2kai, split115, splitrus, splitkaz, afikscreate, verb2words

def LoadSQL(user='root',password='kkairat', database='morphokz'):
    rashifr=LoadRashifSQL(user,password, database)
    rule=LoadRuleSQL(user, password, database)
    afix = LoadAfixSQL(user, password, database)
    endChar = LoadEndCharSQL(user, password, database)
    slovar = LoadSlovarSQL(user, password, database)
    fio = LoadFioSQL(user, password, database)
    geo = LoadGeoSQL(user, password, database)
    return rule, slovar, afix, fio, geo, endChar, rashifr

# -------------------------------------------------------
def LoadAfiksCreateSQL(user1,password1, database1):
    rule={}
    cnx = pymysql.connect(user=user1, password=password1, database=database1)
    cursor = cnx.cursor()
    res= cursor.execute("select name, pos from afikscreate ")
    j=1
    for (cod, coderus) in cursor:
        txt = cod.lower()  # .encode("utf-8")
        code=coderus.lower()
        try:
            ps=[]
            ps1=rule [ txt]
            ps1.append(code)
            rule[txt]=ps1
        except:
            ps=[]
            ps.append(code)
            rule[txt]=ps
        # print ' '+txt+' '+lnk
        j+=1
        #row = res.fetchone()
    cursor.close()
    cnx.close()
    return rule



def LoadWordsplitSQL(user1,password1, database1, table):
    split={}
    cnx = pymysql.connector.connect(user=user1, password=password1, database=database1)
    cursor = cnx.cursor()
    sql='select id,name from {}'.format(table)
    #res=cursor.execute("select id,name from split115")
    res = cursor.execute(sql)
    #row = res.fetchone()
    j=1
    for (id, cod) in cursor:
        word = cod.lower() # .encode("utf-8")
        pos='2'
        try:
            # ps=[]
            ps1=split [ word]
            ps1.append(pos)
            split[word ] =ps1
        except:
            ps=[]
            ps. append (pos)
            split[word]=ps
        j+=1
        #row = res.fetchone()

    cursor.close()
    cnx.close()
    return split


def LoadWord2SQL(user1,password1, database1):
    word2={}
    cnx = mysql.connector.connect(user=user1, password=password1, database=database1)
    cursor = cnx.cursor()
    res=cursor.execute("select id,name from words2")
    #row = res.fetchone()
    j=1
    for (id, cod) in cursor:
        word = cod.lower() # .encode("utf-8")
        pos='2'
        try:
            # ps=[]
            ps1=word2 [ word]
            ps1.append(pos)
            word2[word ] =ps1
        except:
            ps=[]
            ps. append (pos)
            word2[word]=ps
        j+=1
        #row = res.fetchone()

    cursor.close()
    cnx.close()
    return word2

def LoadWord2SQLkai(user1,password1, database1):
    word2={}
    cnx = mysql.connector.connect(user=user1, password=password1, database=database1)
    cursor = cnx.cursor()
    res=cursor.execute("select id,name from words2kai")
    #row = res.fetchone()
    j=1
    for (id, cod) in cursor:
        word = cod.lower() # .encode("utf-8")
        pos='2'
        try:
            # ps=[]
            ps1=word2 [ word]
            ps1.append(pos)
            word2[word ] =ps1
        except:
            ps=[]
            ps. append (pos)
            word2[word]=ps
        j+=1
        #row = res.fetchone()

    cursor.close()
    cnx.close()
    return word2


def LoadGeoSQL(user1,password1, database1):
    geo={}
    cnx = mysql.connector.connect(user=user1, password=password1, database=database1)
    cursor = cnx.cursor()
    res=cursor.execute("select id,name from geo")
    #row = res.fetchone()
    j=1
    for (id, cod) in cursor:
        word = cod.lower() # .encode("utf-8")
        pos='geo'
        try:
            # ps=[]
            ps1=geo [ word]
            ps1.append(pos)
            geo[word ] =ps1
        except:
            ps=[]
            ps. append (pos)
            geo[word]=ps
        j+=1
        #row = res.fetchone()

    cursor.close()
    cnx.close()
    return geo
# ------------------------------------------------------------
def LoadFioSQL(user1,password1, database1):
    fio={}
    cnx = mysql.connector.connect(user=user1, password=password1, database=database1)
    cursor = cnx.cursor()
    res=cursor.execute( "select id,name from fio")
    #row = res.fetchone()
    j=1
    for (id,cod) in cursor:
        word = cod.lower()  # .encode("utf-8")
        pos='fio'
        try: # ps=[]
            ps1=fio[word]
            ps1.append(pos)
            fio[word]=ps1
        except:
            ps=[]
            ps.append(pos)
            fio[ word]=ps
        j+=1
        #row = res.fetchone()

    cursor.close()
    cnx.close()
    return fio

# ------------------------------------------------------------
def LoadSlovarSQL(user1,password1, database1):
    slovar={}
    # shilau=[]
    cnx = pymysql.connect(user=user1, password=password1, database=database1)
    cursor = cnx.cursor()
    res=cursor.execute( "select word, pos, afixadd, lexic, semantic from word_parts order by word")
    #row = res.fetchone()
    j=1
    shilau=[]
    for (cod, coderus, slo, lexic, semantic) in cursor:
        word = cod.lower()  # .encode("utf-8")
        #  if u'қыстай'==word:
        #      ok=1
        pos=coderus.lower()
        afixadd=slo
        if afixadd=="1":
            shilau.append(word)
        try:
            # ps=[]
            ps1=slovar[word]
            ok=0
            for part in ps1:
                if part['pos']==pos:
                    ok=1
                    break
            if ok ==1:
                continue
            desc = {'pos': pos, 'lexic': lexic, 'semantic': semantic}
            ps1.append(desc)
            slovar[word]=ps1
        except:
            ps=[]
            desc={'pos':pos, 'lexic':lexic, 'semantic':semantic}
            ps.append(desc)
            slovar[word]=ps # print ' '+txt+' '+lnk
        j+=1
        #row = res.fetchone()

    cursor.close()
    cnx.close()
    return slovar

# -----------------------------------------------------
#
def LoadEndCharSQL(user1,password1, database1):
    endchar={}
    sp=[]
    cnx = mysql.connector.connect(user=user1, password=password1, database=database1)
    cursor = cnx.cursor()
    sql= "select word_rule, end_char, is_soft, is_hard from word_end_char order by word_rule"
    res=cursor.execute(sql)
    #row = res.fetchone()
    j=1

    for (cod, coderus, slo, hard) in cursor:
        code=cod.lower()
        spis = coderus.lower()  # .encode("utf-8")
        slog=slo
        sp=[ ]
        sp. append (spis)
        sp.append(slog)
        endchar[code]=sp

        j+=1
        #row = res. fetchone()
    cursor.close()
    cnx.close()
    return endchar


# -------------------------------
def LoadRuleSQL(user1,password1, database1):
    rule={}
    cnx = mysql.connector.connect(user=user1, password=password1, database=database1)
    cursor = cnx.cursor()
    res= cursor.execute("select POS_TYPE, RULE_CODE from rule order by RULE_CODE")
    j=1
    for (cod, coderus) in cursor:
        txt = cod.lower()  # .encode("utf-8")
        code=coderus.lower()
        try:
            ps=[]
            ps1=rule [ txt]
            ps1.append(code)
            rule[txt]=ps1
        except:
            ps=[]
            ps.append(code)
            rule[txt]=ps
        # print ' '+txt+' '+lnk
        j+=1
        #row = res.fetchone()
    cursor.close()
    cnx.close()
    return rule
#---------------------

def LoadRashifSQL(user1,password1, database1):
    rashifr = {}
    cnx = mysql.connector.connect(user=user1,password=password1, database=database1)
    cursor = cnx.cursor()

    res = cursor.execute("select code, coderus from rashifr")
    #row = res.fetchone()
    j = 1

    for (cod, coderus) in cursor:
        txt = cod.lower()  # .encode("utf-8")
        code = coderus.lower()
        rashifr.setdefault(txt, '')
        rashifr[txt] = code
        j += 1
        #row = res.fetchone()
    cursor.close()
    cnx.close()
    return rashifr

# ----------------Access MDB
def LoadAfixSQL(user1,password1, database1) :
    afix={}
    cnx = mysql.connector.connect(user=user1, password=password1, database=database1)
    cursor = cnx.cursor()
    sql= "select word_rule, description, ext2 from word_end_data order by description"
    res= cursor .execute(sql)

    j=1
    for (cod, coderus, ext) in cursor:
        try:
            code=cod .lower()
            afixword = coderus.lower()  # .encode("utf-8")
            pos=ext .lower()
            try:
                ps=[]
                ps1=afix[ afixword]
                ps1.append(pos+'!'+ code)
                afix[afixword]=ps1
            except:
                ps=[]
                ps.append(pos+'!'+ code )
                afix[afixword]=ps
                # print ' '+txt+' '+lnk
        except:
            pass
        j+=1
        #row = res.fetchone()
    cursor.close()
    cnx.close()
    return afix
#------------------------------------------

def LoadRashifrMdb( file):
    rashifr = {}
    db_file = file
    user = ''
    password = ''
    odbc_conn_str = 'DRIVER={Microsoft Access Driver (*.mdb)};DBQ=%s' % (db_file)
    conn = pyodbc.connect(odbc_conn_str)
    cursor = conn.cursor()
    res = cursor.execute("select code, coderus from rashifr")
    row = res.fetchone()
    j = 1

    while row:
        txt = row[0].lower()  # .encode("utf-8")
        code = row[1].lower()
        rashifr.setdefault(txt ,'')
        rashifr[txt ] =code
        '''try:
            ps = []
            ps1 = rule[txt]
            ps1.append(code)
            rule[txt] = ps1
        except:
            ps = []
            ps.append(code)
            rule[txt] = ps
        # print ' '+txt+' '+lnk
        '''
        j += 1
        row = res.fetchone()
    conn.close()
    return rashifr


# -------------------------------
def LoadRuleMdb(file):
    rule={}
    db_file = file
    user = ''
    password = ''
    odbc_conn_str = 'DRIVER={Microsoft Access Driver (*.mdb)};DBQ=%s' % (db_file)
    conn = pyodbc.connect(odbc_conn_str)
    cursor = conn.cursor()
    res= cursor.execute("select WORD_TYPE__OID, RULE_CODE from word_rule order by RULE_CODE")
    row = res.fetchone()
    j=1

    while row:
        txt = row[0].lower()  # .encode("utf-8")
        code=row[ 1 ].lower()
        try:
            ps=[]
            ps1=rule [ txt]
            ps1.append(code)
            rule[txt]=ps1
        except:
            ps=[]
            ps.append(code)
            rule[txt]=ps
        # print ' '+txt+' '+lnk
        j+=1
        row = res.fetchone()
    conn.close()
    return rule


# ----------------Access MDB
def LoadAfixMdb(file) :
    afix={}
    db_file = file
    user = ''
    password = ''
    sql= "select word_rule__OID, description, ext2 from word_end_data order by description"

    odbc_conn_str = 'DRIVER={Microsoft Access Driver (*.mdb)};DBQ=%s' % (db_file)
    conn = pyodbc.connect(odbc_conn_str)
    cursor = conn.cursor()
    res= cursor .execute(sql)
    row = res.fetchone()
    j=1

    while row:
        try:
            code=row[0 ] .lower()
            afixword = row[1].lower()  # .encode("utf-8")
            pos=row[2 ] .lower()
            try:
                ps=[]
                ps1=afix[ afixword]
                ps1.append(pos+'!'+ code)
                afix[afixword]=ps1
            except:
                ps=[]
                ps.append(pos+'!'+ code )
                afix[afixword]=ps
                # print ' '+txt+' '+lnk
        except:
            pass
        j+=1
        row = res.fetchone()
    conn.close()
    return afix


# -----------------------------------------------------
#
def LoadEndCharMdb(file):
    endchar={}
    sp=[]
    db_file = file
    user = ''
    password = ''
    sql= "select word_rule__OID, end_char, is_soft, is_hard from word_end_char order by word_rule__OID"

    odbc_conn_str = 'DRIVER={Microsoft Access Driver (*.mdb)};DBQ=%s' % (db_file)
    conn = pyodbc.connect(odbc_conn_str)
    cursor = conn.cursor()
    res=cursor.execute(sql)
    row = res.fetchone()
    j=1

    while row:
        code=row[0].lower()
        spis = row[1].lower()  # .encode("utf-8")
        slog=row[2]
        sp=[ ]
        sp. append (spis)
        sp.append(slog)
        endchar[code]=sp

        j+=1
        row = res. fetchone()
    conn.close()
    return endchar


# ------------------------------------------------------------
def LoadSlovarMdb(file):
    slovar={}
    # shilau=[]
    db_file = file
    user = ''
    password = ''
    odbc_conn_str = 'DRIVER={Microsoft Access Driver (*.mdb)};DBQ=%s' % (db_file)  # mdb
    conn =  pyodbc.connect(odbc_conn_str)
    cursor = conn.cursor()
    res=cursor.execute( "select word, pos, afixadd from word_parts order by word")
    row = res.fetchone()
    j=1
    shilau=[]
    while row:
        word = row[0].lower()  # .encode("utf-8")
        #  if u'қыстай'==word:
        #      ok=1
        pos=row[1].lower()
        afixadd=row[2]
        if afixadd>0:
            shilau.append(word)
        try:
            # ps=[]
            ps1=slovar[word]
            ps1.append(pos)
            slovar[word]=ps1
        except:
            ps=[]
            ps. append(pos)
            slovar[word]=ps # print ' '+txt+' '+lnk
        j+=1
        row = res.fetchone()

    conn.close()
    return slovar


# ------------------------------------------------------------
def LoadFioMdb(file):
    fio={}
    db_file = file
    user = ''
    password = ''
    odbc_conn_str = 'DRIVER={Microsoft Access Driver (*.mdb)};DBQ=%s' % (db_file)  # mdb
    conn = pyodbc.connect(  odbc_conn_str)
    cursor = conn.cursor()
    res=cursor.execute( "select name from fio")
    row = res.fetchone()
    j=1
    while row:
        word = row [0].lower()  # .encode("utf-8")
        pos='fio'
        try: # ps=[]
            ps1=fio[word]
            ps1.append(pos)
            fio[word]=ps1
        except:
            ps=[]
            ps.append(pos)
            fio[ word]=ps
        j+=1
        row = res.fetchone()

    conn.close( )
    return fio


# -------------------------------------------------------
def LoadGeoMdb(file):
    geo={}
    db_file = file
    user = ''
    password = ''
    odbc_conn_str = 'DRIVER={Microsoft Access Driver (*.mdb)};DBQ=%s' % (db_file)  # mdb
    conn = pyodbc.connect(odbc_conn_str)
    cursor = conn.cursor()
    res=cursor.execute("select name from geograf")
    row = res.fetchone()
    j=1
    while row:
        word = row[0].lower() # .encode("utf-8")
        pos='geo'
        try:
            # ps=[]
            ps1=geo [ word]
            ps1.append(pos)
            geo[word ] =ps1
        except:
            ps=[]
            ps. append (pos)
            geo[word]=ps
        j+=1
        row = res.fetchone()

    conn. close()
    return geo


#----------------------
def saveslovar(slovar, file):
    output = open(file, 'wb')
    pickle.dump(slovar, output)
    output.close()


def saveafix(afix, file):
    output = open(file, 'wb')
    pickle.dump(afix, output)
    output.close()


def saverule(rule, file):
    output = open(file, 'wb')
    pickle.dump(rule, output)
    output.close()


def savefio(fio, file):
    output = open(file, 'wb')
    pickle.dump(fio, output)
    output.close()


def savegeo(geo, file):
    output = open(file, 'wb')
    pickle.dump(geo, output)
    output.close()


def saveEndchar(endChar, file):
    output = open(file, 'wb')
    pickle.dump(endChar, output)
    output.close()

def saveword2(word2, file):
    output = open(file, 'wb')
    pickle.dump(word2, output)
    output.close()

def saverashifr(rashifr, file):
    output = open(file, 'wb')
    pickle.dump(rashifr, output)
    output.close()


def loadslovar( file):
    pkl_file = open(file, 'rb')
    slovar = pickle.load(pkl_file)
    pkl_file.close()
    return slovar


def loadafix( file):
    pkl_file = open(file, 'rb')
    afix = pickle.load(pkl_file)
    pkl_file.close()
    return afix


def loadrule( file):
    pkl_file = open(file, 'rb')
    rule = pickle.load(pkl_file)
    pkl_file.close()
    return rule


def loadfio( file):
    pkl_file = open(file, 'rb')
    fio = pickle.load(pkl_file)
    pkl_file.close()
    return fio


def loadgeo( file):
    pkl_file = open(file, 'rb')
    geo = pickle.load(pkl_file)
    pkl_file.close()
    return geo


def loadendChar( file):
    pkl_file = open(file, 'rb')
    endchar = pickle.load(pkl_file)
    pkl_file.close()
    return endchar


def loadrashifr( file):
    pkl_file = open(file, 'rb')
    rash = pickle.load(pkl_file, encoding='utf-8')
    pkl_file.close()
    return rash

def loadword2( file):
    pkl_file = open(file, 'rb')
    word2 = pickle.load(pkl_file)
    pkl_file.close()
    return word2

def loadverb2word( file):
    pkl_file = open(file, 'rb')
    word2 = pickle.load(pkl_file)
    pkl_file.close()
    return word2


DATA_DIR = os.path.dirname(os.path.realpath(__file__))
DATA_DIR = os.path.join(DATA_DIR, 'data')
#slovar = LoadSlovarSQL('root','kairat', 'morphokz')
ok=1
'''
DATA_DIR = os.path.dirname(os.path.realpath(__file__))
DATA_DIR = os.path.join(DATA_DIR, 'data')

word2=LoadWordsplitSQL('root','kairat', 'morphokz','split115')
saveslovar(word2, os.path.join(DATA_DIR,'split115'))
word2=LoadWordsplitSQL('root','kairat', 'morphokz','splitrus')
saveslovar(word2, os.path.join(DATA_DIR,'splitrus'))
word2=LoadWordsplitSQL('root','kairat', 'morphokz','splitkaz')
saveslovar(word2, os.path.join(DATA_DIR,'splitkaz'))
ok=1


word2=LoadWord2SQL('root','kairat', 'morphokz')
saveslovar(word2, os.path.join(DATA_DIR,'word2'))
word2kai=LoadWord2SQLkai('root','kairat', 'morphokz')
saveslovar(word2kai, os.path.join(DATA_DIR,'word2kai'))


#saveword2(word2, file)
ok=1


'''
#afikscreate=LoadAfiksCreateSQL('root','kairat', 'morphokz')
#saveslovar(afikscreate, os.path.join(DATA_DIR,'afikscreate'))

#slovar = LoadSlovarSQL('root','kairat', 'morphokz')
#saveslovar(slovar, os.path.join(DATA_DIR,'slovar'))
ok=1

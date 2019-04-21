#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 16:07:13 2015

@author: Кайрат
"""
from xml.dom.minidom import parse
import xml.dom.minidom
import pickle
import pyodbc
import pymorphy2
#import codecs
slovar={}
afix={}
rule={}
parts = [
  [u'зт','zt'],
  [u'са','san'],
  [u'сн','syn'],
  [u'ес','esm'],
  [u'ет','et'],
  [u'үс','yst'],
  [u'шл','sha'],
  [u'ел','elt'],
  [u'од','oda']
]


def SentenceExtract(line):
   # point=line.find('.')
   # exclamation_mark=line.find('!')
   # question_mark=line.find('?')
  l=''
  sent=[]
  for c in line:
    l=l+c     
    if c=='.':
      sent.append(l)
      l=''
    if c=='!':
      sent.append(l)
      l=''
    if c=='?':
      sent.append(l)
      l=''
  # print(sent)
  return sent

#----------------------------------------------  
def WordExtract(sent):
  spisword=sent.split(' ')
  delimiter=[',','?','.','!',':','"','(',')','[',']']
  words=[]
  for w in spisword:
    if len(w)==0:
      continue
    lastchar=w[-1:]
    if lastchar in delimiter:
      w=w[:-1]
      words.append(w)
      words.append(lastchar)
      continue
    words.append(w)


  return words

#--------------------------------------
def LoadSlovar2(file):
   i=1
   oldword='';
   pos=[]
   for line in open('c:\lingvobaze\word_parts3.txt', encoding='utf-8'):
     i+=1
     break
     line=line.strip()
     s=line.split('\t')
     print(s)
     if oldword==s[1]:
      pos.append(s[2])
      #slovar[s[1]].append(s[2])
     else:
      oldword=s[1]
      pos=[]
      pos.append(s[2])
      slovar[s[1]]=pos
     if i>1600:
      break

# -------- XML Afix
def LoadXmlAfix(file):
  # Open XML document using minidom parser
  DOMTree = xml.dom.minidom.parse(file)
  collection = DOMTree.documentElement
  #if collection.hasAttribute("shelf"):
     #print "Root element : %s % collection.getAttribute("shelf")

  # Get all the movies in the collection
  afixspis = collection.getElementsByTagName("WORD_END_DATA")
  i=1
  oldword='';
  pos=[]
  #afix={}
  for afi in afixspis:
     i+=1
     afiksR = afi.getElementsByTagName('DESCRIPTION')[0]
     afiks=afiksR.childNodes[0].data
     #print ("Type: %s" % afiksR.childNodes[0].data)
     coder = afi.getElementsByTagName('WORD_RULE__OID')[0]
     code=coder.childNodes[0].data
     #print ("pos: %s" % coder.childNodes[0].data)
     morfor = afi.getElementsByTagName('EXT2')[0]
     morfo=morfor.childNodes[0].data
     #print ("morfo: %s" % morfor.childNodes[0].data)
     if oldword==afiks:
        pos.append(morfo+'!'+code)
       
     else:
        oldword=afiks
        pos=[]
        pos.append(morfo+'!'+code)
        afix[afiks]=pos
     
     #if i>11:
      # break
    
# ------------------------------------------------------- 
def LoadSlovar(file):
  input = open(file) #, encoding='utf-8'
  aString = input.read()
  s=aString.split('\n')
  i=1
  oldword='';
  pos=[]
  for l in s:
    i+=1
    line=l.strip()
    if len(line)==0:
       break
    s=line.split('\t')
    #print(i)
    if oldword==s[1]:
      pos.append(s[2].decode("utf-8")) #.decode("utf-8")
      #slovar[s[1]].append(s[2])
    else:
      oldword=s[1]
      pos=[]
      pos.append(s[2].decode("utf-8")) #.decode("utf-8")
      word=s[1].decode("utf-8")
      slovar[word]=pos
    #if i>6:
      #break
  
#-------------------------------------------  
def LoadAfix(file):
  input = open(file, encoding='utf-8')
  aString = input.read()
  s=aString.split('\n')
  i=1
  oldword='';
  pos=[]
  for l in s:
    i+=1
    line=l.strip()
    #print(line)
    if len(line)==0:
       break
    s=line.split('\t')
    #print(s)
    #break
    if oldword==s[2]:
      pos.append(s[4]+'!'+s[1])
     
    else:
      oldword=s[2]
      pos=[]
      pos.append(s[4]+'!'+s[1])
      afix[s[2]]=pos
    if i>160000:
      break
#-------------------------------
def LoadRuleMdb(file):
    db_file = file
    user = ''
    password = ''
    odbc_conn_str = 'DRIVER={Microsoft Access Driver (*.mdb)};DBQ=%s' % (db_file)
    conn = pyodbc.connect(odbc_conn_str)
    cursor = conn.cursor()
    res=cursor.execute("select WORD_TYPE__OID, RULE_CODE from word_rule order by RULE_CODE")
    row = res.fetchone()
    j=1

    while row:
        txt = row[0].lower()  #.encode("utf-8")
        code=row[1].lower()
        try:
             pos=[]
             ps=rule[txt]
             ps.append(code)
             rule[txt]=ps
        except:
             ps=[]
             pos.append(code)
             rule[txt]=pos
        #print ' '+txt+' '+lnk
        j+=1
        row = res.fetchone()
    conn.close()
    return rule

#----------------------
def LoadRule(file):
   i=1
   oldword='';
   #rule={}
   
   for line in open(file): #, encoding='utf-8'
     i+=1
     pos=[]
     #break
     line=line.strip().lower()
     s=line.split('\t')
     #print(s[1])
     try:
         ps=rule[s[1]]
         ps.append(s[2])
         rule[s[1]]=ps
     except:
         pos.append(s[2])
         rule[s[1]]=pos
   return rule

#----------------------
def saveslovar(file):
    output = open(file, 'wb')
    pickle.dump(slovar, output)
    output.close()

def saveafix(file):
    output = open(file, 'wb')
    pickle.dump(afix, output)
    output.close()
def saverule(file):
    output = open(file, 'wb')
    pickle.dump(rule, output)
    output.close()
def loadslovar(file):
    pkl_file = open(file, 'rb')
    slovar = pickle.load(pkl_file)
    pkl_file.close()
    return slovar
def loadsafix(file):
    pkl_file = open(file, 'rb')
    afix = pickle.load(pkl_file)
    pkl_file.close()
    return afix
def loadrule(file):
    pkl_file = open(file, 'rb')
    rule = pickle.load(pkl_file)
    pkl_file.close()
    return rule

#-------------------
def findafix(endw, part):
    pos='';
    try:
        desc=afix[endw]
        morf=''
        for d in desc:
            code=d.split('!')
            #morf=code[0]
            cd=code[1].lower()
            if cd in part:
                morf=code[0]
                break
        return morf
    except:
        return pos
#--------------------------
def postag(word, endw):
  pos=[]
  morfos=[]
  try:
    pos=slovar[word]

    pslat=[]
    for ps in pos:   # берем по списку часть речи
      morf=''
      for i in parts:  # ищем лат соответствие
        pl = i[0]
        if pl==ps:
          pslat=rule[i[1]]
          break
      if len(endw)>0:
          morf=findafix(endw,pslat)
          if len(morf)>0:
              morf=pl+','+morf
          else:
              morf=''
      else:
          morf=pl
      if len(morf)>0:
          morfos.append(morf)

  except:
    pos=[]
  return morfos

def parse(word):
  morfspis = []
  base = [word]
  for i in range(len(word)):
    base.append(word[:-i])
  for w in base:
    if len(w)==0:
      continue

    endword=word[len(w):]
    ps=postag(w, endword)
    if len(ps)>0:
      morf={"norm_word":w, "pos":ps}
      morfspis.append(morf)

  return morfspis



if __name__ == '__main__':     # 
  line = u'Сусыма құм баянсыздықтың тылсым құдіретін танытқысы келгендей, құп-қу жүзіне жолап кеткен сәл таңбаны жалмап жұтып жатыр.'
  
  sentenses=SentenceExtract(line)
  #print (sentenses)
  for sent in sentenses:
    words=WordExtract(sent)
    #print (words)

  i=1
  print u"Идет загрузка базы"

  #LoadRule('c:\lingvobaze\word_rule.txt')
  #LoadRuleMdb(r'C:\lingvobaze\kazyna.mdb')
  #saverule(r'c:\lingvobaze\rule.pkl')
  rule=loadrule(r'c:\lingvobaze\rule.pkl')
  #print rule

  #LoadSlovar('c:\lingvobaze\word_parts3.txt')
  #saveslovar(r'c:\lingvobaze\slovar.pkl')
  slovar=loadslovar(r'c:\lingvobaze\slovar.pkl')
  #print(slovar)
  #for key, item in slovar.items():
  #  print key


  #LoadXmlAfix("c:\lingvobaze\WORD_END_DATA2.xml")
  #saveafix('c:\lingvobaze\afix.pkl')
  afix=loadsafix(r'c:\lingvobaze\afix.pkl')
  #LoadAfix('c:\lingvobaze\WORD_END_DATA2.txt')
  #print(afix)
  print "OK"

  #m={}
  m=parse(u"апа")
  for l in m:
    print l
    print(l["norm_word"])
    for p in l["pos"]:
        print p



   


  #morph = pymorphy2.MorphAnalyzer()
  #k=morph.parse(u'шел')
  #print (k)
  #p = morph.parse(u'стали')
  #print (p)
  #print (p.tag)
  #print p.normal_form

  

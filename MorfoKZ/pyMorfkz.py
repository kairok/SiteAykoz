#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 16:07:13 2015

@author: Кайрат
"""
#from xml.dom.minidom import parse
#import xml.dom.minidom
from unidecode import unidecode
import sys
#sys.getdefaultencoding('utf-8')
#sys.path.append("/home/kai/PythonWork/MorfoKZ/")
import pickle
#import pyodbc
import re
import utilm as util



#slovar={}
#afix={}
#rule={}
endsFam=[u'бай',u'ұлы',u'қыз',u'вич',u'аев',u'ов' ,u'ев']
punctuation=[',','.','!','?',';',':','-','+','*',u'–',u'—','/','~','-']
quotes=['\'','"','(',')','[',']',u'»',u'«',u'``',"''",u'№',u'=',u'_','N','@',u'“',u'”']
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
Glasn=u'аеиоуэыюяәіүұө'
Soglasn=u'кқпстшщфхћцгғбвдмңнруйлжзч'
Gluhie = u"кқпстшщфхћцгбвгд"
Asimil=u'бғг'
slog_phon=['v','cv','vc','vcc','cvc','cvcc']  #,'ccvc'
descr_slog={
    'v':'Дауысты буын',
    'cv':'Ашық буын',
    'vc':'Тұйық буын',
    'vcc':'Тұйық буын',
    'cvc':'Бітеу буын',
    'cvcc':'Бітеу буын',
    'ccvc':'Бітеу буын'
}


descr_char={
    'А':'ашық, тіларты, езулік',
    'Ә':'ашық, тілортасы, езулік',
    'Ы':'қысаң, тіларты, езулік',
    'І':'қысаң, тілортасы, езулік',
    'Ұ':'қысаң, тіларты, еріндік',
    'Ү':'қысаң, тілортасы, еріндік',

'Е':'құранды, тілортасы, емеурін езулік',
    'О':'құранды, тіларты, сүйір еріндік',
    'Ө':'құранды, тілортасы, сүйір еріндік',
    'П':'ерін-еріндік, тоғысыңқы, қатаң',
'В':'',
'Ф':'',
'И':'',
    'Б':'ерін-еріндік, тоғысыңқы, ұяң',
    'М':'ерін-еріндік, тоғысыңқы, үнді',
'Т':'тілұшы, тоғысыңқы, қатаң',
    'Д':'тілұшы, тоғысыңқы, ұяң',
    'Н':'тілұшы, тоғысыңқы, үнді',
    'Қ':'тілшік, тоғысыңқы, қатаң',
    'К':'тілортасы, тоғысыңқы, қатаң',
    'Ғ':'тілшік, тоғысыңқы (жуысыңқы), ұяң',
'Г':'тілортасы, тоғысыңқы (жуысыңқы), ұяң',
    'Ң':'тілшік (тілортасы), тоғысыңқы, үнді',
    'С':'тілұшы, жинақы жуысыңқы, қатаң',
    'З':'тілұшы, жинақы жуысыңқы, ұяң',
    'Р':'тілұшы, діріл жуысыңқы, үнд',
    'Ш':'тілұшы, жайылыңқы жуысыңқы, қатаң',
'Ж':'тілұшы, жинақы жуысыңқы (аффрикат), ұяң',
    'Л':'тілұшы, жанама жуысыңқы, үнд',
    'Й':'тілшік (тілортасы), жуысыңқы, үнді',
    'У':'ерін-еріндік, жуысыңқы, үнді'

}

import os

DATA_DIR =  os.path.dirname(os.path.realpath(__file__))

class pyMorfKz:
    spisrootmest=[u'ма',u'са',u'се',u'ме',u'о',u'он',u'оны',u'сон',u'со',u'бұн',u'бұ',u'ана',u'осы']
    shilau=[]
    soft=[u'е',u'і',u'ү',u'ә',u'и',u'ө']
    rootmestoimen=[
          [u'ма',u'мен'],
          [u'са',u'сен'],
          [u'се',u'сен'],
          [u'ме',u'мен'],
          [u'о',u'ол'],
            [u'оны', u'ол'],
          [u'он',u'ол'],
          [u'сон',u'сол'],
          [u'со',u'сол'],
          [u'бұн',u'бұл'],
          [u'бұ',u'бұл'],
          [u'ана',u'анау'],
        [u'осы',u'бұл'],
    ]
    #__slots__=('slovar','afix','rule','fio','geo','endChar','rashifr', 'word2')
    def __init__(self):
        #--------
        #self.rule, self.slovar, self.afix, self.fio, self.geo, self.endChar, self.rashifr =util.LoadSQL()
        self.rule,self.slovar, self.afix,self.fio,self.geo, self.endChar, self.rashifr, self.words2, self.words2kai,\
            self.split115, self.splitrus, self.splitkaz , self.afikscreate, self.verb2words = util.LoadPikl()
        ok=1
        #util.LoadPikl()
        # -------------------------------

#-------------   Phonetic   ---------------------

    def phonetic(self, word):
        word = word.lower()
        phonword = ''
        guan=['а', 'ы', 'ұ', 'о']
        genish=['ә', 'і', 'ү', 'е', 'ө']
        priznaktembr=''
        for s in word:
            if s in Glasn:
                phonword += 'v'
                if s in  guan and len(priznaktembr)==0:
                    priznaktembr='Жуан тембр'
                if s in genish and len(priznaktembr)==0:
                    priznaktembr = 'Жіңішке тембр'
            if s in Soglasn:
                phonword += 'c'

        words_slog = []
        word_begin = phonword
        last_word = word_begin
        sl = []
        poz = 0
        while True:
            for i in range(0, len(slog_phon)):
                ws = word_begin[:len(slog_phon[i])]
                if ws == slog_phon[i]:
                    if ws in sl:
                        if len(words_slog) == poz:
                            continue
                    # sl=''
                    if slog_phon[i] == 'v' or slog_phon[i] == 'vc' or slog_phon[i] == 'vcc':  # Only start word
                        if len(words_slog) != 0:
                            continue
                    words_slog.append(slog_phon[i])
                    word_begin = word_begin[len(slog_phon[i]):]
                    break
            ok = 1
            if len(word_begin) == 0:
                break
            if last_word != word_begin:
                last_word = word_begin
                continue
            else:
                if len(words_slog) == 0:
                    break
                sls = words_slog.pop()
                # if len(sl)>1:
                sl.append(sls)
                poz = len(words_slog)
                word_begin = sls + word_begin

        txt = word + ' '+priznaktembr +' '
        poz = 0
        for sl in words_slog:
            op = descr_slog[sl]
            w = word[poz:poz + len(sl)]
            poz += len(sl)
            txt += w + ' - ' + op + ', '

        for w in word:
            if w=='-':
                continue
            try:
                op = descr_char[w.upper()]
            except:
                op=''
            txt += w + ' - ' + op + ' , '

        return txt
    #, self.rashifr
#-----------------------------------------------------------------------
    #   Обработка текста
    #  Извлечение предложений
    def SentenceExtract(self, line, max=0):
        result = re.split(r'[\s]', line)
        sent = []
        s = ''
        for i in range(0, len(result)):
            # print result[i]
            result[i] = self.clean_nonchar(result[i])
            if len(result[i]) == 0:
                continue
            word = result[i]
            s += word + ' '
            if '(' in s:
                if ')' not in s:
                    continue
            lastchar = word[-1:]
            if lastchar in '.!?':
                # т.б.
                if '.' in word[:-1]:
                    if len(word[:-1]) < 4:
                        continue
                if len(word) < 3:
                    continue
                if max == 1:
                    if len(s) < 20:
                        continue
                sent.append(s)
                s = ''


        sent.append(s)

        return sent


    def SentenceExtract2(self,line, max=0):

      l=''
      sent=[]
      line=line.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
      for i in range(0,len(line)):
        l=l+line[i]
        if line[i]=='.':
          if i<len(line)-1:
              k = re.findall(u'[А-ЯӘІҢҒҮҰҚӨҺ]{1}|[^ ]', line[i+1])
              if len(k) > 0:
                  #l = l + line[i]
                  continue

          if len(l)>10:   #int(len(line)/2)
                sent.append(l)
          else:
              continue
          l=''
        if line[i]=='!':
          if max==1:
              words=l.split()
              if len(words)>3:
                  sent.append(l)
                  l=''

          else:
                sent.append(l)
                l=''

        if line[i]=='?':
          if max==1:
              words=l.split()
              if len(words)>3:
                  sent.append(l)
                  l=''

          else:
                sent.append(l)
                l=''

      # print(sent)
      if len(l)>1:
          sent.append(l)
      if len(sent)==0:
          sent.append(line)
      return sent

    #----------------------------------------------
    def OnlyWordExtract(self,text):
        result = re.split(r'[\s]', text)
        spisword = []
        for w in result:
            if len(w) == 0:
                continue
            if '[' in w:
                continue
            try:
                re.search(u'([\d])', w).group()
                continue
            except:
                pass
            word = re.match(u'([A-Za-zа-яА-ЯәіңғүұқөһӘІҢҒҮҰҚӨҺ\.-]+)', w).group(0)
            spisword.append(word)

        return spisword

    def clean_nonchar(self,s):
        w=[]
        for i in s:
            try:
                if ord(i)<1500:
                    w.append(i)
            except:
                pass

        return ''.join(w)

    # ----------------------------------------------
    def WordExtract(self, sent):

        spisword = sent.split(' ')
        delimiter = [',', '?', '.', '!', ':',';', '"', '(', ')', '[', ']']
        words = []

        for w in spisword:
            if len(w) == 0:
                continue
            w=w.strip()
            if '.' in w and  len(w)<5:
                words.append(w)
                continue
            tokspis = re.split(u'([^A-Za-zа-яА-ЯәіңғүұқөһӘІҢҒҮҰҚӨҺ\d-])',
                               w)  # re.split(u'(\W)$', w)#    re.split(u'([а-яА-ЯәіңғүұқөһӘІҢҒҮҰҚӨҺ\d-]+)', w)


            for tok in tokspis:
                if unidecode(tok) != '':
                    words.append(tok)

        return words

    #-----------------------   OLD
    def WordExtract3(self, sent):
        spisword = sent.split(' ')
        delimiter = [',', '?', '.', '!', ':',';', '"', '(', ')', '[', ']']
        words = []

        for w in spisword:
            if len(w) == 0:
                continue

            ok=0
            last=[]
            i=1
            for i in range(1,len(w)):
                lastchar=w[-i]
                if lastchar in delimiter:
                    last.append(lastchar)

                    ok=1
                else:
                    break

            if '.' in w and i==1:
                words.append(w)
                continue

            if i==1:
                tokspis = re.split(u'([^A-Za-zа-яА-ЯәіңғүұқөһӘІҢҒҮҰҚӨҺ\d-])',
                                   w)  # re.split(u'(\W)$', w)#    re.split(u'([а-яА-ЯәіңғүұқөһӘІҢҒҮҰҚӨҺ\d-]+)', w)
                for tok in tokspis:
                    if tok != '':
                        words.append(tok)
                #words.append(w)
            else:
                w=w[:-i+1]
                #tokspis = re.split(u'([^A-Za-zа-яА-ЯәіңғүұқөһӘІҢҒҮҰҚӨҺ\d-])',w)
                                     # re.split(u'(\W)$', w)#    re.split(u'([а-яА-ЯәіңғүұқөһӘІҢҒҮҰҚӨҺ\d-]+)', w)
                #for tok in tokspis:
                  #  if tok != '':
                words.append(w)
                #words.append(w[:-i+1])
                last.sort(key=reversed)
                for end in last:
                    words.append(end)

            continue

        return words

    def WordExtract2(self,sent):
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
#----------------------

#-------------------
    def assimil(self,word):
        sogl=[u'б',u'г',u'ғ']
        tosogl=[u'п',u'к',u'қ']
        lastchar=word[len(word)-1:]

        tochange=tosogl[sogl.index(lastchar)]
        w=word[0:len(word)-1]+tochange
        return w

    def slog_define(self, word):
        slog=word[-3:]
        ok=0
        for i in range(len(slog)):
            if slog[i] in self.soft:
                ok=1
                break
        return ok

    def findafix(self,endw, part, word):
        pos='';
        try:
            desc=self.afix[endw]
            morf=''
            for d in desc:
                code=d.split('!')
                #morf=code[0]
                cd=code[1].lower()
                if cd in part:
                    slog=self.slog_define(word)
                    end_char=word[-1:]
                    spis=self.endChar[cd][0]
                    slogrule=self.endChar[cd][1]
                    #if slogrule==0:
                     #   slogrule=''
                    if end_char in spis and slog==slogrule:
                        morf=code[0]
                        break
            return morf
        except:
            return pos
    #--------------------------
    def postag(self,word, endw):
      pos=[]
      morfos=[]
      part=[]
      lexic=[]
      semantic=[]
      try:
            pos=self.slovar[word]


            pslat=[]

            for ps in pos:   # берем по списку часть речи
                  morf=''
                  if ps['pos'] in part:
                      break
                 # if ps==u'шл':
                      #if word not in self.shilau:
                      #    continue
                  for i in parts:  # ищем лат соответствие
                    pl = i[0]
                    if pl==ps['pos']:
                      try:
                        pslat=self.rule[i[1]]
                      except:
                          pslat=''
                      break
                  if len(endw)>0:
                      morf=self.findafix(endw,pslat,word)
                      if len(morf)>0:
                          morf=pl+','+morf
                      else:
                          morf=''
                  else:
                      morf=pl
                  if len(morf)>0:
                      morfos.append(morf)
                      part.append(pl)
                      lexic.append(ps['lexic'])
                      semantic.append(ps['semantic'])

      except:
          pass


      return morfos, part, lexic, semantic
    #--------------------------
    #def extractpos(self,pos):
    #    for ps in pos:


    #--------------------------
    def postagFIOGEO(self,word, endw, baza, priznak):
      pos=[]
      morfos=[]
      part=[]
      try:
        pos=baza[word]  #.lower()
        pslat=[]
        #for ps in pos:   # берем по списку часть речи
        ps=u'зт'
        morf=''
        for i in parts:  # ищем лат соответствие
            pl = i[0]
            if pl==ps:
              pslat=self.rule[i[1]]
              break
        if len(endw)>0:
              morf=self.findafix(endw,pslat, word)
              if len(morf)>0:
                  morf=priznak+','+morf
              else:
                  morf=''
        else:
              morf=priznak
        if len(morf)>0:
              morfos.append(morf)
              part.append(priznak)

      except:
        pos=[]

      return morfos,part

#-------   Расшифровка KZ-RU----------------

    def encript(self,txt):
            rus=''
        #for t in txt:
            t=txt.replace(u'АР+ЖЖ-1Ж',u'ЖЖ-1')
            #txt = txt.replace(u'БР+ЖЖ-2Ж', u'ЖЖ-2')
            #txt = txt.replace(u'БР+ЖЖ-1Ж', u'ЖЖ-1')

            try:
                #rus.append(self.rashifr[t])
                rus=self.rashifr[t]
            except:
                pass
            return rus

    def encript_afiks(self, txt):
            rus = ''

        #for t in txt:
            w=txt.split(',')
            if w[0]=='fio' or w[0]=='geo':
                pos=w[0]
            else:
                if w[0]==u'туынды':
                    pos=''
                else:
                    pos=self.rashifr[w[0]]
            try:
                afiks=w[1].split('+')
            except:
                afiks=''
                #rus.append(pos)
                #rus=pos
                #continue
            for a in afiks:
                af=a.split('/')
                try:
                    pos=pos+','+self.rashifr[af[1]]
                except:
                    pass
            #t = t.replace(u'АР+ЖЖ-1Ж', u'ЖЖ-1')
            # txt = txt.replace(u'БР+ЖЖ-2Ж', u'ЖЖ-2')
            # txt = txt.replace(u'БР+ЖЖ-1Ж', u'ЖЖ-1')

            try:
                #rus.append(pos)
                rus=pos
            except:
                pass
            return rus
#---------------------------------------
    #   Снятие омонимии
    def findfam(self,spis):
        for t in spis:
            if t['pos'] == 'fio':
                return True
        return False

    def findGeo(self, spis):
        for t in spis:
            if t['norm_word'] in u'аудан' or t['norm_word'] in u'ауыл' or t['norm_word'] in u'облыс' :
                return True
        return False

    def omonim(self,morfospisok):
        nomword=0;
        spisok=[]
        i = 0
        for w in range(0,len(morfospisok)):
            if len(morfospisok[w])==1:
                p=morfospisok[w]
                #spisok.append(morfospisok[w])
                #continue
            nomword+=1

            for t in morfospisok[w]:

                #for i in range(0,len(t['pos'])):
                    if len(morfospisok[w]) == 1:
                        spisok.append(t)
                        i += 1
                        break
                    if t['pos']==u'ет' and w<len(morfospisok)-1: #and len(t['pos'])>1:
                        #morfospisok[w].pop(i)
                        #t['pos'].pop()
                        #t['posrus'].pop()
                        #t['tag'].pop()
                        #t['tagrus'].pop()
                        #spisok.append(t)
                        #continue
                        if i>0:
                            break
                        else:
                            continue
                        ok=1

                    if t['pos']=='fio':
                            if w<len(morfospisok):
                                if self.findfam(morfospisok[w+1]):
                                        #if len(spisok)>0:
                                        ind=i
                                        if i>0:
                                            ind=i-1
                                        spisok.pop(ind)

                                        #t["pos"].pop(ind)
                                        #t["posrus"].pop(ind)
                                        #t["tag"].pop(ind)
                                        #t["tagrus"].pop(ind)
                                        ok=1
                                        #break
                    if t['pos'] == 'geo':
                        if w < len(morfospisok):
                            if self.findGeo(morfospisok[w + 1]):
                                spisok.append(t)
                                i += 1
                                break
                                ok = 1
                    if t['pos'] == 'Unknown1' and t['token'].istitle():   #???
                        if nomword>1 and w < len(morfospisok):
                            if self.findGeo(morfospisok[w + 1]):
                                if len(spisok) > 0:
                                    spisok.pop()
                                morf = {"token": t['token'], "norm_word": t['token'], "tag": 'geo', "pos": 'geo',
                                        'posrus': 'geo', "tagrus": 'geo'}
                                spisok.append(morf)
                                i += 1
                                break
                        else:
                            if len(spisok) > 0:
                                spisok.pop()
                            morf = {"token": t['token'], "norm_word": t['token'], "tag": 'fio', "pos": 'fio',
                                    'posrus': 'fio', "tagrus": 'fio'}
                            spisok.append(morf)
                            i += 1
                            break
                    i+=1

                    spisok.append(t)

        return spisok
#------------------------------------------
    def parse(self,word, poz=0):

        morfspis = []
        if len(word.strip())==0:
            return morfspis
        morfspis=self.parseword(word.strip())
        #return morfspis
        ok=1
        #ашып-жұмғанша-ақ
        if morfspis[0]['pos']!='Unknown':
            return morfspis
        if word.find('-')>0:
            if morfspis[0]['posrus']=='Unknown':
                morfspis = []
                word1=word.replace('-','')
                morfspis = self.parseword(word1)
            # тогда по разделим слово
            if morfspis[0]['posrus']=='Unknown':
                morfspis = []
                spis=word.split('-')
                for w in spis:
                    morfspis1=self.parseword(w)
                    for mor in morfspis1:
                        morfspis.append(mor)

        '''
        if word.istitle():
            if poz>1:
                if len(word)<15:
                    morfspis = []
                    morf = {"token": word, "norm_word": word, "tag": 'fio', "pos": 'fio', 'posrus': 'fio', 'tagrus': 'fio'}
                    morfspis.append(morf)
            else:
                for end in endsFam:
                    if end in word:
                        morfspis = []
                        morf = {"token": word, "norm_word": word, "tag": 'fio', "pos": 'fio', 'posrus': 'fio',
                                'tagrus': 'fio'}
                        morfspis.append(morf)
                        break
        '''

        return morfspis


    def createaffiks(self,w, root):

        #root = morfspis[0]['norm_word']
        anal=''
        if len(root) > len(w):
            try:
                endword = root[-(len(root) - len(w)):]
                poscr = self.slovar[w.lower()]
                for i in range(0, len(poscr)):

                    #  Find  Afiks Create
                    anal = ''
                    # for af in self.afikscreate[poscr[i].encode('utf-8')]:
                    for key in self.afikscreate.keys():
                        for af in self.afikscreate[key]:
                            afi = af['afiks']  # .decode('utf-8')
                            afa = u'ыр'
                            if endword == af['afiks']:
                                anal = endword + ' -> ' + af['analitic']
                                break
                    '''
                    if len(anal) > 0:
                        morf = {"token": root, "norm_word": w, "tag": 'T. ' + poscr[i], "pos": poscr[i],
                                'posrus': self.encript(poscr[i]), 'tagrus': self.encript_afiks(poscr[i]),
                                'analitic': anal}
                        morf['phonetic'] = phonetic
                        morf['lexic'] = ''
                        morf['semantic'] = ''
                        morfspis.append(morf)
                    '''
                # break

            except:
                pass

        return anal

#-------------------------------------------------------
    def parseword(self,word, osnova=0):
      morfspis = []
      #  -Мәңгілік
      if len(word)==0:
          return morfspis
      if word[0]=='-' and len(word)>1:
          word=word[1:]
      if len(word)>1:
          if  word[len(word)-1]=='-':
              word=word[:-1]

      phonetic = ''
      analitic=''
      #   NUM
      k=re.findall(u'\d+', word)
      if len(k)>0:
          morf = {"token": word,"norm_word": word, "tag": 'Num', "pos": 'Num', 'posrus': 'Num', 'tagrus': 'Num'}
          morf['phonetic']=phonetic
          morf['analitic'] = analitic
          morf['lexic'] = ''
          morf['semantic'] = ''
          morfspis.append(morf)
          return morfspis
      #   ,.:;!?[]()
      if word in punctuation or word in u'…':
          morf = {"token": word,"norm_word": word, "tag": 'Punct', "pos": 'Punct', 'posrus': 'Punct', 'tagrus': 'Punct'}
          morf['phonetic'] = phonetic
          morf['analitic'] = analitic
          morf['lexic'] = ''
          morf['semantic'] = ''
          morfspis.append(morf)
          return morfspis
      #  "'()[]
      if word in quotes:
          morf = {"token": word, "norm_word": word, "tag": 'quote', "pos": 'quote', 'posrus': 'quote',
                  'tagrus': 'quote'}
          morf['phonetic'] = phonetic
          morf['analitic'] = analitic
          morf['lexic'] = ''
          morf['semantic'] = ''
          morfspis.append(morf)
          return morfspis
      #  М.О.Әуезов   FIO
      k=re.findall(u'[А-ЯӘІҢҒҮҰҚӨҺ]{1}\.[А-ЯӘІҢҒҮҰҚӨҺ]{1}\.?[А-ЯӘІҢҒҮҰҚӨҺа-яәіңғүұқөһ]+', word)
      if len(k) > 0:
          morf = {"token": word,"norm_word": word, "tag": 'fio', "pos": 'fio', 'posrus': 'fio', 'tagrus': 'fio'}
          morf['phonetic'] = phonetic
          morf['analitic'] = analitic
          morf['lexic'] = ''
          morf['semantic'] = ''
          morfspis.append(morf)
          return morfspis
          #  М.О.   Инициалы
      k = re.findall(u'[А-ЯӘІҢҒҮҰҚӨҺ]{1}\.$|[А-ЯӘІҢҒҮҰҚӨҺ]{1}\.[А-ЯӘІҢҒҮҰҚӨҺ]{1}', word)
      if len(k) > 0:
              morf = {"token": word, "norm_word": word, "tag": 'Inic', "pos": 'Inic', 'posrus': 'Inic',
                      'tagrus': 'Inic'}
              morf['phonetic'] = phonetic
              morf['analitic'] = analitic
              morf['lexic'] = ''
              morf['semantic'] = ''
              morfspis.append(morf)
              return morfspis
      #  ҚазПИдің   Abrr
      k=re.findall(u'[А-ЯӘІҢҒҰҚӨҺҮ]{2,7}',word)
      if len(k) > 0:
          morf = {"token": word, "norm_word": word, "tag": 'abbr', "pos": 'abbr', 'posrus': 'abbr',
                  'tagrus': 'abbr'}
          morf['phonetic'] = phonetic
          morf['analitic'] = analitic
          morf['lexic'] = ''
          morf['semantic'] = ''
          morfspis.append(morf)
          return morfspis
      #  жж.  сокр. слова
      k = re.findall(u'^[а-я]{1,2}\.$', word)
      if len(k) > 0:
          morf = {"token": word, "norm_word": word, "tag": 'abbr', "pos": 'abbr', 'posrus': 'abbr',
                  'tagrus': 'abbr'}
          morf['phonetic'] = phonetic
          morf['analitic'] = analitic
          morf['lexic'] = ''
          morf['semantic'] = ''
          morfspis.append(morf)
          return morfspis
      k = re.findall(u'[A-Za-z]{1,}', word)
      if len(k) > 0:
          #  Lat символ
          morf = {"token": word, "norm_word": word, "tag": 'Lat', "pos": 'Lat', 'posrus': 'Lat',
                  "tagrus": 'Lat'}
          morf['phonetic'] = phonetic
          morf['analitic'] = analitic
          morf['lexic'] = ''
          morf['semantic'] = ''
          morfspis.append(morf)
          return morfspis

      #k=re.findall(u'[А-ЯӘІҢҒҮҰҚӨҺа-яәіңғүұқөһ]+{1}', word)
      if len(word)==1:
          #  Неизвестный символ
          morf = {"token": word, "norm_word": word, "tag": 'Unknown', "pos": 'Unknown', 'posrus': 'Unknown',
                  "tagrus": 'Unknown'}
          morf['phonetic'] = phonetic
          morf['analitic'] = analitic
          morf['lexic'] = ''
          morf['semantic'] = ''
          morfspis.append(morf)
          return morfspis

      phonetic = self.phonetic(word)

      #  С прописной буквой
      FLE=False
      if word.istitle():
          FLE=True
      #word=word.lower()
      base = [word]
      for i in range(len(word)):
          if word[:-i].lower().endswith('-'):
              break
          base.append(word[:-i].lower())
          #  Список разбора слова
      spisokPOS=[]
      for w in base:
        if w=='':
          continue
        if len(w)==1:
            break
        endword=word[len(w):]
        lastchar=w[len(w)-1:]
        begchar=endword[0:1]

        #  Двойное слово
        try:
            try:
                pos = self.words2[w.lower()]
                pl = u'туынды, күрделі, анал., қос сөз, қосарлама'
            except:
                pos = self.words2kai[w.lower()]
                pl = u'туынды, күрделі, анал., қос сөз,  қайталама'
            '''
            sep=w.lower().split('-')
            if sep[0]==sep[1]:
                pl = u'туынды, күрделі, анал., қос сөз,  қайталама'
            else:
                pl = u'туынды, күрделі, анал., қос сөз, қосарлама'
            pl = u'туынды, күрделі, анал., қос сөз, қосарлама'
            '''

            #morf = {"token": word, "norm_word": w, "tag":'', "pos": 'зат', 'posrus': '',
            #        'tagrus': '' , 'analitic':pl}
            #morf['phonetic'] = phonetic
            #morfspis.append(morf)
            analitic = pl
            #return morfspis

        except:
           pass

           #  Слитные слова
        try:
               try:
                   pos = self.split115[w.lower()]
                   pl = u'тәсіл/аналитикалық/біріккен сөз'
               except:
                   try:
                       pos = self.splitrus[w.lower()]
                       pl = u'тәсіл/аналитикалық/біріккен сөз/кірме будан'
                   except:
                       pos = self.splitkaz[w.lower()]
                       pl = u'тәсіл/аналитикалық/біріккен сөз/төл будан'

               #morf = {"token": word, "norm_word": w, "tag": '', "pos": 'зат', 'posrus': '',
               #        'tagrus': '', 'analitic': pl}
               #morf['phonetic'] = ''
               #morfspis.append(morf)
               analitic = pl
               #return morfspis

        except:
               pass


        # Ищем аффиксы
        ps,part, lexic, semantic=self.postag(w.lower(), endword)
        #ps=self.postag(w, endword)


        if len(ps)>0:

            #createaffiks(w, )

              ok = 0
              for sp in spisokPOS:
                 for l in range(0,len(part)):
                    if part[l] in sp:
                        part.pop(l)
                        ps.pop(l)
                        break
                        #ok = 1
              #if len(part) == 0:
              #    continue
              for i in range(0,len(part)):
                  if part[i] not in spisokPOS:
                      #  Find  Afiks Create
                        anal=''

                        morf={"token": word,"norm_word":w, "tag":ps[i], "pos":part[i],'posrus':self.encript(part[i]),'tagrus':self.encript_afiks(ps[i]), 'analitic':anal}
                        morf['phonetic'] = phonetic
                        morf['analitic'] = analitic
                        morf['lexic'] = lexic[i]
                        morf['semantic'] = semantic[i]
                        morfspis.append(morf)
                        spisokPOS.append(part[i])


        else:
             #   Проверка на ассимиляцию
            if lastchar in Asimil:
                if begchar in Glasn:
                    w1=self.assimil(w)
                    ps,part, lexic, semantic=self.postag(w1, endword)
                    if len(ps)>0:
                         for i in range(0, len(part)):
                             if part[i] not in spisokPOS:
                                  morf={"token": word,"norm_word":w1, "tag":ps[i], "pos":part[i],'posrus':self.encript(part[i]),'tagrus':self.encript_afiks(ps[i])}
                                  morf['phonetic'] = phonetic
                                  morf['analitic'] = analitic
                                  morf['lexic'] = lexic[i]
                                  morf['semantic'] = semantic[i]
                                  morfspis.append(morf)
                                  #for pa in part:
                                  spisokPOS.append(part[i])
                             #continue

                    # ----------   выпадение т контракқа/контракт
            if begchar == u'к':
                                      w1 = w + u'кт'
                                      # endword = u'а' + endword[1:]
                                      ps, part, lexic, semantic = self.postag(w1, endword[1:])  # [1:]
                                      if len(ps) > 0:
                                          for i in range(0, len(part)):
                                              morf = {"token": word, "norm_word": w1, "tag": ps[i], "pos": part[i],
                                                      'posrus': self.encript(part[i]),
                                                      'tagrus': self.encript_afiks(ps[i])}
                                              morf['phonetic'] = phonetic
                                              morf['analitic'] =analitic
                                              morf['lexic'] = lexic[i]
                                              morf['semantic'] = semantic[i]
                                              morfspis.append(morf)
                                              for pa in part:
                                                  spisokPOS.append(pa)
                                              continue

                    # ----------   замена и на ы  оқи/оқы  оқисың/оқы оқиын/оқы
            if begchar == u'и':
                if len(endword)>0:
                    w1 = w + u'ы'
                    endword=u'й'+endword[1:]
                else:
                    w1 = w + u'ы'
                # endword = u'а' + endword[1:]
                ps, part, lexic, semantic = self.postag(w1, endword)  #[1:]
                if len(ps) > 0:
                 for i in range(0, len(part)):
                     morf = {"token": word, "norm_word": w1, "tag": ps[i], "pos": part[i],
                             'posrus': self.encript(part[i]), 'tagrus': self.encript_afiks(ps[i])}
                     morf['phonetic'] = phonetic
                     morf['analitic'] = analitic
                     morf['lexic'] = lexic[i]
                     morf['semantic'] = semantic[i]
                     morfspis.append(morf)
                     for pa in part:
                         spisokPOS.append(pa)
                     continue

                     # ----------   вставка і    шіриді/шірі +иді
            if begchar == u'и':
                         w1 = w + u'і'
                            # endword = u'й' + endword[1:]

                         # endword = u'а' + endword[1:]
                         ps, part, lexic, semantic = self.postag(w1, endword)  # [1:]
                         if len(ps) > 0:
                             for i in range(0, len(part)):
                                 morf = {"token": word, "norm_word": w1, "tag": ps[i], "pos": part[i],
                                         'posrus': self.encript(part[i]), 'tagrus': self.encript_afiks(ps[i])}
                                 morf['phonetic'] = phonetic
                                 morf['analitic'] = analitic
                                 morf['lexic'] = lexic[i]
                                 morf['semantic'] = semantic[i]
                                 morfspis.append(morf)
                                 for pa in part:
                                     spisokPOS.append(pa)
                                 continue


                     # ----------   замена я на а  жияды/жи
            if begchar == u'я':

                         w1 = w + u''
                         endword = u'а' + endword[1:]

                         ps, part, lexic, semantic = self.postag(w1, endword)  # [1:]
                         if len(ps) > 0:
                             for i in range(0, len(part)):
                                 morf = {"token": word, "norm_word": w1, "tag": ps[i], "pos": part[i],
                                         'posrus': self.encript(part[i]), 'tagrus': self.encript_afiks(ps[i])}
                                 morf['phonetic'] = phonetic
                                 morf['analitic'] = analitic
                                 morf['lexic'] = lexic[i]
                                 morf['semantic'] = semantic[i]
                                 morfspis.append(morf)
                                 for pa in part:
                                     spisokPOS.append(pa)
                                 continue

                     # ----------   замена сүй + у: сүю; күй +у: күю; түй+у: түю
            if begchar == u'ю':
                         w1 = w + u'й'
                         # endword = u'а' + endword[1:]
                         ps, part, lexic, semantic = self.postag(w1, endword[1:])
                         if len(ps) > 0:
                             for i in range(0, len(part)):
                                 if u'ет' not in spisokPOS:
                                     morf = {"token": word, "norm_word": w1, "tag": ps[i], "pos": part[i],
                                             'posrus': self.encript(part[i]), 'tagrus': self.encript_afiks(ps[i])}
                                     morf['phonetic'] = phonetic
                                     morf['analitic'] = analitic
                                     morf['lexic'] = lexic[i]
                                     morf['semantic'] = semantic[i]
                                     morfspis.append(morf)
                                     for pa in part:
                                         spisokPOS.append(pa)
                                     continue

                    # ----------   замена   тиюге/ти у/ТЕ+ге/БС
            if begchar == u'ю':
                                     w1 = w + u''
                                     endword = u'у' + endword[1:]
                                     ps, part, lexic, semantic = self.postag(w1, endword)
                                     if len(ps) > 0:
                                         for i in range(0, len(part)):
                                             if u'ет' not in spisokPOS:
                                                 morf = {"token": word, "norm_word": w1, "tag": ps[i], "pos": part[i],
                                                         'posrus': self.encript(part[i]),
                                                         'tagrus': self.encript_afiks(ps[i])}
                                                 morf['phonetic'] = phonetic
                                                 morf['analitic'] = analitic
                                                 morf['lexic'] = lexic[i]
                                                 morf['semantic'] = semantic[i]
                                                 morfspis.append(morf)
                                                 for pa in part:
                                                     spisokPOS.append(pa)
                                                 continue
                                     else:   #  мұңаюы/мұңай/ет у/ТЕ+ы/ТЖ-3
                                         w1 = w + u'й'
                                         endword = u'у' + endword[1:]
                                         ps, part, lexic, semantic = self.postag(w1, endword)
                                         if len(ps) > 0:
                                             for i in range(0, len(part)):
                                                 if u'ет' not in spisokPOS:
                                                     morf = {"token": word, "norm_word": w1, "tag": ps[i],
                                                             "pos": part[i],
                                                             'posrus': self.encript(part[i]),
                                                             'tagrus': self.encript_afiks(ps[i])}
                                                     morf['phonetic'] = phonetic
                                                     morf['analitic'] = analitic
                                                     morf['lexic'] = lexic[i]
                                                     morf['semantic'] = semantic[i]
                                                     morfspis.append(morf)
                                                     for pa in part:
                                                         spisokPOS.append(pa)
                                                     continue

            #  // проверка на перенос букв і ы  әріп әрпі қойын  - қойны, Ерін  -  ерні,  құлық  -   құлқы қорық қорқы аузында - ауыз
            if begchar==u'ы' or begchar==u'і':
                w1=w[0:-1]+begchar+lastchar
                ps,part, lexic, semantic=self.postag(w1, endword)
                if len(ps)>0:
                    for i in range(0, len(part)):
                      morf={"token": word,"norm_word":w1, "tag":ps[i], "pos":part[i],'posrus':self.encript(part[i]),'tagrus':self.encript_afiks(ps[i])}
                      morf['phonetic'] = phonetic
                      morf['analitic'] = analitic
                      morf['lexic'] = lexic[i]
                      morf['semantic'] = semantic[i]
                      morfspis.append(morf)
                      for pa in part:
                          spisokPOS.append(pa)
                      continue
            #------  құй+а+мын=құямын жай+а+мын=жаямын  қисайатын/қисай|атын
            if  begchar==u'я':
                w1=w+u'й'
                endword=u'а'+endword[1:]
                ps,part, lexic, semantic=self.postag(w1, endword)
                if len(ps)>0:
                    for i in range(0, len(part)):
                      morf={"token": word,"norm_word":w1, "tag":ps[i], "pos":part[i],'posrus':self.encript(part[i]),'tagrus':self.encript_afiks(ps[i])}
                      morf['phonetic'] = phonetic
                      morf['analitic'] = analitic
                      morf['lexic'] = lexic[i]
                      morf['semantic'] = semantic[i]
                      morfspis.append(morf)
                      for pa in part:
                          spisokPOS.append(pa)
                      continue
            #----------   тауып/тап   замена у на п
            if begchar == u'у':
                if len(endword)==1:
                    continue
                w1 = w + u'п'
                #endword = u'а' + endword[1:]
                ps, part, lexic, semantic = self.postag(w1, endword[1:])
                if len(ps) > 0:
                    for i in range(0, len(part)):
                        morf = {"token": word, "norm_word": w1, "tag": ps[i], "pos": part[i],
                                'posrus': self.encript(part[i]), 'tagrus': self.encript_afiks(ps[i])}
                        morf['phonetic'] = phonetic
                        morf['analitic'] = analitic
                        morf['lexic'] = lexic[i]
                        morf['semantic'] = semantic[i]
                        morfspis.append(morf)
                        for pa in part:
                            spisokPOS.append(pa)
                        continue
            # ----------   выпадение ы   жоруы/жоры
            if begchar == u'у':
                            w1 = w + u'ы'
                            # endword = u'а' + endword[1:]
                            ps, part, lexic, semantic = self.postag(w1, endword)
                            if len(ps) > 0:
                                for i in range(0, len(part)):
                                    morf = {"token": word, "norm_word": w1, "tag": ps[i], "pos": part[i],
                                            'posrus': self.encript(part[i]), 'tagrus': self.encript_afiks(ps[i])}
                                    morf['phonetic'] = phonetic
                                    morf['analitic'] = analitic
                                    morf['lexic'] = lexic[i]
                                    morf['semantic'] = semantic[i]
                                    morfspis.append(morf)
                                    for pa in part:
                                        spisokPOS.append(pa)
                                    continue

                                    # ----------   выпадение і рейтингісіне  рейтинг + сіне
            if begchar == u'і':
                                        w1 = w
                                        # endword = u'а' + endword[1:]
                                        ps, part, lexic, semantic = self.postag(w1, endword[1:])
                                        if len(ps) > 0:
                                            for i in range(0, len(part)):
                                                morf = {"token": word, "norm_word": w1, "tag": ps[i], "pos": part[i],
                                                        'posrus': self.encript(part[i]),
                                                        'tagrus': self.encript_afiks(ps[i])}
                                                morf['phonetic'] = phonetic
                                                morf['analitic'] = analitic
                                                morf['lexic'] = lexic[i]
                                                morf['semantic'] = semantic[i]
                                                morfspis.append(morf)
                                                for pa in part:
                                                    spisokPOS.append(pa)
                                                continue

                                    # ----------   выпадение т  нетіп/не
            if begchar == u'п':
                                        w1 = w+u'т'
                                        # endword = u'а' + endword[1:]
                                      #  ps, part = self.postag(w1, endword[1:])  ????
                                        ps, part, lexic, semantic = self.postag(w1, endword)
                                        if len(ps) > 0:
                                            for i in range(0, len(part)):
                                                morf = {"token": word, "norm_word": w1, "tag": ps[i], "pos": part[i],
                                                        'posrus': self.encript(part[i]),
                                                        'tagrus': self.encript_afiks(ps[i])}
                                                morf['phonetic'] = phonetic
                                                morf['analitic'] = analitic
                                                morf['lexic'] = lexic[i]
                                                morf['semantic'] = semantic[i]
                                                morfspis.append(morf)
                                                for pa in part:
                                                    spisokPOS.append(pa)
                                                continue


                                                # ----------   выпадение i    мүлгуге/мүлгі
            if begchar == u'у':
                 w1 = w + u'і'
                 # endword = u'а' + endword[1:]
                 ps, part, lexic, semantic = self.postag(w1, endword)
                 if len(ps) > 0:
                     for i in range(0, len(part)):
                         morf = {"token": word, "norm_word": w1, "tag": ps[i], "pos": part[i],
                                 'posrus': self.encript(part[i]), 'tagrus': self.encript_afiks(ps[i])}
                         morf['phonetic'] = phonetic
                         morf['analitic'] = analitic
                         morf['lexic'] = lexic[i]
                         morf['semantic'] = semantic[i]
                         morfspis.append(morf)
                         for pa in part:
                             spisokPOS.append(pa)
                         continue

                         # ----------   выпадение ы  Елбасын   Елбасы  + ын
            if begchar == u'ы':
                             w1 = w + u'ы'
                             # endword = u'а' + endword[1:]
                             ps, part, lexic, semantic = self.postag(w1, endword)
                             if len(ps) > 0:
                                 for i in range(0, len(part)):
                                    if part[i] not in spisokPOS:
                                         morf = {"token": word, "norm_word": w1, "tag": ps[i], "pos": part[i],
                                                 'posrus': self.encript(part[i]), 'tagrus': self.encript_afiks(ps[i])}
                                         morf['phonetic'] = phonetic
                                         morf['analitic'] = analitic
                                         morf['lexic'] = lexic[i]
                                         morf['semantic'] = semantic[i]
                                         morfspis.append(morf)
                                         #for pa in part:
                                         spisokPOS.append(part[i])
                                    continue


                                    # ----------   выпадение т  коммунист /коммуниссің
            if begchar == u'с':
                 w1 = w + u'ст'
                 # endword = u'а' + endword[1:]
                 ps, part, lexic, semantic = self.postag(w1, endword[1:])
                 if len(ps) > 0:
                     for i in range(0, len(part)):
                         morf = {"token": word, "norm_word": w1, "tag": ps[i], "pos": part[i],
                                 'posrus': self.encript(part[i]), 'tagrus': self.encript_afiks(ps[i])}
                         morf['phonetic'] = phonetic
                         morf['analitic'] = analitic
                         morf['lexic'] = lexic[i]
                         morf['semantic'] = semantic[i]
                         morfspis.append(morf)
                         for pa in part:
                             spisokPOS.append(pa)
                         continue

                         # ----------   выпадение ь  апрелінен/апрель
            if begchar == u'л' or begchar==u'т':
                             w1 = w +endword[0]+ u'ь'
                             # endword = u'а' + endword[1:]
                             ps, part, lexic, semantic = self.postag(w1, endword[1:])
                             if len(ps) > 0:
                                 for i in range(0, len(part)):
                                     morf = {"token": word, "norm_word": w1, "tag": ps[i], "pos": part[i],
                                             'posrus': self.encript(part[i]), 'tagrus': self.encript_afiks(ps[i])}
                                     morf['phonetic'] = phonetic
                                     morf['analitic'] = analitic
                                     morf['lexic'] = lexic[i]
                                     morf['semantic'] = semantic[i]
                                     morfspis.append(morf)
                                     for pa in part:
                                         spisokPOS.append(pa)
                                     continue

                                     # ----------   выпадение л  әкеп/әкел/ет іп/К
            if begchar == u'п':
                                         w1 = w + u'л'
                                         endword = u'і' + endword[1:]
                                         ps, part, lexic, semantic = self.postag(w1, endword)
                                         if len(ps) > 0:
                                             for i in range(0, len(part)):
                                                 morf = {"token": word, "norm_word": w1, "tag": ps[i], "pos": part[i],
                                                         'posrus': self.encript(part[i]),
                                                         'tagrus': self.encript_afiks(ps[i])}
                                                 morf['phonetic'] = phonetic
                                                 morf['analitic'] = analitic
                                                 morf['lexic'] = lexic[i]
                                                 morf['semantic'] = semantic[i]
                                                 morfspis.append(morf)
                                                 for pa in part:
                                                     spisokPOS.append(pa)
                                                 continue

                # ----------  выпадение ы   қырқады/қырық
            if begchar == u'қ':
                            w1 = w + u'ы'+endword[0]
                            # endword = u'а' + endword[1:]
                            ps, part, lexic, semantic = self.postag(w1, endword[1:])
                            if len(ps) > 0:
                                for i in range(0, len(part)):
                                    morf = {"token": word, "norm_word": w1, "tag": ps[i], "pos": part[i],
                                            'posrus': self.encript(part[i]), 'tagrus': self.encript_afiks(ps[i])}
                                    morf['phonetic'] = phonetic
                                    morf['analitic'] = analitic
                                    morf['lexic'] = lexic[i]
                                    morf['semantic'] = semantic[i]
                                    morfspis.append(morf)
                                    for pa in part:
                                        spisokPOS.append(pa)
                                    continue
            #----------------------------------------------------
            #   Тест на местоимение
        if w in self.spisrootmest:
            for mes in self.rootmestoimen:
                if w==mes[0]:
                    w1=mes[1]
                    ps,part, lexic, semantic=self.postag(w1, endword)
                    if len(ps)>0:
                        for parts in ps:
                            if u'ес' in parts:
                                if u'ес' not in spisokPOS:
                                    morf={"token": word,"norm_word":w1, "tag":parts, "pos":u'ес','posrus':self.encript(u'ес'),'tagrus':self.encript_afiks(parts)}
                                    morf['phonetic'] = phonetic
                                    morf['analitic'] = analitic
                                    morf['lexic'] = lexic[0]
                                    morf['semantic'] = semantic[0]
                                    morfspis.append(morf)
                                    for pa in part:
                                        spisokPOS.append(pa)
                                    break

        #-----------  Если с большой буквой возможно имя собственное
        if FLE:
              ps,part=self.postagFIOGEO(w.lower(), endword, self.fio,'fio')
              if len(ps)>0:
                  '''try:
                      morf["tag"].append(ps[0])
                      morf["pos"].append(part[0])
                      morf["posrus"].append(part[0])
                      morf["tagrus"].append(part[0])
                      morfspis.pop()
                  except:'''
                  morf={"token": word,"norm_word":w, "tag":'fio', "pos":'fio','posrus':'fio','tagrus':'fio'}
                  morf['phonetic'] = phonetic
                  morf['analitic'] = analitic
                  morf['lexic'] = ''
                  morf['semantic'] = ''
                  morfspis.append(morf)
              ps,part=self.postagFIOGEO(w.lower(), endword, self.geo,'geo')
              if len(ps)>0:
                  '''try:
                      morfspis.pop()
                      morf["tag"].append(ps[0])
                      morf["pos"].append(part[0])
                      morf["tagrus"].append(part[0])
                      #morf["posrus"].append(part[0])


                  except:'''
                  morf={"token": word,"norm_word":w, "tag":ps[0], "pos":part[0],'posrus':part[0],'tagrus':ps[0]}
                  morf['phonetic'] = phonetic
                  morf['analitic'] = analitic
                  morf['lexic'] = ''
                  morf['semantic'] = ''
                  morfspis.append(morf)


        #     Analitic   Afiks Create
          #   Find Afiks create
        if  len(morfspis) > 0:
            root = morfspis[0]['norm_word']
            if len(root)>len(w):
              try:
                  endword=root[-(len(root)-len(w)):]
                  poscr = self.slovar[w.lower()]
                  poscr = [x['pos'] for x in poscr]
                  for i in range(0, len(poscr)):

                      #  Find  Afiks Create
                      anal = ''
                      #for af in self.afikscreate[poscr[i].encode('utf-8')]:
                      for key in self.afikscreate.keys():
                          if key not in poscr:
                              continue
                          ok=0
                          for af in self.afikscreate[key]:
                              afi = af['afiks']  # .decode('utf-8')
                              afa = u'ыр'
                              if endword == af['afiks']:
                                  anal =endword+' -> '+ af['analitic']
                                  ok=1
                                  break

                          if ok==1:
                              break

                      if len(anal) > 0:
                          for mrelem in morfspis:
                              mrelem['analitic']=anal

                          break
                          '''
                          morf = {"token": root, "norm_word": w, "tag": 'T. '+poscr[i], "pos": poscr[i],
                                  'posrus': self.encript(poscr[i]), 'tagrus': self.encript_afiks(poscr[i]),
                                  'analitic': anal}
                          morf['phonetic'] = phonetic
                          morf['lexic'] = ''
                          morf['semantic'] = ''
                          morfspis.append(morf)
                          '''

                  #break

              except:
                  pass
        ok = 1

      if len(morfspis)==0:
           morf={"token": word,"norm_word":word, "tag":'Unknown', "pos":'Unknown','posrus':'Unknown', "tagrus":'Unknown'}
           morf['analitic'] = analitic
           morf['phonetic'] = phonetic
           morf['lexic'] = ''
           morf['semantic'] = ''
           morfspis.append(morf)
      #self.omonim(morfspis)
      return morfspis
#---------------------------------------------------------------------------------


if __name__ == '__main__':     # 
  line = u'жалтыр, кәрілеуін алмаған, Ең берігін, көріктісін таңдаған Бесікті де ертіп келiп отырмын өзі иіп жасаған, Шебер іздеп шеткі ауылға бармаған Содан бері өтті міне қанша жыл, О, ғажайып бесік беті жап-жасыл Күні кеше көктеп өскен сияқты.  '  #Сондай-ақ.
  filename=''
  #line = u'балада .'
  #print line

  #util.AccessToPicle()
  #exit(-1)
  #line=line.lower()


  morf=pyMorfKz()
  print (u"Идет загрузка базы")
  #

  sentenses=morf.SentenceExtract(line)
  verb2=[]
  for key in morf.verb2words:
      print (key)
      verb2.append(key+" ")
  #print (sentenses)
  for sent in sentenses:
    words=morf.WordExtract(sent)
    print (u"Парсинг")
    for word in words:
          ok=0
          verb=""
          for vb in verb2:
              if word+" " in vb:
                  if vb.find(word)==0:
                      i = words.index(word)
                      verb=vb
                      sl=vb.split(' ')
                      for s in sl:
                          if len(s)>0:
                              if words[i] in s:
                                  i+=1
                                  ok=1
                              else:
                                  ok=0
                                  break

                      if ok==1:
                          break
          if ok==1:
              p=1
              print("{0}  -  {1}".format(vb, morf.verb2words[vb[:len(vb)-1]]))
          m=morf.parse(word,1)
          for t in m:
              ok=1
              try:
                print (t['token'] + ' | ' + t['norm_word'] + ' <' + t['tag'] + ' | ' + t['tagrus'] + '>'+' lexic->'+ t['lexic']+' semantic->'+ t['semantic']+' analitic->'+ t['analitic']+' phonetic '+ t['phonetic'])
              except:
                  print(t['token'] + ' | ' + t['norm_word'] + ' <' + t['tag'] + ' | ' + t['tagrus'] + '>'+' lexic->'+ t['lexic']+' semantic->'+ t['semantic']  + ' phonetic ' + t['phonetic'])
            #print word
            #print(l["norm_word"])
            #for i in range(0,len(l["tag"])):
            #      print u"%s norm_word=%s Pos=%s  PosRus=%s  TagRus=%s" % (word,l["norm_word"],l["tag"][i],l["posrus"][i],l["tagrus"][i])

#-----------------------------
#  Перенос из Базы Access в файл
  #util.AccessToPicle()

  print ('ok!')
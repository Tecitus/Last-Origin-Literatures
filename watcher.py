import requests
import dc_apiwip
import peewee
import datetime
import db
from time import sleep
from retry import retry
import subprocess
from batchindexer import makeindex
import urllib3
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0"}

targetboard = "lastorigin"
today = datetime.datetime.now()
nextday = datetime.datetime(today.year,today.month,today.day,0,0,0) + datetime.timedelta(days=1)

#indfile = open('index.html','a')
giturl = 'https://tecitus.github.io/Last-Origin-Literatures/html/'
'''(requests.exceptions.ConnectionError,peewee.OperationalError)'''
@retry(Exception,tries=99,delay=60)
def gitpush():
  print('gitpush')
  global nextday
  if datetime.datetime.now()< nextday:
    return
  print('premakeindex')
  makeindex()
  print('pregit')
  subprocess.run(['git','add','*'])
  subprocess.run(['git','commit','-m','\'{} regular commit.\''.format(nextday.strftime("%Y-%m-%d"))])
  #subprocess.run(['git','remote','add','origin','https://github.com/Tecitus/Last-Origin-Literature'])
  subprocess.run(['git','push','-u','origin','master'])
  nextday += datetime.timedelta(days=1)
  print('gitpushdone')

'''(urllib3.exceptions.ReadTimeoutError,requests.exceptions.ConnectionError,peewee.OperationalError)'''
@retry(Exception,tries=99,delay=60)
def wrapper(doc):
    if not ((('단' in doc['title']) and ('편' in doc['title'])) or (('문' in doc['title']) and ('학' in doc['title'])) or ((('야' in doc['title']) or ('소' in doc['title'])) and ('설' in doc['title']))):
      return False
    try:
      db.Archive.get(archiveid = int(doc["id"]))
      return True
    except db.Archive.DoesNotExist:
      try:
        db.Blacklist.get(archiveid = int(doc["id"]))
        return False
      except db.Blacklist.DoesNotExist:
        today = datetime.datetime.now()
        if ':' in doc['time']:
          hm = doc['time'].split(':')
          t = datetime.datetime(today.year,today.month,today.day,int(hm[0]),int(hm[1]))
        else:
          if len(doc['time'].split('.')) is 2:
            t = datetime.datetime.strptime('{} '.format(str(today.year))+doc['time'],'%Y %m.%d')
          else:
            t = datetime.datetime.strptime(doc['time'],'%Y.%m.%d')
        url = "https://gall.dcinside.com/mgallery/board/view/?id={}&no={}".format(targetboard, doc['id'])
        params = (('id', targetboard),('no', doc['id']))
        html = requests.get(url, headers=headers, params=params).text
        try:
          db.Archive.create(archiveid = int(doc["id"]), title = doc["title"], url = url, html = html, author = doc['author'], time = t)
        except peewee.IntegrityError:
          return False
        f = open('html/{}.html'.format(doc["id"]),'w')
        f.write(html)
        f.close()
        #indfile.write('<div>{} {} <a href="{}">{}</a> {}</div>\n'.format(doc['id'],doc['author'],giturl+doc['id']+'.html',doc['title'],t.strftime("%Y-%m-%d")))
        print(doc['id'],doc['author'],doc['title'],t,html[:10])

while True:
  for doc in dc_apiwip.board(board_id=targetboard,skip_contents=True,num=50):
    isoverlapped = None
    isoverlapped = wrapper(doc)
    if isoverlapped:
      break
  gitpush()
  sleep(120)

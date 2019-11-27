import requests
import dc_apiwip
import peewee
import datetime
import db
from retry import retry

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0"}

targetboard = "lastorigin"



@retry((requests.exceptions.ConnectionError,peewee.OperationalError),tries=5,delay=10)
def wrapper(doc):
  if not ((('단' in doc['title']) and ('편' in doc['title'])) or (('문' in doc['title']) and ('학' in doc['title'])) or ((('야' in doc['title']) or ('소' in doc['title'])) and ('설' in doc['title']))):
    return
  try:
    db.Archive.get(archiveid = int(doc["id"]))
  except db.Archive.DoesNotExist:
    try:
      db.Blacklist.get(archiveid = int(doc["id"]))
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
      if not doc['author'] or len(doc['author']) == 0:
        author = "Unknown"
      else:
        author = doc['author']
      try:
        db.Archive.create(archiveid = int(doc["id"]), title = doc["title"], url = url, html = html, author = author, time = t)
      except peewee.IntegrityError:
        return
      f = open('html/{}.html'.format(doc["id"]),'w')
      f.write(html)
      f.close()
      print(doc['id'],doc['author'],doc['title'],t,html[:10])


for doc in dc_apiwip.board(board_id=targetboard,skip_contents=True):
  wrapper(doc)

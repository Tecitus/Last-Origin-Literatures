import db
import datetime
#indexes = db.Archive.select()

def makeindex():
  f = open('index.html','w')
  url = "https://tecitus.github.io/Last-Origin-Literatures/html/"
  dcurl = "https://gall.dcinside.com/mgallery/board/view/?id=lastorigin&no={}"
  indexes = db.Archive.select()
  for ind in indexes.order_by(db.Archive.archiveid).iterator():
    if(type(ind.time) == type('str')):
      f.write('<div><a href="{}">{}</a> {} <a href="{}">{}</a> {}</div>\n'.format(dcurl.format(str(ind.archiveid)),str(ind.archiveid),ind.author,url+str(ind.archiveid)+'.html',ind.title,ind.time[:10]))
    else:
      f.write('<div><a href="{}">{}</a> {} <a href="{}">{}</a> {}</div>\n'.format(dcurl.format(str(ind.archiveid)),str(ind.archiveid),ind.author,url+str(ind.archiveid)+'.html',ind.title,ind.time.strftime("%Y-%m-%d")))
  f.close()

def makeblackindex():
  f = open('blackindex.html','w')
  url = "https://tecitus.github.io/Last-Origin-Literatures/html/"
  dcurl = "https://gall.dcinside.com/mgallery/board/view/?id=lastorigin&no={}"
  indexes = db.Blacklist.select()
  s = ''
  for ind in indexes.order_by(db.Blacklist.archiveid).iterator():
    if(type(ind.updated) == type('str')):
      f.write('<div><a href="{}">{}</a> {} <a href="{}">{}</a> {} {}</div>\n'.format(dcurl.format(str(ind.archiveid)),str(ind.archiveid),ind.author,url+str(ind.archiveid)+'.html',ind.title,ind.updated,ind.reason))
    else:
      f.write('<div><a href="{}">{}</a> {} <a href="{}">{}</a> {} {}</div>\n'.format(dcurl.format(str(ind.archiveid)),str(ind.archiveid),ind.author,url+str(ind.archiveid)+'.html',ind.title,ind.updated.strftime("%Y-%m-%d %H:%M:%S",ind.reason)))
  f.close()

if __name__ is '__main__':
  makeindex()

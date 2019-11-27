from peewee import *

db = PostgresqlDatabase('lastorigin', user='lao', password='12345', host='172.30.1.19', port=5432)

class BaseModel(Model):
  id = BigAutoField(primary_key=True,unique=True)
  class Meta:
    database = db

class Archive(BaseModel):
  archiveid = BigIntegerField()
  title = CharField(max_length=256)
  author = CharField(max_length=64)
  time = DateTimeField()
  html = TextField()
  url = CharField(max_length=90)

class Blacklist(BaseModel):
  archiveid = BigIntegerField()
  title = CharField(max_length=256)
  author = CharField(max_length=64)
  reason = CharField(max_length=64)
  url = CharField(max_length=90)
  updated = DateTimeField()

db.connect()
db.create_tables([Archive,Blacklist])

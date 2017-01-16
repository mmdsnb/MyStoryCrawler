#!encoding:utf-8


import inspect, os
import sqlite3
from prettytable import PrettyTable 
import sqlalchemy
from sqlalchemy import Table,Column,Integer,String,MetaData,ForeignKey,TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.orm import sessionmaker  
from sqlalchemy.sql import select
from datetime import datetime
import time
import logging
import sys
import copy

logging.basicConfig(level=logging.DEBUG)
reload(sys)
sys.setdefaultencoding('utf8')

dbpath= os.path.dirname(inspect.stack()[0][1])+os.path.sep+'data.db'
engine=sqlalchemy.create_engine(r'sqlite:///'+dbpath,echo=False)
Base = declarative_base()



class BookIndex(Base):

	__tablename__ ='bookIndex'
	id = Column(Integer,primary_key=True)
	name = Column(String)
	dirName = Column(String)
	url = Column(String)
	status = Column(Integer)
	updateTime = Column(TIMESTAMP)

	def __init__(self,name,dirName,url):
		self.name=name
		self.dirName=dirName
		self.url=url
		self.status=0
		self.updateTime=datetime.now()



metadata=Base.metadata
metadata.create_all(engine)
session = sessionmaker(bind=engine,autoflush=False)() 


def addBookIndex(name,dirName,url):
	book=BookIndex(name,dirName,url)
	session.add(book)
	session.commit()

def addBookIndexes(bookIndexes):
	session.add_all(bookIndexes)
	session.commit()	


def getBookIndexById(id):
	result =  session.query(BookIndex).filter(BookIndex.id==id).first()
	session.close()
	return result


def getBookIndexesByName(bookname):
	result =  session.query(BookIndex).filter_by(name=bookname).filter_by(status=0).order_by(BookIndex.id).all()
	session.commit()
	session.close()
	return result

def updateStatus(bookIndex):
	bookIndex.status=2
	# session.query(BookIndex).filter_by(id=id).update({"status":2})
	session.commit()












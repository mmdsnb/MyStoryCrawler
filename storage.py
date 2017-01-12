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



dbpath= os.path.dirname(inspect.stack()[0][1])+os.path.sep+'data.db'
engine=sqlalchemy.create_engine(r'sqlite:///'+dbpath,echo=True)
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
session = sessionmaker(bind=engine)() 


def addBookIndex(name,dirName,url):
	book=BookIndex(name,dirName,url)
	session.add(book)
	session.commit()

def addBookIndexes(bookIndexes):
	session.add_all(bookIndexes)
	session.commit()	


def getBookIndexesByName(bookname):
	result =  session.query(BookIndex).filter_by(name=bookname).filter_by(status=0).order_by(BookIndex.id).all()
	return result

def getBookIndexById(id):
	result =  session.query(BookIndex).filter_by(id=id).first()
	return result


def demo3():
	result= session.query(BookIndex).filter_by(id=2).filter_by(name='a').all()
	for u in result:
		print(u.name)

















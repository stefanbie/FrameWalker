import mysql.connector
from peewee import *

cnx = mysql.connector.connect(user='dbuser', password='dbuser',
                          host='127.0.0.1',
                          database='Mysql')
cnx.close()
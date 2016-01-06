from peewee import *
from datetime import datetime
#pip install peewee
#pip install PyMySQL
# In %PROGRAMDATA%\MySQL\MySQL Server X.x\my.ini, remove STRICT_TRANS_TABLES and restart MySQL servcie

DB = MySQLDatabase("frameway", host="127.0.0.1", port=3306, user="dbuser", passwd="dbuser")

class BaseModel(Model):
    """A base model that will use our MySQL database"""
    class Meta:
        database = DB

class TestCase(BaseModel):
    timeStamp = DateTimeField('%Y-%m-%d %H:%M:%S.%f')
    comment = TextField()

class Transaction(BaseModel):
    testCase = ForeignKeyField(TestCase, related_name='transaction')
    name = CharField()
    timeStamp = DateTimeField('%Y-%m-%d %H:%M:%S.%f')
    iteration = IntegerField()

class Frame(BaseModel):
    transaction = ForeignKeyField(Transaction, related_name='frame')
    url = TextField()

class Timing(BaseModel):
    frame = ForeignKeyField(Frame, related_name='timing')
    connectEnd = IntegerField()
    connectStart = IntegerField()
    domComplete = IntegerField()
    domContentLoadedEventEnd = IntegerField()
    domContentLoadedEventStart = IntegerField()
    domInteractive = IntegerField()
    domLoading = IntegerField()
    domainLookupEnd = IntegerField()
    domainLookupStart = IntegerField()
    fetchStart = IntegerField()
    loadEventEnd = IntegerField()
    loadEventStart = IntegerField()
    navigationStart = IntegerField()
    redirectEnd = IntegerField()
    redirectStart = IntegerField()
    requestStart = IntegerField()
    responseEnd = IntegerField()
    responseStart = IntegerField()
    secureConnectionStart = IntegerField()
    unloadEventEnd = IntegerField()
    unloadEventStart = IntegerField()

class ResourceTiming(BaseModel):
    frame = ForeignKeyField(Frame,default=None, null=True, related_name='resource')
    connectEnd = FloatField()
    connectStart = FloatField()
    domainLookupEnd = FloatField()
    domainLookupStart = FloatField()
    duration = FloatField()
    entryType = CharField()
    fetchStart = FloatField()
    initiatorType = CharField()
    name = TextField(default="default")
    redirectEnd = FloatField()
    redirectStart = FloatField()
    requestStart = FloatField()
    responseEnd = FloatField()
    responseStart = FloatField()
    secureConnectionStart = FloatField()
    startTime = FloatField()
    workerStart = FloatField()

def insertTestCase(timeStamp, comment):
    return TestCase.create(timeStamp=timeStamp, comment=comment)

def insertTransaction(testCaseID, timeStamp, name, iteration):
    return Transaction.create(testCase = testCaseID, timeStamp = timeStamp, name=name, iteration=iteration)

def insertFrame(transactionID, url):
    return Frame.create(transaction = transactionID, url = url)

def insertRecourceTimings(frameID, recourseTimings):
    for item in recourseTimings:
        item.update( {"frame":frameID})
    with DB.atomic():
        return ResourceTiming.insert_many(recourseTimings).execute()

def init():
    DB.connect()

def destroy():
    DB.close()

#DB.create_tables([Frame, ResourceTiming, TestCase, Transaction])


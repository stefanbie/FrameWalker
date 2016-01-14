from peewee import *
#pip install peewee
#pip install PyMySQL
# In %PROGRAMDATA%\MySQL\MySQL Server X.x\my.ini, remove STRICT_TRANS_TABLES and restart MySQL servcie

DB = MySQLDatabase("frameway", host="127.0.0.1", port=3306, user="dbuser", passwd="dbuser")
timeStampFormat = '%Y-%m-%d %H:%M:%S.%f'


class BaseModel(Model):
    class Meta:
        database = DB


class TestCase(BaseModel):
    timeStamp = DateTimeField(timeStampFormat)
    comment = TextField()


class Transaction(BaseModel):
    testCase = ForeignKeyField(TestCase, related_name='transaction')
    name = CharField()
    timeStamp = DateTimeField(timeStampFormat)
    iteration = IntegerField()


class Frame(BaseModel):
    transaction = ForeignKeyField(Transaction, related_name='frame')
    parentID = IntegerField()
    src = TextField()
    attributes = TextField()


class Timing(BaseModel):
    frame = ForeignKeyField(Frame, default=None, null=True, related_name='timing')
    navigationStart = DoubleField();            redirectStart = DoubleField();          redirectEnd = DoubleField()
    fetchStart = DoubleField();                 domainLookupStart = DoubleField();      domainLookupEnd = DoubleField()
    connectStart = DoubleField();               secureConnectionStart = DoubleField();  connectEnd = DoubleField()
    requestStart = DoubleField();               responseStart = DoubleField();          responseEnd = DoubleField()
    domLoading = DoubleField();                 domInteractive = DoubleField();         domContentLoadedEventStart = DoubleField()
    domContentLoadedEventEnd = DoubleField();   domComplete = DoubleField();            loadEventStart = DoubleField()
    loadEventEnd = DoubleField();               unloadEventEnd = DoubleField();         unloadEventStart = DoubleField()
    redirect_time = IntegerField();             appCache_time = IntegerField();         DNS_time = IntegerField()
    DNSTCP_time = IntegerField();               TCP_time = IntegerField();              blocked_time = IntegerField()
    request_time = IntegerField();              dom_time = IntegerField();              onLoad_time = IntegerField()
    total_time = IntegerField();                relativeMain = IntegerField(default=-1)


class Resource(BaseModel):
    frame = ForeignKeyField(Frame, default=None, null=True, related_name='resource')
    name = TextField()
    startTime = IntegerField()
    duration = IntegerField()


def insertTestCase(timeStamp, comment):
    return TestCase.create(timeStamp=timeStamp, comment=comment)


def insertTransaction(testCaseID, timeStamp, name, iteration):
    return Transaction.create(testCase=testCaseID, timeStamp=timeStamp, name=name, iteration=iteration)


def insertFrame(transactionID, parentID, src, attributes):
    return Frame.create(transaction=transactionID, parentID=parentID, src=src, attributes=attributes)


def insertTiming(frameID, timing):
    timing["frame"] = frameID
    return Timing.insert(timing).execute()


def insertRecources(frameID, recourse):
    if len(recourse) > 0:
        for item in recourse:
            item.update({"frame":frameID})
        with DB.atomic():
            return Resource.insert_many(recourse).execute()
    return None


def init():
    DB.connect()
    if not TestCase.table_exists():
        addTables()


def destroy():
    DB.close()


def addTables():
    DB.create_tables([TestCase, Transaction, Frame, Resource, Timing])


def addRelMain(transaction):
    timings = Timing.select().order_by(+Timing.navigationStart).join(Frame).where(Frame.transaction == transaction.get_id())
    minStart = timings[0].navigationStart
    for timing in timings:
        timing.relativeMain = timing.navigationStart - minStart
        timing.save()
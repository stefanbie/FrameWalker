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
    test_case_id = PrimaryKeyField()
    test_case_timestamp = DateTimeField(timeStampFormat)
    comment = TextField()


class Transaction(BaseModel):
    transaction_id = PrimaryKeyField()
    test_case = ForeignKeyField(TestCase, related_name='transaction')
    transaction_name = CharField()
    timestamp = DateTimeField(timeStampFormat)
    iteration = IntegerField()


class Frame(BaseModel):
    frame_id = PrimaryKeyField()
    transaction = ForeignKeyField(Transaction, related_name='frame')
    parent_id = IntegerField()
    frid = CharField()
    src = TextField()
    hashed_src = CharField()
    attributes = TextField()


class Timing(BaseModel):
    timing_id = PrimaryKeyField()
    frame = ForeignKeyField(Frame, default=None, null=True, related_name='timing')
    navigationStart = DoubleField();            redirectStart = DoubleField();          redirectEnd = DoubleField()
    fetchStart = DoubleField();                 domainLookupStart = DoubleField();      domainLookupEnd = DoubleField()
    connectStart = DoubleField();               secureConnectionStart = DoubleField();  connectEnd = DoubleField()
    requestStart = DoubleField();               responseStart = DoubleField();          responseEnd = DoubleField()
    domLoading = DoubleField();                 domInteractive = DoubleField();         domContentLoadedEventStart = DoubleField()
    domContentLoadedEventEnd = DoubleField();   domComplete = DoubleField();            loadEventStart = DoubleField()
    loadEventEnd = DoubleField();               unloadEventEnd = DoubleField();         unloadEventStart = DoubleField()
    redirect_time = IntegerField();             appcache_time = IntegerField();         dns_time = IntegerField()
    dnstcp_time = IntegerField();               tcp_time = IntegerField();              blocked_time = IntegerField()
    request_time = IntegerField();              dom_time = IntegerField();              onload_time = IntegerField()
    total_time = IntegerField();                relative_main_time = IntegerField(default=-1)


class Resource(BaseModel):
    resource_id = PrimaryKeyField()
    frame = ForeignKeyField(Frame, default=None, null=True, related_name='resource')
    name = TextField()
    startTime = IntegerField()
    duration = IntegerField()


def insertTestCase(timeStamp, comment):
    return TestCase.create(test_case_timestamp=timeStamp, comment=comment)


def insertTransaction(testCaseID, timeStamp, transactionName, iteration):
    return Transaction.create(test_case=testCaseID, timestamp=timeStamp, transaction_name=transactionName, iteration=iteration)


def insertFrame(transactionID, parentID, frid, src, hashedSrc, attributes):
    return Frame.create(transaction=transactionID, parent_id=parentID, frid=frid, src=src, hashed_src=hashedSrc, attributes=attributes)


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
        timing.relative_main_time = timing.navigationStart - minStart
        timing.save()

def lastNavigationStart(transaction):
    timings = Timing.select().order_by(+Timing.navigationStart).join(Frame).where(Frame.transaction == transaction.get_id()-1)
    try:
        return timings[0].navigationStart
    except Exception:
        return -1

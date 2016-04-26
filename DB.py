from peewee import *

'''
Setup:
    pip install peewee
    pip install PyMySQL
    In %PROGRAMDATA%\MySQL\MySQL Server X.x\my.ini, remove STRICT_TRANS_TABLES and restart MySQL servcie

Cleanup:
    DROP TABLE `frameway`.`resource`;
    DROP TABLE `frameway`.`timing`;
    DROP TABLE `frameway`.`frame`;
    DROP TABLE `frameway`.`transaction`;
    DROP TABLE `frameway`.`testcase`
'''

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
    transaction_start_time = DoubleField(default=-1)
    transaction_time = IntegerField(default=-1)


class Frame(BaseModel):
    frame_id = PrimaryKeyField()
    transaction = ForeignKeyField(Transaction, related_name='frame')
    frid = CharField()
    src = TextField()
    hashed_src = CharField()
    attributes = TextField()
    frame_relative_start_time = IntegerField(default=-1)
    frame_time = IntegerField(default=-1)
    resources_relative_start_time = IntegerField(default=-1)
    resources_time = IntegerField(default=-1)


class Timing(BaseModel):
    timing_id = PrimaryKeyField()
    frame = ForeignKeyField(Frame, default=None, null=True, related_name='timing')
    navigationStart = DoubleField()
    redirectStart = DoubleField()
    redirectEnd = DoubleField()
    fetchStart = DoubleField()
    domainLookupStart = DoubleField()
    domainLookupEnd = DoubleField()
    connectStart = DoubleField()
    secureConnectionStart = DoubleField()
    connectEnd = DoubleField()
    requestStart = DoubleField()
    responseStart = DoubleField()
    responseEnd = DoubleField()
    domLoading = DoubleField()
    domInteractive = DoubleField()
    domContentLoadedEventStart = DoubleField()
    domContentLoadedEventEnd = DoubleField()
    domComplete = DoubleField()
    loadEventStart = DoubleField()
    loadEventEnd = DoubleField()
    unloadEventEnd = DoubleField()
    unloadEventStart = DoubleField()
    redirect_time = IntegerField()
    appcache_time = IntegerField()
    dns_time = IntegerField()
    dnstcp_time = IntegerField()
    tcp_time = IntegerField()
    blocked_time = IntegerField()
    request_time = IntegerField()
    dom_time = IntegerField()
    onload_time = IntegerField()
    timing_relative_start_time = IntegerField(default=-1)
    timing_time = IntegerField(default=-1)


class Resource(BaseModel):
    resource_id = PrimaryKeyField()
    frame = ForeignKeyField(Frame, default=None, null=True, related_name='resource')
    name = TextField()
    startTime = IntegerField()
    absolute_start_time = DoubleField(default=-1)
    absolute_end_time = DoubleField(default=-1)
    resource_relative_start_time = IntegerField(default=-1)
    resource_time = IntegerField(default=-1)


def insertTestCase(timeStamp, comment):
    return TestCase.create(test_case_timestamp=timeStamp, comment=comment)


def insertTransaction(testCaseID, timeStamp, transactionName, iteration):
    return Transaction.create(test_case=testCaseID, timestamp=timeStamp, transaction_name=transactionName,
                              iteration=iteration)


def insertFrame(transactionID, frid, src, hashedSrc, attributes):
    return Frame.create(transaction=transactionID, frid=frid, src=src, hashed_src=hashedSrc, attributes=attributes)


def insertTiming(frameID, timing):
    timing["frame"] = frameID
    return Timing.insert(timing).execute()


def insertRecources(frameID, recourse):
    if len(recourse) > 0:
        for item in recourse:
            item.update({"frame": frameID})
        with DB.atomic():
            return Resource.insert_many(recourse).execute()
    return None


def addTransactionTimes(transaction):
    timingStartTimes = Timing.select(Timing.navigationStart.alias('starttime')).join(Frame).where(Frame.transaction == transaction.transaction_id)
    resourceStartTimes = Resource.select(Resource.absolute_start_time.alias('starttime')).join(Frame).where(Frame.transaction == transaction.transaction_id)
    startTime = (timingStartTimes | resourceStartTimes).order_by(+SQL('starttime')).get().starttime
    Transaction.update(transaction_start_time = startTime).where(Transaction.transaction_id==transaction.transaction_id).execute()

    timingEndTimes = Timing.select(Timing.loadEventEnd.alias('endtime')).join(Frame).where(Frame.transaction == transaction.transaction_id)
    resourceEndTimes = Resource.select(Resource.absolute_end_time.alias('endtime')).join(Frame).where(Frame.transaction == transaction.transaction_id)
    endTime = (timingEndTimes | resourceEndTimes).order_by(-SQL('endtime')).get().endtime
    Transaction.update(transaction_time=endTime - startTime).where(Transaction.transaction_id==transaction.transaction_id).execute()


def addFrameTimes(transaction):
    transactionStartTime = TransactionStartTime(transaction)
    frames = Frame.select().where(Frame.transaction == transaction.transaction_id).execute()
    for frame in frames:
        #Add frame_relative_start_time
        timingStartTimes = Timing.select(Timing.navigationStart.alias('starttime')).where(Timing.frame == frame.frame_id)
        resourceStartTimes = Resource.select(Resource.absolute_start_time.alias('starttime')).where(Resource.frame == frame.frame_id)
        startTime = (timingStartTimes | resourceStartTimes).order_by(+SQL('starttime')).get().starttime
        Frame.update(frame_relative_start_time=startTime-transactionStartTime).where(Frame.frame_id == frame.frame_id).execute()
        #Add frame_time
        timingEndTimes = Timing.select(Timing.loadEventEnd.alias('endtime')).where(Timing.frame == frame.frame_id)
        resourceEndTimes = Resource.select(Resource.absolute_end_time.alias('endtime')).where(Resource.frame == frame.frame_id)
        endTime = (timingEndTimes | resourceEndTimes).order_by(-SQL('endtime')).get().endtime
        Frame.update(frame_time=endTime - startTime).where(Frame.frame_id == frame.frame_id).execute()



def addTimingTimes(transaction):
    transactionStartTime = TransactionStartTime(transaction)
    query = 'update timing ' \
            'join frame ' \
            'on frame.frame_id = timing.frame_id ' \
            'set timing_relative_start_time = timing.navigationStart - %d ' \
            'where frame.transaction_id = %d' \
            % (transactionStartTime, transaction.transaction_id)
    DB.execute_sql(query)


def addResourceTimes(transaction):
    transactionStartTime = TransactionStartTime(transaction)
    query = 'update resource ' \
            'join frame ' \
            'on frame.frame_id = resource.frame_id ' \
            'set resource_relative_start_time = resource.absolute_start_time - %d ' \
            'where frame.transaction_id = %d' \
            % (transactionStartTime, transaction.transaction_id)
    DB.execute_sql(query)

    frames = Frame.select().where(Frame.transaction == transaction.transaction_id).execute()
    for frame in frames:
        #Add resources_relative_start_time
        try:
            resources_relative_start_time = Resource.select(Resource.resource_relative_start_time).where(Resource.frame == frame.frame_id).order_by(+Resource.resource_relative_start_time).get().resource_relative_start_time
        except DoesNotExist:
            resources_relative_start_time = -1
        Frame.update(resources_relative_start_time=resources_relative_start_time).where(Frame.frame_id == frame.frame_id).execute()
        #Add resources_time
        try:
            absolute_start_time = Resource.select(Resource.absolute_start_time).where(Resource.frame == frame.frame_id).order_by(+Resource.resource_relative_start_time).get().absolute_start_time
            absolute_end_time = Resource.select(Resource.absolute_end_time).where(Resource.frame == frame.frame_id).order_by(-Resource.absolute_end_time).get().absolute_end_time
        except DoesNotExist:
            absolute_end_time = -1
            absolute_start_time = -1
        totalResourcesTime = absolute_end_time - absolute_start_time
        Frame.update(resources_time=totalResourcesTime).where(Frame.frame_id == frame.frame_id).execute()

def TransactionStartTime(transaction):
    return Transaction.select(Transaction.transaction_start_time).where(Transaction.transaction_id == transaction.transaction_id).get().transaction_start_time


def timingExist(navigationStart):
    try:
        Timing.select().where(Timing.navigationStart == navigationStart).get()
    except Timing.DoesNotExist:
        return False
    return True


def updateFrame(frame, totalResourceTime, relativeResourceTime):
    Frame.update(resources_time=totalResourceTime).where(Frame.frame_id == frame.frame_id).execute()
    Frame.update(resources_relative_start_time=relativeResourceTime).where(Frame.frame_id == frame.frame_id).execute()


def init():
    DB.connect()
    if not TestCase.table_exists():
        addTables()


def destroy():
    DB.close()


def addTables():
    DB.create_tables([TestCase, Transaction, Frame, Resource, Timing])


def addRelTimings(transaction):
    timings = Timing.select().order_by(+Timing.navigationStart).join(Frame).where(
        Frame.transaction == transaction.get_id())
    minStart = timings[0].navigationStart
    for timing in timings:
        timing.relative_main_time = timing.navigationStart - minStart
        timing.save()



def addRelResources(transaction):
    resources = Resource.select().order_by(+Resource.startTime).join(Frame).where(
        Frame.transaction == transaction.get_id())
    minStart = resources[0].startTime
    for resource in resources:
        resource.relative_main_time = timing.navigationStart - minStart
        timing.save()

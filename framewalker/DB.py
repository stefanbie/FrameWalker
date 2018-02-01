from peewee import *
'''
Setup:

    Python:
    pip install peewee
    pip install PyMySQL

DB:

    Install MySQL
    Install MySQL Workbench
    Add new schema "framewalker"
    In %PROGRAMDATA%\MySQL\MySQL Server X.x\my.ini, remove STRICT_TRANS_TABLES and restart MySQL servcie

Create view:

CREATE
    ALGORITHM = UNDEFINED
    DEFINER = `root`@`localhost`
    SQL SECURITY DEFINER
VIEW `all` AS
    SELECT
        `testrun`.`test_run_timestamp` AS `test_run_timestamp`,
        `testrun`.`test_run_product` AS `test_run_product`,
        `testrun`.`test_run_release` AS `test_run_release`,
        `testrun`.`test_run_comment` AS `test_run_comment`,
        `transaction`.`transaction_timestamp` AS `transaction_timestamp`,
        `transaction`.`transaction_name` AS `transaction_name`,
        `transaction`.`transaction_iteration` AS `transaction_iteration`,
        `transaction`.`transaction_time` AS `transaction_time`,
        `frame`.`frame_attributes` AS `frame_attributes`,
        `frame`.`frame_hashed_src` AS `frame_hashed_src`,
        `frame`.`frame_src` AS `frame_src`,
        `frame`.`frame_relative_start_time` AS `frame_relative_start_time`,
        `frame`.`frame_time` AS `frame_time`,
        `frame`.`frame_resources_relative_start_time` AS `frame_resources_relative_start_time`,
        `frame`.`frame_resources_time` AS `frame_resources_time`,
        NULL AS `resource_name`,
        NULL AS `resource_time`,
        NULL AS `resource_relative_start_time`,
        `timing`.`timing_time` AS `timing_time`,
        `timing`.`timing_relative_start_time` AS `timing_relative_start_time`
    FROM
        (((`testrun`
        JOIN `transaction` ON ((`testrun`.`test_run_id` = `transaction`.`test_run_id`)))
        JOIN `frame` ON ((`transaction`.`transaction_id` = `frame`.`transaction_id`)))
        JOIN `timing` ON ((`frame`.`frame_id` = `timing`.`frame_id`)))
    WHERE
        (`testrun`.`test_run_product` = 'News')
    UNION SELECT
        `testrun`.`test_run_timestamp` AS `test_run_timestamp`,
        `testrun`.`test_run_product` AS `test_run_product`,
        `testrun`.`test_run_release` AS `test_run_release`,
        `testrun`.`test_run_comment` AS `test_run_comment`,
        `transaction`.`transaction_timestamp` AS `transaction_timestamp`,
        `transaction`.`transaction_name` AS `transaction_name`,
        `transaction`.`transaction_iteration` AS `transaction_iteration`,
        `transaction`.`transaction_time` AS `transaction_time`,
        `frame`.`frame_attributes` AS `frame_attributes`,
        `frame`.`frame_hashed_src` AS `frame_hashed_src`,
        `frame`.`frame_src` AS `frame_src`,
        `frame`.`frame_relative_start_time` AS `frame_relative_start_time`,
        `frame`.`frame_time` AS `frame_time`,
        `frame`.`frame_resources_relative_start_time` AS `frame_resources_relative_start_time`,
        `frame`.`frame_resources_time` AS `frame_resources_time`,
        `resource`.`resource_name` AS `resource_name`,
        `resource`.`resource_time` AS `resource_time`,
        `resource`.`resource_relative_start_time` AS `resource_relative_start_time`,
        NULL AS `timing_time`,
        NULL AS `timing_relative_start_time`
    FROM
        (((`testrun`
        JOIN `transaction` ON ((`testrun`.`test_run_id` = `transaction`.`test_run_id`)))
        JOIN `frame` ON ((`transaction`.`transaction_id` = `frame`.`transaction_id`)))
        JOIN `resource` ON ((`frame`.`frame_id` = `resource`.`frame_id`)))
    WHERE
        (`testrun`.`test_run_product` = 'News')

Other:

    Drop all tables:
    DROP TABLE `frameway`.`resource`;
    DROP TABLE `frameway`.`timing`;
    DROP TABLE `frameway`.`frame`;
    DROP TABLE `frameway`.`transaction`;
    DROP TABLE `frameway`.`testrun`
'''

timeStampFormat = '%Y-%m-%d %H:%M:%S.%f'
DB = MySQLDatabase(None)


def init(_schemaName, _host, _port, _user, _password):
    DB.init(_schemaName, host=_host, port=_port, user=_user, password=_password)
    DB.connect()
    if not TestRun.table_exists():
        add_tables()


class BaseModel(Model):
    class Meta:
        database = DB


class TestRun(BaseModel):
    test_run_id = PrimaryKeyField()
    test_run_timestamp = DateTimeField(timeStampFormat)
    test_run_comment = TextField()
    test_run_product = TextField()
    test_run_release = TextField()


class Transaction(BaseModel):
    transaction_id = PrimaryKeyField()
    test_run = ForeignKeyField(TestRun, related_name='transaction')
    transaction_name = CharField()
    transaction_timestamp = DateTimeField(timeStampFormat)
    transaction_iteration = IntegerField()
    transaction_start_time = DoubleField(default=-1)
    transaction_time = IntegerField(default=-1)


class Frame(BaseModel):
    frame_id = PrimaryKeyField()
    transaction = ForeignKeyField(Transaction, related_name='frame')
    frame_structure_id = CharField()
    frame_src = TextField()
    frame_hashed_src = CharField()
    frame_attributes = TextField()
    frame_relative_start_time = IntegerField(default=-1)
    frame_time = IntegerField(default=-1)
    frame_resources_relative_start_time = IntegerField(default=-1)
    frame_resources_time = IntegerField(default=-1)


class Timing(BaseModel):
    timing_id = PrimaryKeyField()
    frame = ForeignKeyField(Frame, default=None, null=True, related_name='timing')
    connectEnd = DoubleField()
    connectStart = DoubleField()
    domainLookupEnd = DoubleField()
    domainLookupStart = DoubleField()
    domComplete = DoubleField()
    domContentLoadedEventEnd = DoubleField()
    domContentLoadedEventStart = DoubleField()
    domInteractive = DoubleField()
    domLoading = DoubleField()
    fetchStart = DoubleField()
    loadEventEnd = DoubleField()
    loadEventStart = DoubleField()
    msFirstPaint = DoubleField(default=-1)
    navigationStart = DoubleField()
    redirectEnd = DoubleField()
    redirectStart = DoubleField()
    requestStart = DoubleField()
    responseEnd = DoubleField()
    responseStart = DoubleField()
    secureConnectionStart = DoubleField(default=-1)
    timing_appcache = IntegerField()
    timing_blocked = IntegerField()
    timing_dns = IntegerField()
    timing_dnstcp = IntegerField()
    timing_dom = IntegerField()
    timing_onload = IntegerField()
    timing_redirect = IntegerField()
    timing_relative_start_time = IntegerField(default=-1)
    timing_request = IntegerField()
    timing_tcp = IntegerField()
    timing_time = IntegerField(default=-1)
    unloadEventEnd = DoubleField()
    unloadEventStart = DoubleField()


class Resource(BaseModel):
    resource_id = PrimaryKeyField()
    frame = ForeignKeyField(Frame, default=None, null=True, related_name='resource')
    resource_name = TextField()
    resource_start_time = IntegerField()
    resource_absolute_start_time = DoubleField(default=-1)
    resource_absolute_end_time = DoubleField(default=-1)
    resource_relative_start_time = IntegerField(default=-1)
    resource_time = IntegerField(default=-1)


def add_tables():
    DB.create_tables([TestRun, Transaction, Frame, Resource, Timing])


def insert_test_run(timeStamp, product, release, comment):
    return TestRun.create(test_run_timestamp=timeStamp, test_run_product=product, test_run_release=release, test_run_comment=comment)


def insert_transaction(testRunID, timeStamp, transactionName, iteration):
    return Transaction.create(test_run=testRunID,
                              transaction_timestamp=timeStamp,
                              transaction_name=transactionName,
                              transaction_iteration=iteration)


def insert_frame(transactionID, frameStructureId, src, hashedSrc, attributes):
    return Frame.create(transaction=transactionID,
                        frame_structure_id=frameStructureId,
                        frame_src=src,
                        frame_hashed_src=hashedSrc,
                        frame_attributes=attributes)


def insert_timing(frameID, timing):
    timing["frame"] = frameID
    return Timing.insert(timing).execute()


def insert_recources(frameID, recourse):
    if not recourse is None:
        if len(recourse) > 0:
            for item in recourse:
                item.update({"frame": frameID})
            with DB.atomic():
                return Resource.insert_many(recourse).execute()
    return None


def add_transaction_times(transaction):
    # Add transaction_start_time
    timingStartTimes = Timing\
        .select(Timing.navigationStart.alias('starttime'))\
        .join(Frame)\
        .where(Frame.transaction == transaction.transaction_id)
    resourceStartTimes = Resource\
        .select(Resource.resource_absolute_start_time.alias('starttime'))\
        .join(Frame)\
        .where(Frame.transaction == transaction.transaction_id)
    startTime = (timingStartTimes | resourceStartTimes).order_by(+SQL('starttime')).get().starttime
    Transaction\
        .update(transaction_start_time=startTime)\
        .where(Transaction.transaction_id == transaction.transaction_id)\
        .execute()
    # Add transaction_time
    timingEndTimes = Timing\
        .select(Timing.loadEventEnd.alias('endtime'))\
        .join(Frame)\
        .where(Frame.transaction == transaction.transaction_id)
    resourceEndTimes = Resource\
        .select(Resource.resource_absolute_end_time.alias('endtime'))\
        .join(Frame)\
        .where(Frame.transaction == transaction.transaction_id)
    endTime = (timingEndTimes | resourceEndTimes).order_by(-SQL('endtime')).get().endtime
    Transaction\
        .update(transaction_time=endTime - startTime)\
        .where(Transaction.transaction_id == transaction.transaction_id)\
        .execute()


def add_frame_times(transaction):
    transactionStartTime = transaction_start_time(transaction)
    frames = Frame.select().where(Frame.transaction == transaction.transaction_id).execute()
    for frame in frames:
        # Add frame_relative_start_time
        timingStartTimes = Timing\
            .select(Timing.navigationStart.alias('starttime'))\
            .where(Timing.frame == frame.frame_id)
        resourceStartTimes = Resource\
            .select(Resource.resource_absolute_start_time.alias('starttime'))\
            .where(Resource.frame == frame.frame_id)
        startTime = (timingStartTimes | resourceStartTimes).order_by(+SQL('starttime')).get().starttime
        Frame\
            .update(frame_relative_start_time=startTime-transactionStartTime)\
            .where(Frame.frame_id == frame.frame_id)\
            .execute()
        # Add frame_time
        timingEndTimes = Timing\
            .select(Timing.loadEventEnd.alias('endtime'))\
            .where(Timing.frame == frame.frame_id)
        resourceEndTimes = Resource\
            .select(Resource.resource_absolute_end_time.alias('endtime'))\
            .where(Resource.frame == frame.frame_id)
        endTime = (timingEndTimes | resourceEndTimes).order_by(-SQL('endtime')).get().endtime
        Frame\
            .update(frame_time=endTime - startTime)\
            .where(Frame.frame_id == frame.frame_id)\
            .execute()


def add_timing_times(transaction):
    transactionStartTime = transaction_start_time(transaction)
    query = 'update timing ' \
            'join frame ' \
            'on frame.frame_id = timing.frame_id ' \
            'set timing_relative_start_time = timing.navigationStart - %d ' \
            'where frame.transaction_id = %d' \
            % (transactionStartTime, transaction.transaction_id)
    DB.execute_sql(query)


def add_resource_times(transaction):
    transactionStartTime = transaction_start_time(transaction)
    # Add resource_relative_start_time
    query = 'update resource ' \
            'join frame ' \
            'on frame.frame_id = resource.frame_id ' \
            'set resource_relative_start_time = resource.resource_absolute_start_time - %d ' \
            'where frame.transaction_id = %d' \
            % (transactionStartTime, transaction.transaction_id)
    DB.execute_sql(query)
    # Add total resource times to frames
    frames = Frame\
        .select()\
        .where(Frame.transaction == transaction.transaction_id)\
        .execute()
    for frame in frames:
        # Add resources_relative_start_time
        try:
            resources_relative_start_time = Resource\
                .select(Resource.resource_relative_start_time)\
                .where(Resource.frame == frame.frame_id)\
                .order_by(+Resource.resource_relative_start_time)\
                .get().resource_relative_start_time
        except DoesNotExist:
            resources_relative_start_time = -1
        Frame\
            .update(frame_resources_relative_start_time=resources_relative_start_time)\
            .where(Frame.frame_id == frame.frame_id)\
            .execute()
        # Add resources_time
        try:
            absolute_start_time = Resource\
                .select(Resource.resource_absolute_start_time)\
                .where(Resource.frame == frame.frame_id)\
                .order_by(+Resource.resource_relative_start_time)\
                .get().resource_absolute_start_time
            absolute_end_time = Resource\
                .select(Resource.resource_absolute_end_time)\
                .where(Resource.frame == frame.frame_id)\
                .order_by(-Resource.resource_absolute_end_time)\
                .get().resource_absolute_end_time
        except DoesNotExist:
            absolute_end_time = -1
            absolute_start_time = 0
        totalResourcesTime = absolute_end_time - absolute_start_time
        Frame\
            .update(frame_resources_time=totalResourcesTime)\
            .where(Frame.frame_id == frame.frame_id).execute()


def transaction_start_time(transaction):
    return Transaction\
        .select(Transaction)\
        .where(Transaction.transaction_id == transaction.transaction_id)\
        .get().transaction_start_time


def transaction_by_id(transactionId):
    return Transaction\
        .select(Transaction)\
        .where(Transaction.transaction_id == transactionId)\
        .get()


def delete_test_runs(testRunIds):
    for testRunId in testRunIds:
        transactionIds = Transaction.select(Transaction.transaction_id).where(Transaction.test_run == testRunId).execute()
        delete_transactions(transactionIds)
        TestRun.delete().where(TestRun.test_run_id == testRunId).execute()


def delete_transactions(transactionIds):
    for transactionId in transactionIds:
        frameIds = Frame.select(Frame.frame_id).where(Frame.transaction == transactionId).execute()
        delete_frames(frameIds)
        Transaction.delete().where(Transaction.transaction_id == transactionId).execute()


def delete_frames(frameIds):
    for frameId in frameIds:
        timingIds = Timing.select(Timing.timing_id).where(Timing.frame == frameId).execute()
        delete_timings(timingIds)
        resourceIds = Resource.select(Resource.resource_id).where(Resource.frame == frameId).execute()
        delete_resources(resourceIds)
        Frame.delete().where(Frame.frame_id == frameId).execute()


def delete_timings(timingIds):
    for timingId in timingIds:
        Timing.delete().where(Timing.timing_id == timingId).execute()

def delete_resources(resourceIds):
    for resourceId in resourceIds:
        Resource.delete().where(Resource.resource_id == resourceId).execute()


def filter_frames(transaction, frameFilter):
    for filteredFrame in frameFilter:
        transactionFrames = Frame.select(Frame.frame_id).where(Frame.transaction == transaction.transaction_id)
        filteredFrames = transactionFrames.select().where(Frame.frame_attributes.contains(filteredFrame)).execute()
        delete_frames(filteredFrames)


def filter_resources(transaction, resourceFilter):
    for res in resourceFilter:
        query = Resource.select().join(Frame).join(Transaction).where(Resource.resource_name.contains(res), Transaction.transaction_id == transaction.transaction_id)
        q = query.execute()
        for a in q:
            a.delete_instance()


def test_runs():
    return TestRun.select().execute()


def transactions(testRunId):
    return Transaction.select().where(Transaction.test_run == testRunId).execute()


def transaction_count(testRunId):
    return Transaction.select().where(Transaction.test_run == testRunId).count()


def comment(testRunId):
    try:
        return TestRun.select(TestRun.test_run_comment).where(TestRun.test_run_id == testRunId).get().test_run_comment
    except:
        return None


def update_comment(testRunId, comment):
    TestRun.update(test_run_comment = comment).where(TestRun.test_run_id == testRunId).execute()


def frame_already_exist(testRun, iteration, timing):
   return Timing.select() \
              .join(Frame) \
              .join(Transaction) \
              .join(TestRun) \
              .where((Timing.navigationStart == timing.get('navigationStart'))
                     & (Transaction.transaction_iteration == iteration)
                     & (TestRun.test_run_id == testRun.test_run_id)) \
              .execute().count > 0


def transaction_has_frames(transaction):
    return Frame.select().where(Frame.transaction == transaction.transaction_id).execute().count > 0


def reconnect():
    destroy()
    DB.connect()
    if not TestRun.table_exists():
        add_tables()


def destroy():
    DB.close()
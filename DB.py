import peewee as pw
#pip install peewee
#pip install PyMySQL

myDB = pw.MySQLDatabase("frameway", host="127.0.0.1", port=3306, user="dbuser", passwd="dbuser")

class MySQLModel(pw.Model):
    """A base model that will use our MySQL database"""
    class Meta:
        database = myDB

class Frame(MySQLModel):
    frameId = pw.CharField()
    name = pw.CharField()
    url = pw.CharField()
    class Meta:
        order_by = ('name',)

class Timing(MySQLModel):
    frame = pw.ForeignKeyField(Frame, related_name='timings')
    connectEnd = pw.IntegerField()
    connectStart = pw.IntegerField()
    domComplete = pw.IntegerField()
    domContentLoadedEventEnd = pw.IntegerField()
    domContentLoadedEventStart = pw.IntegerField()
    domInteractive = pw.IntegerField()
    domLoading = pw.IntegerField()
    domainLookupEnd = pw.IntegerField()
    domainLookupStart = pw.IntegerField()
    fetchStart = pw.IntegerField()
    loadEventEnd = pw.IntegerField()
    loadEventStart = pw.IntegerField()
    navigationStart = pw.IntegerField()
    redirectEnd = pw.IntegerField()
    redirectStart = pw.IntegerField()
    requestStart = pw.IntegerField()
    responseEnd = pw.IntegerField()
    responseStart = pw.IntegerField()
    secureConnectionStart = pw.IntegerField()
    unloadEventEnd = pw.IntegerField()
    unloadEventStart = pw.IntegerField()
    class Meta:
        database = myDB

class ResourceTiming(MySQLModel):
    frame = pw.ForeignKeyField(Frame, related_name='resources')
    connectEnd = pw.FloatField()
    connectStart = pw.FloatField()
    domainLookupEnd = pw.FloatField()
    domainLookupStart = pw.FloatField()
    duration = pw.FloatField()
    entryType = pw.CharField()
    fetchStart = pw.FloatField()
    initiatorType = pw.CharField()
    name = pw.CharField()
    redirectEnd = pw.FloatField()
    redirectStart = pw.FloatField()
    requestStart = pw.FloatField()
    responseEnd = pw.FloatField()
    responseStart = pw.FloatField()
    secureConnectionStart = pw.FloatField()
    startTime = pw.FloatField()
    workerStart = pw.FloatField()
    class Meta:
        database = myDB


myDB.connect()

#Frame.create(username = "Stefan")
myDB.create_tables([Frame, Timing, ResourceTiming])
#myDB.create_table(Frame)
myDB.close()
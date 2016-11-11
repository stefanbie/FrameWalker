import DB
import itertools
import operator

testrun_id = 357
DB.init()
timeList = []

def accumulate(l):
    list_builder = []
    it = itertools.groupby(l, operator.itemgetter(0))
    for key, subiter in it:
        element = key, sum(item[1] for item in subiter)
        list_builder.append(element)
    return list_builder

def addTime(structure):
    if len(structure) == 3:
        return 3
    return 2

structureList = DB.frameStructureList(testrun_id)
for row in structureList:
    entry = [row[0], addTime(row[1])]
    timeList.append(entry)
accumulatedTimeList = accumulate(timeList)

for row in accumulatedTimeList:
    print(row[0] + ',' + str(row[1]))



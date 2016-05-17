import DB
testcases = DB.testCases()
template = "{0:10}{1:30}{2:20}{3:15}"
print(template.format('ID', 'TimeStamp', 'TransactionCount', 'Comment'))
for testcase in testcases:
    testCaseId = testcase.test_case_id
    transactionCount = DB.transactionCount(testCaseId)
    print(template.format(str(testcase.test_case_id), str(testcase.test_case_timestamp), str(transactionCount), str(testcase.test_case_comment)))
ids = [testcase.test_case_id for testcase in testcases]
try:
    x = int(input('Test case ID to delete? '))
except ValueError:
    print('Not a valid testcase ID')
    exit()
if x in ids:
    DB.deleteTestRun(x)
    print('Deleted testcase with id ID', x)
else:
    print('Not a valid testcase ID')
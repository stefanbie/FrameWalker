import DB
import sys
import random
import subprocess
import os
import shutil

'''
    Method for parsing input from user to a sequence of numbers.
    Input examples:
        "3" => 3
        "3,4,10" => 3 4 10
        "3-10" => 3 4 5 6 7 8 9 10
'''
def parseIntSet(nputstr=""):
    selection = set()
    invalid = set()
    # tokens are comma seperated values
    tokens = [x.strip() for x in nputstr.split(',')]
    for i in tokens:
        if len(i) > 0:
            if i[:1] == "<":
                i = "1-%s"%(i[1:])
        try:
            # typically tokens are plain old integers
            selection.add(int(i))
        except:
            # if not, then it might be a range
            try:
                token = [int(k.strip()) for k in i.split('-')]
                if len(token) > 1:
                    token.sort()
                    # we have items seperated by a dash
                    # try to build a valid range
                    first = token[0]
                    last = token[len(token)-1]
                    for x in range(first, last+1):
                        selection.add(x)
            except:
                # not an int and not a range...
                invalid.add(i)
    # Report invalid tokens before returning valid selection
    if len(invalid) > 0:
        #print "Invalid set: " + str(invalid)
        return None
    return selection
# end parseIntSet

closing_phrases = {'Goodbye...', 'See you later...', 'Hope to see you again...', 'Bye!', 'Later dude!', 'Farewell!', 'So long!', 'Godspeed!', 'Adios!', 'Ciao!', 'Have a good day...', 'Take care...', 'Catch you later!', 'Sayonara!', 'Au revoir!', 'Have a good one!'}

while True:
    testcases = DB.testCases()

    template = "{0:10}{1:30}{2:20}{3:15}"
    print("====================== [ DATABASE CONTENTS ] ======================\n")
    print(template.format('TC ID', 'TimeStamp', 'TransactionCount', 'Comment'))

    for testcase in testcases:
        testCaseId = testcase.test_case_id
        transactionCount = DB.transactionCount(testCaseId)
        print(template.format(str(testcase.test_case_id), str(testcase.test_case_timestamp), str(transactionCount), str(testcase.test_case_comment)))

    ids = [testcase.test_case_id for testcase in testcases]

    try:
        nputstr = '{}'.format(input("\nEnter command [delete] [backup] [quit] : "))
        if nputstr.lower() in {"q", "quit", "exit"}:
            break

        if nputstr.lower() in {"delete", "d"}:
            test_cases = '{}'.format(input("\nEnter test cases to delete : "))
            selection = parseIntSet(test_cases)
            if selection is None or len(selection) == 0:
                print("Not a valid input, try again...\n")
            else:
                print('\n')
                for n in selection:
                    if n in ids:
                        DB.deleteTestRun(n)
                        print('Deleted test case with id ID: ', n)
                    else:
                        print('Test case with ID %s does not exists!' % n)
                print('\n')

        if nputstr.lower() in {"backup", "b"}:
            _success = False
            while not _success:
                file_name = '{}'.format(input("\nEnter an absolute path to create a backup file (ex. c:\\temp\\backup.sql) : "))
                if file_name:
                    if os.path.isabs(file_name):
                        #os.system("mysqldump -u root -padmin frameway > %s" % file_name)
                        FNULL = open(os.devnull, 'w')
                        if shutil.which("mysqldump") is None:
                            print("ERROR: mysqldump.exe is not accessible! Probably the path of the executable is not set in PATH-environment-variable...\n")
                            break
                        subprocess.call(["mysqldump", "-uroot", "-padmin", "frameway", ">", "%s" % file_name], shell=True, stdout=FNULL, stderr=subprocess.STDOUT)
                        print("The file", file_name, "has been created.\n")
                        _success = True
                    else:
                        print("ERROR: You are required to enter an absolute path! Try again...\n")
                else:
                    print("Empty file name given! Aborting...\n")
                    break

    except:
        print("Oh no! Something went wrong.... \n")
        print(sys.exc_info())

print('\n{0}'.format(*random.sample(closing_phrases, 1)))
import os
import random
import shutil
import subprocess

from framewalker import DB

closing_phrases = {'Goodbye...', 'See you later...', 'Hope to see you again...', 'Bye!', 'Later dude!', 'Farewell!', 'So long!', 'Godspeed!', 'Adios!', 'Ciao!', 'Have a good day...', 'Take care...', 'Catch you later!', 'Sayonara!', 'Au revoir!', 'Have a good one!'}

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

def update_comment():
    test_run = '{}'.format(input("\nEnter ID of test case to change comment : "))

    try:
        int(test_run)
    except ValueError:
        print("Invalid input! Aborting...")
        return

    current_comment = DB.comment(test_run)

    if current_comment is None:
        print("Test case does not exist! Aborting...")
        return

    print("\nCurrent comment for test case ID " + test_run + " is: \"" + str(current_comment) + "\"")
    new_comment = '{}'.format(input("Enter new comment : "))
    if new_comment:
        DB.update_comment(test_run, new_comment)
    else:
        print("Empty comment given! Aborting...")
        return

def backup():
    file_name = '{}'.format(input("\nEnter an absolute path to create a backup file of the database (ex. c:\\temp\\backup.sql) : "))
    if file_name:
        if os.path.isabs(file_name):
            if shutil.which("mysqldump"):
                FNULL = open(os.devnull, 'w')
                subprocess.call(["mysqldump", "-uroot", "-padmin", "framewalker", ">", "%s" % file_name],
                                shell=True, stdout=FNULL, stderr=subprocess.STDOUT)
                print("The file", file_name, "has been created.")
            else:
                print("ERROR: mysqldump.exe is not accessible! Probably the path of the executable is not set in PATH-environment-variable... Aborting!")
                return
        else:
            print("ERROR: You are required to enter an absolute path! Try again...")
            backup()
    else:
        print("Empty file name given! Aborting...")
        return

def delete_transactions():
    testrun_id = '{}'.format(input("\nEnter test run : "))
    print('\n')
    transactions = DB.transactions(testrun_id)
    template = "{0:20}{1:30}{2:20}{3:25}"
    print(template.format('Transaction ID', 'Name', 'Iteration', 'Time'))
    for transaction in transactions:
        print(template.format(str(transaction.transaction_id), str(transaction.transaction_name), str(transaction.transaction_iteration), str(transaction.transaction_time)))

    transactions = '{}'.format(input("\nEnter IDs of transactions to delete : "))
    selection = parseIntSet(transactions)

    if selection is None or len(selection) == 0:
        print("Not a valid input! Aborting...")
        return

    print('\n')
    DB.delete_transactions(selection)

    transactions = DB.transactions(testrun_id)
    print(template.format('Transaction ID', 'Name', 'Iteration', 'Time'))
    for transaction in transactions:
        print(template.format(str(transaction.transaction_id), str(transaction.transaction_name),str(transaction.transaction_iteration), str(transaction.transaction_time)))

def delete_test_runs():
    test_runs = '{}'.format(input("\nEnter IDs of test runs to delete : "))
    selection = parseIntSet(test_runs)

    if selection is None or len(selection) == 0:
        print("Not a valid input! Aborting...")
        return

    print('\n')
    DB.delete_test_runs(selection)
    '''
    for n in selection:
        if n in ids:
            DB.deleteTestRun(n)
            print('Deleted test run with id ID: ', n)
        else:
            print('Test run with ID %s does not exist in the database!' % n)
    '''
DB.init(_schemaName='framewalker', _host='127.0.0.1', _port=3306, _user='dbuser', _password='admin')
while True:
    testruns = DB.test_runs()

    template = "{0:20}{1:30}{2:20}{3:25}{4:10}{5:50}"
    print("\n====================== [ DATABASE CONTENTS ] ======================\n")
    print(template.format('Test run id', 'TimeStamp', 'Transaction count', 'Product', 'Release', 'Comment'))

    for testrun in testruns:
        testRunId = testrun.test_run_id
        transactionCount = DB.transaction_count(testRunId)
        print(template.format(str(testrun.test_run_id), str(testrun.test_run_timestamp), str(transactionCount), str(testrun.test_run_product), str(testrun.test_run_release), str(testrun.test_run_comment)))

    ids = [testrun.test_run_id for testrun in testruns]

    #try:
    nputstr = '{}'.format(input("\nEnter command [delete test run (d)] [delete transaction (dt)] [backup (b)] [edit comment (e)] [quit (q)] : "))
    if nputstr.lower() in {"q", "quit", "exit"}:
        break
    if nputstr.lower() in {"delete test run", "d"}:
        delete_test_runs()

    if nputstr.lower() in {"delete transactions", "dt"}:
        delete_transactions()

    if nputstr.lower() in {"edit comment", "e"}:
        update_comment()

    if nputstr.lower() in {"backup", "b"}:
        backup()

    #except:
    #   print("Oh no! Something went wrong.... \n")
    #    print(sys.exc_info())

print('\n{0}'.format(*random.sample(closing_phrases, 1)))
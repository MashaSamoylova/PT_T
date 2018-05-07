import time
import collections

from db_manager import *

def make_report(scan_time):
    db = get_db()
    c = db.cursor()

    c.execute(
            '''
            SELECT * FROM scandata
            ''')

    scan_information = c.fetchall()
    
    print("DATE: {}".format(time.asctime()))
    print("duration: {} sec".format(scan_time))
    print("number of checks: {}".format(len(scan_information)))

    counter = collections.Counter(
            STATUS_COMPLIANT=0,
            STATUS_NOT_COMPLIANT=0,
            STATUS_NOT_APPLICABLE=0,
            STATUS_ERROR=0,
            STATUS_EXCEPTION=0
            )
    for report in scan_information:
        counter[report[2]] += 1

    statuses = dict(counter)
    print("STATUS_COMPLIANT: {}".format(statuses["STATUS_COMPLIANT"]))
    print("STATUS_NOT_COMPLIANT: {}".format(statuses["STATUS_NOT_COMPLIANT"]))
    print("STATUS_NOT_APPLICABLE: {}".format(statuses["STATUS_NOT_APPLICABLE"]))
    print("STATUS_ERROR: {}".format(statuses["STATUS_ERROR"]))
    print("STATUS_EXCEPTION: {}".format(statuses["STATUS_EXCEPTION"]))

    

                

import time
import collections

from db_manager import *
from get_transport import config

def make_report(scan_time):
    db = get_db()
    c = db.cursor()
    
    c.execute(
            '''
            SELECT * FROM scandata AS t1
            INNER JOIN control AS t2
            ON t1.id=t2.id
            ''')

    scan_information = c.fetchall()
    print(scan_information)
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

    system_information = []
    for report in scan_information:
        counter[report[1]] += 1
        system_information.append("Transport: {}, port: {}, login: {}".format(
            report[6], 
            config['transports'][report[6]]['port'], 
            config['transports'][report[6]]['login']))

    statuses = dict(counter)
    print("STATUS_COMPLIANT: {}".format(statuses["STATUS_COMPLIANT"]))
    print("STATUS_NOT_COMPLIANT: {}".format(statuses["STATUS_NOT_COMPLIANT"]))
    print("STATUS_NOT_APPLICABLE: {}".format(statuses["STATUS_NOT_APPLICABLE"]))
    print("STATUS_ERROR: {}".format(statuses["STATUS_ERROR"]))
    print("STATUS_EXCEPTION: {}".format(statuses["STATUS_EXCEPTION"]))

    print("host: {}".format(config['host']))

    print("SYSTEM_INFORMATION:")
    print(set(system_information))

    for report in scan_information:
        print("ID: {}".format(report[2]))
        print("Title: {}".format(report[3]))
        print("Requirements: {}".format(report[4]))
        print("Description: {}".format(report[5]))





























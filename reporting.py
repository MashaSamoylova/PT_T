import time
import collections

from db_manager import *
from get_transport import config

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

    controls_id = []
    for report in scan_information:
        counter[report[1]] += 1
        controls_id.append(report[0])


    statuses = dict(counter)
    print("STATUS_COMPLIANT: {}".format(statuses["STATUS_COMPLIANT"]))
    print("STATUS_NOT_COMPLIANT: {}".format(statuses["STATUS_NOT_COMPLIANT"]))
    print("STATUS_NOT_APPLICABLE: {}".format(statuses["STATUS_NOT_APPLICABLE"]))
    print("STATUS_ERROR: {}".format(statuses["STATUS_ERROR"]))
    print("STATUS_EXCEPTION: {}".format(statuses["STATUS_EXCEPTION"]))

    c.execute(
            '''
            SELECT * FROM control
            WHERE id in 
            ''' + str(tuple(controls_id)))

    print("host: {}".format(config['host']))
    control_information = c.fetchall()
    system_information = []
    for control_inf in control_information:
        system_information.append("Transport: {}, port: {}, login: {}".format(control_inf[4], config['transports'][control_inf[4]]['port'], config['transports'][control_inf[4]]['login']))

    system_information = set(system_information)
    print("SYSTEM_INFORMATION:")
    print(system_information)

    for control_inf in control_information:
        print("ID: {}".format(control_inf[0]))
        print("Title: {}".format(control_inf[1]))
        print("Requirements: {}".format(control_inf[2]))
        print("Description: {}".format(control_inf[3]))





























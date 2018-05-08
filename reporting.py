import time
from collections import Counter

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
    columns_names = [n[0] for n in c.description]
    scan_information = [dict(zip(columns_names, comp)) for comp in c.fetchall()]

    print("DATE: {}".format(time.asctime()))
    print("duration: {} sec".format(scan_time))
    print("number of checks: {}".format(len(scan_information)))

    counter = Counter({status:0 for status in statuses.values()})

    system_information = []
    for report in scan_information:
        counter[report["status"]] += 1
        system_information.append("Transport: {}, port: {}, login: {}".format(
            report['transport'], 
            config['transports'][report['transport']]['port'], 
            config['transports'][report['transport']]['login']))

    scan_statuses = dict(counter)
    print("STATUS_COMPLIANT: {}".format(scan_statuses["STATUS_COMPLIANT"]))
    print("STATUS_NOT_COMPLIANT: {}".format(scan_statuses["STATUS_NOT_COMPLIANT"]))
    print("STATUS_NOT_APPLICABLE: {}".format(scan_statuses["STATUS_NOT_APPLICABLE"]))
    print("STATUS_ERROR: {}".format(scan_statuses["STATUS_ERROR"]))
    print("STATUS_EXCEPTION: {}".format(scan_statuses["STATUS_EXCEPTION"]))

    print("host: {}".format(config['host']))

    print("SYSTEM_INFORMATION:")
    print(set(system_information))

    for report in scan_information:
        print("ID: {}".format(report["id"]))
        print("Title: {}".format(report["title"]))
        print("Requirements: {}".format(report["requirements"]))
        print("Description: {}".format(report["description"]))





























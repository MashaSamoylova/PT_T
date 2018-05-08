import time
from collections import Counter

from jinja2 import Environment, PackageLoader, FileSystemLoader, select_autoescape
from weasyprint import HTML, CSS

from db_manager import *
from get_transport import config

env = Environment(
    loader=FileSystemLoader('templates'),
    autoescape=select_autoescape(['html', 'xml'])
)

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

    scan_date = time.asctime()

    counter = Counter({status:0 for status in statuses.values()})
    
    used_transports = set([report['transport'] for report in scan_information])
    transports = {transport : config['transports'][transport] for transport in used_transports}

    for report in scan_information:
        counter[report["status"]] += 1

    scan_statuses = dict(counter)

    report_template = env.get_template("index.html").render(
        scan_date=scan_date,
        scan_time=scan_time,
        system_host=config['host'],
        transports=transports,
        total_checks=len(scan_information),
        STATUS_COMPLIANT_checks=scan_statuses["STATUS_COMPLIANT"],
        STATUS_NOT_COMPLIANT_checks=scan_statuses["STATUS_NOT_COMPLIANT"],
        STATUS_NOT_APPLICABLE_checks=scan_statuses["STATUS_NOT_APPLICABLE"],
        STATUS_ERROR_checks=scan_statuses["STATUS_ERROR"],
        STATUS_EXCEPTION_checks=scan_statuses["STATUS_EXCEPTION"],
        comp_data=scan_information
        )
    
    styles = [CSS(filename='./templates/style.css')]
    HTML(string = report_template).write_pdf('sample_report.pdf', stylesheets=styles)  


























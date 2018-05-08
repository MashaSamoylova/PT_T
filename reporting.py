import time
from collections import Counter

from jinja2 import Environment, PackageLoader, FileSystemLoader, select_autoescape
from weasyprint import HTML, CSS

from db_manager import *
from config import config

def make_report(scan_time):
    db = get_db()
    c = db.cursor()
    c.execute(
            '''
            SELECT * FROM scandata AS t1
            INNER JOIN control AS t2
            ON t1.id=t2.id
            ''')

    scan_date = time.asctime()
    columns_names = [n[0] for n in c.description]
    scan_information = [dict(zip(columns_names, comp)) for comp in c.fetchall()]

    used_transports = set([report['transport'] for report in scan_information])
    transports = {transport : config['transports'][transport] for transport in used_transports}

    counter = Counter({status:0 for status in statuses.values()})
    for report in scan_information:
        counter[report["status"]] += 1

    scan_statuses = {key+"_checks": value for key, value in dict(counter).items()}

    render_data = {
        'scan_date': scan_date,
        'scan_time': scan_time,
        'system_host': config['host'],
        'transports' : transports,
        'total_checks': len(scan_information),
        'comp_data' : scan_information
    }
    render_data.update(scan_statuses)

    env = Environment(
        loader=FileSystemLoader('templates'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    report_template = env.get_template('index.html').render(**render_data)
    styles = [CSS(filename='./templates/style.css')]
    HTML(string = report_template).write_pdf('sample_report.pdf', stylesheets=styles)  

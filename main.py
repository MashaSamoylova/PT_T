#!/usr/bin/env python3.5
import os
import time
import json
import importlib

from db_manager import *
from reporting import *
import scripts

def add_control(control_id, status):
    statuses = dict(enumerate([
        "STATUS_COMPLIANT",
        "STATUS_NOT_COMPLIANT",
        "STATUS_NOT_APPLICABLE",
        "STATUS_ERROR",
        "STATUS_EXCEPTION"]
        ,1))

    db = get_db()
    c = db.cursor()

    c.execute(
            '''
            SELECT * FROM control WHERE id=?
            ''', (str(control_id),))

    comp_data = c.fetchone()

    c.execute(
            '''
            INSERT INTO scandata(id, description, status) 
            VALUES(?,?,?)
            ''', tuple(list(comp_data) + [statuses[status]])
    )
    db.commit()
    db.close()

def main():
    counter = 0
    prepare_db()
    begin_time = time.time()
    for module_name in os.listdir("./scripts"):
        if module_name.endswith('.py'):
            module = importlib.import_module('.' + module_name[:-3], package='scripts')
            add_control(counter, module.main())
            counter = counter + 1
    make_report(time.time()-begin_time)

if __name__=="__main__":
    main()

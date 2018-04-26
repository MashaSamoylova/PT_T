#!/usr/bin/env python3.5
import os
import json
import importlib

from db_manager import *

def check_executable_python(file_name):
    return file_name.split(".")[-1:][0]=="py"

def add_control(control_id, status):
    statuses = dict(enumerate(
        ["STATUS_COMPLIANT",
        "STATUS_NOT_COMPLIANT",
        "STATUS_NOT_APPLICABLE",
        "STATUS_ERROR",
        "STATUS_EXCEPTION"]
        ,1))

    db = get_db()
    c = db.cursor()

    c.execute('''
            SELECT * FROM control WHERE id=?
            ''', (str(control_id),))

    comp_data = c.fetchone()

    print(comp_data)

    c.execute('''
            INSERT INTO scandata(id, description, status) 
            VALUES(?,?,?)
            ''', 
            tuple(list(comp_data) + [statuses[status]])
    )
    db.commit()
    db.close()

def main():
    for f in filter(check_executable_python, os.listdir("./scripts")):
        mod = importlib.import_module("scripts." + f[:-3])
        add_control(456, mod.main())

if __name__=="__main__":
    prepare_db()
    main()

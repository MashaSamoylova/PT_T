#!/usr/bin/env python3.5
import os
import json
import importlib

import sqlite3

DBNAME = "data.db"

def get_db():
    return sqlite3.connect(DBNAME)

def check_executable_python(file_name):
    return file_name.split(".")[-1:][0]=="py"

def main():
    for f in filter(check_executable_python, os.listdir("./scripts")):
        mod = importlib.import_module("scripts." + f[:-3])
        mod.main()

if __name__=="__main__":
    db = get_db()
    c = db.cursor()
    c.execute(
            '''
            CREATE TABLE IF NOT EXISTS 
            control(
            id INTEGER PRIMARY KEY,
            description TEXT
            )
            '''
    )

    c.execute(
            '''
            CREATE TABLE IF NOT EXISTS
            scandata(
            id INTEGER PRIMARY KEY,
            description,
            status
            )
            '''
    )
    db.commit()

    with open("controls.json") as f:
        controls = json.load(f)

    for complaint_record in controls:
        c.execute(
            '''
            INSERT INTO control(id, description)
            VALUES (?,?)
            ''', 
            tuple(complaint_record))
        
        db.commit()
    main()

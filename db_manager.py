import sqlite3
import json

DBNAME = "data.db"

def get_db():
    return sqlite3.connect(DBNAME)

def prepare_db():
    db = get_db()
    c = db.cursor()
    c.execute(
            '''
            CREATE TABLE IF NOT EXISTS 
            control(
            id INTEGER PRIMARY KEY,
            description TEXT
            )
            ''')

    c.execute(
            '''
            CREATE TABLE IF NOT EXISTS
            scandata(
            id INTEGER PRIMARY KEY,
            description,
            status
            )
            ''')

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
    db.close()


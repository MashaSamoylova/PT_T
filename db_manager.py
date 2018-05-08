import sqlite3
import json

DBNAME = "data.db"

statuses = dict(enumerate([
    "STATUS_COMPLIANT",
    "STATUS_NOT_COMPLIANT",
    "STATUS_NOT_APPLICABLE",
    "STATUS_ERROR",
    "STATUS_EXCEPTION"]
    ,1))

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
            title TEXT,
            requirements TEXT,
            description TEXT,
            transport TEXT
            )
            ''')

    c.execute(
            '''
            CREATE TABLE IF NOT EXISTS
            scandata(
            id INTEGER PRIMARY KEY,
            status TEXT
            )
            ''')

    db.commit()

    with open("controls.json") as f:
        controls = json.load(f)

    for complaint_record in controls:
        c.execute(
            '''
            INSERT INTO control(id, title, requirements, description, transport)
            VALUES (?,?,?,?,?)
            ''', 
            (
                complaint_record["id"],
                complaint_record["title"],
                complaint_record["requirements"],
                complaint_record["description"],
                complaint_record["transport"],
            ))
        db.commit()
    db.close()


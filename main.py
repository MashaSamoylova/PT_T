#!/usr/bin/env python3.5
import os
import time
import importlib

from db_manager import *
from reporting import *
from config import statuses

from get_transport import *


def add_control(control_id, status):
    db = get_db()
    c = db.cursor()

    c.execute(
            '''
            INSERT INTO scandata(id,status)
            VALUES(?,?)
            ''',
            (control_id, statuses[status]))
    db.commit()
    db.close()

def main():
    prepare_db()
    counter = 0
    begin_time = time.time()
    for module_name in os.listdir("./scripts"):
        if module_name.endswith('.py'):
            module = importlib.import_module('.' + module_name[:-3], package='scripts')
            add_control(counter, module.main())
            counter = counter + 1
    make_report(time.time()-begin_time)

if __name__ == "__main__":
    print(get_transport("SSH").exec("ls /"))
    print(get_transport("SQL").exec("SELECT `id`, `password` FROM `users` WHERE `email`='webmaster@python.org'"))

   # main()

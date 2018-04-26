#!/usr/bin/env python3.5
import os
import importlib

def check_executable_python(file_name):
    return file_name.split(".")[-1:][0]=="py"

def main():
    for f in filter(check_executable_python, os.listdir("./scripts")):
        mod = importlib.import_module("scripts."+f[:-3])
        mod.main()

if __name__=="__main__":
    main()

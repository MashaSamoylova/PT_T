import os

def check_ExecutablePython(file_name):
    return file_name.split(".")[-1:][0]=="py" and os.access(file_name, os.X_OK) 

def main():
    files = os.listdir("./scripts")

    for f in filter(check_ExecutablePython, os.listdir(./scripts)):
        import f
        f.main()

if __name__=="__main__":
    main()

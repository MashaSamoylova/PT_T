##!/usr/bin/env python3.5
from get_transport import *

def main():
    try:
        get_transport("SSH", "localhost", 4000, "root", "screencast").get_file("/root/test1")
    except TransportIOError:
        return 2
    except TransportConnectionError:
        return 4
    return 1

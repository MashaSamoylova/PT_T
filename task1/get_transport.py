#!/usr/bin/env python3.5
from ssh_transport import get_transportSSH
import pytest

class UnknownTransport(Exception):
    pass

def get_transport(transport_name, host, port, login, passwd):
    transport_names = {'ssh':get_transportSSH}

    if transport_name not in transport_names.keys():
        raise UnknownTransport

    return transport_names[transport_name](host,port,login, passwd)

###TESTS###
def test_get_transport():
    get_transport('ssh', "localhost", 4000, "root", "screencast")
    with pytest.raises(UnknownTransport):
        get_transport('ssh1', "localhost", 4000, "root", "screencast")

if __name__=="__main__":
    get_transport('ssh', "localhost", 4000, "root", "screencast").get_file("asdf")

import pytest
from get_transport import *

def test_init():
        SSH("localhost", 4000, "root", "screencast")
        with pytest.raises(TransportConnectionError):
            SSH("localhost1", 4000, "root", "screencast")
            SSH("localhost", 40001, "root", "screencast")
            SSH("localhost", 4000, "root1", "screencast")
            SSH("localhost", 4000, "root", "screencast1")

def test_exec():
    SSH("localhost", 4000, "root", "screencast").exec("ls /")

def test_get_file():
    SSH("localhost", 4000, "root", "screencast").get_file("/root/test")
    with pytest.raises(TransportError):
        SSH("localhost", 4000, "root", "screencast").get_file("/root/test1")        

def test_get_transport():
    get_transport('ssh', "localhost", 4000, "root", "screencast")
    with pytest.raises(UnknownTransport):
        get_transport('ssh1', "localhost", 4000, "root", "screencast")

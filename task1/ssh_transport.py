import paramiko
import pytest
import socket

class TransportError(Exception):
    pass

class TransportConnectionError(Exception):
    pass

class SSH():
    def __init__(self, host, port_, login, passwd):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            self.client.connect(hostname=host, username=login, password=passwd, port=port_)
        except 	paramiko.BadHostKeyException:
            raise TransportConnectionError("BadHostKeyException")
        except 	paramiko.AuthenticationException:
            raise TransportConnectionError("AuthenticationException")
        except paramiko.SSHException:
            raise TransportConnectionError("SSHException")
        except socket.error:
            raise TransportConnectionError("socket.error")

    def exec(self, command):
        try:
            stdin, stdout, stderr = self.client.exec_command(command)
        except SSHException:
            raise TransportConnectionError("SSHException")

        if stderr.read():
            raise TransportError
        
        print(stdout.read().decode())

    def get_file(self, path):
        sftp_client = self.client.open_sftp()
        try:
            remote_file = sftp_client.open(path)
        except IOError:
            raise TransportError("IOError")
        
        return remote_file.read().decode()


def get_transportSSH(host, port_, login, passwd):
    return SSH(host, port_,login, passwd)

###TESTS###
def test_init():
        SSH("localhost", 4000, "root", "screencast")
        with pytest.raises(TransportConnectionError):
            SSH("localhost1", 4000, "root", "screencast")
            SSH("localhost", 40001, "root", "screencast")
            SSH("localhost", 4000, "root1", "screencast")
            SSH("localhost", 4000, "root", "screencast1")

def test_exec():
    SSH("localhost", 4000, "root", "screencast").exec("ls /")
    with pytest.raises(TransportError):
        SSH("localhost", 4000, "root", "screencast").exec("asdfafsd")


def test_get_file():
    SSH("localhost", 4000, "root", "screencast").get_file("/root/test")
    with pytest.raises(TransportError):
        SSH("localhost", 4000, "root", "screencast").get_file("/root/test1")

        

##!/usr/bin/env python3.5
import paramiko
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

        print(stdout.read().decode())
        return [stdin, stdout, stderr]

    def get_file(self, path):
        sftp_client = self.client.open_sftp()
        try:
            remote_file = sftp_client.open(path)
        except IOError:
            raise TransportError("IOError")
        
        return remote_file.read().decode()


def get_transportSSH(host, port_, login, passwd):
    return SSH(host, port_,login, passwd)


class UnknownTransport(Exception):
    pass

def get_transport(transport_name, host, port, login, passwd):
    transport_names = {'ssh':get_transportSSH}

    if transport_name not in transport_names.keys():
        raise UnknownTransport

    return transport_names[transport_name](host,port,login, passwd)

if __name__=="__main__":
    get_transport('ssh', "localhost", 4000, "root", "screencast").get_file("asdf")

##!/usr/bin/env python3.5
import paramiko
import socket
import json


with open("env.json") as f:
    config = json.load(f)

class TransportError(Exception):
    pass

class TransportConnectionError(Exception):
    pass

class UnknownTransport(Exception):
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
            return self.client.exec_command(command)
        except SSHException:
            raise TransportConnectionError("SSHException")

    def get_file(self, path):
        sftp_client = self.client.open_sftp()
        try:
            remote_file = sftp_client.open(path)
        except IOError:
            raise TransportError("IOError")
        
        return remote_file.read().decode()

def get_transport(transport_name, host="", port="",login="", password=""):
    transport_names = {'SSH':SSH}
    
    transport_name = transport_name.upper()
    if transport_name not in transport_names:
        raise UnknownTransport

    if not host: host = config['host']
    if not port: port = config[transport_name]['port']
    if not login: login = config[transport_name]['login']
    if not password: password = config[transport_name]['password']

    print(login, port,  host, password)

    return transport_names[transport_name](host,port,login, password)

if __name__=="__main__":
    get_transport('ssh', "localhost", 4000, "root", "screencast")

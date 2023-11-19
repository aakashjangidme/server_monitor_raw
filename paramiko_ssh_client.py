import logging

import paramiko

from ssh_client import SSHClient


class ParamikoSSHClient(SSHClient):
    def __init__(self, hostname: str, username: str, password: str, verbose: bool = False):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.client = None
        self.verbose = verbose

    def connect(self) -> None:
        if self.verbose:
            logging.info(f"ParamikoSSHClient::connecting to {self.hostname}")
        if not self.client:
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.client.connect(self.hostname, username=self.username, password=self.password)

    def execute_command(self, command: str) -> str:
        if self.client is None:
            raise RuntimeError("SSH connection not established. Call connect() first.")
        if self.verbose:
            logging.info(f"Executing command on {self.hostname}: {command}")
        stdin, stdout, stderr = self.client.exec_command(command)
        return stdout.read().decode("utf-8")

    def disconnect(self) -> None:
        if self.verbose:
            logging.info(f"ParamikoSSHClient::disconnecting from {self.hostname}")
        if self.client:
            self.client.close()

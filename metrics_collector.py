from typing import Dict, List

from server_metric import MemoryUsage, DiskSpace, RunningProcesses
from ssh_client import SSHClient


class MetricsCollector:
    def __init__(self, ssh_client: SSHClient):
        self.ssh_client = ssh_client

        if self.ssh_client is None:
            assert "ssh_client is not initialised"

    def collect_metrics(self, metric_type):
        # Add logic to collect different types of metrics
        if metric_type == 'memory':
            return self.get_memory_usage()
        elif metric_type == 'disk_space':
            return self.get_disk_space()
        elif metric_type == 'running_processes':
            return self.get_running_processes()

    def collect_memory_usage(self) -> str:
        return self.ssh_client.execute_command("free -m")

    def collect_disk_space(self) -> str:
        return self.ssh_client.execute_command("df -h")

    def collect_running_processes(self) -> str:
        return self.ssh_client.execute_command("ps aux")

    def get_memory_usage(self) -> Dict[str, str]:
        raw_data = self.collect_memory_usage()
        parsed_data = MemoryUsage.parse(raw_data)
        return parsed_data

    def get_disk_space(self) -> Dict[str, str]:
        raw_data = self.collect_disk_space()
        parsed_data = DiskSpace.parse(raw_data)
        return parsed_data

    def get_running_processes(self) -> List[Dict[str, str]]:
        raw_data = self.collect_running_processes()
        parsed_data = RunningProcesses.parse(raw_data)
        return parsed_data

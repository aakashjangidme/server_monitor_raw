from data_aggregator import DataAggregator
from metrics_collector import MetricsCollector
from ssh_client import SSHClient


class ServerMetricsAggregator:
    def __init__(self, ssh_client: SSHClient):
        self.ssh_client = ssh_client
        self.data_aggregator = DataAggregator()
        self.metrics_collector: MetricsCollector | None = None

    def connect_ssh(self):
        self.ssh_client.connect()
        if not self.metrics_collector:
            self.metrics_collector = MetricsCollector(self.ssh_client)

    def disconnect_ssh(self):
        if self.ssh_client:
            self.ssh_client.disconnect()

    def aggregate_metrics(self):
        self.connect_ssh()

        metrics: list[str] = [
            "memory",
            "disk_space",
            "running_processes",
        ]

        for metric_type in metrics:
            metric_type_output = self.metrics_collector.collect_metrics(metric_type)
            self.data_aggregator.add_metric(metric_type, metric_type_output)

        aggregated_metrics = self.data_aggregator.get_aggregated_metrics()

        self.disconnect_ssh()

        return aggregated_metrics

# # Collect and parse memory metrics
# memory_output = self.metrics_collector.collect_memory_usage()
# memory_metrics = MemoryUsage.parse(memory_output)
# self.data_aggregator.add_metric(f"memory", memory_metrics)
#
# # Collect and parse disk space metrics
# disk_space_output = self.metrics_collector.collect_disk_space()
# disk_space_metrics = DiskSpace.parse(disk_space_output)
# self.data_aggregator.add_metric(f"disk_space", disk_space_metrics)
#
# # Collect and parse  running processes  metrics
# running_processes_output = self.metrics_collector.collect_running_processes()
# running_processes_metrics = RunningProcesses.parse(running_processes_output)
# self.data_aggregator.add_metric(f"running_processes", running_processes_metrics)

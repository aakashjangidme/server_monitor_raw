import json
import logging

import yaml

from alarm import AlarmManager
from filtered_metrics import get_filtered_metrics
from paramiko_ssh_client import ParamikoSSHClient
from server_metrics_aggregator import ServerMetricsAggregator

with open('server_config.yaml', 'r') as config_file:
    server_config = yaml.safe_load(config_file)


def main():
    aggregated_metrics = []

    for server in server_config['servers']:
        server_name = server.get('name')
        ssh_client = ParamikoSSHClient(server['address'], server['username'], server['password'])

        server_aggregator = ServerMetricsAggregator(ssh_client)
        metrics = server_aggregator.aggregate_metrics()

        server_data = {server_name: metrics}
        aggregated_metrics.append(server_data)

        alarm_manager = AlarmManager(server)

        alarm_manager.check_alarms(server_data)

    filtered_metrics = get_filtered_metrics(aggregated_metrics, server_config)

    print(json.dumps(filtered_metrics))


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    # print(json.dumps(server_config, indent=2))
    main()

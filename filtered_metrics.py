def get_filtered_metrics(metrics, server_config):
    """
    get filtered metrics based on the filters defined in the server_config.yaml
    :param metrics: aggregated metric list
    :param server_config: from server_config.yaml
    :return: filtered_metrics
    """
    filtered_metrics = []

    for server in server_config['servers']:
        server_name = server['name']
        server_data = next((data for data in metrics if server_name in data), None)

        if server_data:
            filtered_data = {
                server_name: {
                    'memory': server_data[server_name]['memory'],
                    'disk_space': {mp: data for mp, data in server_data[server_name]['disk_space'].items() if
                                   mp in server['mount_points']},
                    'running_processes': [process_data for process_data in server_data[server_name]['running_processes']
                                          if any(process in process_data['command'] for process in server['processes'])]
                }
            }

            # Include processes from YAML not found in server metrics
            filtered_data[server_name]['running_processes'].extend({
                                                                       "user": "",
                                                                       "pid": "",
                                                                       "cpu_usage": "",
                                                                       "memory_usage": "",
                                                                       "command": f"Process {process} not found",
                                                                   } for process in server['processes'] if not any(
                process_data['command'].__contains__(process) for process_data in
                filtered_data[server_name]['running_processes']))

            # Include disk space from YAML not found in server metrics
            filtered_data[server_name]['disk_space'].update({
                mount_point: {
                    "size": "N/A",
                    "used": "N/A",
                    "available": "N/A",
                    "capacity": "N/A",
                } for mount_point in server['mount_points'] if
                mount_point not in filtered_data[server_name]['disk_space']
            })

            filtered_metrics.append(filtered_data)

    return filtered_metrics

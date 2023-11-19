import logging
from typing import Dict

from send_notification import send_email_notification
from utils import parse_condition


def evaluate_condition(expression: str, metric_type: str, server_name: str, metric_value: float, condition: Dict):
    """
    Evaluate the condition using eval and handle alarms accordingly.
    """
    try:
        if eval(expression):
            logging.debug(
                f"{metric_type.capitalize()} Alarm on {server_name}: value {metric_value} is {condition['operator']} {condition['value']} MB")
            send_email_notification(server_name, metric_type, condition['value'],
                                    f"current metric_value = {metric_value}")
    except Exception as e:
        logging.error(f"Error checking alarm for {metric_type} on {server_name}: {str(e)}")
        # Handle the error, e.g., send an error notification


def extract_metric_values(metric_type: str, server_metrics: Dict, alarms_config) -> Dict:
    """
    Extract metric values based on metric type.
    """
    if metric_type == "memory":
        return {metric_type: server_metrics.get(metric_type, {}).get(metric_type, None)}
    elif metric_type == "disk_space":
        return {mount_point: server_metrics.get(metric_type, {}).get(mount_point, {}).get('available', None)
                for mount_point in alarms_config.get('mount_points', [])}


def process_metric_values(metric_values: Dict, metric_type: str) -> Dict:
    """
    Process metric values based on metric type.
    """
    if metric_type == "disk_space":
        return {mount_point: gb_to_mb(float(value[:-1])) for mount_point, value in metric_values.items() if
                value is not None}
    return metric_values


class AlarmManager:
    def __init__(self, alarms_config):
        self.alarms_config: dict = alarms_config
        logging.debug(f"alarms_config = {alarms_config}")

    def check_alarms(self, server_metrics):
        logging.debug(f"server_metrics = {server_metrics}")

        server_name, server_metrics = next(iter(server_metrics.items()))

        logging.debug(f"server_name = {server_name}")

        for metric_type, alarms in self.alarms_config.get('alarms', {}).items():
            logging.debug(f"metric_type = {metric_type}, alarms = {alarms}")

            metric_values = extract_metric_values(metric_type, server_metrics, self.alarms_config)

            logging.debug(f"metric_values = {metric_values}")

            metric_values = process_metric_values(metric_values, metric_type)

            if metric_values is not None:
                for alarm in alarms:
                    logging.debug(f"alarm = {alarm}")

                    condition = parse_condition(alarm)

                    logging.debug(f"condition = {condition}")

                    for mount_point, metric_value in metric_values.items():
                        if metric_value is not None:
                            expression = f"{metric_value} {condition['operator']} {condition['value']}"
                            evaluate_condition(expression, metric_type, server_name, metric_value, condition)

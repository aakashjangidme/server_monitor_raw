from typing import Dict, List, Union


class DataAggregator:
    def __init__(self):
        self.metrics = {}

    def add_metric(self, metric_name: str, metric_data: Union[Dict[str, str], List[Dict[str, str]]]):
        # Add the parsed metric data to the structured format
        self.metrics[metric_name] = metric_data

    def get_aggregated_metrics(self) -> Dict[str, Dict[str, str]]:
        return self.metrics

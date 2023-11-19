from abc import ABC, abstractmethod
from typing import Dict, List


class ServerMetric(ABC):
    @staticmethod
    @abstractmethod
    def parse(raw_data: str) -> Dict[str, str]:
        pass


class MemoryUsage(ServerMetric):
    @staticmethod
    def parse(raw_data: str) -> Dict[str, str]:
        parsed_data = {}
        lines = raw_data.split("\n")

        # Parse memory data from the 'free -m' command
        for line in lines[1:]:
            parts = line.split()
            if len(parts) >= 2:
                key = parts[0].strip(':')
                # Change key names to 'memory' and 'swap'
                if key == 'Mem':
                    key = 'memory'
                elif key == 'Swap':
                    key = 'swap'

                value = parts[1]
                parsed_data[key] = value

        return parsed_data


class DiskSpace(ServerMetric):
    @staticmethod
    def parse(raw_data: str) -> Dict[str, str]:
        parsed_data = {}
        lines = raw_data.split("\n")

        # Parse disk space data from the 'df -h' command
        for line in lines[1:]:
            parts = line.split()
            if len(parts) >= 6:
                filesystem, size, used, available, capacity, mount_point = parts
                parsed_data[mount_point] = {
                    "size": size,
                    "used": used,
                    "available": available,
                    "capacity": capacity,
                }

        return parsed_data


class RunningProcesses(ServerMetric):
    @staticmethod
    def parse(raw_data: str) -> List[Dict[str, str]]:
        parsed_data = []
        lines = raw_data.split("\n")

        # Parse process data from the 'ps aux' command
        for line in lines[1:]:
            parts = line.split(None, 10)
            if len(parts) == 11:
                user, pid, cpu, memory, vsz, rss, tty, stat, start, time, command = parts
                parsed_data.append({
                    "user": user,
                    "pid": pid,
                    "cpu_usage": cpu,
                    "memory_usage": memory,
                    "command": command,
                })

        return parsed_data

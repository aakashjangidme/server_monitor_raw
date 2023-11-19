import unittest
from unittest.mock import patch

from alarm import evaluate_condition
from utils import parse_unit_value, gb_to_mb, parse_condition


class TestServerMonitorRaw(unittest.TestCase):

    def test_parse_unit_value(self):
        self.assertEqual(parse_unit_value("5.gb"), 5120.0)

    def test_gb_to_mb(self):
        self.assertEqual(gb_to_mb(5.0), 5120.0)

    def test_parse_condition(self):
        self.assertEqual(parse_condition("memory < 5.gb"), {'metric': 'memory', 'operator': '<', 'value': 5120.0})

    def test_evaluate_condition(self):
        with patch("send_notification.send_email_notification") as mock_send_email:
            evaluate_condition("5.0 < 5120.0", "memory", "server-1", 5.0,
                               {'metric': 'memory', 'operator': '<', 'value': 5120.0})


if __name__ == '__main__':
    unittest.main()

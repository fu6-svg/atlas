"""Tests for the Project Atlas health monitor."""

import os
import sys
import unittest

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_PATH = os.path.join(PROJECT_ROOT, "src")

# 让测试文件可以直接导入 src 目录中的项目模块
if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)

from health_monitor import (
    get_battery_health,
    get_cpu_health,
    get_overall_health,
    get_sensor_health,
    get_temperature_health,
)


class HealthMonitorTestCase(unittest.TestCase):
    """Test health calculation return values."""

    def setUp(self):
        """Create a healthy robot status dictionary for repeated tests."""
        # setUp 保存重复使用的测试数据，避免每个测试都重新写一遍
        self.robot_status = {
            "name": "Atlas",
            "mode": "AUTO",
            "battery": 95,
            "temperature": 36.5,
            "speed": 18,
            "location": "Lab A",
            "cpu_usage": 35,
            "camera_status": "OK",
            "imu_status": "OK"
        }

    def test_battery_health_returns_expected_levels(self):
        """Battery health should match critical, low, and good thresholds."""
        self.assertEqual(get_battery_health(5), "CRITICAL")
        self.assertEqual(get_battery_health(9), "CRITICAL")
        self.assertEqual(get_battery_health(10), "LOW")
        self.assertEqual(get_battery_health(19), "LOW")
        self.assertEqual(get_battery_health(20), "GOOD")
        self.assertEqual(get_battery_health(95), "GOOD")

    def test_temperature_health_returns_expected_levels(self):
        """Temperature health should match good, high, and critical levels."""
        self.assertEqual(get_temperature_health(70), "GOOD")
        self.assertEqual(get_temperature_health(71), "HIGH")
        self.assertEqual(get_temperature_health(90), "HIGH")
        self.assertEqual(get_temperature_health(91), "CRITICAL")

    def test_cpu_health_returns_expected_levels(self):
        """CPU health should match good, high, and critical levels."""
        self.assertEqual(get_cpu_health(90), "GOOD")
        self.assertEqual(get_cpu_health(91), "HIGH")
        self.assertEqual(get_cpu_health(95), "HIGH")
        self.assertEqual(get_cpu_health(96), "CRITICAL")

    def test_sensor_health_returns_good_or_error(self):
        """Sensor health should be GOOD only when the sensor status is OK."""
        self.assertEqual(get_sensor_health("OK"), "GOOD")
        self.assertEqual(get_sensor_health("ERROR"), "ERROR")

    def test_overall_health_returns_healthy_for_normal_values(self):
        """Overall health should be HEALTHY when all subsystems are normal."""
        self.assertEqual(get_overall_health(self.robot_status), "HEALTHY")

    def test_overall_health_returns_warning_for_low_battery(self):
        """Overall health should be WARNING when battery is low."""
        self.robot_status["battery"] = 15
        self.assertEqual(get_overall_health(self.robot_status), "WARNING")

    def test_overall_health_returns_warning_for_high_temperature(self):
        """Overall health should be WARNING when temperature is high."""
        self.robot_status["temperature"] = 80
        self.assertEqual(get_overall_health(self.robot_status), "WARNING")

    def test_overall_health_returns_warning_for_high_cpu(self):
        """Overall health should be WARNING when CPU usage is high."""
        self.robot_status["cpu_usage"] = 92
        self.assertEqual(get_overall_health(self.robot_status), "WARNING")

    def test_overall_health_returns_critical_for_critical_battery(self):
        """Overall health should be CRITICAL when battery is critical."""
        self.robot_status["battery"] = 5
        self.assertEqual(get_overall_health(self.robot_status), "CRITICAL")

    def test_overall_health_returns_critical_for_camera_error(self):
        """Overall health should be CRITICAL when camera has an error."""
        self.robot_status["camera_status"] = "ERROR"
        self.assertEqual(get_overall_health(self.robot_status), "CRITICAL")

    def test_overall_health_returns_critical_for_imu_error(self):
        """Overall health should be CRITICAL when IMU has an error."""
        self.robot_status["imu_status"] = "ERROR"
        self.assertEqual(get_overall_health(self.robot_status), "CRITICAL")


if __name__ == "__main__":
    unittest.main()

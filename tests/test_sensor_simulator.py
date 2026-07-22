"""Tests for the Project Atlas sensor simulator."""

import os
import sys
import unittest
from unittest.mock import patch

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_PATH = os.path.join(PROJECT_ROOT, "src")

# 让测试文件可以直接导入 src 目录中的项目模块
if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)

from sensor_simulator import keep_value_in_range, simulate_sensor_update


class SensorSimulatorTestCase(unittest.TestCase):
    """Test sensor value updates and range limits."""

    def setUp(self):
        """Create a robot status dictionary for repeated tests."""
        # 测试使用固定初始值，方便检查随机变化后的结果
        self.robot_status = {
            "name": "Atlas",
            "mode": "AUTO",
            "battery": 50,
            "temperature": 30.0,
            "speed": 10.0,
            "location": "Lab A",
            "cpu_usage": 40,
            "camera_status": "OK",
            "imu_status": "OK"
        }

    def test_keep_value_in_range_limits_values(self):
        """Values should stay inside the requested range."""
        self.assertEqual(keep_value_in_range(-1, 0, 100), 0)
        self.assertEqual(keep_value_in_range(101, 0, 100), 100)
        self.assertEqual(keep_value_in_range(50, 0, 100), 50)
        self.assertEqual(keep_value_in_range(0, 0, 100), 0)
        self.assertEqual(keep_value_in_range(100, 0, 100), 100)

    @patch("sensor_simulator.random.random")
    @patch("sensor_simulator.random.uniform")
    @patch("sensor_simulator.random.randint")
    def test_simulate_sensor_update_updates_values_in_place(
        self,
        mock_randint,
        mock_uniform,
        mock_random
    ):
        """Sensor update should apply controlled random changes in place."""
        # mock 固定随机输出，让测试结果稳定可预测
        mock_randint.side_effect = [3, 12]
        mock_uniform.side_effect = [2.5, -4.5]
        mock_random.side_effect = [0.1, 0.96]

        original_dictionary = self.robot_status
        updated_status = simulate_sensor_update(self.robot_status)

        self.assertIs(updated_status, original_dictionary)
        self.assertEqual(updated_status["battery"], 47)
        self.assertEqual(updated_status["temperature"], 32.5)
        self.assertEqual(updated_status["speed"], 5.5)
        self.assertEqual(updated_status["cpu_usage"], 52)
        self.assertEqual(updated_status["camera_status"], "OK")
        self.assertEqual(updated_status["imu_status"], "ERROR")

    @patch("sensor_simulator.random.random")
    @patch("sensor_simulator.random.uniform")
    @patch("sensor_simulator.random.randint")
    def test_simulate_sensor_update_keeps_values_inside_limits(
        self,
        mock_randint,
        mock_uniform,
        mock_random
    ):
        """Sensor update should not allow values outside valid limits."""
        # 这些 mock 值会尝试把数据推到边界之外
        self.robot_status["battery"] = 2
        self.robot_status["temperature"] = 119.0
        self.robot_status["speed"] = 1.0
        self.robot_status["cpu_usage"] = 98

        mock_randint.side_effect = [4, 15]
        mock_uniform.side_effect = [4.0, -5.0]
        mock_random.side_effect = [0.95, 0.01]

        updated_status = simulate_sensor_update(self.robot_status)

        self.assertEqual(updated_status["battery"], 0)
        self.assertEqual(updated_status["temperature"], 120)
        self.assertEqual(updated_status["speed"], 0)
        self.assertEqual(updated_status["cpu_usage"], 100)
        self.assertEqual(updated_status["camera_status"], "ERROR")
        self.assertEqual(updated_status["imu_status"], "OK")


if __name__ == "__main__":
    unittest.main()

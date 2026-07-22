"""Tests for the Project Atlas robot runtime."""

import os
import sys
import unittest

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_PATH = os.path.join(PROJECT_ROOT, "src")

# 让测试文件可以直接导入 src 目录中的项目模块
if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)

from robot_runtime import (
    apply_safety_decision,
    get_event_level,
    reset_robot_after_emergency,
)


class RobotRuntimeTestCase(unittest.TestCase):
    """Test runtime safety decisions and emergency reset behavior."""

    def setUp(self):
        """Create a healthy robot status dictionary for repeated tests."""
        # 每个测试都拿到新的字典，避免测试之间互相影响
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

    def test_apply_safety_decision_keeps_healthy_robot_normal(self):
        """Healthy robot should keep its mode and speed."""
        decision = apply_safety_decision(self.robot_status)

        self.assertEqual(decision, "NORMAL OPERATION")
        self.assertEqual(self.robot_status["mode"], "AUTO")
        self.assertEqual(self.robot_status["speed"], 18)

    def test_apply_safety_decision_limits_warning_robot_speed(self):
        """Warning robot should reduce speed to 10 when moving too fast."""
        self.robot_status["battery"] = 15
        self.robot_status["speed"] = 25

        decision = apply_safety_decision(self.robot_status)

        self.assertEqual(decision, "LIMITED OPERATION")
        self.assertEqual(self.robot_status["speed"], 10)

    def test_apply_safety_decision_keeps_slow_warning_robot_speed(self):
        """Warning robot should keep speed when already moving slowly."""
        self.robot_status["battery"] = 15
        self.robot_status["speed"] = 6

        decision = apply_safety_decision(self.robot_status)

        self.assertEqual(decision, "LIMITED OPERATION")
        self.assertEqual(self.robot_status["speed"], 6)

    def test_apply_safety_decision_stops_critical_robot(self):
        """Critical robot should enter emergency mode and stop."""
        self.robot_status["battery"] = 5
        self.robot_status["speed"] = 25

        decision = apply_safety_decision(self.robot_status)

        self.assertEqual(decision, "EMERGENCY STOP")
        self.assertEqual(self.robot_status["mode"], "EMERGENCY")
        self.assertEqual(self.robot_status["speed"], 0)

    def test_get_event_level_returns_expected_levels(self):
        """Runtime decisions should map to event levels."""
        self.assertEqual(get_event_level("NORMAL OPERATION"), "INFO")
        self.assertEqual(get_event_level("LIMITED OPERATION"), "WARNING")
        self.assertEqual(get_event_level("EMERGENCY STOP"), "CRITICAL")
        self.assertEqual(get_event_level("SOMETHING ELSE"), "UNKNOWN")

    def test_reset_robot_after_emergency_resets_only_required_fields(self):
        """Emergency reset should not repair battery, temperature, or CPU."""
        self.robot_status["mode"] = "EMERGENCY"
        self.robot_status["speed"] = 25
        self.robot_status["battery"] = 5
        self.robot_status["temperature"] = 95
        self.robot_status["cpu_usage"] = 98
        self.robot_status["camera_status"] = "ERROR"
        self.robot_status["imu_status"] = "ERROR"

        reset_robot_after_emergency(self.robot_status)

        self.assertEqual(self.robot_status["mode"], "MANUAL")
        self.assertEqual(self.robot_status["speed"], 0)
        self.assertEqual(self.robot_status["camera_status"], "OK")
        self.assertEqual(self.robot_status["imu_status"], "OK")
        self.assertEqual(self.robot_status["battery"], 5)
        self.assertEqual(self.robot_status["temperature"], 95)
        self.assertEqual(self.robot_status["cpu_usage"], 98)


if __name__ == "__main__":
    unittest.main()

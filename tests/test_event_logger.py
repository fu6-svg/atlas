"""Tests for the Project Atlas runtime event logger."""

import csv
import os
import sys
import tempfile
import unittest

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_PATH = os.path.join(PROJECT_ROOT, "src")

# 让测试文件可以直接导入 src 目录中的项目模块
if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)

from event_logger import (
    EVENT_LOG_HEADER,
    clear_runtime_events,
    create_event_log_if_needed,
    get_safety_reason,
    log_runtime_event,
)


class EventLoggerTestCase(unittest.TestCase):
    """Test runtime event reasons and CSV file operations."""

    def setUp(self):
        """Create a healthy robot status dictionary for repeated tests."""
        # 每个测试使用独立字典，避免状态污染
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

    def test_get_safety_reason_returns_normal_reason(self):
        """Healthy robot should report that all systems are normal."""
        reason = get_safety_reason(self.robot_status)
        self.assertEqual(reason, "All systems normal")

    def test_get_safety_reason_reports_battery_problems(self):
        """Battery problems should produce clear safety reasons."""
        self.robot_status["battery"] = 5
        self.assertIn("Battery critically low", get_safety_reason(
            self.robot_status
        ))

        self.robot_status["battery"] = 15
        self.assertIn("Battery low", get_safety_reason(self.robot_status))

    def test_get_safety_reason_reports_temperature_problems(self):
        """Temperature problems should produce clear safety reasons."""
        self.robot_status["temperature"] = 95
        self.assertIn("Temperature critical", get_safety_reason(
            self.robot_status
        ))

        self.robot_status["temperature"] = 80
        self.assertIn("Temperature high", get_safety_reason(
            self.robot_status
        ))

    def test_get_safety_reason_reports_cpu_problems(self):
        """CPU problems should produce clear safety reasons."""
        self.robot_status["cpu_usage"] = 98
        self.assertIn("CPU usage critical", get_safety_reason(
            self.robot_status
        ))

        self.robot_status["cpu_usage"] = 92
        self.assertIn("CPU usage high", get_safety_reason(self.robot_status))

    def test_get_safety_reason_reports_sensor_failures(self):
        """Sensor failures should produce clear safety reasons."""
        self.robot_status["camera_status"] = "ERROR"
        self.assertIn("Camera failure", get_safety_reason(self.robot_status))

        self.robot_status["camera_status"] = "OK"
        self.robot_status["imu_status"] = "ERROR"
        self.assertIn("IMU failure", get_safety_reason(self.robot_status))

    def test_get_safety_reason_combines_multiple_problems(self):
        """Multiple problems should be combined with semicolons."""
        self.robot_status["battery"] = 5
        self.robot_status["temperature"] = 95
        self.robot_status["camera_status"] = "ERROR"

        reason = get_safety_reason(self.robot_status)

        self.assertIn("Battery critically low", reason)
        self.assertIn("Temperature critical", reason)
        self.assertIn("Camera failure", reason)
        self.assertIn("; ", reason)

    def test_create_event_log_if_needed_creates_file_with_header(self):
        """Event log creation should write the expected header."""
        with tempfile.TemporaryDirectory() as temporary_directory:
            file_path = os.path.join(temporary_directory, "events.csv")

            create_event_log_if_needed(file_path)

            with open(file_path, "r", newline="", encoding="utf-8") as file:
                reader = csv.reader(file)
                header = next(reader)

            self.assertEqual(header, EVENT_LOG_HEADER)

    def test_log_runtime_event_appends_rows(self):
        """Runtime event logging should append data rows without overwrite."""
        with tempfile.TemporaryDirectory() as temporary_directory:
            file_path = os.path.join(temporary_directory, "events.csv")

            log_runtime_event(
                self.robot_status,
                1,
                "INFO",
                "NORMAL OPERATION",
                "All systems normal",
                file_path
            )
            log_runtime_event(
                self.robot_status,
                2,
                "WARNING",
                "LIMITED OPERATION",
                "Battery low",
                file_path
            )

            with open(file_path, "r", newline="", encoding="utf-8") as file:
                reader = csv.reader(file)
                rows = []
                for row in reader:
                    rows.append(row)

            self.assertEqual(rows[0], EVENT_LOG_HEADER)
            self.assertEqual(len(rows), 3)
            self.assertEqual(rows[1][1], "1")
            self.assertEqual(rows[2][1], "2")

    def test_clear_runtime_events_leaves_only_header(self):
        """Clearing runtime events should keep only the header row."""
        with tempfile.TemporaryDirectory() as temporary_directory:
            file_path = os.path.join(temporary_directory, "events.csv")

            log_runtime_event(
                self.robot_status,
                1,
                "INFO",
                "NORMAL OPERATION",
                "All systems normal",
                file_path
            )
            clear_runtime_events(file_path)

            with open(file_path, "r", newline="", encoding="utf-8") as file:
                reader = csv.reader(file)
                rows = []
                for row in reader:
                    rows.append(row)

            self.assertEqual(rows, [EVENT_LOG_HEADER])


if __name__ == "__main__":
    unittest.main()

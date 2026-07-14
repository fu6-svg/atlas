"""CSV data logging functions for Project Atlas."""

import csv
import os
from datetime import datetime

from health_monitor import get_overall_health

DEFAULT_LOG_PATH = os.path.join("data", "sensor_log.csv")

LOG_HEADER = [
    "timestamp",
    "cycle",
    "name",
    "mode",
    "battery",
    "temperature",
    "speed",
    "location",
    "cpu_usage",
    "camera_status",
    "imu_status",
    "overall_health"
]


def create_log_file_if_needed(file_path):
    """Create the CSV log file and parent directory if needed."""
    parent_directory = os.path.dirname(file_path)

    # 如果 data 文件夹不存在，先创建文件夹
    if parent_directory != "" and os.path.exists(parent_directory) is False:
        os.makedirs(parent_directory)

    # 如果 CSV 文件不存在，创建文件并写入表头
    if os.path.exists(file_path) is False:
        clear_log_file(file_path)


def log_robot_status(robot_status, cycle_number, file_path):
    """Append one robot status row to the CSV log file."""
    create_log_file_if_needed(file_path)
    timestamp = datetime.now().isoformat(timespec="seconds")
    overall_health = get_overall_health(robot_status)

    row = [
        timestamp,
        cycle_number,
        robot_status["name"],
        robot_status["mode"],
        robot_status["battery"],
        robot_status["temperature"],
        robot_status["speed"],
        robot_status["location"],
        robot_status["cpu_usage"],
        robot_status["camera_status"],
        robot_status["imu_status"],
        overall_health
    ]

    # 使用 append 模式追加新数据，避免覆盖旧日志
    with open(file_path, "a", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(row)


def clear_log_file(file_path):
    """Recreate the CSV log file with only the header row."""
    parent_directory = os.path.dirname(file_path)

    # 清空前同样确认父文件夹存在
    if parent_directory != "" and os.path.exists(parent_directory) is False:
        os.makedirs(parent_directory)

    # 使用 write 模式重建文件，只保留 CSV 表头
    with open(file_path, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(LOG_HEADER)


def show_recent_log_entries(file_path, number_of_entries):
    """Display the most recent rows from the CSV log file."""
    if os.path.exists(file_path) is False:
        print("No log file found.")
        return

    rows = []

    # 读取 CSV 文件，把数据行保存到列表中
    with open(file_path, "r", newline="", encoding="utf-8") as csv_file:
        reader = csv.reader(csv_file)
        header = next(reader, None)

        for row in reader:
            rows.append(row)

    if header is None or len(rows) == 0:
        print("No log entries found.")
        return

    start_index = len(rows) - number_of_entries
    if start_index < 0:
        start_index = 0

    print()
    print("========== Recent Sensor Logs ==========")
    print(", ".join(header))

    # 只显示最近的指定行数，方便查看最新传感器数据
    index = start_index
    while index < len(rows):
        print(", ".join(rows[index]))
        index = index + 1

    print("========================================")
    print()

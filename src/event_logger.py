"""Runtime event logging functions for Project Atlas."""

import csv
import os
from datetime import datetime

DEFAULT_EVENT_LOG_PATH = os.path.join(
    "data",
    "runtime_events.csv"
)

EVENT_LOG_HEADER = [
    "timestamp",
    "cycle",
    "event_level",
    "decision",
    "reason",
    "mode",
    "battery",
    "temperature",
    "speed",
    "cpu_usage",
    "camera_status",
    "imu_status"
]


def create_event_log_if_needed(file_path):
    """Create the runtime event log file if it does not exist."""
    parent_directory = os.path.dirname(file_path)

    # 如果 data 文件夹不存在，先创建文件夹
    if parent_directory != "" and os.path.exists(parent_directory) is False:
        os.makedirs(parent_directory)

    # 只在文件不存在时写入表头，避免重复写表头
    if os.path.exists(file_path) is False:
        clear_runtime_events(file_path)


def get_safety_reason(robot_status):
    """Return a clear reason for the current robot safety state."""
    reasons = []

    # 逐项检查健康问题，多个问题会一起记录
    if robot_status["battery"] < 10:
        reasons.append("Battery critically low")
    elif robot_status["battery"] < 20:
        reasons.append("Battery low")

    if robot_status["temperature"] > 90:
        reasons.append("Temperature critical")
    elif robot_status["temperature"] > 70:
        reasons.append("Temperature high")

    if robot_status["cpu_usage"] > 95:
        reasons.append("CPU usage critical")
    elif robot_status["cpu_usage"] > 90:
        reasons.append("CPU usage high")

    if robot_status["camera_status"] != "OK":
        reasons.append("Camera failure")

    if robot_status["imu_status"] != "OK":
        reasons.append("IMU failure")

    if len(reasons) == 0:
        return "All systems normal"

    return "; ".join(reasons)


def log_runtime_event(
    robot_status,
    cycle_number,
    event_level,
    decision,
    reason,
    file_path=DEFAULT_EVENT_LOG_PATH
):
    """Append one runtime event row to the CSV event log."""
    create_event_log_if_needed(file_path)
    timestamp = datetime.now().isoformat(timespec="seconds")

    row = [
        timestamp,
        cycle_number,
        event_level,
        decision,
        reason,
        robot_status["mode"],
        robot_status["battery"],
        robot_status["temperature"],
        robot_status["speed"],
        robot_status["cpu_usage"],
        robot_status["camera_status"],
        robot_status["imu_status"]
    ]

    # 使用 append 模式追加事件，保留历史运行记录
    with open(file_path, "a", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(row)


def show_recent_runtime_events(file_path, number_of_entries):
    """Display the most recent runtime event rows."""
    if os.path.exists(file_path) is False:
        print("No runtime event log found.")
        return

    rows = []

    # 读取 CSV 文件，跳过表头后保存事件行
    with open(file_path, "r", newline="", encoding="utf-8") as csv_file:
        reader = csv.reader(csv_file)
        header = next(reader, None)

        for row in reader:
            rows.append(row)

    if header is None or len(rows) == 0:
        print("No runtime events found.")
        return

    start_index = len(rows) - number_of_entries
    if start_index < 0:
        start_index = 0

    print()
    print("========== Recent Runtime Events ==========")
    print(", ".join(header))

    # 只显示最近的事件，方便定位最新安全决策
    index = start_index
    while index < len(rows):
        print(", ".join(rows[index]))
        index = index + 1

    print("===========================================")
    print()


def clear_runtime_events(file_path):
    """Recreate the runtime event log with only the header row."""
    parent_directory = os.path.dirname(file_path)

    # 清空日志前确保目录存在
    if parent_directory != "" and os.path.exists(parent_directory) is False:
        os.makedirs(parent_directory)

    # 使用 write 模式重建文件，只保留 CSV 表头
    with open(file_path, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(EVENT_LOG_HEADER)

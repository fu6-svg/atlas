"""Sensor data simulation functions for Project Atlas."""

import random
import time

from data_logger import DEFAULT_LOG_PATH, log_robot_status
from health_monitor import show_health_report
from robot_status import show_robot_status


def keep_value_in_range(value, minimum_value, maximum_value):
    """Return a value that stays inside the allowed range."""
    # 限制数值范围，避免模拟数据超过真实传感器边界
    if value < minimum_value:
        return minimum_value
    if value > maximum_value:
        return maximum_value
    return value


def simulate_sensor_update(robot_status):
    """Update robot sensor data in place and return robot_status."""
    # 随机生成传感器变化，模拟真实机器人运行中的数据波动
    battery_drop = random.randint(1, 4)
    temperature_change = random.uniform(-2.0, 4.0)
    speed_change = random.uniform(-5.0, 5.0)
    cpu_change = random.randint(-10, 15)

    # 直接更新同一个字典，让其他模块看到最新状态
    robot_status["battery"] = robot_status["battery"] - battery_drop
    robot_status["temperature"] = (
        robot_status["temperature"] + temperature_change
    )
    robot_status["speed"] = robot_status["speed"] + speed_change
    robot_status["cpu_usage"] = robot_status["cpu_usage"] + cpu_change

    # 对模拟结果做范围限制，保证数据仍然合理
    robot_status["battery"] = keep_value_in_range(
        robot_status["battery"],
        0,
        100
    )
    robot_status["temperature"] = keep_value_in_range(
        robot_status["temperature"],
        -40,
        120
    )
    if robot_status["speed"] < 0:
        robot_status["speed"] = 0
    robot_status["cpu_usage"] = keep_value_in_range(
        robot_status["cpu_usage"],
        0,
        100
    )

    robot_status["temperature"] = round(robot_status["temperature"], 1)
    robot_status["speed"] = round(robot_status["speed"], 1)

    # 摄像头大约 90% 正常，10% 错误
    if random.random() < 0.9:
        robot_status["camera_status"] = "OK"
    else:
        robot_status["camera_status"] = "ERROR"

    # IMU 大约 95% 正常，5% 错误
    if random.random() < 0.95:
        robot_status["imu_status"] = "OK"
    else:
        robot_status["imu_status"] = "ERROR"

    return robot_status


def run_sensor_simulation(robot_status, number_of_cycles, delay_seconds):
    """Run repeated sensor updates and display status each cycle."""
    # 使用基础 for 循环重复模拟指定次数
    for cycle_number in range(1, number_of_cycles + 1):
        print()
        print("Sensor Simulation Cycle:", cycle_number)
        simulate_sensor_update(robot_status)
        log_robot_status(robot_status, cycle_number, DEFAULT_LOG_PATH)
        show_robot_status()
        show_health_report(robot_status)

        # time.sleep 用来模拟两次传感器读取之间的等待时间
        time.sleep(delay_seconds)

    return robot_status

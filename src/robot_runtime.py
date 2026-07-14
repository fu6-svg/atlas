"""Automatic robot runtime loop for Project Atlas."""

import time

from data_logger import DEFAULT_LOG_PATH, log_robot_status
from health_monitor import get_overall_health, show_health_report
from robot_status import show_robot_status
from sensor_simulator import simulate_sensor_update


def apply_safety_decision(robot_status):
    """Apply a basic safety decision based on robot health."""
    overall_health = get_overall_health(robot_status)

    # 严重健康问题时，立即进入急停模式并停止运动
    if overall_health == "CRITICAL":
        robot_status["mode"] = "EMERGENCY"
        robot_status["speed"] = 0
        return "EMERGENCY STOP"

    # 警告状态下限制速度，允许机器人低速运行
    if overall_health == "WARNING":
        if robot_status["speed"] > 10:
            robot_status["speed"] = 10
        return "LIMITED OPERATION"

    # 健康状态下保持正常运行
    if overall_health == "HEALTHY":
        return "NORMAL OPERATION"

    return "UNKNOWN HEALTH STATE"


def run_robot_runtime(
    robot_status,
    number_of_cycles,
    delay_seconds,
    log_file_path=DEFAULT_LOG_PATH
):
    """Run the automatic robot runtime loop."""
    for cycle_number in range(1, number_of_cycles + 1):
        print()
        print("Runtime Cycle:", cycle_number)

        # 每个周期先读取模拟传感器数据，再做安全决策
        simulate_sensor_update(robot_status)
        runtime_decision = apply_safety_decision(robot_status)

        log_robot_status(robot_status, cycle_number, log_file_path)
        show_robot_status()
        show_health_report(robot_status)
        print("Runtime Decision:", runtime_decision)

        # 如果进入急停模式，立即停止运行循环
        if robot_status["mode"] == "EMERGENCY":
            print("Emergency stop activated. Runtime stopped early.")
            break

        # 最后一个周期结束后不需要等待
        if cycle_number < number_of_cycles:
            time.sleep(delay_seconds)

    return robot_status


def reset_robot_after_emergency(robot_status):
    """Reset the robot after an emergency stop."""
    # 复位只恢复人工控制和传感器状态，不自动修复电池、温度或 CPU
    robot_status["mode"] = "MANUAL"
    robot_status["speed"] = 0
    robot_status["camera_status"] = "OK"
    robot_status["imu_status"] = "OK"
    return robot_status

"""Robot status data and functions for the Atlas Robot Dashboard."""

from health_monitor import show_health_report
from input_utils import (
    get_minimum_number,
    get_number_in_range,
    get_status_input,
)

robot_status = {
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


def show_robot_status():
    """Display current robot status values."""
    print()
    print("========== Robot Status ==========")
    print("Robot Name   :", robot_status["name"])
    print("Mode         :", robot_status["mode"])
    print("Battery      :", robot_status["battery"], "%")
    print("Temperature  :", robot_status["temperature"], "°C")
    print("Speed        :", robot_status["speed"], "km/h")
    print("Location     :", robot_status["location"])
    print("CPU Usage    :", robot_status["cpu_usage"], "%")
    print("Camera Status:", robot_status["camera_status"])
    print("IMU Status   :", robot_status["imu_status"])
    print("==================================")
    print()


def update_robot_status():
    """Update robot health and sensor status values."""
    print()
    print("Update Robot Status")

    # 逐项更新机器人状态，方便初学者理解数据流向
    robot_status["battery"] = get_number_in_range("Battery (%): ", 0, 100)
    robot_status["temperature"] = get_number_in_range(
        "Temperature (°C): ",
        -40,
        120
    )
    robot_status["speed"] = get_minimum_number("Speed (km/h): ", 0)
    robot_status["location"] = input("Location: ")
    robot_status["cpu_usage"] = get_number_in_range("CPU Usage (%): ", 0, 100)
    robot_status["camera_status"] = get_status_input("Camera Status: ")
    robot_status["imu_status"] = get_status_input("IMU Status: ")
    print("Robot status updated.")


def change_robot_mode():
    """Change the robot mode to AUTO, MANUAL, or EMERGENCY."""
    print()
    print("Choose Robot Mode")
    print("1.AUTO")
    print("2.MANUAL")
    print("3.EMERGENCY")

    mode_choice = input("Please choose a mode: ")

    # 只允许切换到预设的三种机器人模式
    if mode_choice == "1":
        robot_status["mode"] = "AUTO"
        print("Robot mode changed to AUTO.")
    elif mode_choice == "2":
        robot_status["mode"] = "MANUAL"
        print("Robot mode changed to MANUAL.")
    elif mode_choice == "3":
        robot_status["mode"] = "EMERGENCY"
        print("Robot mode changed to EMERGENCY.")
    else:
        print("Invalid mode. Robot mode was not changed.")

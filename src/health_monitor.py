"""Robot health calculation and report functions."""


def get_battery_health(battery):
    """Return the health level for the robot battery."""
    # 电池低于 10% 是严重风险，低于 20% 是普通警告
    if battery < 10:
        return "CRITICAL"
    if battery < 20:
        return "LOW"
    return "GOOD"


def get_temperature_health(temperature):
    """Return the health level for the robot temperature."""
    # 温度超过 90°C 是严重风险，超过 70°C 是普通警告
    if temperature > 90:
        return "CRITICAL"
    if temperature > 70:
        return "HIGH"
    return "GOOD"


def get_cpu_health(cpu_usage):
    """Return the health level for the robot CPU usage."""
    # CPU 使用率超过 95% 是严重风险，超过 90% 是普通警告
    if cpu_usage > 95:
        return "CRITICAL"
    if cpu_usage > 90:
        return "HIGH"
    return "GOOD"


def get_sensor_health(sensor_status):
    """Return the health level for a robot sensor."""
    # 传感器只有 OK 才表示正常，其他状态都视为错误
    if sensor_status == "OK":
        return "GOOD"
    return "ERROR"


def get_overall_health(robot_status):
    """Return the overall robot health level."""
    battery_health = get_battery_health(robot_status["battery"])
    temperature_health = get_temperature_health(robot_status["temperature"])
    cpu_health = get_cpu_health(robot_status["cpu_usage"])
    camera_health = get_sensor_health(robot_status["camera_status"])
    imu_health = get_sensor_health(robot_status["imu_status"])

    # 任意子系统严重异常时，整机状态为 CRITICAL
    if battery_health == "CRITICAL":
        return "CRITICAL"
    if temperature_health == "CRITICAL":
        return "CRITICAL"
    if cpu_health == "CRITICAL":
        return "CRITICAL"
    if camera_health == "ERROR":
        return "CRITICAL"
    if imu_health == "ERROR":
        return "CRITICAL"

    # 普通风险时，整机状态为 WARNING
    if battery_health == "LOW":
        return "WARNING"
    if temperature_health == "HIGH":
        return "WARNING"
    if cpu_health == "HIGH":
        return "WARNING"

    return "HEALTHY"


def show_health_report(robot_status):
    """Display the robot health report."""
    battery_health = get_battery_health(robot_status["battery"])
    temperature_health = get_temperature_health(robot_status["temperature"])
    cpu_health = get_cpu_health(robot_status["cpu_usage"])
    camera_health = get_sensor_health(robot_status["camera_status"])
    imu_health = get_sensor_health(robot_status["imu_status"])
    overall_health = get_overall_health(robot_status)

    print()
    print("========== Health Report ==========")
    print("Battery Health    :", battery_health)
    print("Temperature Health:", temperature_health)
    print("CPU Health        :", cpu_health)
    print("Camera Health     :", camera_health)
    print("IMU Health        :", imu_health)
    print("Overall Health    :", overall_health)
    print("===================================")
    print()

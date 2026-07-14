"""Reusable input validation functions for the Atlas Robot Dashboard."""


def get_number_input(message):
    """Read a number from the user and return it as a float."""
    while True:
        user_input = input(message)

        # 使用 try/except 防止用户输入非数字导致程序崩溃
        try:
            return float(user_input)
        except ValueError:
            print("Please enter a valid number.")


def get_number_in_range(message, minimum_value, maximum_value):
    """Read a number that must stay inside a valid range."""
    while True:
        number = get_number_input(message)

        # 检查数字是否在安全范围内
        if number >= minimum_value and number <= maximum_value:
            return number

        print("Value must be between", minimum_value, "and", maximum_value)


def get_minimum_number(message, minimum_value):
    """Read a number that must be greater than or equal to a minimum."""
    while True:
        number = get_number_input(message)

        # 检查数字是否不小于最小值
        if number >= minimum_value:
            return number

        print("Value must be greater than or equal to", minimum_value)


def get_status_input(message):
    """Read a sensor status that must be OK or ERROR."""
    while True:
        status = input(message)
        status = status.upper()

        # 传感器状态只允许 OK 或 ERROR，避免拼写错误影响判断
        if status == "OK" or status == "ERROR":
            return status

        print("Status must be OK or ERROR.")

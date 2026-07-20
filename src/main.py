"""Atlas Robot Dashboard entry point."""

from auth import handle_login
from data_logger import (
    DEFAULT_LOG_PATH,
    clear_log_file,
    log_robot_status,
    show_recent_log_entries,
)
from event_logger import (
    DEFAULT_EVENT_LOG_PATH,
    clear_runtime_events,
    show_recent_runtime_events,
)
from health_monitor import show_health_report
from input_utils import get_number_in_range
from robot_status import (
    change_robot_mode,
    robot_status,
    show_robot_status,
    update_robot_status,
)
from robot_runtime import (
    reset_robot_after_emergency,
    run_robot_runtime,
)
from sensor_simulator import (
    run_sensor_simulation,
    simulate_sensor_update,
)


def print_title():
    """Print the dashboard title."""
    print("==================================")
    print("Atlas Robot Dashboard")
    print("==================================")


def print_menu():
    """Print the main menu options."""
    print()
    print("1.Login")
    print("2.Show Robot Status")
    print("3.Update Robot Status")
    print("4.Change Robot Mode")
    print("5.Show Health Report")
    print("6.Simulate One Sensor Update")
    print("7.Run Sensor Simulation")
    print("8.Show Recent Sensor Logs")
    print("9.Clear Sensor Logs")
    print("10.Run Robot Runtime")
    print("11.Reset Robot After Emergency")
    print("12.Show Recent Runtime Events")
    print("13.Clear Runtime Events")
    print("14.Exit")


def get_integer_in_range(message, minimum_value, maximum_value):
    """Read an integer that must stay inside a valid range."""
    while True:
        user_input = input(message)

        # 模拟次数必须是整数，避免 range() 收到小数
        try:
            number = int(user_input)
        except ValueError:
            print("Please enter a valid integer.")
            continue

        # 检查整数是否在允许范围内
        if number >= minimum_value and number <= maximum_value:
            return number

        print("Value must be between", minimum_value, "and", maximum_value)


def handle_one_sensor_update():
    """Run one simulated sensor update and display the results."""
    simulate_sensor_update(robot_status)
    log_robot_status(robot_status, 1, DEFAULT_LOG_PATH)
    show_robot_status()
    show_health_report(robot_status)


def handle_sensor_simulation():
    """Ask for simulation settings and run the sensor simulation."""
    number_of_cycles = get_integer_in_range(
        "Number of cycles (1-20): ",
        1,
        20
    )
    delay_seconds = get_number_in_range("Delay seconds (0-5): ", 0, 5)
    run_sensor_simulation(robot_status, number_of_cycles, delay_seconds)


def handle_recent_logs():
    """Ask how many recent log rows to display."""
    number_of_entries = get_integer_in_range(
        "Recent log rows (1-50): ",
        1,
        50
    )
    show_recent_log_entries(DEFAULT_LOG_PATH, number_of_entries)


def handle_clear_logs():
    """Ask for confirmation before clearing sensor logs."""
    confirmation = input("Type YES to clear sensor logs: ")

    # 清空日志是危险操作，必须让用户明确输入 YES
    if confirmation == "YES":
        clear_log_file(DEFAULT_LOG_PATH)
        print("Sensor logs cleared.")
    else:
        print("Clear sensor logs canceled.")


def handle_robot_runtime():
    """Ask for runtime settings and run the robot runtime."""
    number_of_cycles = get_integer_in_range(
        "Runtime cycles (1-50): ",
        1,
        50
    )
    delay_seconds = get_number_in_range("Delay seconds (0-5): ", 0, 5)
    run_robot_runtime(robot_status, number_of_cycles, delay_seconds)


def handle_emergency_reset():
    """Ask for confirmation before resetting after emergency."""
    confirmation = input("Type RESET to reset robot: ")

    # RESET 输入大小写都可以接受，strip 用来去掉前后空格
    if confirmation.strip().upper() == "RESET":
        reset_robot_after_emergency(robot_status)
        print("Robot reset after emergency.")
    else:
        print("Emergency reset canceled.")


def handle_recent_runtime_events():
    """Ask how many recent runtime events to display."""
    number_of_entries = get_integer_in_range(
        "Recent runtime events (1-50): ",
        1,
        50
    )
    show_recent_runtime_events(DEFAULT_EVENT_LOG_PATH, number_of_entries)


def handle_clear_runtime_events():
    """Ask for confirmation before clearing runtime events."""
    confirmation = input("Type YES to clear runtime events: ")

    # 清空运行事件日志前，要求用户明确确认
    if confirmation.strip().upper() == "YES":
        clear_runtime_events(DEFAULT_EVENT_LOG_PATH)
        print("Runtime events cleared.")
    else:
        print("Clear runtime events canceled.")


def run_dashboard():
    """Run the Atlas Robot Dashboard main menu."""
    print_title()

    while True:
        print_menu()
        user_choice = input("Please choose an option: ")

        # 根据用户输入决定下一步操作
        if user_choice == "1":
            handle_login()
        elif user_choice == "2":
            show_robot_status()
        elif user_choice == "3":
            update_robot_status()
        elif user_choice == "4":
            change_robot_mode()
        elif user_choice == "5":
            show_health_report(robot_status)
        elif user_choice == "6":
            handle_one_sensor_update()
        elif user_choice == "7":
            handle_sensor_simulation()
        elif user_choice == "8":
            handle_recent_logs()
        elif user_choice == "9":
            handle_clear_logs()
        elif user_choice == "10":
            handle_robot_runtime()
        elif user_choice == "11":
            handle_emergency_reset()
        elif user_choice == "12":
            handle_recent_runtime_events()
        elif user_choice == "13":
            handle_clear_runtime_events()
        elif user_choice == "14":
            break
        else:
            print("Invalid option. Please try again.")


def main():
    """Start the Atlas Robot Dashboard program."""
    run_dashboard()


if __name__ == "__main__":
    main()

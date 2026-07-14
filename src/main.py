"""Atlas Robot Dashboard entry point."""

from auth import handle_login
from health_monitor import show_health_report
from robot_status import (
    change_robot_mode,
    robot_status,
    show_robot_status,
    update_robot_status,
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
    print("6.Exit")


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
            break
        else:
            print("Invalid option. Please try again.")


def main():
    """Start the Atlas Robot Dashboard program."""
    run_dashboard()


if __name__ == "__main__":
    main()

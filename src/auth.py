"""Authentication functions for the Atlas Robot Dashboard."""


def handle_login():
    """Show the temporary login module message."""
    user_name = input("Please input your user name: ")
    password = input("Please input your password: ")
    if user_name == "Atlas" and password == "123456":
        print("Login Success!")
    else:
        print("Login Failed!")

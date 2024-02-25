from cli import main_menu, add_shopping_trip_interface, add_user_guess_interface, calculate_leaderboard_interface, add_user_interface
from db import connect_db

def run_cli():
    conn = connect_db()
    if conn is None:
        return

    while True:
        choice = main_menu()
        if choice == "1":
            add_shopping_trip_interface(conn)
        elif choice == "2":
            add_user_guess_interface(conn)
        elif choice == "3":
            calculate_leaderboard_interface(conn)
        elif choice == "4":  # Handle the new "Add User" action
            add_user_interface(conn)
        elif choice == "5":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    run_cli()
from tabulate import tabulate
from db import connect_db, add_shopping_trip, add_user_guess, calculate_leaderboard, fetch_all_users, add_user

def main_menu():
    print("\nSelect an action:")
    print("1. Add shopping trip")
    print("2. Add user guess")
    print("3. Check leaderboard")
    print("4. Add user")  # New option for adding a user
    print("5. Exit")
    return input("Enter your choice (1-5): ")

def add_user_interface(conn):
    name = input("Enter the new user's name: ")
    try:
        add_user(conn, name)  # Utilizes the add_user function from db.py
        print(f"User '{name}' added successfully.")
    except Exception as e:
        print(f"Failed to add user '{name}'. Error: {e}")

def add_shopping_trip_interface(conn):
    date = input("Enter the date of the shopping trip (YYYY-MM-DD): ")
    total = input("Enter the total cost: ")
    add_shopping_trip(conn, date, total)
    print("Shopping trip added successfully.")

def add_user_guess_interface(conn):
    users = fetch_all_users(conn)
    if not users:
        print("No users available. Please add users first.")
        return

    print("Select a user:")
    for idx, (user_id, name) in enumerate(users, start=1):
        print(f"{idx}. {name}")
    user_choice = input("Enter the number of the user: ")
    try:
        selected_user_id = users[int(user_choice) - 1][0]  # Adjust index and get user_id
    except (IndexError, ValueError):
        print("Invalid selection.")
        return

    date = input("Enter the date of the shopping trip you are guessing for (YYYY-MM-DD): ")
    guess = input("Enter your guess: ")
    add_user_guess(conn, selected_user_id, date, guess)  # Ensure this function uses user_id for the guess
    print("Guess added successfully.")

def calculate_leaderboard_interface(conn):
    leaderboard = calculate_leaderboard(conn)
    if leaderboard:
        print("Leaderboard:")
        # Using tabulate to create a table. Headers are "User" and "Total Difference"
        print(tabulate(leaderboard, headers=['User', 'Total Difference'], tablefmt='grid'))
    else:
        print("No guesses have been made yet.")
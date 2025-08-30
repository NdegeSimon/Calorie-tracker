from operations import add_user, add_activity, list_activities, list_users, display_emissions_bar_chart, delete_user, EMISSION_FACTORS, add_goal, list_goals, delete_all_activities, verify_user, export_activities_to_json
from models import SessionLocal, User
from tabulate import tabulate
from datetime import datetime
import json
import os

def save_session(username):
    """Save session data to a file."""
    try:
        with open("session.json", "w") as f:
            json.dump({"username": username}, f)
        print("Session saved successfully.")
    except Exception as e:
        print(f"Error saving session: {e}")

def load_session():
    """Load session data."""
    try:
        with open("session.json", "r") as f:
            return json.load(f).get("username")
    except (FileNotFoundError, json.JSONDecodeError):
        return None

def clear_session():
    """Clear session data."""
    if os.path.exists("session.json"):
        try:
            os.remove("session.json")
            print("Session cleared successfully.")
        except Exception as e:
            print(f"Error clearing session: {e}")

def main():
    while True:
        current_user = load_session()
        print("EcoTracker Menu")
        print("1. Log in")
        print("2. Sign Up")
        if current_user:
            print(f"Logged in as: {current_user}")
            print("3. Add Activity")
            print("4. List Activities")
            print("5. List Users")
            print("6. Display Emissions Bar Chart")
            print("7. Add Goal")
            print("8. List Goals")
            print("9. Delete User")
            print("10. Delete All Activities")
            print("11. Export Activities to JSON")
            print("12. Logout")
            print("13. Exit")
        else:
            print("3-11. [Requires login]")
            print("12. Exit")
        choice = input("Choose an option (1-13): ").strip()

        if choice == "1":
            if current_user:
                print(f"Already logged in as {current_user}. Use option 12 to logout.")
                print("===============================")
                continue
            username = input("Input Username: ").strip()
            password = input("Input Password: ").strip()
            print("===============================")
            if not username or not password:
                print("Username and password cannot be empty.")
                print("===============================")
                continue
            if verify_user(username, password):
                save_session(username)
                print(f"User {username} logged in successfully.")
            else:
                print("Invalid username or password.")
            print("===============================")
            
        elif choice == "2":
            username = input("Input Username: ").strip()
            password = input("Input Password: ").strip()
            print("===============================")
            if not username or not password:
                print("Username and password cannot be empty.")
                print("===============================")
                continue
            add_user(username, password)
            print("===============================")
        
        elif choice in ["3", "4", "5", "6", "7", "8", "9", "10", "11"]:
            if not current_user:
                print("Please log in to continue.")
                print("===============================")
                continue

            if choice == "3":
                session = SessionLocal()
                try:
                    users = session.query(User).all()
                    if not users:
                        print("No users found! Please add a user first.\n")
                        continue
                    print("Available users:")
                    for user in users:
                        print(f"ID: {user.id}, Username: {user.username}")
                    user_id = input("Input User ID: ").strip()
                    if not user_id.isdigit():
                        print("User ID must be a number!\n")
                        continue
                    user_id = int(user_id)
                    
                    print("Available activity types:", ", ".join(EMISSION_FACTORS.keys()))
                    activity_type = input("Input Activity Type: ").strip()
                    if not activity_type:
                        print("Activity type cannot be empty!\n")
                        continue
                    
                    quantity = input("Input Quantity (e.g., km for transport, kWh for electricity): ").strip()
                    try:
                        quantity = float(quantity)
                        if quantity <= 0:
                            print("Quantity must be positive!\n")
                            continue
                    except ValueError:
                        print("Quantity must be a number!\n")
                        continue
                    
                    if activity_type in EMISSION_FACTORS:
                        calculated_emission = EMISSION_FACTORS[activity_type] * quantity
                        print(f"Auto-calculated emission: {calculated_emission:.2f} kg CO2")
                        override = input("Use this value? (y/n): ").strip().lower()
                        if override == 'n':
                            emission = input("Input Manual Emission: ").strip()
                            try:
                                emission = float(emission)
                                if emission < 0:
                                    print("Emission cannot be negative!\n")
                                    continue
                            except ValueError:
                                print("Emission must be a number!\n")
                                continue
                        else:
                            emission = calculated_emission
                    else:
                        print("No auto-calculation for this activity type.")
                        emission = input("Input Emission: ").strip()
                        try:
                            emission = float(emission)
                            if emission < 0:
                                print("Emission cannot be negative!\n")
                                continue
                        except ValueError:
                            print("Emission must be a number!\n")
                            continue
                    
                    add_activity(user_id, activity_type, quantity, emission)
                finally:
                    session.close()
                    print("===============================")
        
            elif choice == "4":
                list_activities()
                print("===============================")
        
            elif choice == "5":
                list_users()
                print("===============================")
        
            elif choice == "6":
                display_emissions_bar_chart()
                print("===============================")
        
            elif choice == "7":
                session = SessionLocal()
                try:
                    users = session.query(User).all()
                    if not users:
                        print("No users found! Please add a user first.\n")
                        continue
                    print("Available users:")
                    for user in users:
                        print(f"ID: {user.id}, Username: {user.username}")
                    user_id = input("Input User ID for the goal: ").strip()
                    if not user_id.isdigit():
                        print("User ID must be a number!\n")
                        continue
                    user_id = int(user_id)
                    
                    description = input("Goal Description: ").strip()
                    target_emission = input("Target Emission (kg CO2): ").strip()
                    try:
                        target_emission = float(target_emission)
                    except ValueError:
                        print("Target emission must be a number!\n")
                        continue
                    deadline = input("Deadline (YYYY-MM-DD): ").strip()
                    try:
                        deadline_dt = datetime.strptime(deadline, "%Y-%m-%d")
                    except ValueError:
                        print("Invalid date format!\n")
                        continue
                    add_goal(user_id, description, target_emission, deadline_dt)
                finally:
                    session.close()
                    print("===============================")
        
            elif choice == "8":
                list_goals()
                print("===============================")
        
            elif choice == "9":
                session = SessionLocal()
                try:
                    users = session.query(User).all()
                    if not users:
                        print("No users found!\n")
                        continue
                    print("Available users:")
                    for user in users:
                        print(f"ID: {user.id}, Username: {user.username}")
                    print("===============================")
                    user_id = input("Input User ID to delete: ").strip()
                    if not user_id.isdigit():
                        print("User ID must be a number!\n")
                        continue
                    user_id = int(user_id)
                    if session.query(User).filter_by(id=user_id, username=current_user).first():
                        print("Cannot delete the currently logged-in user!")
                        continue
                    delete_user(user_id)
                finally:
                    session.close()
                    print("===============================")
        
            elif choice == "10":
                confirm = input("Are you sure you want to delete all activities? (y/n): ").strip().lower()
                if confirm == 'y':
                    delete_all_activities()
                else:
                    print("Operation cancelled.\n")
                print("===============================")
        
            elif choice == "11":
                filename = input("Enter filename for JSON export (default: emissions.json): ").strip() or "emissions.json"
                export_activities_to_json(current_user, filename)
                print("===============================")

        elif choice == "12":
            if current_user:
                clear_session()
                print("Logged out successfully.")
                print("===============================")
            else:
                print("Exiting EcoTracker...")
                print("Thank you for Visiting EcoTracker. See you next time!")
                print("===============================")
                break
        
        elif choice == "13" and current_user:
            print("Exiting EcoTracker...")
            print("Thank you for Visiting EcoTracker. See you next time!")
            print("===============================")
            break
        
        else:
            print("Invalid choice! Please try again.\n")
            print("===============================")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting... (Interrupted by user)")
        print("===============================")
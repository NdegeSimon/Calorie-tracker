from operations import add_user, add_activity, list_activities, list_users, display_emissions_bar_chart, delete_user, EMISSION_FACTORS, add_goal, list_goals, delete_all_activities
from models import SessionLocal, User

def main():
    while True:
        print("EcoTracker Menu")
        print("1. Add User")
        print("2. Add Activity")
        print("3. List Activities")
        print("4. List Users")
        print("5. Display Emissions Bar Chart")
        print("6. Add Goal")
        print("7. List Goals")
        print("8. Delete User")
        print("9. Delete All Activities")
        print("10. Exit")
        choice = input("Choose an option (1-10): ").strip()

        if choice == "1":
            username = input("Input Username: ").strip()
            add_user(username)
        
        elif choice == "2":
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
                
                # Try automatic emission calculation
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
        
        elif choice == "3":
            list_activities()
        
        elif choice == "4":
            list_users()
        
        elif choice == "5":
            display_emissions_bar_chart()
        # ...existing code above...

        elif choice == "6":
            # Add Goal
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
                    from datetime import datetime
                    deadline_dt = datetime.strptime(deadline, "%Y-%m-%d")
                except ValueError:
                    print("Invalid date format!\n")
                    continue
                add_goal(user_id, description, target_emission, deadline_dt)
            finally:
                session.close()
        
        elif choice == "7":
            # List Goals
            list_goals()
        
        elif choice == "8":
            # Delete User
            session = SessionLocal()
            try:
                users = session.query(User).all()
                if not users:
                    print("No users found!\n")
                    continue
                print("Available users:")
                for user in users:
                    print(f"ID: {user.id}, Username: {user.username}")
                
                user_id = input("Input User ID to delete: ").strip()
                if not user_id.isdigit():
                    print("User ID must be a number!\n")
                    continue
                user_id = int(user_id)
                delete_user(user_id)
            finally:
                session.close()
        
        elif choice == "9":
            # Delete All Activities
            confirm = input("Are you sure you want to delete all activities? (y/n): ").strip().lower()
            if confirm == 'y':
                delete_all_activities()
            else:
                print("Operation cancelled.\n")
        
        elif choice == "10":
            print("Exiting EcoTracker...")
            break
        
        else:
            print("Invalid choice! Please try again.\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting... (Interrupted by user)")
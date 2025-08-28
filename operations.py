from sqlalchemy.orm import Session
from models import User, Activity, SessionLocal
from tabulate import tabulate
from sqlalchemy.sql import func

# Emission factors dictionary (kg CO2 per unit of quantity)
# Sources: Our World in Data for transport; global averages for electricity.
EMISSION_FACTORS = {
    "Driving": 0.170,  # kg CO2 per km (petrol car average)
    "Flying Domestic": 0.246,  # kg CO2 per km
    "Flying International": 0.154,  # kg CO2 per km (short-haul)
    "Bus": 0.089,  # kg CO2 per km
    "Train": 0.035,  # kg CO2 per km (national rail)
    "Electricity": 0.475,  # kg CO2 per kWh (global average)
    # Add more as needed, e.g., "Beef Consumption": 60.0  # kg CO2 per kg
}

def calculate_emission(activity_type: str, quantity: float) -> float:
    factor = EMISSION_FACTORS.get(activity_type)
    if factor:
        return quantity * factor
    return 0.0  # Return 0 if no factor, to indicate manual input needed

def add_user(username: str):
    print("Add new User")
    if not username:
        print("Username cannot be empty!")
        return
    try:
        session = SessionLocal()
        new_user = User(username=username)
        session.add(new_user)
        session.commit()
        print(f"User '{username}' added!\n")
    except Exception as e:
        session.rollback()
        print(f"Error adding user: {e}\n")
    finally:
        session.close()

def add_activity(user_id: int, activity_type: str, quantity: float, emission: float = None):
    print("Add new Activity")
    session = SessionLocal()
    try:
        user = session.query(User).filter_by(id=user_id).first()
        if not user:
            print(f"No user found with ID {user_id}!\n")
            return
        
        # Use provided emission or calculated one
        if emission is None:
            emission = calculate_emission(activity_type, quantity)
            if emission == 0.0:
                print("No auto-calculation available for this activity type.")
                return  # Will prompt for manual in main.py
        
        new_activity = Activity(
            user_id=user_id,
            activity_type=activity_type,
            quantity=quantity,
            emission=emission
        )
        session.add(new_activity)
        session.commit()
        print("Activity added!\n")
    except Exception as e:
        session.rollback()
        print(f"Error adding activity: {e}\n")
    finally:
        session.close()

def list_activities():
    print("Activities")
    session = SessionLocal()
    try:
        activities = session.query(Activity).all()
        if not activities:
            print("No activities found!\n")
            return
        table = []
        for a in activities:
            user = session.query(User).filter_by(id=a.user_id).first()
            username = user.username if user else "Unknown"
            table.append([a.id, a.activity_type, username, a.emission, a.activity_date])
        print(tabulate(table, headers=["ID", "Activity Type", "User", "Emission", "Date"], tablefmt="grid"))
        print()
    except Exception as e:
        print(f"Error listing activities: {e}\n")
    finally:
        session.close()

def list_users():
    print("Users")
    session = SessionLocal()
    try:
        users = session.query(User).all()
        if not users:
            print("No users found!\n")
            return
        table = []
        for u in users:
            table.append([u.id, u.username, u.created_at])
        print(tabulate(table, headers=["ID", "Username", "Created At"], tablefmt="grid"))
        print()
    except Exception as e:
        print(f"Error listing users: {e}\n")
    finally:
        session.close()

def display_emissions_bar_chart():
    print("Total Emissions by User (Bar Chart)")
    session = SessionLocal()
    try:
        results = (
            session.query(User.username, func.sum(Activity.emission).label("total_emission"))
            .join(Activity)
            .group_by(User.id)
            .all()
        )
        if not results:
            print("No activities found to display!\n")
            return

        max_emission = max(r[1] for r in results)
        max_bar_length = 50
        bar_char = "█"

        table = []
        for username, total_emission in results:
            bar_length = int((total_emission / max_emission) * max_bar_length) if max_emission > 0 else 0
            bar = bar_char * bar_length
            table.append([username, f"{total_emission:.2f}", bar])

        print(tabulate(table, headers=["Username", "Total Emission (kg CO2)", "Bar"], tablefmt="grid"))
        print()
    except Exception as e:
        print(f"Error generating bar chart: {e}\n")
    finally:
        session.close()

def delete_user(user_id: int):
    print("Delete User")
    session = SessionLocal()
    try:
        user = session.query(User).filter_by(id=user_id).first()
        if not user:
            print(f"No user found with ID {user_id}!\n")
            return
        session.delete(user)
        session.commit()
        print(f"User ID {user_id} and associated activities deleted!\n")
    except Exception as e:
        session.rollback()
        print(f"Error deleting user: {e}\n")
    finally:
        session.close()
        
def get_all_users():
    session = SessionLocal()
    try:
        users = session.query(User).all()
        return users
    except Exception as e:
        print(f"Error retrieving users: {e}\n")
        return []
    finally:
        session.close()
def delete_all_activities():
    print("Delete All Activities")
    session = SessionLocal()
    try:
        deleted = session.query(Activity).delete()
        session.commit()
        print(f"Deleted {deleted} activities!\n")
    except Exception as e:
        session.rollback()
        print(f"Error deleting activities: {e}\n")
    finally:
        session.close()
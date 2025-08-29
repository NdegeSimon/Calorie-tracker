from sqlalchemy.orm import Session
from models import User, Activity, SessionLocal
from tabulate import tabulate
from sqlalchemy.sql import func
from models import Goal
from datetime import datetime
from passlib.hash import bcrypt
import json
import traceback

# Emission factors dictionary (kg CO2 per unit of quantity)
EMISSION_FACTORS = {
    "Driving": 0.170,  # kg CO2 per km (petrol car average)
    "Flying Domestic": 0.246,  # kg CO2 per km
    "Flying International": 0.154,  # kg CO2 per km (short-haul)
    "Bus": 0.089,  # kg CO2 per km
    "Train": 0.035,  # kg CO2 per km (national rail)
    "Electricity": 0.475,  # kg CO2 per kWh (global average)
}

def verify_user(username: str, password: str) -> bool:
    """Verify user credentials against the database."""
    session = SessionLocal()
    try:
        user = session.query(User).filter_by(username=username).first()
        if not user:
            print(f"No user found with username: {username}")
            return False
        if not hasattr(user, 'password_hash'):
            print("Error: User model missing password_hash field")
            return False
        if bcrypt.verify(password, user.password_hash):
            print(f"Login successful for {username}")
            return True
        else:
            print("Incorrect password")
            return False
    except Exception as e:
        print(f"Error verifying user: {e}")
        traceback.print_exc()
        return False
    finally:
        session.close()

def calculate_emission(activity_type: str, quantity: float) -> float:
    factor = EMISSION_FACTORS.get(activity_type)
    if factor:
        return quantity * factor
    return 0.0

def add_user(username: str, password: str) -> bool:
    """Add a new user with hashed password."""
    session = SessionLocal()
    try:
        if session.query(User).filter_by(username=username).first():
            print(f"Error: Username {username} already exists.")
            return False
        password_hash = bcrypt.hash(password)
        new_user = User(username=username, password_hash=password_hash)
        session.add(new_user)
        session.commit()
        print(tabulate([[f"User '{username}' added!"]], tablefmt="grid"))
        return True
    except Exception as e:
        session.rollback()
        print(f"Error adding user: {e}")
        traceback.print_exc()
        return False
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
        
        if emission is None:
            emission = calculate_emission(activity_type, quantity)
            if emission == 0.0:
                print("No auto-calculation available for this activity type.")
                return
        
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

def add_goal(user_id: int, description: str, target_emission: float, deadline: datetime):
    session = SessionLocal()
    try:
        new_goal = Goal(
            user_id=user_id,
            description=description,
            target_emission=target_emission,
            deadline=deadline
        )
        session.add(new_goal)
        session.commit()
        print("Goal added!\n")
    except Exception as e:
        session.rollback()
        print(f"Error adding goal: {e}\n")
    finally:
        session.close()

def list_goals():
    session = SessionLocal()
    try:
        goals = session.query(Goal).all()
        if not goals:
            print("No goals found!\n")
            return
        table = [(g.id, g.user_id, g.description, g.target_emission, g.deadline.strftime('%Y-%m-%d')) for g in goals]
        print(tabulate(table, headers=["ID", "User ID", "Description", "Target Emission", "Deadline"], tablefmt="grid"))
        print()
    except Exception as e:
        print(f"Error listing goals: {e}\n")
    finally:
        session.close()

def delete_all_activities():
    print("Delete All Activities")
    session = SessionLocal()
    try:
        deleted = session.query(Activity).delete()
        session.commit()
        print(tabulate([[f"Deleted {deleted} activities!"]], tablefmt="grid"))
    except Exception as e:
        session.rollback()
        print(f"Error deleting activities: {e}\n")
    finally:
        session.close()

def export_activities_to_json(username: str, filename: str = "emissions.json"):
    """Export a user's activities to a JSON file."""
    session = SessionLocal()
    try:
        user = session.query(User).filter_by(username=username).first()
        if not user:
            print(f"No user found with username {username}!\n")
            return
        activities = session.query(Activity).filter_by(user_id=user.id).all()
        if not activities:
            print(f"No activities found for user {username}!\n")
            return
        
        data = {
            "username": username,
            "activities": [
                {
                    "id": a.id,
                    "activity_type": a.activity_type,
                    "quantity": a.quantity,
                    "emission": a.emission,
                    "date": a.activity_date.strftime("%Y-%m-%d %H:%M:%S")
                } for a in activities
            ]
        }
        
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)
        print(f"Activities exported to {filename} successfully!\n")
    except Exception as e:
        print(f"Error exporting activities to JSON: {e}\n")
    finally:
        session.close()
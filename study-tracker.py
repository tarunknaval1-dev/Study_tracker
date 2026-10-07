import json
from datetime import date
from pathlib import Path

DATA_FILE = Path("study_sessions.json")


def load_sessions():
    if DATA_FILE.exists():
        with open(DATA_FILE, "r") as file:
            return json.load(file)

    return []


def save_sessions(sessions):
    with open(DATA_FILE, "w") as file:
        json.dump(sessions, file, indent=4)


def add_study_session(sessions):
    subject = input("Enter subject name: ").strip()
    topic = input("Enter topic studied: ").strip()

    if not subject or not topic:
        print("Subject and topic cannot be empty.")
        return

    try:
        minutes = int(input("Enter study time in minutes: "))

        if minutes <= 0:
            print("Study time must be greater than zero.")
            return

    except ValueError:
        print("Please enter a valid number.")
        return

    session = {
        "subject": subject,
        "topic": topic,
        "minutes": minutes,
        "date": str(date.today())
    }

    sessions.append(session)
    save_sessions(sessions)

    print("Study session added successfully!")


def main():
    sessions = load_sessions()

    while True:
        print("\n--- Personal Study Tracker ---")
        print("1. Add Study Session")
        print("2. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_study_session(sessions)

        elif choice == "2":
            print("Keep learning!")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
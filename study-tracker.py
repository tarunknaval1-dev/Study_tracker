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

    sessions.append({
        "subject": subject,
        "topic": topic,
        "minutes": minutes,
        "date": str(date.today())
    })

    save_sessions(sessions)
    print("Study session added successfully!")


def view_sessions(sessions):
    if not sessions:
        print("\nNo study sessions recorded yet.\n")
        return

    print("\n--- Study Session History ---")
    total_minutes = 0

    for number, session in enumerate(sessions, start=1):
        print(
            f"{number}. {session['date']} | "
            f"{session['subject']} | "
            f"{session['topic']} | "
            f"{session['minutes']} minutes"
        )
        total_minutes += session["minutes"]

    hours, minutes = divmod(total_minutes, 60)
    print(f"\nTotal study time: {hours} hour(s), {minutes} minute(s)\n")


def subject_summary(sessions):
    if not sessions:
        print("\nNo study sessions recorded yet.\n")
        return

    subject_totals = {}

    for session in sessions:
        subject = session["subject"]
        subject_totals[subject] = (
            subject_totals.get(subject, 0) + session["minutes"]
        )

    print("\n--- Study Time by Subject ---")

    for subject, total_minutes in sorted(subject_totals.items()):
        hours, minutes = divmod(total_minutes, 60)
        print(f"{subject}: {hours} hour(s), {minutes} minute(s)")

    print()


def main():
    sessions = load_sessions()

    while True:
        print("\n--- Personal Study Tracker ---")
        print("1. Add Study Session")
        print("2. View Study Sessions")
        print("3. Subject-wise Summary")
        print("4. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_study_session(sessions)
        elif choice == "2":
            view_sessions(sessions)
        elif choice == "3":
            subject_summary(sessions)
        elif choice == "4":
            print("Keep learning!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
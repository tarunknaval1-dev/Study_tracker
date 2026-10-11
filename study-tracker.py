import csv
import json
from datetime import date, timedelta
from pathlib import Path

DATA_FILE = Path("study_sessions.json")
GOAL_FILE = Path("study_goal.json")
CSV_FILE = Path("study_sessions_export.csv")


def load_sessions():
    if not DATA_FILE.exists():
        return []

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        print("Could not read study_sessions.json. Starting with no sessions.")
        return []


def save_sessions(sessions):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(sessions, file, indent=4)


def load_goal():
    if not GOAL_FILE.exists():
        return 0

    try:
        with open(GOAL_FILE, "r", encoding="utf-8") as file:
            return json.load(file).get("daily_goal_minutes", 0)
    except (json.JSONDecodeError, OSError):
        return 0


def save_goal(minutes):
    with open(GOAL_FILE, "w", encoding="utf-8") as file:
        json.dump({"daily_goal_minutes": minutes}, file, indent=4)


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
        print("Please enter a valid whole number.")
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


def set_daily_goal():
    try:
        minutes = int(input("Set your daily study goal in minutes: "))
        if minutes <= 0:
            print("The goal must be greater than zero.")
            return
    except ValueError:
        print("Please enter a valid whole number.")
        return

    save_goal(minutes)
    print(f"Daily study goal set to {minutes} minutes.")


def show_daily_progress(sessions):
    goal = load_goal()

    if goal <= 0:
        print("\nSet a daily goal first using the menu.\n")
        return

    today = str(date.today())
    studied_today = sum(
        session["minutes"]
        for session in sessions
        if session["date"] == today
    )

    print("\n--- Today's Study Progress ---")
    print(f"Goal: {goal} minutes")
    print(f"Studied: {studied_today} minutes")

    if studied_today >= goal:
        print(f"Goal reached! You are {studied_today - goal} minute(s) over your goal.")
    else:
        print(f"{goal - studied_today} minute(s) left to reach your goal.")
    print()


def show_weekly_report(sessions):
    today = date.today()
    week_start = today - timedelta(days=today.weekday())
    week_end = week_start + timedelta(days=6)

    weekly_sessions = []

    for session in sessions:
        try:
            session_date = date.fromisoformat(session["date"])
        except (ValueError, KeyError):
            continue

        if week_start <= session_date <= week_end:
            weekly_sessions.append(session)

    print(f"\n--- Weekly Study Report ({week_start} to {week_end}) ---")

    if not weekly_sessions:
        print("No study sessions recorded this week.\n")
        return

    total_minutes = sum(session["minutes"] for session in weekly_sessions)
    hours, minutes = divmod(total_minutes, 60)

    print(f"Sessions: {len(weekly_sessions)}")
    print(f"Total study time: {hours} hour(s), {minutes} minute(s)")

    subject_totals = {}
    for session in weekly_sessions:
        subject = session["subject"]
        subject_totals[subject] = (
            subject_totals.get(subject, 0) + session["minutes"]
        )

    print("\nTime by subject:")
    for subject, total in sorted(subject_totals.items()):
        print(f"- {subject}: {total} minutes")
    print()


def export_to_csv(sessions):
    if not sessions:
        print("\nNo study sessions available to export.\n")
        return

    fieldnames = ["subject", "topic", "minutes", "date"]

    with open(CSV_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(sessions)

    print(f"\nStudy sessions exported to {CSV_FILE}\n")


def main():
    sessions = load_sessions()

    while True:
        print("\n--- Personal Study Tracker ---")
        print("1. Add Study Session")
        print("2. View Study Sessions")
        print("3. Subject-wise Summary")
        print("4. Set Daily Study Goal")
        print("5. View Today's Progress")
        print("6. View Weekly Report")
        print("7. Export Sessions to CSV")
        print("8. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_study_session(sessions)
        elif choice == "2":
            view_sessions(sessions)
        elif choice == "3":
            subject_summary(sessions)
        elif choice == "4":
            set_daily_goal()
        elif choice == "5":
            show_daily_progress(sessions)
        elif choice == "6":
            show_weekly_report(sessions)
        elif choice == "7":
            export_to_csv(sessions)
        elif choice == "8":
            print("Keep learning!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
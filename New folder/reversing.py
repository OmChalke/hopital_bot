def calculate_grade(average):
    if average >= 90:
        return "A"
    elif average >= 75:
        return "B"
    elif average >= 50:
        return "C"
    else:
        return "D"

students_data = {}

def add_student():
    name = input("Enter student name: ").strip()
    subjects = {}
    for subject in ['Math', 'Science', 'English']:
        while True:
            try:
                mark = float(input(f"Enter marks in {subject}: "))
                if mark < 0 or mark > 100:
                    raise ValueError("Marks must be between 0 and 100.")
                subjects[subject] = mark
                break
            except ValueError as e:
                print(f"Invalid input: {e}")

    average = sum(subjects.values()) / 3
    grade = calculate_grade(average)

    students_data[name] = {
        **subjects,
        "Average": round(average, 2),
        "Grade": grade
    }
    print(f"Student '{name}' added successfully.\n")

def view_reports():
    if not students_data:
        print("No student records found.\n")
        return

    print("\nStudent Records:")
    for student, data in students_data.items():
        print(f"\nName: {student}")
        for key, value in data.items():
            print(f"{key}: {value}")
    print()

def save_to_file(filename="student_report.txt"):
    with open(filename, "w") as f:
        for student, data in students_data.items():
            f.write(f"Name: {student}\n")
            for key, value in data.items():
                f.write(f"{key}: {value}\n")
            f.write("-" * 30 + "\n")
    print(f"All records saved to '{filename}' successfully.\n")

def menu():
    while True:
        print("--- Student Performance Tracker ---")
        print("1. Add a new student")
        print("2. View all student reports")
        print("3. Save and Exit")

        choice = input("Enter your choice (1/2/3): ")

        if choice == '1':
            add_student()
        elif choice == '2':
            view_reports()
        elif choice == '3':
            save_to_file()
            print("Goodbye!")
            break
        else:
            print("Invalid choice! Please try again.\n")

menu()


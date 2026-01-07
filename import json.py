import json
import os

FILE_NAME = "students.json"


# ------------- Helper functions for file handling -------------

def load_students():
    """Load students list from JSON file; return empty list if file missing."""
    if not os.path.exists(FILE_NAME):
        return []
    try:
        with open(FILE_NAME, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        # If file is corrupt or empty
        return []


def save_students(students):
    """Save students list to JSON file."""
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        json.dump(students, f, indent=4)


# ------------- CRUD operations -------------

def add_student():
    students = load_students()

    print("--- Add New Student ---")
    name = input("Enter name: ").strip()
    roll_no = input("Enter roll no: ").strip()

    # Check duplicate roll number
    for s in students:
        if s["roll_no"] == roll_no:
            print("A student with this roll no already exists. Try again.")
            return

    try:
        marks = float(input("Enter marks: ").strip())
    except ValueError:
        print("Invalid marks. Use numbers only.")
        return

    course = input("Enter course (optional): ").strip()

    student = {
        "name": name,
        "roll_no": roll_no,
        "marks": marks,
        "course": course
    }

    students.append(student)
    save_students(students)
    print("Student added successfully!")


def find_student_index(students, roll_no):
    for i, s in enumerate(students):
        if s["roll_no"] == roll_no:
            return i
    return -1


def update_student():
    students = load_students()
    if not students:
        print("No students to update.")
        return

    print("--- Update Student ---")
    roll_no = input("Enter roll no to update: ").strip()
    idx = find_student_index(students, roll_no)

    if idx == -1:
        print("Student not found.")
        return

    student = students[idx]
    print(f"Current name: {student['name']}")
    new_name = input("Enter new name (leave blank to keep same): ").strip()
    if new_name:
        student["name"] = new_name

    print(f"Current marks: {student['marks']}")
    new_marks = input("Enter new marks (leave blank to keep same): ").strip()
    if new_marks:
        try:
            student["marks"] = float(new_marks)
        except ValueError:
            print("Invalid marks input. Keeping old marks.")

    print(f"Current course: {student.get('course', '')}")
    new_course = input("Enter new course (leave blank to keep same): ").strip()
    if new_course:
        student["course"] = new_course

    students[idx] = student
    save_students(students)
    print("Student updated successfully!")


def delete_student():
    students = load_students()
    if not students:
        print("No students to delete.")
        return

    print("--- Delete Student ---")
    roll_no = input("Enter roll no to delete: ").strip()
    idx = find_student_index(students, roll_no)

    if idx == -1:
        print("Student not found.")
        return

    confirm = input("Are you sure you want to delete this student? (y/n): ").strip().lower()
    if confirm == "y":
        students.pop(idx)
        save_students(students)
        print("Student deleted successfully!")
    else:
        print("Delete cancelled.")


def search_student():
    students = load_students()
    if not students:
        print("No students to search.")
        return

    print("--- Search Student ---")
    roll_no = input("Enter roll no to search: ").strip()
    idx = find_student_index(students, roll_no)

    if idx == -1:
        print("Student not found.")
        return

    s = students[idx]
    print("Student found:")
    print(f"Name   : {s['name']}")
    print(f"Roll No: {s['roll_no']}")
    print(f"Marks  : {s['marks']}")
    print(f"Course : {s.get('course', '')}")


# ------------- Display in table -------------

def display_students():
    students = load_students()
    if not students:
        print("No student records found.")
        return

    print("--- All Students ---")

    # Simple text table (no external libraries)
    headers = ["Roll No", "Name", "Marks", "Course"]

    # Compute column widths
    col_widths = {
        "roll_no": max(len("Roll No"), *(len(s["roll_no"]) for s in students)),
        "name": max(len("Name"), *(len(s["name"]) for s in students)),
        "marks": max(len("Marks"), *(len(str(s["marks"])) for s in students)),
        "course": max(len("Course"), *(len(s.get("course", "")) for s in students)),
    }

    # Separator line
    sep = "+-" + "-+-".join([
        "-" * col_widths["roll_no"],
        "-" * col_widths["name"],
        "-" * col_widths["marks"],
        "-" * col_widths["course"],
    ]) + "-+"

    # Header
    print(sep)
    print(
        "| "
        + headers[0].ljust(col_widths["roll_no"])
        + " | "
        + headers[1].ljust(col_widths["name"])
        + " | "
        + headers[2].ljust(col_widths["marks"])
        + " | "
        + headers[3].ljust(col_widths["course"])
        + " |"
    )
    print(sep)

    # Rows
    for s in students:
        print(
            "| "
            + s["roll_no"].ljust(col_widths["roll_no"])
            + " | "
            + s["name"].ljust(col_widths["name"])
            + " | "
            + str(s["marks"]).ljust(col_widths["marks"])
            + " | "
            + s.get("course", "").ljust(col_widths["course"])
            + " |"
        )
    print(sep)


# ------------- Main menu loop -------------

def main():
    while True:
        print("====== Student Management System ======")
        print("1. Add Student")
        print("2. Update Student")
        print("3. Delete Student")
        print("4. Search Student")
        print("5. Display All Students")
        print("6. Exit")

        choice = input("Enter your choice (1-6): ").strip()

        if choice == "1":
            add_student()
        elif choice == "2":
            update_student()
        elif choice == "3":
            delete_student()
        elif choice == "4":
            search_student()
        elif choice == "5":
            display_students()
        elif choice == "6":
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")


if __name__ == "__main__":
    main()
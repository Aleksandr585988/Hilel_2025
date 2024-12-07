
import csv


class StorageHandler:
    def __init__(self, filename):
        self.filename = filename
        self.students = self.load_data()

    def load_data(self):
        """Load data from CSV into memory."""
        students = {}
        try:
            with open(self.filename, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    student_id = int(row['ID'])
                    students[student_id] = {
                        "name": row['Name'],
                        "marks": list(map(int, row['Marks'].split(','))),
                        "info": row['Info']
                    }
        except FileNotFoundError:
            print(f"File {self.filename} not found.")
        except Exception as e:
            print(f"Error loading data: {e}")

        return students

    def save_data(self):
        """Write data to CSV."""
        with open(self.filename, mode='w', newline='', encoding='utf-8') as file:
            fieldnames = ['ID', 'Name', 'Marks', 'Info']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for student_id, student in self.students.items():
                marks = student['marks'] if student['marks'] is not None else []
                info = student.get('info', '')
                row = {
                    'ID': student_id,
                    'Name': student['name'],
                    'Marks': ','.join(map(str, marks)),
                    'Info': info
                }
                writer.writerow(row)

    def add_student(self, student: dict) -> dict:
        """Add student to memory and CSV file."""
        if student.get('marks') is None:
            student['marks'] = []

        if 'info' not in student:
            student['info'] = ""

        student_id = max(self.students.keys(), default=0) + 1

        self.students[student_id] = student
        print(f"Added student '{student['name']}' with ID {student_id}.")

        try:
            self.save_data()
            print("Data saved to CSV successfully.")
        except Exception as e:
            print(f"Error saving data: {e}")

        return student

    def update_student(self, student_id: int, payload: dict) -> dict | None:
        """ Update student data in memory and in CSV. """
        student = self.students.get(student_id)
        if student:
            if payload.get("name"):
                student["name"] = payload["name"]
            if payload.get("marks") is not None:
                student["marks"] = payload["marks"]
            if payload.get("info"):
                student["info"] = payload["info"]
            self.save_data()
            return student
        return None

    def delete_student(self, student_id: int) -> None:
        """ Delete student from memory and from CSV file. """
        if student_id in self.students:
            del self.students[student_id]
            self.save_data()


storage_handler = StorageHandler('students.csv')


def show_students() -> None:
    print("=" * 20)
    print("List of students:\n")

    if storage_handler.students:
        for student_id, student in storage_handler.students.items():
            marks = ", ".join(map(str, student['marks']))
            name = student['name']
            info = student['info'] if student['info'] else "No additional info"

            print(f"ID: {student_id} | Name: {name} | Marks: {marks} | Info: {info}")
    else:
        print("No students found.")

    print("=" * 20)


def add_mark():
    student_id = input("Enter student ID to add a mark: ")

    try:
        id_ = int(student_id)
    except ValueError:
        print(f"ID '{student_id}' is not a valid value.")
        return

    student = storage_handler.students.get(id_)

    if student is None:
        print(f"Student with ID '{id_}' not found.")
        return

    if student['marks'] is None:
        student['marks'] = []

    while True:
        mark_input = input("Enter marks to add (from 1 to 5), separated by commas: ")

        try:
            marks = [int(item) for item in mark_input.split(',')]
            if all(1 <= mark <= 5 for mark in marks):
                break
            else:
                print("All marks must be between 1 and 5.")
        except ValueError:
            print(f"'{mark_input}' is not a valid mark. Marks must be numbers from 1 to 5, separated by commas.")

    student['marks'].extend(marks)
    storage_handler.save_data()
    print(f"Marks {marks} added for student '{student['name']}'.")


def student_details(student: dict) -> None:
    print(f"Detailed information: {student['name']} - Marks: {student['marks']}, Info: {student['info']}")


def ask_student_payload():
    prompt = ("Enter student data: you can enter 'First Last' for the name,"
              " 4,5,4,5,4,5 for the marks or both values: ")
    input_data = input(prompt)

    items = input_data.split(";")

    if len(items) == 1:
        if "," in items[0]:
            try:
                marks = [int(item) for item in items[0].split(",")]
                return {"name": None, "marks": marks, "info": ""}
            except ValueError:
                print("Marks are incorrect. Template: 4,5,4,5,4,5. Marks must be numbers.")
                return None
        else:
            name = items[0].strip()
            if not name:
                print("Name cannot be empty. Student not added.")
                return None
            return {"name": name, "marks": None, "info": ""}

    if len(items) == 2:
        name = items[0].strip()
        if not name:
            print("Name cannot be empty. Student not added.")
            return None
        try:
            marks = [int(item) for item in items[1].split(",")]
            return {"name": name, "marks": marks, "info": ""}
        except ValueError:
            print("Marks are incorrect. Template: 4,5,4,5,4,5. Marks must be numbers.")
            return None

    print("Mandatory fields (name, marks) are missing. Student not added.")
    return None


def handle_management_command(command: str):

    if command == "show list":
        show_students()

    elif command == "get by id":
        search_id = input("Enter student ID to retrieve data: ")
        try:
            id_ = int(search_id)
        except ValueError:
            print(f"ID '{search_id}' is not a valid value.")
        else:
            student = storage_handler.students.get(id_)
            if student:
                student_details(student)
            else:
                print(f"Student with ID '{id_}' not found.")

    elif command == "delete":
        delete_id = input("Enter student ID to delete: ")
        try:
            id_ = int(delete_id)
        except ValueError:
            print(f"ID '{delete_id}' is not a valid value.")
        else:
            storage_handler.delete_student(id_)

    elif command == "add":
        data = ask_student_payload()
        if data:
            student = storage_handler.add_student(data)
            if student:
                print(f"New student '{student}' added.")
        else:
            print("No data provided for adding student.")

    elif command == "rename":
        update_id = input("Enter student ID to update data: ")
        try:
            id_ = int(update_id)
        except ValueError:
            print(f"ID '{update_id}' is not a valid value.")
        else:
            data = ask_student_payload()
            if data:
                updated_student = storage_handler.update_student(id_, data)
                if updated_student:
                    print(f"Student data updated: {updated_student}")
                else:
                    print("Failed to update student data.")

    elif command == "add mark":
        add_mark()
    else:
        print(f"Unknown command: {command}")


def handle_user_input():
    SYSTEM_COMMANDS = ("exit", "help")
    MANAGEMENT_COMMANDS = ("show list", "get by id", "add", "delete", "rename", "add mark")
    AVAILABLE_COMMANDS = SYSTEM_COMMANDS + MANAGEMENT_COMMANDS

    help_message = (
        "Welcome to the gradebook.\n"
        f"Available commands: {AVAILABLE_COMMANDS}\n"
    )
    print(help_message)

    while True:
        command = input("Enter command: ").strip()

        if command == "exit":
            print("See you next time..")
            break
        elif command == "help":
            print(help_message)
        elif command in MANAGEMENT_COMMANDS:
            handle_management_command(command=command)
        else:
            print(f"Unknown command: {command}")


if __name__ == '__main__':
    handle_user_input()

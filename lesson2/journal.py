students = {
    1: {
        "name": "John Doe",
        "marks": [4, 5, 1, 4, 5, 2, 5],
        "info": "John is 22 years old. Hobby: music",
    },
    2: {
        "name": "Mary Black",
        "marks": [4, 1, 3, 4, 5, 1, 2, 2],
        "info": "Mary is 23 years old. Hobby: football",
                                                            },
}

LAST_ID_CONTEXT = 2


def show_students() -> None:
    print("=" * 20)
    print("List of students:\n")
    for student_id, student in students.items():
        print(f"{student_id} {student['name']}, Marks: {student['marks']}")
    print("=" * 20)


def search_student(id_: int) -> dict | None:
    return students.get(id_)


def delete_student(id_: int) -> None:
    if search_student(id_):
        del students[id_]
        print(f"Student with ID '{id_}' was deleted.")
    else:
        print(f"Student with ID '{id_}' not found.")


def update_student(id_: int, payload: dict) -> dict | None:
    student = students.get(id_)
    if student:
        if payload.get("name") is not None:
            student["name"] = payload["name"]
        if payload.get("marks") is not None:
            student["marks"] = payload["marks"]
        return student
    else:
        print(f"Student with ID '{id_}' not found.")
        return None


def add_student(student: dict) -> dict | None:
    global LAST_ID_CONTEXT

    if not student.get("name"):
        print("Missing mandatory field: name. Student not added.")
        return None
    LAST_ID_CONTEXT += 1
    students[LAST_ID_CONTEXT] = student
    return student


def add_mark():
    student_id = input("Enter student ID to add a mark: ")

    if not student_id:
        print("ID cannot be empty.")
        return

    try:
        id_ = int(student_id)
    except ValueError:
        print(f"ID '{student_id}' is not a valid value.")
        return

    student = search_student(id_)
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
    print(f"Marks {marks} added for student '{student['name']}'.")


def student_details(student: dict) -> None:
    print(f"Detailed information: {student['name']} - Marks: {student['marks']}, Info: {student['info']}")


def ask_student_payload():
    prompt = ("Enter student data: you can enter 'First Last' for the name,"
              " '4,5,4,5,4,5' for the marks or both values: ")
    input_data = input(prompt)

    items = input_data.split(";")

    if len(items) == 1:
        if "," in items[0]:
            try:
                marks = [int(item) for item in items[0].split(",")]
                return {"name": None, "marks": marks}
            except ValueError:
                print("Marks are incorrect. Template: '4,5,4,5,4,5'. Marks must be numbers.")
                return None
        else:
            name = items[0].strip()
            if not name:
                print("Name cannot be empty. Student not added.")
                return None
            return {"name": name, "marks": None}

    if len(items) == 2:
        name = items[0].strip()
        if not name:
            print("Name cannot be empty. Student not added.")
            return None
        try:
            marks = [int(item) for item in items[1].split(",")]
            return {"name": name, "marks": marks}
        except ValueError:
            print("Marks are incorrect. Template: '4,5,4,5,4,5'. Marks must be numbers.")
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
            student = search_student(id_)
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
            delete_student(id_)
    elif command == "add":
        data = ask_student_payload()
        if data:
            student = add_student(data)
            if student:
                print(f"New student '{student['name']}' added.")
            else:
                print("Student was not added.")
    elif command == "rename":
        update_id = input("Enter student ID to update data: ")
        try:
            id_ = int(update_id)
        except ValueError:
            print(f"ID '{update_id}' is not a valid value.")
        else:
            data = ask_student_payload()
            if data:
                updated_student = update_student(id_, data)
                if updated_student:
                    print(f"Student data updated: {updated_student}")
                else:
                    print("Failed to update student data.")
            else:
                print("Invalid data entered for update.")
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

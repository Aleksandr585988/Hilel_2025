students = [
    {
        'id': 1,
        "first_name": "John",
        "last_name": "Doe",
        "marks": [4, 5, 1, 4, 5, 2, 5],
        "info": "John is 22 y.o. Hobbies: music",
    },
    {
        'id': 2,
        "first_name": "Marry",
        "last_name": "Black",
        "marks": [4, 1, 3, 4, 5, 1, 2, 2],
        "info": "Marry is 23 y.o. Hobbies: football",
    },
]

COMMANDS = ("quit", "show", "retrieve", "add")


def find_student(first_name: str, last_name: str) -> dict | None:
    for student in students:
        if student["first_name"] == first_name and student["last_name"] == last_name:
            return student
    return None


def show_students() -> None:
    print("=" * 20)
    print("The list of students:\n")
    for student in students:
        print(f"{student['id']} {student['last_name']} {student['first_name']},",
              f"Marks: {student['marks']}")

    print("=" * 20)


def show_student(student_id: int):
    student = next((s for s in students if s['id'] == student_id), None)
    if student:
        print("Details about student:\n")
        print(
            f"id: {student['id']}\n"
            f"Name: {student['first_name']} {student['last_name']}\n"
            f"Marks: {student['marks']}\n"
            f"Details: {student['info']}\n"
        )
    else:
        print(f"No student with ID {student_id}.")


def validate_name(name: str) -> None:  # Check for empty and digit string.
    if not isinstance(name, str) or not name.strip() or any(char.isdigit() for char in name):
        raise ValueError("The name must be a non-empty string and cannot contain numbers.")


def get_valid_name(prompt: str) -> str:
    while True:
        try:
            name = input(prompt).strip()
            validate_name(name)
            return name
        except ValueError as a:
            print(f"Error: {a}")


def add_student(first_name: str, last_name: str, marks: list = None, info: str = None):
    """ Checking for the existence of a student in a function. """
    existing_student = find_student(first_name, last_name)
    if existing_student:
        print(f"A student with the name {first_name} {last_name} already exists.")
        a = input('add? yes/no: ')
        if a == 'no':
            return None

    if marks is None:
        marks = []

    validate_name(first_name)
    validate_name(last_name)

    student_id = len(students) + 1

    instance = {
        "id": student_id,
        "first_name": first_name,
        "last_name": last_name,
        "marks": marks,
        "info": info
    }

    students.append(instance)

    print(f"Студент {first_name} {last_name} successfully added with ID: {student_id}.")
    return instance


def main():
    print(f"Welcome to the Digital Journal!\nAvailable commands: {COMMANDS}")
    while True:
        user_input = input("Enter the command: ")

        if user_input not in COMMANDS:
            print(f"The {user_input} command is not available.\n")
            continue

        if user_input == "quit":
            print("See you next time.")
            break

        try:
            if user_input == "show":
                show_students()
            elif user_input == "retrieve":
                student_id = int(input("Please enter the student ID you are looking for: "))
                show_student(student_id)
            elif user_input == "add":
                f_name = get_valid_name("Enter student name: ")
                l_name = get_valid_name("Enter your last name: ")

                marks = input("Enter grades (separated by commas) (optional field): ").strip()
                marks = [int(mark) for mark in marks.split(',') if mark.isdigit()] if marks else []
                info = input("Enter additional information (optional field): ").strip() or None

                add_student(f_name, l_name, marks, info)

        except NotImplementedError as error:
            print(f"Function '{error}' is not ready to run.")
        except Exception as error:
            print(error)


if __name__ == '__main__':
    main()

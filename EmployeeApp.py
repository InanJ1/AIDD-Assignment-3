"""
EmployeeApp.py — CLI user interface for Employee Management.
Business rules are enforced in employee.py; persistence and helpers in storage.py.
"""
from typing import List
from employee import Employee
from storage import load_employees, save_employees, create_employee, edit_employee, delete_employee, display_employees


def prompt(msg: str) -> str:
    return input(msg).strip()


def menu() -> None:
    employees: List[Employee] = load_employees()
    print("Employee Management App")
    print("-----------------------")
    while True:
        print("\nMenu: [A]dd  [E]dit  [D]elete  [L]ist  [Q]uit")
        choice = prompt("Choose an option: ").lower()
        try:
            if choice == 'a':
                emp_id = prompt("ID: ")
                fname = prompt("First name: ")
                lname = prompt("Last name: ")
                dept = prompt("Department (3 letters): ")
                phone = prompt("Phone (10 digits or formatted): ")
                e = create_employee(employees, emp_id, fname, lname, dept, phone)
                print(f"Added: {e}")
            elif choice == 'e':
                idx = int(prompt("Index to edit (1-based): ")) - 1
                print("Leave a field empty to keep current value.")
                fname = prompt("New first name: ")
                lname = prompt("New last name: ")
                dept  = prompt("New department (3 letters): ")
                phone = prompt("New phone: ")
                kwargs = {}
                if fname: kwargs['fname'] = fname
                if lname: kwargs['lname'] = lname
                if dept:  kwargs['dept'] = dept
                if phone: kwargs['phone'] = phone
                e = edit_employee(employees, idx, **kwargs)
                print(f"Updated: {e}")
            elif choice == 'd':
                idx = int(prompt("Index to delete (1-based): ")) - 1
                removed = delete_employee(employees, idx)
                print(f"Deleted: {removed}")
            elif choice == 'l':
                print("\n" + display_employees(employees))
            elif choice == 'q':
                save_employees(employees)
                print("Goodbye!")
                break
            else:
                print("Invalid option. Please choose A/E/D/L/Q.")
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    menu()

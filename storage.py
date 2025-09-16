"""
storage.py — Persistence & operations for Employee list.
Handles CSV load/save and CRUD helpers around Employee objects.
"""
import csv
from typing import List
from employee_model import Employee

CSV_FILE = "employee_data.csv"
CSV_HEADERS = ["id", "fname", "lname", "department", "phNumber"]


def load_employees(path: str = CSV_FILE) -> List[Employee]:
    """
    Load Employee objects from CSV. Creates an empty file with headers if missing.
    """
    employees: List[Employee] = []
    try:
        with open(path, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)
            if rows and rows[0] == CSV_HEADERS:
                rows = rows[1:]
            for row in rows:
                if not row or all(not c.strip() for c in row):
                    continue
                employees.append(Employee.from_csv_row(row))
    except FileNotFoundError:
        # Initialize a fresh file with headers
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(CSV_HEADERS)
    return employees


def save_employees(employees: List[Employee], path: str = CSV_FILE) -> None:
    """Write Employee objects back to CSV (overwrites file)."""
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(CSV_HEADERS)
        for e in employees:
            writer.writerow(e.to_csv_row())


# -----------------------
# CRUD helpers (Step 4)
# -----------------------
def create_employee(employees: List[Employee], emp_id: str, fname: str, lname: str, dept: str, phone: str) -> Employee:
    """Create and append a new Employee; persist to CSV. Raises ValueError on validation failures."""
    # Prevent duplicate IDs
    if any(e.id == str(emp_id) for e in employees):
        raise ValueError(f"Employee with ID {emp_id} already exists.")
    e = Employee(str(emp_id), fname, lname, dept, phone)
    employees.append(e)
    save_employees(employees)
    return e


def edit_employee(employees: List[Employee], index: int, *, fname: str = None, lname: str = None, dept: str = None, phone: str = None) -> Employee:
    """
    Edit an existing Employee by list index (0-based). ID cannot be changed.
    Raises IndexError if index invalid; ValueError for validation issues.
    """
    if index < 0 or index >= len(employees):
        raise IndexError("Invalid employee index.")
    e = employees[index]
    if fname is not None:
        e.fname = fname
    if lname is not None:
        e.lname = lname
    if dept is not None:
        e.department = dept
    if phone is not None:
        e.phNumber = phone
    save_employees(employees)
    return e


def delete_employee(employees: List[Employee], index: int) -> Employee:
    """Delete an Employee by list index; persist to CSV. Raises IndexError if invalid."""
    if index < 0 or index >= len(employees):
        raise IndexError("Invalid employee index.")
    removed = employees.pop(index)
    save_employees(employees)
    return removed


def display_employees(employees: List[Employee]) -> str:
    """Return a neatly formatted string of employees for display (does not print)."""
    lines = []
    for i, e in enumerate(employees, start=1):
        lines.append(f"{i}. {e.id} - {e.lname}, {e.fname} - {e.department} - {e.phNumber}")
    return "\n".join(lines) if lines else "(No employees found)"

# employee_model.py
import re
import logging

# Patterns
_NAME_PATTERN  = re.compile(r"^(?=.*[A-Za-z])[A-Za-z\s\-']+$")  # letters + space/hyphen/apostrophe
_DEPT_PATTERN  = re.compile(r"^[A-Z]{3}$")                      # exactly 3 uppercase letters
_DIGITS_ONLY   = re.compile(r"\D+")                             # non-digits

class Employee:
    """
    Business rules / validation live here.
    - First/last name: non-empty, letters (allow space, -, ')
    - Department: exactly 3 uppercase letters (e.g., ENG, HRM)
    - Phone: exactly 10 digits; stored as digits, formatted on read
    - id: read-only after creation
    """
    def __init__(self, emp_id: str, fname: str, lname: str, department: str, phNumber: str) -> None:
        self._id = str(emp_id)

        # Use property setters to validate
        self.fname = fname
        self.lname = lname
        self.department = department
        self.phNumber = phNumber

    # ----- id (read-only) -----
    @property
    def id(self) -> str:
        return self._id

    # ----- first name -----
    @property
    def fname(self) -> str:
        return self._fname

    @fname.setter
    def fname(self, value: str) -> None:
        if not isinstance(value, str) or not value.strip():
            raise ValueError("First name cannot be empty.")
        if not _NAME_PATTERN.match(value.strip()):
            # This also covers digits-in-name case
            raise ValueError("First name cannot contain digits.")
        self._fname = value.strip().title()

    # ----- last name -----
    @property
    def lname(self) -> str:
        return self._lname

    @lname.setter
    def lname(self, value: str) -> None:
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Last name cannot be empty.")
        if not _NAME_PATTERN.match(value.strip()):
            raise ValueError("Last name contains invalid characters.")
        self._lname = value.strip().title()

    # ----- department (3 uppercase letters) -----
    @property
    def department(self) -> str:
        return self._department

    @department.setter
    def department(self, value: str) -> None:
        if not isinstance(value, str):
            raise ValueError("Department must be exactly 3 uppercase letters.")
        v = value.strip().upper()
        if not _DEPT_PATTERN.match(v):
            raise ValueError("Department must be exactly 3 uppercase letters.")
        self._department = v

    # ----- phone (10 digits; formatted on read) -----
    @property
    def phNumber(self) -> str:
        d = self._ph_digits
        return f"({d[0:3]}){d[3:6]}-{d[6:10]}"

    @phNumber.setter
    def phNumber(self, value: str) -> None:
        if not isinstance(value, str):
            raise ValueError("Phone number must have exactly 10 digits.")
        digits = _DIGITS_ONLY.sub("", value)
        if len(digits) != 10:
            raise ValueError("Phone number must have exactly 10 digits.")
        self._ph_digits = digits

    # helpers for storage
    def raw_phone(self) -> str:
        return self._ph_digits

    def to_csv_row(self):
        return [self.id, self.fname, self.lname, self.department, self.raw_phone()]

    @staticmethod
    def from_csv_row(row):
        if len(row) != 5:
            raise ValueError("CSV row must be: id,fname,lname,department,phNumber")
        return Employee(emp_id=row[0], fname=row[1], lname=row[2], department=row[3], phNumber=row[4])


# ---- mini tests (Step 7) ----
def _run_basic_tests() -> None:
    logging.basicConfig(filename='employee_test.log',
                        level=logging.INFO,
                        format='%(levelname)s:%(message)s')

    def check(label, fn, expect_error=False):
        """
        If expect_error=True, we PASS when an exception happens (because we wanted rejection).
        If expect_error=False, we PASS when no exception happens.
        """
        try:
            fn()
            if expect_error:
                logging.error("FAIL: %s -> expected an error but none happened.", label)
            else:
                logging.info("PASS: %s", label)
        except Exception as e:
            if expect_error:
                logging.info("PASS: %s (caught: %s)", label, e)
            else:
                logging.error("FAIL: %s -> %s", label, e)

    # ✅ should succeed
    check("Valid employee", lambda: Employee("1", "Ada", "Lovelace", "ENG", "3175551212"))

    # ❌ should be rejected (so we expect errors = True)
    check("Reject digits in fname", lambda: Employee("2", "A9a", "Smith", "HRM", "3175551212"), expect_error=True)
    check("Reject empty lname",   lambda: Employee("3", "Alan", "   ", "FIN", "3175551212"), expect_error=True)
    check("Reject wrong dept",    lambda: Employee("4", "Grace", "Hopper", "Finance", "3175551212"), expect_error=True)
    check("Reject short phone",   lambda: Employee("5", "Linus", "Torvalds", "ITD", "12345"), expect_error=True)

    # id read-only check
    def _id_readonly():
        e = Employee("9", "Mary", "Johnson", "QAQ", "1112223333")
        try:
            setattr(e, "id", "10")
        except AttributeError:
            pass
        else:
            raise AssertionError("ID was mutated but should be read-only.")
    check("ID read-only", _id_readonly)

if __name__ == "__main__":
    _run_basic_tests()
    print("Basic tests executed. See employee_test.log for results.")

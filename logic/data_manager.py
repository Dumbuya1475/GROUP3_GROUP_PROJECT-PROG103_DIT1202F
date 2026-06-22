"""
data_manager.py - JSON-based data persistence and business logic for StudyTrack

Demonstrates structured programming principles:
    - Variables & constants     (see ui/theme.py: GRADE_SCALE)
    - Data types                (str, int, float, list, dict, bool)
    - Decision structures       (if / elif / else throughout)
    - Iteration (loops)         (for loops for searching/filtering/aggregating)
    - User-defined functions    (20+ functions, each with a single responsibility)
"""

import json
import os
import hashlib
from datetime import datetime

from ui.theme import GRADE_SCALE

# ─────────────────────────────────────────────
# CONSTANTS — FILE PATHS
# ─────────────────────────────────────────────
DATA_DIR        = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
USERS_FILE      = os.path.join(DATA_DIR, "users.json")
COURSES_FILE    = os.path.join(DATA_DIR, "courses.json")
ENROLLS_FILE    = os.path.join(DATA_DIR, "enrollments.json")
GRADES_FILE     = os.path.join(DATA_DIR, "grades.json")


# ─────────────────────────────────────────────
# GENERIC HELPER FUNCTIONS
# ─────────────────────────────────────────────
def hash_password(password: str) -> str:
    """Return a SHA-256 hash of a plaintext password."""
    return hashlib.sha256(password.encode()).hexdigest()


def load_json(filepath: str):
    """Load JSON data from a file. Returns an empty list if the file doesn't exist."""
    if not os.path.exists(filepath):
        return []
    with open(filepath, "r") as f:
        return json.load(f)


def save_json(filepath: str, data) -> None:
    """Persist data to a JSON file, creating the data directory if needed."""
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)


def timestamp() -> str:
    """Return the current date and time as a formatted string."""
    return datetime.now().strftime("%Y-%m-%d %H:%M")


# ─────────────────────────────────────────────
# GRADING LOGIC (decision structure example)
# ─────────────────────────────────────────────
def score_to_grade(score: float) -> dict:
    """
    Convert a numeric score (0-100) into a letter grade and grade point.

    Demonstrates a decision structure (if/elif/else equivalent) by
    iterating through the GRADE_SCALE from highest to lowest threshold.

    Parameters:
        score - Numeric score between 0 and 100

    Returns:
        {'letter': 'A', 'point': 4.0}
    """
    # GRADE_SCALE is already ordered from highest to lowest threshold
    for minimum, letter, point in GRADE_SCALE:
        if score >= minimum:
            return {"letter": letter, "point": point}
    # Fallback (should not be reached since 0 is the lowest threshold)
    return {"letter": "F", "point": 0.0}


def calculate_gpa(grade_records: list) -> float:
    """
    Calculate a student's GPA from a list of grade records.

    Each grade record must have 'point' and 'credit_hours' keys.
    Uses a weighted average: sum(point * credit_hours) / sum(credit_hours)

    Parameters:
        grade_records - List of dicts with 'point' and 'credit_hours'

    Returns:
        GPA as a float rounded to 2 decimal places (0.0 if no records)
    """
    if not grade_records:
        return 0.0

    total_points  = 0.0
    total_credits = 0

    for record in grade_records:
        total_points  += record["point"] * record["credit_hours"]
        total_credits += record["credit_hours"]

    if total_credits == 0:
        return 0.0

    return round(total_points / total_credits, 2)


# ─────────────────────────────────────────────
# USER FUNCTIONS (Admin, Lecturer, Student)
# ─────────────────────────────────────────────
def register_user(full_name: str, email: str, password: str, role: str,
                   student_id: str = "") -> dict:
    """
    Register a new user account.

    Parameters:
        full_name  - User's full name
        email      - Unique email address
        password   - Plaintext password (hashed before storage)
        role       - 'admin' | 'lecturer' | 'student'
        student_id - Optional student ID number (students only)

    Returns:
        {'success': True, 'user': {...}} or {'success': False, 'error': '...'}
    """
    users = load_json(USERS_FILE)

    # ── Validation (decision structures) ──
    if not full_name.strip():
        return {"success": False, "error": "Full name is required."}
    if "@" not in email or "." not in email:
        return {"success": False, "error": "Please enter a valid email address."}
    if len(password) < 6:
        return {"success": False, "error": "Password must be at least 6 characters."}
    if role not in ("admin", "lecturer", "student"):
        return {"success": False, "error": "Invalid role selected."}

    # Check for duplicate email (loop + decision)
    for user in users:
        if user["email"].lower() == email.lower():
            return {"success": False, "error": "An account with this email already exists."}

    new_user = {
        "id":         len(users) + 1,
        "full_name":  full_name.strip(),
        "email":      email.lower().strip(),
        "password":   hash_password(password),
        "role":       role,
        "student_id": student_id.strip() if role == "student" else "",
        "created_at": timestamp(),
    }
    users.append(new_user)
    save_json(USERS_FILE, users)
    return {"success": True, "user": new_user}


def login_user(email: str, password: str) -> dict:
    """
    Authenticate a user by email and password.

    Returns:
        {'success': True, 'user': {...}} or {'success': False, 'error': '...'}
    """
    users  = load_json(USERS_FILE)
    hashed = hash_password(password)

    for user in users:
        if user["email"].lower() == email.lower() and user["password"] == hashed:
            return {"success": True, "user": user}

    return {"success": False, "error": "Invalid email or password."}


def get_all_users(role: str = None) -> list:
    """Return all users, optionally filtered by role."""
    users = load_json(USERS_FILE)
    if role:
        return [u for u in users if u["role"] == role]
    return users


def get_user_by_id(user_id: int):
    """Return a single user dict by ID, or None if not found."""
    for user in load_json(USERS_FILE):
        if user["id"] == user_id:
            return user
    return None


def delete_user(user_id: int) -> bool:
    """Remove a user account (admin action). Returns True on success."""
    users = load_json(USERS_FILE)
    filtered = [u for u in users if u["id"] != user_id]
    if len(filtered) == len(users):
        return False
    save_json(USERS_FILE, filtered)
    return True


# ─────────────────────────────────────────────
# COURSE FUNCTIONS (Admin creates, Lecturer is assigned)
# ─────────────────────────────────────────────
def create_course(code: str, title: str, credit_hours: int,
                   lecturer_id: int, capacity: int = 40) -> dict:
    """
    Create a new course (admin action).

    Parameters:
        code         - Course code, e.g. 'CS101'
        title        - Course title
        credit_hours - Number of credit hours (used in GPA weighting)
        lecturer_id  - ID of the assigned lecturer
        capacity     - Maximum number of students that can enroll

    Returns:
        {'success': True, 'course': {...}} or {'success': False, 'error': '...'}
    """
    courses = load_json(COURSES_FILE)

    if not code.strip():
        return {"success": False, "error": "Course code is required."}
    if not title.strip():
        return {"success": False, "error": "Course title is required."}
    if credit_hours <= 0:
        return {"success": False, "error": "Credit hours must be greater than zero."}

    # Check for duplicate course code
    for course in courses:
        if course["code"].upper() == code.upper():
            return {"success": False, "error": "A course with this code already exists."}

    new_course = {
        "id":           len(courses) + 1,
        "code":         code.upper().strip(),
        "title":        title.strip(),
        "credit_hours": credit_hours,
        "lecturer_id":  lecturer_id,
        "capacity":     capacity,
        "created_at":   timestamp(),
    }
    courses.append(new_course)
    save_json(COURSES_FILE, courses)
    return {"success": True, "course": new_course}


def get_all_courses(lecturer_id: int = None) -> list:
    """Return all courses, optionally filtered by assigned lecturer."""
    courses = load_json(COURSES_FILE)
    if lecturer_id:
        return [c for c in courses if c["lecturer_id"] == lecturer_id]
    return courses


def get_course_by_id(course_id: int):
    """Return a single course dict by ID, or None if not found."""
    for course in load_json(COURSES_FILE):
        if course["id"] == course_id:
            return course
    return None


def delete_course(course_id: int) -> bool:
    """Remove a course (admin action). Returns True on success."""
    courses  = load_json(COURSES_FILE)
    filtered = [c for c in courses if c["id"] != course_id]
    if len(filtered) == len(courses):
        return False
    save_json(COURSES_FILE, filtered)
    return True


# ─────────────────────────────────────────────
# ENROLLMENT FUNCTIONS (Student registers for courses)
# ─────────────────────────────────────────────
def enroll_student(student_id: int, course_id: int) -> dict:
    """
    Register a student for a course.

    Checks for duplicate enrollment and course capacity before enrolling.

    Returns:
        {'success': True} or {'success': False, 'error': '...'}
    """
    enrollments = load_json(ENROLLS_FILE)
    course = get_course_by_id(course_id)

    if not course:
        return {"success": False, "error": "Course not found."}

    # Prevent duplicate enrollment (loop + decision)
    for e in enrollments:
        if e["student_id"] == student_id and e["course_id"] == course_id:
            return {"success": False, "error": "You are already registered for this course."}

    # Check capacity (loop to count current enrollments)
    current_count = 0
    for e in enrollments:
        if e["course_id"] == course_id:
            current_count += 1

    if current_count >= course["capacity"]:
        return {"success": False, "error": "This course has reached its enrollment capacity."}

    new_enrollment = {
        "id":           len(enrollments) + 1,
        "student_id":   student_id,
        "course_id":    course_id,
        "enrolled_at":  timestamp(),
    }
    enrollments.append(new_enrollment)
    save_json(ENROLLS_FILE, enrollments)
    return {"success": True}


def get_enrollments(student_id: int = None, course_id: int = None) -> list:
    """Return enrollments filtered by student or course ID."""
    enrollments = load_json(ENROLLS_FILE)
    if student_id:
        return [e for e in enrollments if e["student_id"] == student_id]
    if course_id:
        return [e for e in enrollments if e["course_id"] == course_id]
    return enrollments


def drop_course(student_id: int, course_id: int) -> bool:
    """Remove a student's enrollment from a course."""
    enrollments = load_json(ENROLLS_FILE)
    filtered = [
        e for e in enrollments
        if not (e["student_id"] == student_id and e["course_id"] == course_id)
    ]
    if len(filtered) == len(enrollments):
        return False
    save_json(ENROLLS_FILE, filtered)
    return True


# ─────────────────────────────────────────────
# GRADE FUNCTIONS (Lecturer enters, Student views)
# ─────────────────────────────────────────────
def submit_grade(student_id: int, course_id: int, score: float) -> dict:
    """
    Submit or update a grade for a student in a course.

    Automatically computes the letter grade and grade point using
    score_to_grade(). If a grade record already exists for this
    student/course pair, it is updated rather than duplicated.

    Parameters:
        student_id - The student's user ID
        course_id  - The course ID
        score      - Numeric score from 0 to 100

    Returns:
        {'success': True, 'grade': {...}} or {'success': False, 'error': '...'}
    """
    if score < 0 or score > 100:
        return {"success": False, "error": "Score must be between 0 and 100."}

    course = get_course_by_id(course_id)
    if not course:
        return {"success": False, "error": "Course not found."}

    grade_info = score_to_grade(score)
    grades = load_json(GRADES_FILE)

    # Update existing record if found (loop + decision)
    for g in grades:
        if g["student_id"] == student_id and g["course_id"] == course_id:
            g["score"]        = score
            g["letter"]       = grade_info["letter"]
            g["point"]        = grade_info["point"]
            g["credit_hours"] = course["credit_hours"]
            g["updated_at"]   = timestamp()
            save_json(GRADES_FILE, grades)
            return {"success": True, "grade": g}

    # Otherwise create a new record
    new_grade = {
        "id":           len(grades) + 1,
        "student_id":   student_id,
        "course_id":    course_id,
        "score":        score,
        "letter":       grade_info["letter"],
        "point":        grade_info["point"],
        "credit_hours": course["credit_hours"],
        "updated_at":   timestamp(),
    }
    grades.append(new_grade)
    save_json(GRADES_FILE, grades)
    return {"success": True, "grade": new_grade}


def get_grades(student_id: int = None, course_id: int = None) -> list:
    """Return grade records filtered by student or course ID."""
    grades = load_json(GRADES_FILE)
    if student_id:
        return [g for g in grades if g["student_id"] == student_id]
    if course_id:
        return [g for g in grades if g["course_id"] == course_id]
    return grades


def get_student_gpa(student_id: int) -> float:
    """Convenience wrapper: fetch a student's grades and compute their GPA."""
    grades = get_grades(student_id=student_id)
    return calculate_gpa(grades)


# ─────────────────────────────────────────────
# SEED DEMO DATA
# ─────────────────────────────────────────────
def seed_demo_data() -> None:
    """Populate JSON files with demo records if they are currently empty."""
    users = load_json(USERS_FILE)
    if users:
        return  # Already seeded — do nothing

    demo_users = [
        {"id": 1, "full_name": "Mr. Elijah Fullah",   "email": "admin@limkokwing.edu.sl",    "password": hash_password("admin123"),   "role": "admin",    "student_id": "",      "created_at": "2026-03-01 09:00"},
        {"id": 2, "full_name": "Dr. Sheik Umar Kanu", "email": "lecturer@limkokwing.edu.sl", "password": hash_password("lecturer123"),"role": "lecturer", "student_id": "",      "created_at": "2026-03-01 09:00"},
        {"id": 3, "full_name": "Ms. Sarah Kelly",     "email": "skelly@limkokwing.edu.sl",   "password": hash_password("lecturer123"),"role": "lecturer", "student_id": "",      "created_at": "2026-03-02 09:00"},
        {"id": 4, "full_name": "Ibrahim Bangura",     "email": "student@limkokwing.edu.sl",  "password": hash_password("student123"), "role": "student",  "student_id": "LK2026-001", "created_at": "2026-03-05 10:00"},
        {"id": 5, "full_name": "Aminata Bah",         "email": "aminata@limkokwing.edu.sl",  "password": hash_password("student123"), "role": "student",  "student_id": "LK2026-002", "created_at": "2026-03-05 10:00"},
        {"id": 6, "full_name": "Ibrahim Sankoh",      "email": "ibrahim@limkokwing.edu.sl",  "password": hash_password("student123"), "role": "student",  "student_id": "LK2026-003", "created_at": "2026-03-06 11:00"},
        {"id": 7, "full_name": "Mohamed Bangura",     "email": "mohamed@limkokwing.edu.sl",  "password": hash_password("student123"), "role": "student",  "student_id": "LK2026-004", "created_at": "2026-03-07 09:00"},
        {"id": 8, "full_name": "Rebecca Kamara",      "email": "rebecca@limkokwing.edu.sl",  "password": hash_password("student123"), "role": "student",  "student_id": "LK2026-005", "created_at": "2026-03-07 10:00"},
        {"id": 9, "full_name": "Deen Conteh",         "email": "deen@limkokwing.edu.sl",     "password": hash_password("student123"), "role": "student",  "student_id": "LK2026-006", "created_at": "2026-03-07 11:00"},
    ]
    save_json(USERS_FILE, demo_users)

    demo_courses = [
        {"id": 1, "code": "PROG103", "title": "Principles of Structured Programming", "credit_hours": 4, "lecturer_id": 2, "capacity": 40, "created_at": "2026-03-01 09:00"},
        {"id": 2, "code": "DBMS102", "title": "Database Management Systems",          "credit_hours": 3, "lecturer_id": 2, "capacity": 35, "created_at": "2026-03-01 09:00"},
        {"id": 3, "code": "MATH101", "title": "Computerized Mathematics",             "credit_hours": 3, "lecturer_id": 3, "capacity": 45, "created_at": "2026-03-01 09:00"},
        {"id": 4, "code": "COMM104", "title": "Data Communication",                   "credit_hours": 3, "lecturer_id": 3, "capacity": 30, "created_at": "2026-03-01 09:00"},
    ]
    save_json(COURSES_FILE, demo_courses)

    demo_enrollments = [
        {"id": 1,  "student_id": 4, "course_id": 1, "enrolled_at": "2026-03-10 09:00"},
        {"id": 2,  "student_id": 4, "course_id": 2, "enrolled_at": "2026-03-10 09:00"},
        {"id": 3,  "student_id": 4, "course_id": 3, "enrolled_at": "2026-03-10 09:00"},
        {"id": 4,  "student_id": 5, "course_id": 1, "enrolled_at": "2026-03-11 10:00"},
        {"id": 5,  "student_id": 5, "course_id": 4, "enrolled_at": "2026-03-11 10:00"},
        {"id": 6,  "student_id": 6, "course_id": 1, "enrolled_at": "2026-03-12 08:00"},
        {"id": 7,  "student_id": 6, "course_id": 2, "enrolled_at": "2026-03-12 08:00"},
        {"id": 8,  "student_id": 6, "course_id": 3, "enrolled_at": "2026-03-12 08:00"},
        {"id": 9,  "student_id": 7, "course_id": 1, "enrolled_at": "2026-03-13 09:00"},
        {"id": 10, "student_id": 7, "course_id": 2, "enrolled_at": "2026-03-13 09:00"},
        {"id": 11, "student_id": 7, "course_id": 4, "enrolled_at": "2026-03-13 09:00"},
        {"id": 12, "student_id": 8, "course_id": 1, "enrolled_at": "2026-03-14 10:00"},
        {"id": 13, "student_id": 8, "course_id": 3, "enrolled_at": "2026-03-14 10:00"},
        {"id": 14, "student_id": 9, "course_id": 1, "enrolled_at": "2026-03-15 11:00"},
        {"id": 15, "student_id": 9, "course_id": 2, "enrolled_at": "2026-03-15 11:00"},
        {"id": 16, "student_id": 9, "course_id": 3, "enrolled_at": "2026-03-15 11:00"},
        {"id": 17, "student_id": 9, "course_id": 4, "enrolled_at": "2026-03-15 11:00"},
    ]
    save_json(ENROLLS_FILE, demo_enrollments)

    # Pre-populate a few grades (others left blank to demo lecturer entry flow)
    demo_grades = []
    grade_seed = [
        (4, 1, 78), (4, 2, 85), (4, 3, 91),
        (5, 1, 64),
        (6, 1, 55), (6, 2, 72),
        (7, 1, 88), (7, 2, 74),
        (8, 1, 69),
        (9, 1, 95), (9, 2, 90), (9, 3, 82),
    ]
    for idx, (student_id, course_id, score) in enumerate(grade_seed, start=1):
        course = next(c for c in demo_courses if c["id"] == course_id)
        info = score_to_grade(score)
        demo_grades.append({
            "id":           idx,
            "student_id":   student_id,
            "course_id":    course_id,
            "score":        score,
            "letter":       info["letter"],
            "point":        info["point"],
            "credit_hours": course["credit_hours"],
            "updated_at":   "2026-06-01 12:00",
        })
    save_json(GRADES_FILE, demo_grades)

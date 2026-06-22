# StudyTrack — Student Academic Portal

**PROG103: Principles of Structured Programming**
**Limkokwing University of Creative Technology Sierra Leone**
**Final Group Project | Semester 02 | June 2026**

---

## 📌 Project Overview

StudyTrack is a GUI-based Student Academic Portal built with Python and Tkinter. It digitises the core academic workflow for a Sierra Leonean tertiary institution: course creation, student registration, and grade management — replacing manual, paper-based record keeping.

**System Category (per Project Brief, Section 4):** Education System — Student Academic Portal

---

## 🌍 SDG Alignment

| SDG | Connection |
|-----|------------|
| **SDG 4** – Quality Education | Digitises course registration and grade tracking, giving students transparent, real-time access to their academic record |
| **SDG 9** – Industry, Innovation & Infrastructure | Demonstrates locally-built digital infrastructure for Sierra Leonean institutions |

---

## 🖥️ System Features

### Three User Roles

| Role | Capabilities |
|------|--------------|
| **Admin** | Create/delete courses, assign lecturers, create lecturer/admin accounts, remove user accounts, view system-wide statistics |
| **Lecturer** | View assigned courses, see enrolled student rosters, enter/update numeric scores (auto-converted to letter grades) |
| **Student** | Register/drop courses, view enrolled courses, view grades and transcript, see live GPA calculation |

### Core Screens
- **Login** — Email/password authentication
- **Register** — Self-service student account creation (Lecturer/Admin accounts are created by an Admin)
- **Role-based Dashboards** — Each role sees only the data and actions relevant to it

---

## 🏗️ Structured Programming Principles Applied

| Principle | Where Applied |
|-----------|---------------|
| **Variables & Constants** | `ui/theme.py` — colours, fonts, dimensions; `GRADE_SCALE` constant table |
| **Data Types** | `str`, `int`, `float` (scores/GPA), `list`, `dict`, `bool` throughout |
| **Decision Structures (if/elif/else)** | `score_to_grade()` grade-band lookup, all form validation, capacity checks in `enroll_student()` |
| **Iteration (loops)** | `calculate_gpa()` weighted sum loop, all `get_*` filter functions, roster-building loops in dashboards |
| **User-defined Functions (3+ required)** | 22 functions in `data_manager.py` alone: `score_to_grade()`, `calculate_gpa()`, `enroll_student()`, `submit_grade()`, `create_course()`, etc. |
| **Modular Structure** | Separated into `ui/` (presentation) and `logic/` (business logic/data) packages |
| **Input Module** | All registration, login, course creation, and grade entry forms |
| **Processing Module** | `logic/data_manager.py` — all calculations and validation |
| **Output Module** | Dashboards, transcript table, stat cards, badges |

### Key Algorithm: GPA Calculation
```python
def calculate_gpa(grade_records: list) -> float:
    total_points  = 0.0
    total_credits = 0
    for record in grade_records:
        total_points  += record["point"] * record["credit_hours"]
        total_credits += record["credit_hours"]
    return round(total_points / total_credits, 2) if total_credits else 0.0
```
This is a **credit-weighted GPA**, matching real university grading systems (a 4-credit course affects GPA more than a 2-credit course).

---

## 📁 Project Structure

```
studytrack/
├── main.py                    # Entry point
├── README.md                  # This file
├── LICENSE                    # MIT License
├── data/                      # JSON data files (auto-created on first run)
│   ├── users.json
│   ├── courses.json
│   ├── enrollments.json
│   └── grades.json
├── ui/                        # Presentation layer
│   ├── app.py                 # Screen router / controller
│   ├── theme.py                # Visual constants + GRADE_SCALE
│   ├── widgets.py              # Reusable GUI components
│   ├── auth_screens.py         # Login, Register
│   ├── student_dashboard.py    # Student: register, grades, GPA
│   ├── lecturer_dashboard.py   # Lecturer: roster, grade entry
│   └── admin_dashboard.py      # Admin: courses, users, stats
└── logic/                     # Business logic layer
    └── data_manager.py         # All data operations + grading/GPA logic
```

---

## ⚙️ How to Run

### Requirements
- Python 3.8+
- Tkinter (bundled with Python on Windows/macOS; on Linux: `sudo apt install python3-tk`)

### Steps
```bash
git clone https://github.com/YOUR_USERNAME/PROG103_FinalProject_Class_GroupName.git
cd PROG103_FinalProject_Class_GroupName
python main.py
```

### Demo Accounts

| Email | Password | Role |
|-------|----------|------|
| `admin@limkokwing.edu.sl` | `admin123` | Admin |
| `lecturer@limkokwing.edu.sl` | `lecturer123` | Lecturer |
| `skelly@limkokwing.edu.sl` | `lecturer123` | Lecturer |
| `student@limkokwing.edu.sl` | `student123` | Student (Ibrahim Bangura) |
| `aminata@limkokwing.edu.sl` | `student123` | Student |
| `ibrahim@limkokwing.edu.sl` | `student123` | Student (Ibrahim Sankoh) |
| `mohamed@limkokwing.edu.sl` | `student123` | Student (Mohamed Bangura) |
| `rebecca@limkokwing.edu.sl` | `student123` | Student (Rebecca Kamara) |
| `deen@limkokwing.edu.sl` | `student123` | Student (Deen Conteh) |

The system seeds 4 demo courses, 9 demo users, and sample grades on first launch.

---

## 🔒 Data, Privacy & Compliance

- Passwords are hashed with **SHA-256** — never stored in plaintext
- All data stored **locally** in JSON — no external network calls
- Grade and academic data only visible to the relevant student, their lecturer, and admin
- No third-party data sharing

## 📊 Data Accessibility & Interoperability

- JSON storage format is human-readable and portable to any database (SQLite, MySQL, etc.)
- Business logic (`logic/data_manager.py`) is fully decoupled from the GUI — the storage backend can be swapped without touching UI code

---

## 📜 License

MIT License — see `LICENSE` file.

---

## 👥 Group Members

| Name | Contribution |
|------|--------------|
| [Member 1] | Project Lead / Data Layer |
| [Member 2] | Auth Screens / GUI Design |
| [Member 3] | Student & Lecturer Dashboards |
| [Member 4] | Admin Dashboard / Testing |
| [Member 5] | Documentation / GitHub Submission |

---

## 🙏 Acknowledgements

- Examiner: **Elijah Fullah**
- Checked by: **Sheik Umar Kanu**
- Faculty: **Limkokwing University of Creative Technology, Sierra Leone**

"""
StudyTrack - Student Academic Portal
PROG103: Principles of Structured Programming — Final Project

System Category: EDUCATION SYSTEM (Student Academic Portal)
SDG Alignment: SDG 4 — Quality Education

Allows three roles to interact with a shared academic record system:
    - Admin    : manages courses, lecturers, and students
    - Lecturer : enters and updates grades for assigned courses
    - Student  : registers for courses and views grades / GPA

Author: [Your Group Name]
Institution: Limkokwing University of Creative Technology, Sierra Leone
"""

import tkinter as tk
from ui.app import StudyTrackApp


def main():
    """Launch the StudyTrack application."""
    root = tk.Tk()
    app = StudyTrackApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

"""
lecturer_dashboard.py - Lecturer Dashboard for StudyTrack
View assigned courses and enter/update student grades.
"""

import tkinter as tk
from tkinter import messagebox
from ui.theme import *
from ui.widgets import (make_button, make_stat_card, make_scrollable_frame,
                         make_section_header, make_badge, make_entry,
                         grade_color)
from logic.data_manager import (get_all_courses, get_enrollments, get_grades,
                                 submit_grade, get_user_by_id, get_course_by_id)


class LecturerDashboard(tk.Frame):
    """
    Lecturer dashboard with:
    - Stat cards: assigned courses, total students, grades entered, pending
    - My Courses tab — lists assigned courses with student counts
    - Enter Grades view — per-course roster with score entry
    """

    def __init__(self, parent, user, on_logout):
        super().__init__(parent, bg=BG_MAIN)
        self.user      = user
        self.on_logout = on_logout
        self._build()

    def _build(self):
        self._build_navbar()
        self._build_body()

    # ─── NAVBAR ───────────────────────────────────────────────────────
    def _build_navbar(self):
        nav = tk.Frame(self, bg=WHITE, height=NAV_HEIGHT,
                       highlightbackground=LIGHT_GRAY, highlightthickness=1)
        nav.pack_propagate(False)
        nav.pack(fill="x")

        logo_frame = tk.Frame(nav, bg=WHITE)
        logo_frame.pack(side="left", padx=PAD)
        logo_box = tk.Frame(logo_frame, bg=BLUE, width=32, height=32)
        logo_box.pack_propagate(False)
        logo_box.pack(side="left", pady=14, padx=(0, 6))
        tk.Label(logo_box, text="👨‍🏫", bg=BLUE, fg=WHITE, font=(FONT_FAMILY, 12)).pack(expand=True)
        tk.Label(logo_frame, text="StudyTrack", font=FONT_LOGO, bg=WHITE, fg=NAVY).pack(side="left")

        nav_btns = tk.Frame(nav, bg=WHITE)
        nav_btns.pack(side="left", padx=20)
        self._nav_btn(nav_btns, "🏠 Dashboard",  self._show_dashboard, active=True)
        self._nav_btn(nav_btns, "📚 My Modules", self._show_courses)

        right = tk.Frame(nav, bg=WHITE)
        right.pack(side="right", padx=PAD)
        tk.Label(right, text=f"👨‍🏫 {self.user['full_name']}",
                 font=FONT_BODY, bg=WHITE, fg=TEXT_MID).pack(side="left", padx=8)
        make_button(right, "Logout", self.on_logout, style="ghost").pack(side="left")

    def _nav_btn(self, parent, text, cmd, active=False):
        bg = BLUE if active else WHITE
        fg = WHITE if active else TEXT_MID
        lbl = tk.Label(parent, text=text, font=FONT_NAV, bg=bg, fg=fg,
                       padx=14, pady=18, cursor="hand2")
        lbl.pack(side="left")
        lbl.bind("<Button-1>", lambda e: cmd())

    # ─── BODY ─────────────────────────────────────────────────────────
    def _build_body(self):
        self.body = tk.Frame(self, bg=BG_MAIN)
        self.body.pack(fill="both", expand=True)
        self._show_dashboard()

    def _clear_body(self):
        for w in self.body.winfo_children():
            w.destroy()

    # ─── DASHBOARD ────────────────────────────────────────────────────
    def _show_dashboard(self):
        self._clear_body()
        scroll_outer, scroll_inner = make_scrollable_frame(self.body)
        scroll_outer.pack(fill="both", expand=True)

        container = tk.Frame(scroll_inner, bg=BG_MAIN, padx=PAD*2, pady=PAD)
        container.pack(fill="both", expand=True)

        tk.Label(container, text="Lecturer Dashboard", font=FONT_HEADING1,
                 bg=BG_MAIN, fg=TEXT_DARK).pack(anchor="w")
        tk.Label(container, text="Manage your modules and student grades",
                 font=FONT_BODY, bg=BG_MAIN, fg=DARK_GRAY).pack(anchor="w", pady=(4, PAD))

        my_courses = get_all_courses(lecturer_id=self.user["id"])

        total_students = 0
        total_graded   = 0
        total_pending  = 0
        for course in my_courses:
            enrollments = get_enrollments(course_id=course["id"])
            grades      = get_grades(course_id=course["id"])
            total_students += len(enrollments)
            total_graded   += len(grades)
            total_pending  += len(enrollments) - len(grades)

        row = tk.Frame(container, bg=BG_MAIN)
        row.pack(fill="x", pady=(0, PAD))
        stat_data = [
            ("📚", len(my_courses),   "Assigned Courses", BLUE),
            ("👥", total_students,    "Total Students",   NAVY),
            ("✅", total_graded,      "Grades Entered",   SUCCESS),
            ("⏳", total_pending,     "Pending Grades",   ORANGE),
        ]
        for icon, val, label, color in stat_data:
            card = make_stat_card(row, icon, val, label, color)
            card.pack(side="left", fill="both", expand=True, padx=6)

        make_section_header(container, "My Assigned Courses",
                            "View All", self._show_courses)

        if not my_courses:
            tk.Label(container, text="You have not been assigned any courses yet.",
                     font=FONT_BODY, bg=BG_MAIN, fg=DARK_GRAY).pack(pady=20)
        else:
            for course in my_courses:
                self._build_course_card(container, course)

    def _build_course_card(self, parent, course):
        """Course card with roster count and 'Enter Grades' action."""
        card = tk.Frame(parent, bg=WHITE, highlightbackground=LIGHT_GRAY, highlightthickness=1)
        card.pack(fill="x", pady=6)

        body = tk.Frame(card, bg=WHITE, padx=PAD, pady=PAD)
        body.pack(fill="x")

        top = tk.Frame(body, bg=WHITE)
        top.pack(fill="x")
        tk.Label(top, text=f"{course['code']} — {course['title']}", font=FONT_HEADING3,
                 bg=WHITE, fg=TEXT_DARK).pack(side="left")
        make_badge(top, f"{course['credit_hours']} Credit Hrs", BLUE).pack(side="right")

        enrollments = get_enrollments(course_id=course["id"])
        grades      = get_grades(course_id=course["id"])
        pending     = len(enrollments) - len(grades)

        tk.Label(body, text=f"👥 {len(enrollments)} students enrolled  •  ✅ {len(grades)} graded  •  ⏳ {pending} pending",
                 font=FONT_SMALL, bg=WHITE, fg=DARK_GRAY).pack(anchor="w", pady=4)

        make_button(card, "📝 Enter / Update Grades",
                    lambda c=course: self._show_grade_entry(c),
                    style="primary").pack(side="right", padx=PAD, pady=(0, PAD))

    # ─── MY COURSES (full list) ───────────────────────────────────────
    def _show_courses(self):
        self._clear_body()
        scroll_outer, scroll_inner = make_scrollable_frame(self.body)
        scroll_outer.pack(fill="both", expand=True)

        container = tk.Frame(scroll_inner, bg=BG_MAIN, padx=PAD*2, pady=PAD)
        container.pack(fill="both", expand=True)

        tk.Label(container, text="My Courses", font=FONT_HEADING1,
                 bg=BG_MAIN, fg=TEXT_DARK).pack(anchor="w")

        my_courses = get_all_courses(lecturer_id=self.user["id"])
        if not my_courses:
            tk.Label(container, text="No assigned courses.",
                     font=FONT_BODY, bg=BG_MAIN, fg=DARK_GRAY).pack(pady=40)
        else:
            for course in my_courses:
                self._build_course_card(container, course)

        make_button(container, "← Back to Dashboard", self._show_dashboard,
                    style="ghost").pack(anchor="w", pady=PAD)

    # ─── GRADE ENTRY VIEW ─────────────────────────────────────────────
    def _show_grade_entry(self, course):
        """Show roster for a course with editable score fields."""
        self._clear_body()
        scroll_outer, scroll_inner = make_scrollable_frame(self.body)
        scroll_outer.pack(fill="both", expand=True)

        container = tk.Frame(scroll_inner, bg=BG_MAIN, padx=PAD*2, pady=PAD)
        container.pack(fill="both", expand=True)

        tk.Label(container, text=f"Enter Grades: {course['code']}", font=FONT_HEADING1,
                 bg=BG_MAIN, fg=TEXT_DARK).pack(anchor="w")
        tk.Label(container, text=course["title"], font=FONT_BODY,
                 bg=BG_MAIN, fg=DARK_GRAY).pack(anchor="w", pady=(0, PAD))

        enrollments = get_enrollments(course_id=course["id"])
        if not enrollments:
            tk.Label(container, text="No students enrolled in this course yet.",
                     font=FONT_BODY, bg=BG_MAIN, fg=DARK_GRAY).pack(pady=40)
        else:
            self.score_entries = {}  # student_id -> Entry widget
            for e in enrollments:
                student = get_user_by_id(e["student_id"])
                if student:
                    self._build_roster_row(container, student, course)

        make_button(container, "← Back to My Courses", self._show_courses,
                    style="ghost").pack(anchor="w", pady=PAD)

    def _build_roster_row(self, parent, student, course):
        """Single student row with score entry and Save button."""
        card = tk.Frame(parent, bg=WHITE, highlightbackground=LIGHT_GRAY, highlightthickness=1)
        card.pack(fill="x", pady=4)

        row = tk.Frame(card, bg=WHITE, padx=PAD, pady=PAD_SM)
        row.pack(fill="x")

        # Student info
        info = tk.Frame(row, bg=WHITE)
        info.pack(side="left", fill="both", expand=True)
        tk.Label(info, text=student["full_name"], font=FONT_BODY_BOLD,
                 bg=WHITE, fg=TEXT_DARK).pack(anchor="w")
        tk.Label(info, text=student.get("student_id", ""), font=FONT_SMALL,
                 bg=WHITE, fg=DARK_GRAY).pack(anchor="w")

        # Current grade badge (if exists)
        existing_grades = get_grades(student_id=student["id"], course_id=course["id"])
        existing = next((g for g in existing_grades if g["course_id"] == course["id"]), None)

        if existing:
            make_badge(row, f"{existing['letter']} ({existing['score']}%)",
                       grade_color(existing["letter"])).pack(side="left", padx=PAD)

        # Score entry
        entry_frame, entry = make_entry(row, placeholder="Score (0-100)", width=14)
        entry_frame.pack(side="left", padx=PAD_SM)
        if existing:
            entry.delete(0, "end")
            entry.config(fg=TEXT_DARK)
            entry.insert(0, str(existing["score"]))

        make_button(row, "💾 Save",
                    lambda s=student, en=entry: self._save_grade(s, course, en),
                    style="success").pack(side="left")

    def _save_grade(self, student, course, entry):
        """Validate and submit a grade for one student."""
        raw = entry.get_value() if hasattr(entry, "get_value") else entry.get()

        if not raw.strip():
            messagebox.showerror("Missing Score", "Please enter a score before saving.")
            return

        try:
            score = float(raw)
        except ValueError:
            messagebox.showerror("Invalid Score", "Score must be a number between 0 and 100.")
            return

        result = submit_grade(student["id"], course["id"], score)
        if result["success"]:
            grade = result["grade"]
            messagebox.showinfo("Saved ✅",
                                f"{student['full_name']}: {grade['score']}% → "
                                f"Grade {grade['letter']} ({grade['point']} pts)")
            self._show_grade_entry(course)
        else:
            messagebox.showerror("Error", result["error"])

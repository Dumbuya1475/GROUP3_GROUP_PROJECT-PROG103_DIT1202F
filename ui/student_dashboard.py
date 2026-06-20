"""
student_dashboard.py - Student Dashboard for StudyTrack
Register for courses, view grades, track GPA.
"""

import tkinter as tk
from tkinter import messagebox
from ui.theme import *
from ui.widgets import (make_button, make_stat_card, make_scrollable_frame,
                         make_section_header, make_badge, make_divider,
                         grade_color, make_table)
from logic.data_manager import (get_all_courses, get_enrollments, enroll_student,
                                 drop_course, get_grades, get_student_gpa,
                                 get_user_by_id, get_course_by_id)


class StudentDashboard(tk.Frame):
    """
    Student dashboard with:
    - Stat cards: enrolled courses, GPA, completed courses, pending grades
    - Available Courses tab (register)
    - My Courses tab (drop / view)
    - My Grades tab (transcript view with GPA)
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
        logo_box = tk.Frame(logo_frame, bg=NAVY, width=32, height=32)
        logo_box.pack_propagate(False)
        logo_box.pack(side="left", pady=14, padx=(0, 6))
        tk.Label(logo_box, text="🎓", bg=NAVY, fg=WHITE, font=(FONT_FAMILY, 14)).pack(expand=True)
        tk.Label(logo_frame, text="StudyTrack", font=FONT_LOGO, bg=WHITE, fg=NAVY).pack(side="left")

        nav_btns = tk.Frame(nav, bg=WHITE)
        nav_btns.pack(side="left", padx=20)
        self._nav_btn(nav_btns, "🏠 Dashboard",        self._show_dashboard, active=True)
        self._nav_btn(nav_btns, "📚 Available Courses", self._show_available_courses)
        self._nav_btn(nav_btns, "📖 My Courses",        self._show_my_courses)
        self._nav_btn(nav_btns, "📊 My Grades",         self._show_grades)

        right = tk.Frame(nav, bg=WHITE)
        right.pack(side="right", padx=PAD)
        tk.Label(right, text=f"👤 {self.user['full_name']}  ({self.user['student_id']})",
                 font=FONT_BODY, bg=WHITE, fg=TEXT_MID).pack(side="left", padx=8)
        make_button(right, "Logout", self.on_logout, style="ghost").pack(side="left")

    def _nav_btn(self, parent, text, cmd, active=False):
        bg = NAVY if active else WHITE
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

        tk.Label(container, text=f"Welcome, {self.user['full_name'].split()[0]}! 👋",
                 font=FONT_HEADING1, bg=BG_MAIN, fg=TEXT_DARK).pack(anchor="w")
        tk.Label(container, text="Here's an overview of your academic progress",
                 font=FONT_BODY, bg=BG_MAIN, fg=DARK_GRAY).pack(anchor="w", pady=(4, PAD))

        my_enrollments = get_enrollments(student_id=self.user["id"])
        my_grades      = get_grades(student_id=self.user["id"])
        gpa            = get_student_gpa(self.user["id"])

        graded_course_ids = [g["course_id"] for g in my_grades]
        pending = [e for e in my_enrollments if e["course_id"] not in graded_course_ids]

        row = tk.Frame(container, bg=BG_MAIN)
        row.pack(fill="x", pady=(0, PAD))
        stat_data = [
            ("📚", len(my_enrollments), "Enrolled Courses", NAVY),
            ("📊", gpa,                 "Current GPA",      GOLD),
            ("✅", len(my_grades),      "Graded Courses",   SUCCESS),
            ("⏳", len(pending),        "Pending Grades",   ORANGE),
        ]
        for icon, val, label, color in stat_data:
            card = make_stat_card(row, icon, val, label, color)
            card.pack(side="left", fill="both", expand=True, padx=6)

        # My courses summary
        make_section_header(container, "My Enrolled Courses",
                            "View All", self._show_my_courses)
        if not my_enrollments:
            tk.Label(container, text="You are not enrolled in any courses yet.",
                     font=FONT_BODY, bg=BG_MAIN, fg=DARK_GRAY).pack(pady=10)
            make_button(container, "Browse Available Courses",
                        self._show_available_courses, style="primary").pack(anchor="w")
        else:
            for e in my_enrollments[:4]:
                course = get_course_by_id(e["course_id"])
                if course:
                    self._build_course_summary_card(container, course)

    def _build_course_summary_card(self, parent, course):
        """Compact course card showing code, title, and grade status."""
        card = tk.Frame(parent, bg=WHITE, highlightbackground=LIGHT_GRAY, highlightthickness=1)
        card.pack(fill="x", pady=4)

        row = tk.Frame(card, bg=WHITE, padx=PAD, pady=PAD_SM)
        row.pack(fill="x")

        info = tk.Frame(row, bg=WHITE)
        info.pack(side="left", fill="both", expand=True)
        tk.Label(info, text=f"{course['code']} — {course['title']}", font=FONT_BODY_BOLD,
                 bg=WHITE, fg=TEXT_DARK).pack(anchor="w")
        tk.Label(info, text=f"{course['credit_hours']} credit hours", font=FONT_SMALL,
                 bg=WHITE, fg=DARK_GRAY).pack(anchor="w")

        grades = get_grades(student_id=self.user["id"], course_id=course["id"])
        my_grade = next((g for g in grades if g["course_id"] == course["id"]), None)
        if my_grade:
            make_badge(row, f"{my_grade['letter']} ({my_grade['score']}%)",
                       grade_color(my_grade["letter"])).pack(side="right")
        else:
            make_badge(row, "Not graded yet", MID_GRAY).pack(side="right")

    # ─── AVAILABLE COURSES ────────────────────────────────────────────
    def _show_available_courses(self):
        self._clear_body()
        scroll_outer, scroll_inner = make_scrollable_frame(self.body)
        scroll_outer.pack(fill="both", expand=True)

        container = tk.Frame(scroll_inner, bg=BG_MAIN, padx=PAD*2, pady=PAD)
        container.pack(fill="both", expand=True)

        tk.Label(container, text="Available Courses", font=FONT_HEADING1,
                 bg=BG_MAIN, fg=TEXT_DARK).pack(anchor="w")
        tk.Label(container, text="Register for courses offered this semester",
                 font=FONT_BODY, bg=BG_MAIN, fg=DARK_GRAY).pack(anchor="w", pady=(4, PAD))

        all_courses = get_all_courses()
        my_enrollments = get_enrollments(student_id=self.user["id"])
        my_course_ids = [e["course_id"] for e in my_enrollments]

        if not all_courses:
            tk.Label(container, text="No courses available at the moment.",
                     font=FONT_BODY, bg=BG_MAIN, fg=DARK_GRAY).pack(pady=40)
        else:
            for course in all_courses:
                self._build_available_course_card(container, course, my_course_ids)

        make_button(container, "← Back to Dashboard", self._show_dashboard,
                    style="ghost").pack(anchor="w", pady=PAD)

    def _build_available_course_card(self, parent, course, my_course_ids):
        """Card for an available course with Register button."""
        card = tk.Frame(parent, bg=WHITE, highlightbackground=LIGHT_GRAY, highlightthickness=1)
        card.pack(fill="x", pady=6)

        body = tk.Frame(card, bg=WHITE, padx=PAD, pady=PAD)
        body.pack(fill="x")

        top = tk.Frame(body, bg=WHITE)
        top.pack(fill="x")
        tk.Label(top, text=f"{course['code']} — {course['title']}", font=FONT_HEADING3,
                 bg=WHITE, fg=TEXT_DARK).pack(side="left")
        make_badge(top, f"{course['credit_hours']} Credit Hrs", NAVY).pack(side="right")

        lecturer = get_user_by_id(course["lecturer_id"])
        lect_name = lecturer["full_name"] if lecturer else "TBA"
        tk.Label(body, text=f"👨‍🏫  {lect_name}", font=FONT_BODY,
                 bg=WHITE, fg=DARK_GRAY).pack(anchor="w", pady=2)

        enrolled_count = len(get_enrollments(course_id=course["id"]))
        tk.Label(body, text=f"👥 {enrolled_count}/{course['capacity']} seats filled",
                 font=FONT_SMALL, bg=WHITE, fg=MID_GRAY).pack(anchor="w")

        if course["id"] in my_course_ids:
            make_badge(card, "✔ Registered", SUCCESS).pack(side="right", padx=PAD, pady=(0, PAD))
        elif enrolled_count >= course["capacity"]:
            make_badge(card, "Course Full", DANGER).pack(side="right", padx=PAD, pady=(0, PAD))
        else:
            make_button(card, "Register", lambda c=course: self._register(c),
                        style="primary").pack(side="right", padx=PAD, pady=(0, PAD))

    def _register(self, course):
        """Register the student for a course."""
        result = enroll_student(self.user["id"], course["id"])
        if result["success"]:
            messagebox.showinfo("Registered! 🎉",
                                f"You have successfully registered for {course['code']} — {course['title']}.")
            self._show_available_courses()
        else:
            messagebox.showerror("Registration Failed", result["error"])

    # ─── MY COURSES ───────────────────────────────────────────────────
    def _show_my_courses(self):
        self._clear_body()
        scroll_outer, scroll_inner = make_scrollable_frame(self.body)
        scroll_outer.pack(fill="both", expand=True)

        container = tk.Frame(scroll_inner, bg=BG_MAIN, padx=PAD*2, pady=PAD)
        container.pack(fill="both", expand=True)

        tk.Label(container, text="My Courses", font=FONT_HEADING1,
                 bg=BG_MAIN, fg=TEXT_DARK).pack(anchor="w")

        my_enrollments = get_enrollments(student_id=self.user["id"])
        if not my_enrollments:
            tk.Label(container, text="You haven't registered for any courses yet.",
                     font=FONT_BODY, bg=BG_MAIN, fg=DARK_GRAY).pack(pady=40)
        else:
            for e in my_enrollments:
                course = get_course_by_id(e["course_id"])
                if course:
                    self._build_my_course_card(container, course)

        make_button(container, "← Back to Dashboard", self._show_dashboard,
                    style="ghost").pack(anchor="w", pady=PAD)

    def _build_my_course_card(self, parent, course):
        """Card for an enrolled course with Drop option."""
        card = tk.Frame(parent, bg=WHITE, highlightbackground=LIGHT_GRAY, highlightthickness=1)
        card.pack(fill="x", pady=6)

        body = tk.Frame(card, bg=WHITE, padx=PAD, pady=PAD)
        body.pack(fill="x")

        tk.Label(body, text=f"{course['code']} — {course['title']}", font=FONT_HEADING3,
                 bg=WHITE, fg=TEXT_DARK).pack(anchor="w")
        tk.Label(body, text=f"{course['credit_hours']} credit hours", font=FONT_BODY,
                 bg=WHITE, fg=DARK_GRAY).pack(anchor="w")

        grades = get_grades(student_id=self.user["id"], course_id=course["id"])
        my_grade = next((g for g in grades if g["course_id"] == course["id"]), None)

        btn_row = tk.Frame(card, bg=WHITE, padx=PAD, pady=(0, PAD))
        btn_row.pack(fill="x")
        if my_grade:
            make_badge(btn_row, f"Grade: {my_grade['letter']}", grade_color(my_grade["letter"])).pack(side="left")
        else:
            make_button(btn_row, "Drop Course",
                        lambda c=course: self._drop(c), style="danger").pack(side="left")

    def _drop(self, course):
        """Drop a course after confirmation (only allowed if ungraded)."""
        if messagebox.askyesno("Drop Course",
                               f"Are you sure you want to drop {course['code']}?"):
            if drop_course(self.user["id"], course["id"]):
                messagebox.showinfo("Dropped", f"You have dropped {course['code']}.")
                self._show_my_courses()

    # ─── GRADES / TRANSCRIPT ──────────────────────────────────────────
    def _show_grades(self):
        self._clear_body()
        scroll_outer, scroll_inner = make_scrollable_frame(self.body)
        scroll_outer.pack(fill="both", expand=True)

        container = tk.Frame(scroll_inner, bg=BG_MAIN, padx=PAD*2, pady=PAD)
        container.pack(fill="both", expand=True)

        tk.Label(container, text="My Grades & Transcript", font=FONT_HEADING1,
                 bg=BG_MAIN, fg=TEXT_DARK).pack(anchor="w")

        gpa = get_student_gpa(self.user["id"])
        gpa_card = tk.Frame(container, bg=NAVY, padx=PAD*2, pady=PAD)
        gpa_card.pack(fill="x", pady=PAD)
        tk.Label(gpa_card, text="Cumulative GPA", font=FONT_BODY,
                 bg=NAVY, fg="#B9C3D9").pack(anchor="w")
        tk.Label(gpa_card, text=f"{gpa} / 4.00", font=FONT_HEADING1,
                 bg=NAVY, fg=GOLD).pack(anchor="w")

        grades = get_grades(student_id=self.user["id"])
        if not grades:
            tk.Label(container, text="No grades recorded yet.",
                     font=FONT_BODY, bg=BG_MAIN, fg=DARK_GRAY).pack(pady=20)
        else:
            # Build table rows
            rows = []
            for g in grades:
                course = get_course_by_id(g["course_id"])
                if course:
                    rows.append((course["code"], course["title"], g["score"],
                                g["letter"], g["point"], g["credit_hours"]))

            table_frame = tk.Frame(container, bg=WHITE,
                                   highlightbackground=LIGHT_GRAY, highlightthickness=1)
            table_frame.pack(fill="x", pady=PAD_SM)
            table = make_table(table_frame,
                               columns=["Code", "Course Title", "Score", "Grade", "Points", "Credits"],
                               rows=rows,
                               col_widths=[80, 280, 70, 70, 70, 70])
            table.pack(fill="x", padx=PAD, pady=PAD)

        make_button(container, "← Back to Dashboard", self._show_dashboard,
                    style="ghost").pack(anchor="w", pady=PAD)

"""
admin_dashboard.py - Admin Dashboard for StudyTrack
Create courses, manage users, view system-wide statistics.
"""

import tkinter as tk
from tkinter import messagebox
from ui.theme import *
from ui.widgets import (make_button, make_stat_card, make_scrollable_frame,
                         make_section_header, make_badge, make_form_field,
                         make_dropdown, make_entry)
from logic.data_manager import (get_all_courses, get_all_users, create_course,
                                 delete_course, delete_user, get_enrollments,
                                 get_grades, get_user_by_id, register_user)


class AdminDashboard(tk.Frame):
    """
    Admin dashboard with:
    - Stat cards: total courses, students, lecturers, enrollments
    - Manage Modules tab — create / delete courses
    - Manage Users tab — view / create / delete lecturer & student accounts
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
        logo_box = tk.Frame(logo_frame, bg=GOLD, width=32, height=32)
        logo_box.pack_propagate(False)
        logo_box.pack(side="left", pady=14, padx=(0, 6))
        tk.Label(logo_box, text="⚙️", bg=GOLD, fg=WHITE, font=(FONT_FAMILY, 12)).pack(expand=True)
        tk.Label(logo_frame, text="StudyTrack", font=FONT_LOGO, bg=WHITE, fg=NAVY).pack(side="left")

        nav_btns = tk.Frame(nav, bg=WHITE)
        nav_btns.pack(side="left", padx=20)
        self._nav_btn(nav_btns, "🏠 Dashboard",       self._show_dashboard, active=True)
        self._nav_btn(nav_btns, "📚 Manage Modules",  self._show_courses)
        self._nav_btn(nav_btns, "👥 Manage Users",    self._show_users)

        right = tk.Frame(nav, bg=WHITE)
        right.pack(side="right", padx=PAD)
        tk.Label(right, text=f"⚙️ {self.user['full_name']}",
                 font=FONT_BODY, bg=WHITE, fg=TEXT_MID).pack(side="left", padx=8)
        make_button(right, "Logout", self.on_logout, style="ghost").pack(side="left")

    def _nav_btn(self, parent, text, cmd, active=False):
        bg = GOLD if active else WHITE
        fg = NAVY if active else TEXT_MID
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

        tk.Label(container, text="Admin Dashboard", font=FONT_HEADING1,
                 bg=BG_MAIN, fg=TEXT_DARK).pack(anchor="w")
        tk.Label(container, text="System-wide overview of StudyTrack academic portal",
                 font=FONT_BODY, bg=BG_MAIN, fg=DARK_GRAY).pack(anchor="w", pady=(4, PAD))

        all_courses   = get_all_courses()
        all_students  = get_all_users(role="student")
        all_lecturers = get_all_users(role="lecturer")
        all_enrolls   = get_enrollments()

        row = tk.Frame(container, bg=BG_MAIN)
        row.pack(fill="x", pady=(0, PAD))
        stat_data = [
            ("📚", len(all_courses),   "Total Modules",      NAVY),
            ("🧑‍🎓", len(all_students), "Total Students",     BLUE),
            ("👨‍🏫", len(all_lecturers),"Total Lecturers",    GOLD),
            ("📝", len(all_enrolls),   "Total Enrollments",  SUCCESS),
        ]
        for icon, val, label, color in stat_data:
            card = make_stat_card(row, icon, val, label, color)
            card.pack(side="left", fill="both", expand=True, padx=6)

        cols = tk.Frame(container, bg=BG_MAIN)
        cols.pack(fill="both", expand=True, pady=PAD)
        left  = tk.Frame(cols, bg=BG_MAIN)
        right = tk.Frame(cols, bg=BG_MAIN, width=320)
        left.pack(side="left", fill="both", expand=True, padx=(0, PAD))
        right.pack(side="right", fill="y")
        right.pack_propagate(False)

        make_section_header(left, "All Modules", "Manage", self._show_courses)
        for course in all_courses[:5]:
            self._build_course_row(left, course)

        make_section_header(right, "Quick Actions")
        qa = tk.Frame(right, bg=WHITE, highlightbackground=LIGHT_GRAY, highlightthickness=1)
        qa.pack(fill="x")
        make_button(qa, "+ Create New Module", self._show_create_course,
                    style="primary").pack(fill="x", padx=PAD, pady=(PAD, PAD_SM))
        make_button(qa, "+ Create Lecturer Account", self._show_create_user,
                    style="outline").pack(fill="x", padx=PAD, pady=(0, PAD))

    def _build_course_row(self, parent, course):
        """Compact course row for the admin dashboard list."""
        card = tk.Frame(parent, bg=WHITE, highlightbackground=LIGHT_GRAY, highlightthickness=1)
        card.pack(fill="x", pady=4)

        row = tk.Frame(card, bg=WHITE, padx=PAD, pady=PAD_SM)
        row.pack(fill="x")

        lecturer = get_user_by_id(course["lecturer_id"])
        lect_name = lecturer["full_name"] if lecturer else "Unassigned"

        info = tk.Frame(row, bg=WHITE)
        info.pack(side="left", fill="both", expand=True)
        tk.Label(info, text=f"{course['code']} — {course['title']}", font=FONT_BODY_BOLD,
                 bg=WHITE, fg=TEXT_DARK).pack(anchor="w")
        tk.Label(info, text=f"Lecturer: {lect_name}  •  {course['credit_hours']} credits",
                 font=FONT_SMALL, bg=WHITE, fg=DARK_GRAY).pack(anchor="w")

        enrolled = len(get_enrollments(course_id=course["id"]))
        make_badge(row, f"{enrolled}/{course['capacity']}", NAVY).pack(side="right")

    # ─── MANAGE MODULES ───────────────────────────────────────────────
    def _show_courses(self):
        self._clear_body()
        scroll_outer, scroll_inner = make_scrollable_frame(self.body)
        scroll_outer.pack(fill="both", expand=True)

        container = tk.Frame(scroll_inner, bg=BG_MAIN, padx=PAD*2, pady=PAD)
        container.pack(fill="both", expand=True)

        tk.Label(container, text="Manage Modules", font=FONT_HEADING1,
                 bg=BG_MAIN, fg=TEXT_DARK).pack(anchor="w")

        make_button(container, "+ Create New Module", self._show_create_course,
                    style="primary").pack(anchor="w", pady=PAD)

        all_courses = get_all_courses()
        if not all_courses:
            tk.Label(container, text="No modules created yet.",
                     font=FONT_BODY, bg=BG_MAIN, fg=DARK_GRAY).pack(pady=20)
        else:
            for course in all_courses:
                self._build_full_course_card(container, course)

        make_button(container, "← Back to Dashboard", self._show_dashboard,
                    style="ghost").pack(anchor="w", pady=PAD)

    def _build_full_course_card(self, parent, course):
        """Module card with delete action for the management view."""
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
        lect_name = lecturer["full_name"] if lecturer else "Unassigned"
        enrolled = len(get_enrollments(course_id=course["id"]))

        tk.Label(body, text=f"👨‍🏫 {lect_name}  •  👥 {enrolled}/{course['capacity']} enrolled",
                 font=FONT_BODY, bg=WHITE, fg=DARK_GRAY).pack(anchor="w", pady=2)

        make_button(card, "🗑 Delete Course",
                    lambda c=course: self._delete_course(c),
                    style="danger").pack(side="right", padx=PAD, pady=(0, PAD))

    def _delete_course(self, course):
        if messagebox.askyesno("Delete Course",
                               f"Delete {course['code']} — {course['title']}?\n"
                               "This cannot be undone."):
            if delete_course(course["id"]):
                messagebox.showinfo("Deleted", "Course has been removed.")
                self._show_courses()

    def _show_create_course(self):
        """Form to create a new course."""
        self._clear_body()
        container = tk.Frame(self.body, bg=BG_MAIN, padx=PAD*2, pady=PAD)
        container.pack(fill="both", expand=True)

        tk.Label(container, text="Create New Course", font=FONT_HEADING1,
                 bg=BG_MAIN, fg=TEXT_DARK).pack(anchor="w", pady=(0, PAD))

        card = tk.Frame(container, bg=WHITE, padx=PAD*2, pady=PAD*2,
                        highlightbackground=LIGHT_GRAY, highlightthickness=1)
        card.pack(fill="x")

        self.code_entry   = make_form_field(card, "Course Code *", placeholder="e.g. CS201")
        self.title_entry  = make_form_field(card, "Course Title *", placeholder="e.g. Data Structures")
        self.credit_entry = make_form_field(card, "Credit Hours *", placeholder="e.g. 3")
        self.cap_entry    = make_form_field(card, "Capacity", placeholder="e.g. 40")

        lecturers = get_all_users(role="lecturer")
        lecturer_names = [f"{l['full_name']} (ID:{l['id']})" for l in lecturers]
        self.lecturer_dropdown = make_dropdown(card, "Assign Lecturer *", lecturer_names)

        self.error_lbl = tk.Label(card, text="", font=FONT_SMALL, bg=WHITE, fg=DANGER)
        self.error_lbl.pack(anchor="w")

        btn_row = tk.Frame(card, bg=WHITE)
        btn_row.pack(fill="x", pady=(PAD_SM, 0))
        make_button(btn_row, "✔ Create Course", self._handle_create_course,
                    style="primary").pack(side="left")
        make_button(btn_row, "Cancel", self._show_courses,
                    style="ghost").pack(side="left", padx=PAD_SM)

    def _handle_create_course(self):
        code   = self.code_entry.get_value()
        title  = self.title_entry.get_value()
        credit = self.credit_entry.get_value()
        cap    = self.cap_entry.get_value()
        lect_selection = self.lecturer_dropdown.get()

        if not lect_selection:
            self.error_lbl.config(text="⚠  Please assign a lecturer.")
            return

        try:
            credit_val = int(credit)
        except ValueError:
            self.error_lbl.config(text="⚠  Credit hours must be a number.")
            return

        cap_val = 40
        if cap.strip():
            try:
                cap_val = int(cap)
            except ValueError:
                self.error_lbl.config(text="⚠  Capacity must be a number.")
                return

        # Extract lecturer ID from "Name (ID:3)" format
        lecturer_id = int(lect_selection.split("ID:")[1].rstrip(")"))

        result = create_course(code, title, credit_val, lecturer_id, cap_val)
        if result["success"]:
            messagebox.showinfo("Created ✅", f"Course {result['course']['code']} created successfully!")
            self._show_courses()
        else:
            self.error_lbl.config(text=f"⚠  {result['error']}")

    # ─── MANAGE USERS ─────────────────────────────────────────────────
    def _show_users(self):
        self._clear_body()
        scroll_outer, scroll_inner = make_scrollable_frame(self.body)
        scroll_outer.pack(fill="both", expand=True)

        container = tk.Frame(scroll_inner, bg=BG_MAIN, padx=PAD*2, pady=PAD)
        container.pack(fill="both", expand=True)

        tk.Label(container, text="Manage Users", font=FONT_HEADING1,
                 bg=BG_MAIN, fg=TEXT_DARK).pack(anchor="w")

        make_button(container, "+ Create Lecturer / Admin Account", self._show_create_user,
                    style="primary").pack(anchor="w", pady=PAD)

        make_section_header(container, "Lecturers")
        lecturers = get_all_users(role="lecturer")
        if not lecturers:
            tk.Label(container, text="No lecturers registered.",
                     font=FONT_BODY, bg=BG_MAIN, fg=DARK_GRAY).pack(pady=10)
        for l in lecturers:
            self._build_user_row(container, l)

        make_section_header(container, "Students")
        students = get_all_users(role="student")
        if not students:
            tk.Label(container, text="No students registered.",
                     font=FONT_BODY, bg=BG_MAIN, fg=DARK_GRAY).pack(pady=10)
        for s in students:
            self._build_user_row(container, s)

        make_button(container, "← Back to Dashboard", self._show_dashboard,
                    style="ghost").pack(anchor="w", pady=PAD)

    def _build_user_row(self, parent, user):
        """Row for a single user in the management list."""
        card = tk.Frame(parent, bg=WHITE, highlightbackground=LIGHT_GRAY, highlightthickness=1)
        card.pack(fill="x", pady=3)

        row = tk.Frame(card, bg=WHITE, padx=PAD, pady=PAD_SM)
        row.pack(fill="x")

        info = tk.Frame(row, bg=WHITE)
        info.pack(side="left", fill="both", expand=True)
        label = user["full_name"]
        if user["role"] == "student" and user.get("student_id"):
            label += f"  ({user['student_id']})"
        tk.Label(info, text=label, font=FONT_BODY_BOLD,
                 bg=WHITE, fg=TEXT_DARK).pack(anchor="w")
        tk.Label(info, text=user["email"], font=FONT_SMALL,
                 bg=WHITE, fg=DARK_GRAY).pack(anchor="w")

        role_colors = {"admin": GOLD, "lecturer": BLUE, "student": NAVY}
        make_badge(row, user["role"].title(), role_colors.get(user["role"], MID_GRAY)).pack(side="right", padx=(0, PAD_SM))

        if user["id"] != self.user["id"]:  # cannot delete self
            make_button(row, "Remove", lambda u=user: self._delete_user(u),
                        style="danger").pack(side="right")

    def _delete_user(self, user):
        if messagebox.askyesno("Remove User", f"Remove {user['full_name']}'s account?"):
            if delete_user(user["id"]):
                messagebox.showinfo("Removed", "User account removed.")
                self._show_users()

    def _show_create_user(self):
        """Form to create a new lecturer or admin account."""
        self._clear_body()
        container = tk.Frame(self.body, bg=BG_MAIN, padx=PAD*2, pady=PAD)
        container.pack(fill="both", expand=True)

        tk.Label(container, text="Create Staff Account", font=FONT_HEADING1,
                 bg=BG_MAIN, fg=TEXT_DARK).pack(anchor="w", pady=(0, PAD))

        card = tk.Frame(container, bg=WHITE, padx=PAD*2, pady=PAD*2,
                        highlightbackground=LIGHT_GRAY, highlightthickness=1)
        card.pack(fill="x")

        self.name_entry  = make_form_field(card, "Full Name *", placeholder="e.g. Dr. Fatmata Sesay")
        self.email_entry = make_form_field(card, "Email Address *", placeholder="e.g. fsesay@limkokwing.edu.sl")
        self.pass_entry  = make_form_field(card, "Temporary Password *", placeholder="Min. 6 characters", show="*")
        self.role_dropdown = make_dropdown(card, "Role *", ["lecturer", "admin"])

        self.error_lbl = tk.Label(card, text="", font=FONT_SMALL, bg=WHITE, fg=DANGER)
        self.error_lbl.pack(anchor="w")

        btn_row = tk.Frame(card, bg=WHITE)
        btn_row.pack(fill="x", pady=(PAD_SM, 0))
        make_button(btn_row, "✔ Create Account", self._handle_create_user,
                    style="primary").pack(side="left")
        make_button(btn_row, "Cancel", self._show_users,
                    style="ghost").pack(side="left", padx=PAD_SM)

    def _handle_create_user(self):
        name  = self.name_entry.get_value()
        email = self.email_entry.get_value()
        pwd   = self.pass_entry.get_value()
        role  = self.role_dropdown.get()

        result = register_user(name, email, pwd, role)
        if result["success"]:
            messagebox.showinfo("Created ✅", f"{role.title()} account created for {name}.")
            self._show_users()
        else:
            self.error_lbl.config(text=f"⚠  {result['error']}")

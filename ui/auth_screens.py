"""
auth_screens.py - Login and Registration screens for StudyTrack
"""

import tkinter as tk
from ui.theme import *
from ui.widgets import make_button, make_form_field, make_dropdown
from logic.data_manager import login_user, register_user


def build_left_panel(parent, headline, tagline, bullets):
    """Build the navy brand panel shared by Login and Register screens."""
    panel = tk.Frame(parent, bg=NAVY, width=420)
    panel.pack_propagate(False)
    panel.pack(side="left", fill="y")

    overlay = tk.Frame(panel, bg=NAVY_DARK)
    overlay.place(relx=0, rely=0.62, relwidth=1, relheight=0.5)

    logo_frame = tk.Frame(panel, bg=NAVY)
    logo_frame.place(relx=0.08, rely=0.12)
    logo_box = tk.Frame(logo_frame, bg=GOLD, width=50, height=50)
    logo_box.pack_propagate(False)
    logo_box.pack(side="left", padx=(0, 10))
    tk.Label(logo_box, text="🎓", font=(FONT_FAMILY, 22), bg=GOLD).pack(expand=True)
    tk.Label(logo_frame, text="StudyTrack", font=FONT_LOGO,
             bg=NAVY, fg=WHITE).pack(side="left")

    tk.Label(panel, text=headline, font=FONT_HEADING1, bg=NAVY, fg=WHITE,
             wraplength=320, justify="left").place(relx=0.08, rely=0.30)
    tk.Label(panel, text=tagline, font=FONT_BODY, bg=NAVY, fg="#B9C3D9",
             wraplength=320, justify="left").place(relx=0.08, rely=0.43)

    y = 0.55
    for bullet in bullets:
        tk.Label(panel, text=f"●  {bullet}", font=FONT_BODY,
                 bg=NAVY, fg=WHITE, anchor="w").place(relx=0.08, rely=y)
        y += 0.07

    return panel


# ─────────────────────────────────────────────
# LOGIN SCREEN
# ─────────────────────────────────────────────
class LoginScreen(tk.Frame):
    """Login screen with email/password and demo account hints."""

    def __init__(self, parent, on_login_success, on_go_register):
        super().__init__(parent, bg=WHITE)
        self.on_login_success = on_login_success
        self.on_go_register   = on_go_register
        self._build()

    def _build(self):
        build_left_panel(
            self,
            headline="Welcome to StudyTrack",
            tagline="Your academic journey, organized in one place. Register for courses, track grades, and monitor your GPA.",
            bullets=[
                "Register for courses each semester",
                "View grades as they're entered",
                "Track your GPA in real time",
            ]
        )

        right = tk.Frame(self, bg=WHITE)
        right.pack(side="right", fill="both", expand=True)
        tk.Frame(right, bg=WHITE).pack(expand=True)

        form = tk.Frame(right, bg=WHITE, padx=60)
        form.pack(fill="x")

        tk.Label(form, text="Sign In", font=FONT_HEADING1,
                 bg=WHITE, fg=TEXT_DARK).pack(anchor="w")
        tk.Label(form, text="Enter your credentials to access your portal",
                 font=FONT_BODY, bg=WHITE, fg=DARK_GRAY).pack(anchor="w", pady=(4, PAD))

        self.email_entry = make_form_field(form, "Email Address", placeholder="you@limkokwing.edu.sl")
        self.pass_entry  = make_form_field(form, "Password", placeholder="Enter your password", show="*")

        self.error_lbl = tk.Label(form, text="", font=FONT_SMALL, bg=WHITE, fg=DANGER)
        self.error_lbl.pack(anchor="w")

        make_button(form, "Sign In", self._handle_login, style="primary", width=30)\
            .pack(fill="x", pady=(PAD_SM, PAD))

        row = tk.Frame(form, bg=WHITE)
        row.pack()
        tk.Label(row, text="Don't have an account?", font=FONT_BODY,
                 bg=WHITE, fg=DARK_GRAY).pack(side="left")
        link = tk.Label(row, text="  Register Now", font=FONT_BODY_BOLD,
                        bg=WHITE, fg=NAVY, cursor="hand2")
        link.pack(side="left")
        link.bind("<Button-1>", lambda e: self.on_go_register())

        # Demo accounts hint
        hint = tk.Frame(form, bg=OFF_WHITE)
        hint.pack(fill="x", pady=(PAD, 0))
        tk.Label(hint, text="Demo accounts:", font=FONT_SMALL,
                 bg=OFF_WHITE, fg=DARK_GRAY).pack(anchor="w", padx=10, pady=(8, 0))
        for line in ["Admin: admin@limkokwing.edu.sl / admin123",
                     "Lecturer: lecturer@limkokwing.edu.sl / lecturer123",
                     "Student: mohamed@limkokwing.edu.sl / student123"]:
            tk.Label(hint, text=line, font=FONT_SMALL,
                     bg=OFF_WHITE, fg=MID_GRAY).pack(anchor="w", padx=10)
        tk.Label(hint, text="", bg=OFF_WHITE).pack(pady=2)

        tk.Frame(right, bg=WHITE).pack(expand=True)

    def _handle_login(self):
        email = self.email_entry.get_value()
        pwd   = self.pass_entry.get_value()

        if not email or not pwd:
            self.error_lbl.config(text="⚠  Please fill in all fields.")
            return

        result = login_user(email, pwd)
        if result["success"]:
            self.error_lbl.config(text="")
            self.on_login_success(result["user"])
        else:
            self.error_lbl.config(text=f"⚠  {result['error']}")


# ─────────────────────────────────────────────
# REGISTER SCREEN
# ─────────────────────────────────────────────
class RegisterScreen(tk.Frame):
    """Registration screen — students self-register; role fixed to student."""

    def __init__(self, parent, on_register_success, on_go_login):
        super().__init__(parent, bg=WHITE)
        self.on_register_success = on_register_success
        self.on_go_login         = on_go_login
        self._build()

    def _build(self):
        build_left_panel(
            self,
            headline="Join StudyTrack",
            tagline="Create your student account to register for courses and track your academic progress.",
            bullets=[
                "Quick course registration",
                "Real-time grade visibility",
                "Automatic GPA calculation",
            ]
        )

        right = tk.Frame(self, bg=WHITE)
        right.pack(side="right", fill="both", expand=True)
        tk.Frame(right, bg=WHITE).pack(expand=True)

        form = tk.Frame(right, bg=WHITE, padx=60)
        form.pack(fill="x")

        tk.Label(form, text="Create Student Account", font=FONT_HEADING1,
                 bg=WHITE, fg=TEXT_DARK).pack(anchor="w")
        tk.Label(form, text="Lecturer and Admin accounts are created by the Administrator",
                 font=FONT_BODY, bg=WHITE, fg=DARK_GRAY,
                 wraplength=360, justify="left").pack(anchor="w", pady=(4, PAD))

        self.name_entry  = make_form_field(form, "Full Name", placeholder="e.g. Aminata Bah")
        self.sid_entry   = make_form_field(form, "Student ID", placeholder="e.g. LK2026-004")
        self.email_entry = make_form_field(form, "Email Address", placeholder="you@limkokwing.edu.sl")
        self.pass_entry  = make_form_field(form, "Password", placeholder="Create a strong password", show="*")
        self.confirm_entry = make_form_field(form, "Confirm Password", placeholder="Re-enter your password", show="*")

        self.error_lbl = tk.Label(form, text="", font=FONT_SMALL, bg=WHITE, fg=DANGER)
        self.error_lbl.pack(anchor="w")

        make_button(form, "Create Account", self._handle_register, style="primary", width=30)\
            .pack(fill="x", pady=(PAD_SM, PAD))

        link_row = tk.Frame(form, bg=WHITE)
        link_row.pack()
        tk.Label(link_row, text="Already have an account?", font=FONT_BODY,
                 bg=WHITE, fg=DARK_GRAY).pack(side="left")
        link = tk.Label(link_row, text="  Sign In", font=FONT_BODY_BOLD,
                        bg=WHITE, fg=NAVY, cursor="hand2")
        link.pack(side="left")
        link.bind("<Button-1>", lambda e: self.on_go_login())

        tk.Frame(right, bg=WHITE).pack(expand=True)

    def _handle_register(self):
        name    = self.name_entry.get_value()
        sid     = self.sid_entry.get_value()
        email   = self.email_entry.get_value()
        pwd     = self.pass_entry.get_value()
        confirm = self.confirm_entry.get_value()

        if not all([name, sid, email, pwd, confirm]):
            self.error_lbl.config(text="⚠  Please fill in all fields.")
            return
        if pwd != confirm:
            self.error_lbl.config(text="⚠  Passwords do not match.")
            return

        result = register_user(name, email, pwd, "student", student_id=sid)
        if result["success"]:
            self.error_lbl.config(text="")
            self.on_register_success(result["user"])
        else:
            self.error_lbl.config(text=f"⚠  {result['error']}")

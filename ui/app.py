"""
app.py - StudyTrack Application Controller
Manages screen transitions: Login → Register → role-based Dashboard
"""

import tkinter as tk
from ui.theme import *
from logic.data_manager import seed_demo_data


class StudyTrackApp:
    """
    Root application controller.
    Manages which screen/frame is currently displayed and routes
    users to the correct dashboard based on their role.
    """

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("StudyTrack — Student Academic Portal")
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.minsize(900, 600)
        self.root.configure(bg=WHITE)

        self._centre_window()
        seed_demo_data()

        self.current_frame = None
        self._show_login()

    def _centre_window(self):
        """Centre the application window on the display."""
        self.root.update_idletasks()
        w, h = WINDOW_WIDTH, WINDOW_HEIGHT
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        x = (screen_w // 2) - (w // 2)
        y = (screen_h // 2) - (h // 2)
        self.root.geometry(f"{w}x{h}+{x}+{y}")

    # ─────────────────────────────────────────────
    # SCREEN SWITCHER
    # ─────────────────────────────────────────────
    def _switch_to(self, new_frame: tk.Frame):
        """Destroy the current screen and display new_frame instead."""
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = new_frame
        self.current_frame.pack(fill="both", expand=True)

    # ─────────────────────────────────────────────
    # NAVIGATION
    # ─────────────────────────────────────────────
    def _show_login(self):
        from ui.auth_screens import LoginScreen
        frame = LoginScreen(
            self.root,
            on_login_success=self._on_login_success,
            on_go_register=self._show_register,
        )
        self._switch_to(frame)

    def _show_register(self):
        from ui.auth_screens import RegisterScreen
        frame = RegisterScreen(
            self.root,
            on_register_success=self._on_login_success,
            on_go_login=self._show_login,
        )
        self._switch_to(frame)

    def _show_dashboard(self, user: dict):
        """Route the user to the correct dashboard based on their role."""
        role = user.get("role", "student")

        if role == "admin":
            from ui.admin_dashboard import AdminDashboard
            frame = AdminDashboard(self.root, user=user, on_logout=self._show_login)

        elif role == "lecturer":
            from ui.lecturer_dashboard import LecturerDashboard
            frame = LecturerDashboard(self.root, user=user, on_logout=self._show_login)

        else:  # student (default)
            from ui.student_dashboard import StudentDashboard
            frame = StudentDashboard(self.root, user=user, on_logout=self._show_login)

        self._switch_to(frame)

    # ─────────────────────────────────────────────
    # CALLBACKS
    # ─────────────────────────────────────────────
    def _on_login_success(self, user: dict):
        """Called after successful login or registration."""
        self._show_dashboard(user)

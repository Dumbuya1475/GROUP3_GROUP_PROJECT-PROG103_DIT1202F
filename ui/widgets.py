"""
widgets.py - Reusable GUI components for StudyTrack
"""

import tkinter as tk
from tkinter import ttk
from ui.theme import *


# ─────────────────────────────────────────────
# STYLED BUTTON
# ─────────────────────────────────────────────
def make_button(parent, text, command, style="primary", width=None):
    """
    Create a styled tkinter Button.

    style: 'primary' | 'secondary' | 'danger' | 'outline' | 'ghost' | 'success'
    """
    styles = {
        "primary":   {"bg": NAVY,    "fg": WHITE,    "activebackground": NAVY_DARK},
        "secondary": {"bg": GOLD,    "fg": NAVY,     "activebackground": GOLD_LIGHT},
        "danger":    {"bg": DANGER,  "fg": WHITE,    "activebackground": "#962b20"},
        "outline":   {"bg": WHITE,   "fg": NAVY,     "activebackground": LIGHT_GRAY},
        "ghost":     {"bg": BG_MAIN, "fg": TEXT_MID, "activebackground": LIGHT_GRAY},
        "success":   {"bg": SUCCESS, "fg": WHITE,    "activebackground": "#1e6b3f"},
    }
    s = styles.get(style, styles["primary"])
    kwargs = {
        "text": text, "command": command,
        "bg": s["bg"], "fg": s["fg"],
        "activebackground": s["activebackground"], "activeforeground": s["fg"],
        "font": FONT_BTN, "relief": "flat", "cursor": "hand2",
        "padx": 16, "pady": 8, "bd": 0,
    }
    if width:
        kwargs["width"] = width
    return tk.Button(parent, **kwargs)


# ─────────────────────────────────────────────
# STYLED ENTRY WITH PLACEHOLDER
# ─────────────────────────────────────────────
def make_entry(parent, placeholder="", show=None, width=30):
    """Create a bordered Entry widget with placeholder support. Returns (frame, entry)."""
    frame = tk.Frame(parent, bg=WHITE, highlightbackground=LIGHT_GRAY, highlightthickness=1)
    entry = tk.Entry(frame, font=FONT_BODY, bd=0, bg=WHITE,
                     fg=MID_GRAY if placeholder else TEXT_DARK,
                     insertbackground=NAVY, width=width)
    if show:
        entry.config(show=show)
    entry.pack(fill="x", padx=10, pady=8)

    if placeholder:
        entry.insert(0, placeholder)

        def on_in(e):
            if entry.get() == placeholder:
                entry.delete(0, "end")
                entry.config(fg=TEXT_DARK)
                if show:
                    entry.config(show=show)

        def on_out(e):
            if not entry.get():
                entry.config(fg=MID_GRAY, show="")
                entry.insert(0, placeholder)

        entry.bind("<FocusIn>", on_in)
        entry.bind("<FocusOut>", on_out)

    def get_value():
        val = entry.get()
        return "" if val == placeholder else val

    entry.get_value = get_value
    return frame, entry


def make_form_field(parent, label, placeholder="", show=None, width=35):
    """Labelled form field. Returns the Entry widget (with .get_value())."""
    tk.Label(parent, text=label, font=FONT_BODY_BOLD,
             bg=parent["bg"], fg=TEXT_DARK).pack(anchor="w", pady=(PAD_SM, 2))
    frame, entry = make_entry(parent, placeholder=placeholder, show=show, width=width)
    frame.pack(fill="x", pady=(0, PAD_SM))
    return entry


# ─────────────────────────────────────────────
# DROPDOWN (COMBOBOX)
# ─────────────────────────────────────────────
def make_dropdown(parent, label, values, width=33):
    """Labelled dropdown selector. Returns the ttk.Combobox widget."""
    tk.Label(parent, text=label, font=FONT_BODY_BOLD,
             bg=parent["bg"], fg=TEXT_DARK).pack(anchor="w", pady=(PAD_SM, 2))
    combo = ttk.Combobox(parent, values=values, font=FONT_BODY,
                         width=width, state="readonly")
    if values:
        combo.current(0)
    combo.pack(fill="x", pady=(0, PAD_SM))
    return combo


# ─────────────────────────────────────────────
# STAT CARD
# ─────────────────────────────────────────────
def make_stat_card(parent, icon, value, label, accent_color=NAVY):
    """Dashboard metric card with icon bubble, big value, and label."""
    card = tk.Frame(parent, bg=CARD_BG, highlightbackground=LIGHT_GRAY, highlightthickness=1)

    icon_frame = tk.Frame(card, bg=accent_color, width=44, height=44)
    icon_frame.pack_propagate(False)
    icon_frame.pack(anchor="w", padx=PAD, pady=(PAD, 4))
    tk.Label(icon_frame, text=icon, bg=accent_color, fg=WHITE,
             font=(FONT_FAMILY, 18)).pack(expand=True)

    tk.Label(card, text=str(value), font=FONT_STAT,
             bg=CARD_BG, fg=TEXT_DARK).pack(anchor="w", padx=PAD)
    tk.Label(card, text=label, font=FONT_LABEL,
             bg=CARD_BG, fg=DARK_GRAY).pack(anchor="w", padx=PAD, pady=(0, PAD))
    return card


# ─────────────────────────────────────────────
# BADGE
# ─────────────────────────────────────────────
def make_badge(parent, text, color=SUCCESS, text_color=WHITE):
    """Small coloured badge label."""
    return tk.Label(parent, text=text, font=FONT_SMALL,
                    bg=color, fg=text_color, padx=8, pady=2)


def grade_color(letter: str) -> str:
    """Return a colour associated with a letter grade."""
    mapping = {"A": SUCCESS, "B": BLUE, "C": ORANGE, "D": ORANGE, "F": DANGER}
    return mapping.get(letter, MID_GRAY)


# ─────────────────────────────────────────────
# SECTION HEADER
# ─────────────────────────────────────────────
def make_section_header(parent, title, link_text=None, link_cmd=None):
    """Section header row with optional right-aligned link."""
    row = tk.Frame(parent, bg=BG_MAIN)
    row.pack(fill="x", pady=(PAD, PAD_SM))
    tk.Label(row, text=title, font=FONT_HEADING2,
             bg=BG_MAIN, fg=TEXT_DARK).pack(side="left")
    if link_text and link_cmd:
        lbl = tk.Label(row, text=link_text, font=FONT_BODY,
                       bg=BG_MAIN, fg=NAVY, cursor="hand2")
        lbl.pack(side="right")
        lbl.bind("<Button-1>", lambda e: link_cmd())
    return row


# ─────────────────────────────────────────────
# DIVIDER
# ─────────────────────────────────────────────
def make_divider(parent):
    """Subtle horizontal divider line."""
    tk.Frame(parent, bg=LIGHT_GRAY, height=1).pack(fill="x", pady=PAD_SM)


# ─────────────────────────────────────────────
# SCROLLABLE FRAME
# ─────────────────────────────────────────────
def make_scrollable_frame(parent, bg=BG_MAIN):
    """Vertically scrollable container that stretches to fill the full width.

    Returns (outer_frame, inner_frame) — pack/grid content inside inner_frame.
    """
    outer = tk.Frame(parent, bg=bg)
    canvas = tk.Canvas(outer, bg=bg, highlightthickness=0, bd=0)
    scrollbar = ttk.Scrollbar(outer, orient="vertical", command=canvas.yview)
    inner = tk.Frame(canvas, bg=bg)

    # Keep track of the window ID so we can resize it to match canvas width
    inner_window_id = canvas.create_window((0, 0), window=inner, anchor="nw")

    def on_inner_configure(event):
        # Update scroll region whenever inner content changes size
        canvas.configure(scrollregion=canvas.bbox("all"))

    def on_canvas_configure(event):
        # Stretch the inner frame to always match the canvas's visible width
        canvas.itemconfig(inner_window_id, width=event.width)

    inner.bind("<Configure>", on_inner_configure)
    canvas.bind("<Configure>", on_canvas_configure)

    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    def on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    canvas.bind_all("<MouseWheel>", on_mousewheel)

    return outer, inner


# ─────────────────────────────────────────────
# SIMPLE TABLE (Treeview wrapper)
# ─────────────────────────────────────────────
def make_table(parent, columns, rows, col_widths=None):
    """
    Create a read-only table using ttk.Treeview.

    Parameters:
        columns    - list of column header strings
        rows       - list of tuples, one per row
        col_widths - optional list of pixel widths per column

    Returns:
        ttk.Treeview widget
    """
    style = ttk.Style()
    style.configure("Custom.Treeview", font=FONT_BODY, rowheight=28,
                    background=WHITE, fieldbackground=WHITE)
    style.configure("Custom.Treeview.Heading", font=FONT_BODY_BOLD,
                    background=NAVY, foreground=WHITE)

    tree = ttk.Treeview(parent, columns=columns, show="headings",
                        style="Custom.Treeview", height=min(len(rows), 12) or 1)
    for i, col in enumerate(columns):
        tree.heading(col, text=col)
        width = col_widths[i] if col_widths else 140
        tree.column(col, width=width, anchor="w")

    for row in rows:
        tree.insert("", "end", values=row)

    return tree

"""
theme.py - StudyTrack visual theme constants
Academic-feeling palette: deep navy, gold accent, clean whites.
"""
  
# ─────────────────────────────────────────────
# COLOUR PALETTE
# ─────────────────────────────────────────────
NAVY        = "#1B2A4A"
NAVY_DARK   = "#101A30"
GOLD        = "#D4A437"
GOLD_LIGHT  = "#E8C572"
GREEN       = "#2E8B57"
RED         = "#C0392B"
ORANGE      = "#E08E2A"
BLUE        = "#2E6FA8"
WHITE       = "#FFFFFF"
OFF_WHITE   = "#F6F7FA"
BG_MAIN     = "#EEF1F6"
LIGHT_GRAY  = "#E1E5EC"
MID_GRAY    = "#9AA5B1"
DARK_GRAY   = "#5A6472"
TEXT_DARK   = "#1C2333"
TEXT_MID    = "#3D4554"
CARD_BG     = "#FFFFFF"
DANGER      = "#C0392B"
SUCCESS     = "#2E8B57"

# ─────────────────────────────────────────────
# TYPOGRAPHY
# ─────────────────────────────────────────────
FONT_FAMILY    = "Segoe UI"
FONT_HEADING1  = (FONT_FAMILY, 24, "bold")
FONT_HEADING2  = (FONT_FAMILY, 18, "bold")
FONT_HEADING3  = (FONT_FAMILY, 14, "bold")
FONT_BODY      = (FONT_FAMILY, 11)
FONT_BODY_BOLD = (FONT_FAMILY, 11, "bold")
FONT_SMALL     = (FONT_FAMILY, 9)
FONT_LABEL     = (FONT_FAMILY, 10)
FONT_NAV       = (FONT_FAMILY, 11, "bold")
FONT_STAT      = (FONT_FAMILY, 28, "bold")
FONT_LOGO      = (FONT_FAMILY, 20, "bold")
FONT_BTN       = (FONT_FAMILY, 11, "bold")
FONT_MONO      = ("Consolas", 11)

# ─────────────────────────────────────────────
# DIMENSIONS
# ─────────────────────────────────────────────
WINDOW_WIDTH  = 1100
WINDOW_HEIGHT = 700
NAV_HEIGHT    = 60
PAD           = 20
PAD_SM        = 10
PAD_XS        = 6

# ─────────────────────────────────────────────
# GRADE SCALE (used by grading logic)
# ─────────────────────────────────────────────
# Tuples of (minimum_score, letter_grade, grade_point)
GRADE_SCALE = [
    (80, "A", 4.0),
    (70, "B", 3.0),
    (60, "C", 2.0),
    (50, "D", 1.0),
    (0,  "F", 0.0),
]

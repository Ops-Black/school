"""
نظام التصميم الاحترافي — محدّث
شريط جانبي بنفسجي داكن + محتوى أبيض + تحسينات UX
"""

# ══════════════════════════════════════════
# Palette — محدّث
# ═══════════════════════════════════════════
C = {
    # Sidebar (dark purple — Slack-style)
    "sb_bg":          "#3F0E40",
    "sb_header":      "#350D36",
    "sb_active_bg":   "#1164A3",
    "sb_active_txt":  "#FFFFFF",
    "sb_txt":         "#CFC3CF",
    "sb_muted":       "#9E849F",
    "sb_hover":       "rgba(255,255,255,0.10)",
    "sb_border":      "rgba(255,255,255,0.08)",
    "sb_accent":      "#F5A623",
    "sb_active_line": "#F5A623",  # ✨ الخط الجانبي للـ Active

    # Content (light)
    "bg_page":        "#F4F5F7",   # ✨ أخف قليلاً
    "bg_card":        "#FFFFFF",
    "bg_input":       "#FFFFFF",
    "bg_header":      "#F6F6F6",
    "bg_hover":       "#F2F7FC",

    # Borders — ✨ أخف
    "border":         "#E5E7EB",
    "border_light":   "#F0F0F0",
    "border_focus":   "#1264A3",

    # Text
    "text":           "#1D1C1D",
    "text_sec":       "#616061",
    "text_muted":     "#9CA3AF",
    "text_white":     "#FFFFFF",

    # Brand blue
    "primary":        "#1264A3",
    "primary_dk":     "#0B4D81",
    "primary_lt":     "#E8F5FA",
    "primary_text":   "#FFFFFF",

    # Semantic
    "success":        "#10B981",   # أخضر أوضح
    "success_lt":     "#D1FAE5",
    "success_text":   "#10B981",
    "danger":         "#EF4444",   # أحمر أوضح
    "danger_lt":      "#FEE2E2",
    "danger_text":    "#EF4444",
    "warning":        "#F59E0B",   # برتقالي أوضح
    "warning_lt":     "#FEF3C7",
    "warning_text":   "#F59E0B",

    #  ألوان أيقونات الإجراءات
    "action_view":    "#3B82F6",   # أزرق للعين
    "action_edit":    "#F59E0B",   # برتقالي للتعديل
    "action_delete":  "#EF4444",   # أحمر للحذف

    # ✨ ألوان أزرار التصدير
    "excel_bg":       "#107C41",
    "excel_fg":       "#FFFFFF",
    "word_bg":        "#2B579A",
    "word_fg":        "#FFFFFF",
    "scan_bg":        "#6B7280",
    "scan_fg":        "#FFFFFF",

    # ✨ زر إضافة طالب
    "add_bg":         "#10B981",
    "add_bg_hover":   "#059669",
    "add_fg":         "#FFFFFF",

    # Aliases (backward compat)
    "bg_sidebar":     "#3F0E40",
    "bg_sidebar2":    "#350D36",
    "bg_app":         "#350D36",
    "sidebar_text":   "#CFC3CF",
    "sidebar_muted":  "#9E849F",
    "sidebar_active": "#FFFFFF",
    "sidebar_border": "rgba(255,255,255,0.08)",
    "accent_gold":    "#F5A623",
    "accent":         "#F5A623",
    "accent_glow":    "rgba(245,166,35,0.15)",
    "border_dk":      "rgba(255,255,255,0.08)",
    "purple":         "#7C3AED",
    "purple_lt":      "#F5F3FF",
}

# ═══════════════════════════════════════════
# Main Stylesheet
# ══════════════════════════════════════════
MAIN_STYLE = f"""
/* ════════════════════════════════════════
   الخط — Cairo (عربي احترافي)
════════════════════════════════════════ */
* {{
    font-family: "Cairo", "Segoe UI", Tahoma, Arial;
    font-size: 13px;
}}

QWidget {{
    color: {C['text']};
    background-color: transparent;
}}

QMainWindow {{
    background-color: {C['bg_page']};
}}

QDialog {{
    background-color: {C['bg_card']};
    color: {C['text']};
}}

QLabel {{
    background: transparent;
    color: {C['text']};
}}

/* ════════════════════════════════════════
   SIDEBAR — مع خط جانبي للـ Active
════════════════════════════════════════ */
QWidget#sidebar {{
    background-color: {C['sb_bg']};
}}

QWidget#logo_area {{
    background-color: {C['sb_header']};
}}

QWidget#user_chip {{
    background-color: {C['sb_header']};
    border-top: 1px solid {C['sb_border']};
}}

QWidget#sidebar QLabel,
QWidget#logo_area QLabel,
QWidget#user_chip QLabel {{
    color: {C['sb_txt']};
    background: transparent;
}}

QLabel#school_badge {{
    color: {C['sb_accent']};
    background: rgba(245,166,35,0.12);
    border: 1px solid rgba(245,166,35,0.25);
    border-radius: 6px;
    padding: 5px 8px;
    font-size: 12px;
    font-weight: bold;
}}

QLabel#app_title {{
    color: {C['sb_muted']};
    font-size: 11px;
    background: transparent;
    letter-spacing: 0.5px;
}}

QLabel#nav_section {{
    color: {C['sb_muted']};
    font-size: 10px;
    font-weight: bold;
    padding: 12px 16px 4px;
    background: transparent;
    letter-spacing: 1.5px;
}}

/* ── Nav Buttons ── */
QPushButton#navBtn {{
    background-color: transparent;
    color: {C['sb_txt']};
    border: none;
    border-right: 3px solid transparent;
    border-radius: 4px;
    text-align: right;
    padding: 9px 14px 9px 11px;
    font-size: 13px;
    margin: 1px 6px;
}}

QPushButton#navBtn:hover {{
    background-color: {C['sb_hover']};
    color: #FFFFFF;
    border-right: 3px solid rgba(255,255,255,0.3);
}}

QPushButton#navBtn[active="true"] {{
    background-color: {C['sb_active_bg']};
    color: {C['sb_active_txt']};
    font-weight: bold;
    border-right: 3px solid {C['sb_active_line']};
    border-radius: 4px;
}}

/* ════════════════════════════════════════
   TOPBAR
════════════════════════════════════════ */
QFrame#topbar {{
    background-color: {C['bg_card']};
    border-bottom: 1px solid {C['border_light']};
}}

QFrame#topbar QLabel {{
    color: {C['text']};
    background: transparent;
}}

QLabel#page_title {{
    font-size: 18px;
    font-weight: bold;
    color: {C['text']};
    background: transparent;
}}

QFrame#search_wrap {{
    background-color: {C['bg_input']};
    border: 1px solid {C['border']};
    border-radius: 8px;
}}

QLineEdit#search_input {{
    background: transparent;
    border: none;
    color: {C['text']};
    font-size: 13px;
    padding: 7px 10px;
}}

QLineEdit#search_input::placeholder {{
    color: {C['text_muted']};
    font-style: italic;
}}

QPushButton#iconBtn {{
    background-color: transparent;
    border: 1px solid {C['border']};
    border-radius: 8px;
    color: {C['text_sec']};
    font-size: 14px;
    min-width: 36px;
    min-height: 34px;
    padding: 2px 8px;
}}

QPushButton#iconBtn:hover {{
    background-color: {C['bg_hover']};
    color: {C['text']};
    border-color: {C['text_sec']};
}}

/* ═══════════════════════════════════════
   CONTENT
════════════════════════════════════════ */
QWidget#content_area {{
    background-color: {C['bg_page']};
}}

QStackedWidget {{
    background-color: {C['bg_page']};
}}

QScrollArea {{
    background: transparent;
    border: none;
}}

QScrollArea > QWidget > QWidget {{
    background: transparent;
}}

/* ════════════════════════════════════════
   CARDS — حدود أخف
════════════════════════════════════════ */
QFrame#card {{
    background-color: {C['bg_card']};
    border: 1px solid {C['border_light']};
    border-radius: 10px;
    color: {C['text']};
}}

QFrame#card QLabel {{
    color: {C['text']};
    background: transparent;
}}

QFrame#kpi_card {{
    background-color: {C['bg_card']};
    border: 1px solid {C['border_light']};
    border-radius: 10px;
    color: {C['text']};
}}

QFrame#kpi_card QLabel {{
    color: {C['text']};
    background: transparent;
}}

QLabel#section_title {{
    font-size: 15px;
    font-weight: bold;
    color: {C['text']};
    background: transparent;
}}

QLabel#muted {{
    color: {C['text_muted']};
    background: transparent;
}}

/* ════════════════════════════════════════
   TABLE
════════════════════════════════════════ */
QTableWidget {{
    background-color: {C['bg_card']};
    color: {C['text']};
    border: 1px solid {C['border_light']};
    border-radius: 10px;
    gridline-color: {C['border_light']};
    outline: 0;
    alternate-background-color: #FAFBFC;
    selection-background-color: {C['primary_lt']};
    selection-color: {C['primary']};
}}

QTableWidget::item {{
    padding: 10px 14px;
    color: {C['text']};
    background-color: transparent;
    border-bottom: 1px solid {C['border_light']};
}}

QTableWidget::item:hover {{
    background-color: {C['bg_hover']};
}}

QTableWidget::item:selected {{
    background-color: {C['primary_lt']};
    color: {C['primary']};
}}

QHeaderView::section {{
    background-color: #FAFBFC;
    color: {C['text_sec']};
    font-weight: bold;
    font-size: 11px;
    padding: 10px 14px;
    border: none;
    border-bottom: 2px solid {C['border']};
    letter-spacing: 0.5px;
}}

QHeaderView::section:first {{
    border-top-right-radius: 10px;
}}

QHeaderView::section:last {{
    border-top-left-radius: 10px;
}}

QTableCornerButton::section {{
    background: #FAFBFC;
    border: none;
}}

/* ════════════════════════════════════════
   BUTTONS
════════════════════════════════════════ */

/* زر إضافة طالب — أخضر واضح */
QPushButton#addStudentBtn {{
    background-color: {C['add_bg']};
    color: {C['add_fg']};
    border: none;
    border-radius: 8px;
    padding: 0 22px;
    font-weight: bold;
    font-size: 14px;
    min-height: 40px;
}}

QPushButton#addStudentBtn:hover {{
    background-color: {C['add_bg_hover']};
    color: #FFFFFF;
}}

QPushButton#addStudentBtn:pressed {{
    background-color: #047857;
    color: #FFFFFF;
}}

/* أزرار التصدير */
QPushButton#excelBtn {{
    background-color: {C['excel_bg']};
    color: {C['excel_fg']};
    border: none;
    border-radius: 8px;
    padding: 0 18px;
    font-weight: bold;
    font-size: 13px;
    min-height: 38px;
}}

QPushButton#excelBtn:hover {{
    background-color: #0D6B37;
}}

QPushButton#wordBtn {{
    background-color: {C['word_bg']};
    color: {C['word_fg']};
    border: none;
    border-radius: 8px;
    padding: 0 18px;
    font-weight: bold;
    font-size: 13px;
    min-height: 38px;
}}

QPushButton#wordBtn:hover {{
    background-color: #1E4478;
}}

QPushButton#scanBtn {{
    background-color: {C['scan_bg']};
    color: {C['scan_fg']};
    border: none;
    border-radius: 8px;
    padding: 0 18px;
    font-weight: bold;
    font-size: 13px;
    min-height: 38px;
}}

QPushButton#scanBtn:hover {{
    background-color: #4B5563;
}}

/* Primary Button */
QPushButton#primaryBtn {{
    background-color: {C['primary']};
    color: #FFFFFF;
    border: none;
    border-radius: 8px;
    padding: 0 20px;
    font-weight: bold;
    min-height: 38px;
    font-size: 13px;
}}

QPushButton#primaryBtn:hover {{
    background-color: {C['primary_dk']};
}}

QPushButton#primaryBtn:pressed {{
    background-color: #083F6B;
}}

QPushButton#primaryBtn:disabled {{
    background-color: {C['border']};
    color: {C['text_muted']};
}}

QPushButton#accentBtn {{
    background-color: {C['sb_accent']};
    color: #1D1C1D;
    border: none;
    border-radius: 8px;
    padding: 0 18px;
    font-weight: bold;
    min-height: 38px;
}}

QPushButton#accentBtn:hover {{
    background-color: #E09A1A;
}}

QPushButton#ghostBtn {{
    background-color: {C['bg_card']};
    color: {C['text']};
    border: 1px solid {C['border']};
    border-radius: 8px;
    padding: 0 16px;
    min-height: 38px;
}}

QPushButton#ghostBtn:hover {{
    background-color: {C['bg_header']};
    border-color: {C['text_sec']};
}}

QPushButton#dangerBtn {{
    background-color: {C['bg_card']};
    color: {C['danger']};
    border: 1px solid {C['border']};
    border-radius: 8px;
    padding: 0 14px;
    min-height: 36px;
}}

QPushButton#dangerBtn:hover {{
    background-color: {C['danger_lt']};
    border-color: {C['danger']};
}}

/* أيقونات الإجراءات — ملونة */
QPushButton#viewBtn {{
    background-color: transparent;
    color: {C['action_view']};
    border: 1px solid rgba(59,130,246,0.2);
    border-radius: 6px;
    padding: 4px 10px;
    min-width: 32px;
    min-height: 30px;
}}

QPushButton#viewBtn:hover {{
    background-color: rgba(59,130,246,0.1);
    border-color: {C['action_view']};
}}

QPushButton#editBtn {{
    background-color: transparent;
    color: {C['action_edit']};
    border: 1px solid rgba(245,158,11,0.2);
    border-radius: 6px;
    padding: 4px 10px;
    min-width: 32px;
    min-height: 30px;
}}

QPushButton#editBtn:hover {{
    background-color: rgba(245,158,11,0.1);
    border-color: {C['action_edit']};
}}

QPushButton#deleteBtn {{
    background-color: transparent;
    color: {C['action_delete']};
    border: 1px solid rgba(239,68,68,0.2);
    border-radius: 6px;
    padding: 4px 10px;
    min-width: 32px;
    min-height: 30px;
}}

QPushButton#deleteBtn:hover {{
    background-color: {C['danger_lt']};
    border-color: {C['action_delete']};
}}

/* ════════════════════════════════════════
   INPUTS
════════════════════════════════════════ */
QLineEdit, QTextEdit, QSpinBox, QDoubleSpinBox, QDateEdit {{
    background-color: {C['bg_card']};
    color: {C['text']};
    border: 1px solid {C['border']};
    border-radius: 8px;
    padding: 8px 12px;
    font-size: 13px;
    selection-background-color: {C['primary']};
    selection-color: white;
}}

QLineEdit:focus, QTextEdit:focus, QSpinBox:focus,
QDoubleSpinBox:focus, QDateEdit:focus {{
    border: 2px solid {C['border_focus']};
    padding: 7px 11px;
}}

QLineEdit:hover, QSpinBox:hover, QDoubleSpinBox:hover {{
    border-color: {C['text_sec']};
}}

QLineEdit::placeholder {{
    color: {C['text_muted']};
}}

QSpinBox::up-button, QSpinBox::down-button,
QDoubleSpinBox::up-button, QDoubleSpinBox::down-button {{
    border: none;
    width: 20px;
}}

QDateEdit::drop-down {{
    border: none;
    width: 26px;
}}

/* ─ ComboBox ── */
QComboBox {{
    background-color: {C['bg_card']};
    color: {C['text']};
    border: 1px solid {C['border']};
    border-radius: 8px;
    padding: 8px 12px;
    font-size: 13px;
}}

QComboBox:focus {{
    border: 2px solid {C['border_focus']};
    padding: 7px 11px;
}}

QComboBox:hover {{
    border-color: {C['text_sec']};
}}

QComboBox::drop-down {{
    border: none;
    width: 26px;
}}

QComboBox QAbstractItemView {{
    background-color: {C['bg_card']};
    color: {C['text']};
    border: 1px solid {C['border']};
    border-radius: 8px;
    padding: 4px;
    outline: 0;
}}

QComboBox QAbstractItemView::item {{
    color: {C['text']};
    background-color: transparent;
    padding: 8px 12px;
    min-height: 28px;
    border-radius: 4px;
}}

QComboBox QAbstractItemView::item:hover,
QComboBox QAbstractItemView::item:selected {{
    background-color: {C['primary_lt']};
    color: {C['primary']};
}}

/* ═══════════════════════════════════════
   TABS
════════════════════════════════════════ */
QTabWidget::pane {{
    background-color: {C['bg_card']};
    border: 1px solid {C['border_light']};
    border-radius: 10px;
    top: -1px;
}}

QTabWidget QWidget {{
    color: {C['text']};
}}

QTabWidget QLabel {{
    color: {C['text']};
    background: transparent;
}}

QTabBar::tab {{
    background: transparent;
    color: {C['text_sec']};
    border: none;
    border-bottom: 2px solid transparent;
    padding: 10px 18px;
    font-size: 13px;
}}

QTabBar::tab:selected {{
    color: {C['primary']};
    border-bottom: 2px solid {C['primary']};
    font-weight: bold;
}}

QTabBar::tab:hover:!selected {{
    color: {C['text']};
    border-bottom: 2px solid {C['border']};
}}

/* ════════════════════════════════════════
   SCROLLBAR
════════════════════════════════════════ */
QScrollBar:vertical {{
    width: 6px;
    background: transparent;
    margin: 2px 0;
}}

QScrollBar::handle:vertical {{
    background: #D0D0D0;
    border-radius: 3px;
    min-height: 28px;
}}

QScrollBar::handle:vertical:hover {{
    background: #ABABAB;
}}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0;
}}

QScrollBar:horizontal {{
    height: 6px;
    background: transparent;
    margin: 0 2px;
}}

QScrollBar::handle:horizontal {{
    background: #D0D0D0;
    border-radius: 3px;
    min-width: 28px;
}}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
    width: 0;
}}

/* ════════════════════════════════════════
   CHECKBOX
════════════════════════════════════════ */
QCheckBox {{
    color: {C['text']};
    font-size: 13px;
    spacing: 8px;
    background: transparent;
}}

QCheckBox::indicator {{
    width: 16px;
    height: 16px;
    border: 1.5px solid {C['border']};
    border-radius: 4px;
    background-color: {C['bg_card']};
}}

QCheckBox::indicator:hover {{
    border-color: {C['primary']};
}}

QCheckBox::indicator:checked {{
    background-color: {C['primary']};
    border-color: {C['primary']};
}}

/* ════════════════════════════════════════
   LIST WIDGET
════════════════════════════════════════ */
QListWidget {{
    background-color: {C['bg_card']};
    color: {C['text']};
    border: 1px solid {C['border_light']};
    border-radius: 10px;
    outline: 0;
    padding: 4px;
}}

QListWidget::item {{
    color: {C['text']};
    background: transparent;
    padding: 9px 12px;
    border-radius: 6px;
}}

QListWidget::item:hover {{
    background-color: {C['bg_header']};
}}

QListWidget::item:selected {{
    background-color: {C['primary_lt']};
    color: {C['primary']};
    font-weight: bold;
}}

/* ════════════════════════════════════════
   DIALOGS
════════════════════════════════════════ */
QMessageBox {{
    background-color: {C['bg_card']};
    color: {C['text']};
}}

QMessageBox QLabel {{
    color: {C['text']};
    background: transparent;
    min-width: 280px;
}}

QMessageBox QPushButton {{
    background-color: {C['primary']};
    color: white;
    border: none;
    border-radius: 6px;
    padding: 6px 20px;
    font-weight: bold;
    min-width: 80px;
    min-height: 32px;
}}

QMessageBox QPushButton:hover {{
    background-color: {C['primary_dk']};
}}

QDialogButtonBox QPushButton {{
    background-color: {C['bg_header']};
    color: {C['text']};
    border: 1px solid {C['border']};
    border-radius: 6px;
    padding: 0 16px;
    min-height: 34px;
    min-width: 80px;
    font-size: 13px;
}}

QDialogButtonBox QPushButton:hover {{
    background-color: {C['border']};
}}

QInputDialog {{
    background-color: {C['bg_card']};
    color: {C['text']};
}}

QInputDialog QLabel {{
    color: {C['text']};
    background: transparent;
}}

/* ════════════════════════════════════════
   PROGRESSBAR
════════════════════════════════════════ */
QProgressBar {{
    background-color: {C['bg_header']};
    border: none;
    border-radius: 4px;
    min-height: 6px;
    max-height: 6px;
    color: transparent;
}}

QProgressBar::chunk {{
    background-color: {C['primary']};
    border-radius: 4px;
}}

QProgressDialog {{
    background-color: {C['bg_card']};
    color: {C['text']};
}}

QProgressDialog QLabel {{
    color: {C['text']};
    background: transparent;
}}

/* ════════════════════════════════════════
   TOOLTIP
════════════════════════════════════════ */
QToolTip {{
    background-color: #1D1C1D;
    color: white;
    border: none;
    border-radius: 6px;
    padding: 6px 10px;
    font-size: 12px;
}}

/* ════════════════════════════════════════
   CALENDAR
════════════════════════════════════════ */
QCalendarWidget {{
    background-color: {C['bg_card']};
    color: {C['text']};
}}

QCalendarWidget QAbstractItemView {{
    background-color: {C['bg_card']};
    color: {C['text']};
    selection-background-color: {C['primary']};
    selection-color: white;
}}

QCalendarWidget QToolButton {{
    color: {C['text']};
    background: transparent;
    border: none;
    padding: 4px;
}}

QCalendarWidget QMenu {{
    background-color: {C['bg_card']};
    color: {C['text']};
}}
"""
"""
النافذة الرئيسية — شريط جانبي احترافي
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from ui.style import MAIN_STYLE, C
import core.db as DB

ROLE_PAGES = {
    "مدير":     ["dashboard", "students", "fees", "attendance", "grades", "teachers", "parents", "accounting", "calendar", "reports", "audit", "settings"],
    "محاسب":    ["dashboard", "fees", "accounting", "reports"],
    "معلم":     ["dashboard", "attendance", "grades"],
    "موظف":     ["dashboard", "students"],
    "سكرتيرة":  ["dashboard", "students", "attendance"],
}

NAV = [
    ("MAIN", None, None),
    ("dashboard",    "لوحة التحكم",     "🏠"),
    ("students",     "الطلاب",           "👨🎓"),
    ("fees",         "الأقساط",          "💰"),
    ("attendance",   "الغياب",           ""),
    ("grades",       "الدرجات",          "📊"),
    ("teachers",     "المدرسون",         "👩‍🏫"),
    ("parents",      "أولياء الأمور",   "👪"),
    ("MANAGE", None, None),
    ("accounting",   "المحاسبة",         "🧾"),
    ("calendar",     "التقويم",          "🗓️"),
    ("reports",      "التقارير",         "📈"),
    ("audit",        "سجل العمليات",     "🔍"),
    ("settings",     "الإعدادات",        "️"),
]

TITLES = {
    "dashboard": "لوحة التحكم", "students": "الطلاب", "fees": "الأقساط والمدفوعات",
    "attendance": "سجل الغياب", "grades": "الدرجات والنتائج", "teachers": "المدرسون",
    "parents": "أولياء الأمور", "accounting": "المحاسبة", "calendar": "التقويم المدرسي",
    "reports": "التقارير", "audit": "سجل العمليات", "settings": "الإعدادات",
}

class MainWindow(QMainWindow):
    def __init__(self, school_id, user_info):
        super().__init__()
        self.school_id  = school_id
        self.user_info  = user_info
        self.role       = user_info["role"]
        self.perms      = ROLE_PAGES.get(self.role, ["dashboard"])
        school          = dict(DB.get_school(school_id) or {})
        self.school_name = school.get("name", "المدرسة")
        self.setWindowTitle(f"نظام إدارة المدرسة — {self.school_name}")
        self.setMinimumSize(1140, 720)
        self.resize(1360, 820)
        self.setLayoutDirection(Qt.RightToLeft)
        self.setStyleSheet(MAIN_STYLE)
        self._build()
        self.show_page("dashboard")
        QTimer.singleShot(5000, self._tick_notif)
        self._timer = QTimer(self); self._timer.timeout.connect(self._tick_notif); self._timer.start(30_000)

    # ─── BUILD ──────────────────────────────────────────────
    def _build(self):
        central = QWidget(); self.setCentralWidget(central)
        root = QHBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)
        root.addWidget(self._make_sidebar())

        right = QWidget(); right.setObjectName("content_area")
        rl = QVBoxLayout(right); rl.setContentsMargins(0, 0, 0, 0); rl.setSpacing(0)
        rl.addWidget(self._make_topbar())
        self.stack = QStackedWidget()
        self.stack.setStyleSheet(f"background: {C['bg_page']};")
        rl.addWidget(self.stack)
        root.addWidget(right)
        self._init_pages()

    def _make_sidebar(self):
        sb = QWidget(); sb.setObjectName("sidebar"); sb.setFixedWidth(195)
        outer = QVBoxLayout(sb); outer.setContentsMargins(0,0,0,0); outer.setSpacing(0)

        # Logo area
        logo_area = QWidget(); logo_area.setObjectName("logo_area")
        logo_area.setStyleSheet(f"background: {C['bg_app']}; border-bottom: 1px solid {C['border_dk']};")
        la = QVBoxLayout(logo_area); la.setContentsMargins(14,16,14,14); la.setSpacing(6)

        badge_lbl = QLabel(f"    {self.school_name}  ")
        badge_lbl.setObjectName("school_badge")
        badge_lbl.setWordWrap(True)
        la.addWidget(badge_lbl)

        app_title = QLabel("نظام إدارة المدرسة")
        app_title.setObjectName("app_title")
        la.addWidget(app_title)
        outer.addWidget(logo_area)

        # Nav
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; } QWidget { background: transparent; }")
        nav_w = QWidget(); nav_w.setStyleSheet("background: transparent;")
        nav_lay = QVBoxLayout(nav_w); nav_lay.setContentsMargins(0,8,0,8); nav_lay.setSpacing(1)

        self.nav_btns = {}
        for key, label, icon in NAV:
            if label is None:
                sec = QLabel(key)
                sec.setObjectName("nav_section")
                nav_lay.addWidget(sec)
                continue
            if key not in self.perms:
                continue
            btn = QPushButton(f"  {icon}   {label}")
            btn.setObjectName("navBtn")
            btn.setFixedHeight(40)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setProperty("active", "false")  # ✨ خاصية active
            btn.clicked.connect(lambda _, k=key: self.show_page(k))
            nav_lay.addWidget(btn)
            self.nav_btns[key] = btn

        nav_lay.addStretch()
        scroll.setWidget(nav_w)
        outer.addWidget(scroll)

        # User chip
        chip = QWidget(); chip.setObjectName("user_chip")
        chip.setStyleSheet(f"background: rgba(255,255,255,0.03); border-top: 1px solid {C['border_dk']};")
        chip.setFixedHeight(62)
        cl = QHBoxLayout(chip); cl.setContentsMargins(14,10,14,10); cl.setSpacing(10)

        av_letter = (user_info_name := self.user_info.get("full_name", "م"))[0]
        avatar = QLabel(av_letter); avatar.setFixedSize(36,36); avatar.setAlignment(Qt.AlignCenter)
        avatar.setStyleSheet(f"background: {C['accent']}; color: #1F2328; border-radius: 18px; font-weight: bold; font-size: 15px;")

        info = QVBoxLayout(); info.setSpacing(1)
        name_lbl = QLabel(self.user_info.get("full_name", "مستخدم"))
        name_lbl.setStyleSheet(f"color: #EAECF5; font-size: 12px; font-weight: bold; background: transparent;")
        role_lbl = QLabel(self.role)
        role_lbl.setStyleSheet(f"color: #F5A623; font-size: 10px; background: transparent;")
        info.addWidget(name_lbl); info.addWidget(role_lbl)

        logout_btn = QPushButton("↩"); logout_btn.setObjectName("iconBtn"); logout_btn.setFixedSize(28,28)
        logout_btn.setToolTip("تسجيل الخروج"); logout_btn.setCursor(Qt.PointingHandCursor)
        logout_btn.setStyleSheet(f"background: rgba(255,255,255,0.06); border: 1px solid {C['border_dk']}; border-radius:6px; color:#7B82A0; font-size:14px;")
        logout_btn.clicked.connect(self.close)

        cl.addWidget(avatar); cl.addLayout(info); cl.addStretch(); cl.addWidget(logout_btn)
        outer.addWidget(chip)
        return sb

    def _make_topbar(self):
        tb = QFrame(); tb.setObjectName("topbar"); tb.setFixedHeight(56)
        lay = QHBoxLayout(tb); lay.setContentsMargins(24,0,20,0); lay.setSpacing(12)

        self.page_title_lbl = QLabel("لوحة التحكم"); self.page_title_lbl.setObjectName("page_title")
        lay.addWidget(self.page_title_lbl)
        lay.addStretch()

        # Search
        sw = QFrame(); sw.setObjectName("search_wrap"); sw.setFixedHeight(36); sw.setFixedWidth(280)
        sl = QHBoxLayout(sw); sl.setContentsMargins(10,0,10,0); sl.setSpacing(6)
        search_icon = QLabel("🔍"); search_icon.setStyleSheet("font-size:14px; color:#8B949E; background:transparent;")
        self.search_inp = QLineEdit(); self.search_inp.setObjectName("search_input")
        self.search_inp.setPlaceholderText("ابحث بالاسم أو رقم الطالب...")  # ✨ Placeholder أوضح
        self.search_inp.textChanged.connect(self._on_search)
        sl.addWidget(search_icon); sl.addWidget(self.search_inp)
        lay.addWidget(sw)

        # Dark mode toggle
        self.dark_btn = QPushButton("🌙"); self.dark_btn.setObjectName("iconBtn")
        self.dark_btn.setFixedSize(36,36); self.dark_btn.setToolTip("الوضع الليلي / النهاري")
        self.dark_btn.setCursor(Qt.PointingHandCursor)
        self.dark_btn.clicked.connect(self._toggle_dark)
        lay.addWidget(self.dark_btn)

        # Notif bell
        self.notif_btn = QPushButton(""); self.notif_btn.setObjectName("iconBtn")
        self.notif_btn.setFixedSize(36,36); self.notif_btn.setToolTip("الإشعارات")
        self.notif_btn.setCursor(Qt.PointingHandCursor)
        self.notif_btn.clicked.connect(self._show_notifs)
        lay.addWidget(self.notif_btn)
        return tb

    def _init_pages(self):
        from ui.pages import (DashboardPage, StudentsPage, FeesPage, AttendancePage,
                               GradesPage, TeachersPage, ParentsPage, AccountingPage,
                                CalendarPage, ReportsPage, AuditPage, SettingsPage)
        mp = {"dashboard":DashboardPage, "students":StudentsPage, "fees":FeesPage,
               "attendance":AttendancePage, "grades":GradesPage, "teachers":TeachersPage,
               "parents":ParentsPage, "accounting":AccountingPage, "calendar":CalendarPage,
               "reports":ReportsPage, "audit":AuditPage, "settings":SettingsPage}
        self.pages = {}
        for key, Cls in mp.items():
            if key not in self.perms: continue
            page = Cls(self.school_id, self.user_info)
            self.stack.addWidget(page)
            self.pages[key] = (page, TITLES.get(key, key))

    def show_page(self, key):
        if key not in self.pages: return
        page, title = self.pages[key]
        self.stack.setCurrentWidget(page)
        self.page_title_lbl.setText(title)
        page.refresh()
        # ✨ تحديث الـ active state مع خط جانبي
        for k, btn in self.nav_btns.items():
            active = "true" if k == key else "false"
            btn.setProperty("active", active)
            btn.style().unpolish(btn); btn.style().polish(btn)

    def _current_key(self):
        for k, (p, _) in self.pages.items():
            if self.stack.currentWidget() is p:  return k
        return ""

    def _on_search(self, text):
        if self._current_key() == "students" and "students" in self.pages:
            self.pages["students"][0].refresh(text)

    def _tick_notif(self):
        try:
            cnt = DB.get_stats(self.school_id)["notifications"]
            self.notif_btn.setText(f"🔔 {cnt}" if cnt > 0 else "🔔")
        except Exception: pass

    def _toggle_dark(self):
        """تبديل بين الوضع الليلي والنهاري"""
        self._dark_mode = not getattr(self, "_dark_mode", False)
        if self._dark_mode:
            dark_ss = """
{ font-family: Tahoma, Arial; font-size: 13px; }
QWidget { color: #E0E0E0; }
QMainWindow, QDialog { background-color: #1A1A2E; }
QFrame#topbar { background-color: #16213E; border-bottom: 2px solid #0F3460; }
QFrame#topbar QLabel { color: #E0E0E0; background: transparent; }
QLabel#page_title { color: #E0E0E0; font-size:17px; font-weight:bold; background:transparent; }
QLabel { color: #E0E0E0; background: transparent; }
QWidget#content_area { background-color: #1A1A2E; }
QFrame#card, QFrame#kpi_card { background-color: #16213E; border-color: #0F3460; color:#E0E0E0; }
QFrame#card QLabel, QFrame#kpi_card QLabel { color: #E0E0E0; background:transparent; }
QTableWidget { background-color: #16213E; color: #E0E0E0; border-color: #0F3460; }
QTableWidget::item { color: #E0E0E0; background-color: #16213E; border-bottom: 1px solid #0F3460; }
QTableWidget::item:selected { background-color: #0F3460; color: #90CAF9; }
QTableWidget::item:hover { background-color: #0D2B4E; color: #E0E0E0; }
QHeaderView::section { background-color: #0F3460; color: #90CAF9; border-bottom: 2px solid #1565C0; }
QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox, QDateEdit, QTextEdit { background-color: #0F3460; color: #E0E0E0; border: 1.5px solid #1565C0; border-radius:8px; padding:8px 12px; }
QComboBox QAbstractItemView { background-color: #0F3460; color: #E0E0E0; }
QComboBox QAbstractItemView::item { color: #E0E0E0; }
QPushButton#primaryBtn { background-color: #1565C0; color: white; border:none; border-radius:8px; padding:0 20px; font-weight:bold; min-height:38px; }
QPushButton#ghostBtn { background-color: #0F3460; color: #E0E0E0; border: 1.5px solid #1565C0; border-radius:8px; padding:0 16px; min-height:36px; }
QPushButton#iconBtn { background-color: #0F3460; border: 1.5px solid #1565C0; border-radius:6px; color:#90CAF9; min-width:34px; min-height:32px; padding:2px 8px; }
QTabWidget::pane { background-color: #16213E; border-color: #0F3460; }
QTabBar::tab { color: #90CAF9; background:transparent; border:none; border-bottom:2px solid transparent; padding:10px 20px; }
QTabBar::tab:selected { color: #42A5F5; border-bottom:2px solid #42A5F5; font-weight:bold; }
QMessageBox { background-color: #16213E; color:#E0E0E0; }
QMessageBox QLabel { color: #E0E0E0; background:transparent; }
QWidget#sidebar { background-color: #0D1117; }
QPushButton#navBtn { color: #9CA3B4; background:transparent; border:none; border-radius:8px; padding:10px 14px; margin:1px 8px; }
QPushButton#navBtn:hover { background-color: rgba(255,255,255,0.08); color: white; }
QPushButton#navBtn[active=true] { background-color: rgba(74,108,247,0.25); color:#A5B4FC; font-weight:bold; border-right:3px solid #4A6CF7; border-radius:0 8px 8px 0; }
QScrollArea { background: transparent; border: none; }
QScrollBar:vertical { width:8px; background:transparent; }
QScrollBar::handle:vertical { background:#1565C0; border-radius:4px; min-height:30px; }
QListWidget { background-color: #16213E; color:#E0E0E0; border:1.5px solid #0F3460; border-radius:10px; }
QListWidget::item { color:#E0E0E0; }
QListWidget::item:hover { background-color: #0D2B4E; }
QListWidget::item:selected { background-color: #0F3460; color:#90CAF9; }
"""
            QApplication.instance().setStyleSheet(dark_ss)
            self.dark_btn.setText("☀️")
            self.dark_btn.setToolTip("الوضع النهاري")
        else:
            from ui.style import MAIN_STYLE
            QApplication.instance().setStyleSheet(MAIN_STYLE)
            self.dark_btn.setText("")
            self.dark_btn.setToolTip("الوضع الليلي")

    def _show_notifs(self):
        notifs = DB.get_notifications(self.school_id)
        dlg = QDialog(self); dlg.setWindowTitle("الإشعارات"); dlg.setFixedSize(480, 440)
        dlg.setLayoutDirection(Qt.RightToLeft); dlg.setStyleSheet(MAIN_STYLE)
        lay = QVBoxLayout(dlg); lay.setContentsMargins(24,20,24,20); lay.setSpacing(12)
        hdr = QLabel(f"🔔  الإشعارات ({len(notifs)})")
        hdr.setStyleSheet("font-size: 15px; font-weight: bold;")
        lay.addWidget(hdr)

        scroll = QScrollArea(); scroll.setWidgetResizable(True); scroll.setStyleSheet("border:none;")
        inner = QWidget(); il = QVBoxLayout(inner); il.setContentsMargins(0,0,0,0); il.setSpacing(8)

        if not notifs:
            empty = QLabel("✅  لا توجد إشعارات جديدة")
            empty.setAlignment(Qt.AlignCenter)
            empty.setStyleSheet(f"color: {C['text_muted']}; padding: 20px;")
            il.addWidget(empty)

        for n in notifs:
            n = dict(n)
            card = QFrame()
            is_fee = "قسط" in (n.get("type") or "")
            bg = C['warning_lt'] if is_fee else C['primary_lt']
            border = C['warning'] if is_fee else C['primary']
            card.setStyleSheet(f"background: {bg}; border-radius: 10px; border-right: 3px solid {border};")
            cl = QHBoxLayout(card); cl.setContentsMargins(14,10,14,10)
            icon = "⚠️" if is_fee else "📅"
            msg = QLabel(f"  {icon}  {n.get('message','')}")
            msg.setWordWrap(True)
            msg.setStyleSheet(f"color: {C['text']}; background: transparent;")
            cl.addWidget(msg)
            il.addWidget(card)

        il.addStretch(); scroll.setWidget(inner); lay.addWidget(scroll)

        close_btn = QPushButton("✅  تم الاطلاع"); close_btn.setObjectName("primaryBtn")
        close_btn.clicked.connect(lambda: (DB.mark_read(self.school_id), dlg.accept(), self._tick_notif()))
        lay.addWidget(close_btn)
        dlg.exec()
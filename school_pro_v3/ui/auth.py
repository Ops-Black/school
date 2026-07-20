"""
شاشات: التفعيل، اختيار المدرسة، تسجيل الدخول
- إصلاح sqlite3.Row → dict
- تصميم احترافي بدون Segoe UI
- نص مرئي في كل الحالات
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from core.license import is_activated, activate, machine_id_display
import core.db as DB
from ui.style import MAIN_STYLE, C

# ─── Shared dark-screen stylesheet ─────────────────────────
DARK_SS = """
QWidget, QDialog { background: #0D1117; color: #E6EDF3; }
QLabel { color: #E6EDF3; background: transparent; }
QLineEdit {
    background: #161B22;
    color: #E6EDF3;
    border: 1px solid #30363D;
    border-radius: 8px;
    padding: 10px 14px;
    font-size: 14px;
    selection-background-color: #0969DA;
    selection-color: white;
}
QLineEdit:focus {
    border: 2px solid #388BFD;
    background: #1C2128;
    padding: 9px 13px;
}
QLineEdit::placeholder { color: #484F58; }
QPushButton#main_action {
    background: #238636;
    color: white;
    border: 1px solid #2EA043;
    border-radius: 8px;
    padding: 12px 24px;
    font-size: 14px;
    font-weight: bold;
    min-height: 42px;
}
QPushButton#main_action:hover { background: #2EA043; }
QPushButton#main_action:pressed { background: #1A6328; }
QPushButton#blue_action {
    background: #0969DA;
    color: white;
    border: 1px solid #0550AE;
    border-radius: 8px;
    padding: 12px 24px;
    font-size: 14px;
    font-weight: bold;
    min-height: 42px;
}
QPushButton#blue_action:hover { background: #0550AE; }
QPushButton#ghost_action {
    background: transparent;
    color: #58A6FF;
    border: 1px solid #30363D;
    border-radius: 8px;
    padding: 9px 20px;
    font-size: 13px;
    min-height: 36px;
}
QPushButton#ghost_action:hover { background: rgba(88,166,255,0.1); }
QPushButton#link_btn {
    background: transparent;
    color: #58A6FF;
    border: none;
    font-size: 12px;
    text-decoration: underline;
    min-height: 0;
    padding: 4px;
}
QPushButton#link_btn:hover { color: #79C0FF; }
QListWidget {
    background: #161B22;
    border: 1px solid #30363D;
    border-radius: 10px;
    color: #E6EDF3;
    outline: none;
    padding: 4px;
}
QListWidget::item {
    padding: 13px 16px;
    border-radius: 8px;
    color: #E6EDF3;
    border: none;
    font-size: 13px;
}
QListWidget::item:hover { background: rgba(255,255,255,0.05); }
QListWidget::item:selected { background: rgba(9,105,218,0.25); color: #58A6FF; font-weight: bold; }
QScrollBar:vertical { width: 6px; background: transparent; }
QScrollBar::handle:vertical { background: #30363D; border-radius: 3px; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
"""

def _sep(parent_layout, color="#21262D"):
    line = QFrame(); line.setFrameShape(QFrame.HLine)
    line.setStyleSheet(f"color: {color}; background: {color}; max-height: 1px; border: none;")
    parent_layout.addWidget(line)


# ══════════════════════════════════════════════════════════════
# ACTIVATION SCREEN
# ══════════════════════════════════════════════════════════════
class ActivationScreen(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("تفعيل البرنامج")
        self.setFixedSize(480, 400)
        self.setWindowFlags(Qt.Window | Qt.WindowTitleHint | Qt.CustomizeWindowHint)
        self.setLayoutDirection(Qt.RightToLeft)
        self.setStyleSheet(DARK_SS)
        self._build()

    def _build(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # Top color bar
        bar = QFrame(); bar.setFixedHeight(4)
        bar.setStyleSheet("background: qlineargradient(x1:0,y1:0,x2:1,y2:0,stop:0 #F0B429,stop:1 #E8921A);")
        root.addWidget(bar)

        # Content
        content = QWidget(); lay = QVBoxLayout(content)
        lay.setContentsMargins(48, 40, 48, 40); lay.setSpacing(20)

        # Icon
        icon_lbl = QLabel("🔐")
        icon_lbl.setAlignment(Qt.AlignCenter)
        icon_lbl.setStyleSheet("font-size: 52px; background: transparent; color: #F0B429;")
        lay.addWidget(icon_lbl)

        # Title
        title = QLabel("تفعيل البرنامج")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 22px; font-weight: bold; color: #F0B429; background: transparent;")
        lay.addWidget(title)

        # Subtitle
        sub = QLabel("أدخل رمز التفعيل للمتابعة\nهذا الجهاز سيُفعَّل نهائياً ولن يُطلب الرمز مجدداً")
        sub.setAlignment(Qt.AlignCenter)
        sub.setWordWrap(True)
        sub.setStyleSheet("color: #8B949E; font-size: 12px; line-height: 1.6; background: transparent;")
        lay.addWidget(sub)

        # Machine ID
        mid_frame = QFrame()
        mid_frame.setStyleSheet("background: #161B22; border: 1px solid #30363D; border-radius: 8px; padding: 8px;")
        mid_lay = QHBoxLayout(mid_frame); mid_lay.setContentsMargins(12, 8, 12, 8)
        mid_icon = QLabel("💻"); mid_icon.setStyleSheet("background: transparent; color: #8B949E;")
        mid_text = QLabel(f"معرّف الجهاز: {machine_id_display()}")
        mid_text.setStyleSheet("color: #8B949E; font-size: 11px; font-family: Courier New, monospace; background: transparent;")
        mid_lay.addWidget(mid_icon); mid_lay.addWidget(mid_text); mid_lay.addStretch()
        lay.addWidget(mid_frame)

        # Key input
        self.key_input = QLineEdit()
        self.key_input.setPlaceholderText("أدخل رمز التفعيل هنا...")
        self.key_input.setAlignment(Qt.AlignCenter)
        self.key_input.setFixedHeight(46)
        lay.addWidget(self.key_input)

        # Error label
        self.err = QLabel("")
        self.err.setAlignment(Qt.AlignCenter)
        self.err.setStyleSheet("color: #F85149; font-size: 12px; background: transparent;")
        self.err.setFixedHeight(20)
        lay.addWidget(self.err)

        # Button
        btn = QPushButton("✓  تفعيل البرنامج")
        btn.setObjectName("main_action")
        btn.clicked.connect(self._activate)
        lay.addWidget(btn)

        root.addWidget(content)
        self.key_input.returnPressed.connect(self._activate)

    def _activate(self):
        ok, msg = activate(self.key_input.text().strip())
        if ok:
            self.accept()
        else:
            self.err.setText(f"✗  {msg}")
            self.key_input.selectAll()
            self.key_input.setFocus()
            # Shake animation
            anim = QPropertyAnimation(self, b"pos")
            anim.setDuration(300)
            pos = self.pos()
            anim.setKeyValueAt(0,   pos)
            anim.setKeyValueAt(0.2, pos + QPoint(8, 0))
            anim.setKeyValueAt(0.4, pos + QPoint(-8, 0))
            anim.setKeyValueAt(0.6, pos + QPoint(6, 0))
            anim.setKeyValueAt(0.8, pos + QPoint(-6, 0))
            anim.setKeyValueAt(1,   pos)
            anim.start(QAbstractAnimation.DeleteWhenStopped)


# ══════════════════════════════════════════════════════════════
# SCHOOL SELECTOR
# ══════════════════════════════════════════════════════════════
class SchoolSelectorDialog(QDialog):
    selected_school = None

    def __init__(self):
        super().__init__()
        self.setWindowTitle("نظام إدارة المدرسة")
        self.setFixedSize(580, 520)
        self.setLayoutDirection(Qt.RightToLeft)
        self.setStyleSheet(DARK_SS)
        self._build()

    def _build(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # Top bar
        bar = QFrame(); bar.setFixedHeight(4)
        bar.setStyleSheet("background: qlineargradient(x1:0,y1:0,x2:1,y2:0,stop:0 #0969DA,stop:1 #6E40C9);")
        root.addWidget(bar)

        content = QWidget(); lay = QVBoxLayout(content)
        lay.setContentsMargins(40, 36, 40, 36); lay.setSpacing(20)

        # Header
        hdr = QHBoxLayout()
        icon = QLabel("🏫")
        icon.setStyleSheet("font-size: 36px; background: transparent;")
        title_col = QVBoxLayout(); title_col.setSpacing(2)
        t1 = QLabel("نظام إدارة المدرسة الأهلية")
        t1.setStyleSheet("font-size: 18px; font-weight: bold; color: #E6EDF3; background: transparent;")
        t2 = QLabel("اختر المدرسة للمتابعة")
        t2.setStyleSheet("color: #8B949E; font-size: 12px; background: transparent;")
        title_col.addWidget(t1); title_col.addWidget(t2)
        hdr.addWidget(icon); hdr.addLayout(title_col); hdr.addStretch()
        lay.addLayout(hdr)

        _sep(lay)

        # Schools list label
        lbl = QLabel("المدارس المسجلة")
        lbl.setStyleSheet("font-size: 11px; font-weight: bold; color: #8B949E; letter-spacing: 1px; background: transparent;")
        lay.addWidget(lbl)

        self.school_list = QListWidget()
        self.school_list.setMinimumHeight(220)
        self.school_list.doubleClicked.connect(self._select)
        lay.addWidget(self.school_list)

        # Buttons
        btn_lay = QHBoxLayout(); btn_lay.setSpacing(10)
        add_btn = QPushButton("➕  مدرسة جديدة")
        add_btn.setObjectName("ghost_action")
        add_btn.clicked.connect(self._add_school)
        enter_btn = QPushButton("الدخول  ←")
        enter_btn.setObjectName("blue_action")
        enter_btn.clicked.connect(self._select)
        btn_lay.addWidget(add_btn); btn_lay.addStretch(); btn_lay.addWidget(enter_btn)
        lay.addLayout(btn_lay)

        root.addWidget(content)
        self._load()

    def _load(self):
        self.school_list.clear()
        schools = DB.get_schools()
        for s in schools:
            s = dict(s)  # ← FIX: convert sqlite3.Row to dict
            principal = s.get("principal") or "لم يُحدَّد المدير"
            year = s.get("academic_year") or ""
            text = f"  🏫  {s['name']}  |  {principal}  |  {year}"
            item = QListWidgetItem(text)
            item.setData(Qt.UserRole, s["id"])
            self.school_list.addItem(item)
        if schools:
            self.school_list.setCurrentRow(0)

    def _select(self):
        item = self.school_list.currentItem()
        if not item:
            QMessageBox.warning(self, "تنبيه", "اختر مدرسة أولاً")
            return
        self.selected_school = item.data(Qt.UserRole)
        self.accept()

    def _add_school(self):
        dlg = NewSchoolDialog(self)
        if dlg.exec():
            self._load()


# ══════════════════════════════════════════════════════════════
# NEW SCHOOL DIALOG
# ══════════════════════════════════════════════════════════════
class NewSchoolDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("إنشاء مدرسة جديدة")
        self.setFixedWidth(500)
        self.setLayoutDirection(Qt.RightToLeft)
        self.setStyleSheet(MAIN_STYLE)
        self._build()

    def _build(self):
        lay = QVBoxLayout(self)
        lay.setContentsMargins(28, 24, 28, 24)
        lay.setSpacing(14)

        # Title
        title_row = QHBoxLayout()
        icon = QLabel("🏫")
        icon.setStyleSheet("font-size: 24px; background: transparent;")
        title = QLabel("إنشاء مدرسة جديدة")
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: #1F2328;")
        title_row.addWidget(icon); title_row.addWidget(title); title_row.addStretch()
        lay.addLayout(title_row)

        # Divider
        d = QFrame(); d.setFrameShape(QFrame.HLine)
        d.setStyleSheet(f"color: {C['border']}; background: {C['border']}; max-height:1px; border:none;")
        lay.addWidget(d)

        def row(label_text, widget):
            container = QWidget()
            container_lay = QVBoxLayout(container)
            container_lay.setContentsMargins(0, 0, 0, 0)
            container_lay.setSpacing(4)
            lbl = QLabel(label_text)
            lbl.setStyleSheet(f"font-size: 12px; font-weight: bold; color: {C['text_sec']}; background: transparent;")
            container_lay.addWidget(lbl)
            container_lay.addWidget(widget)
            lay.addWidget(container)

        self.name = QLineEdit(); self.name.setPlaceholderText("الاسم الرسمي للمدرسة")
        row("اسم المدرسة *", self.name)

        self.princ = QLineEdit(); self.princ.setPlaceholderText("اسم المدير المسؤول")
        row("مدير المدرسة", self.princ)

        # Two columns
        row2 = QHBoxLayout(); row2.setSpacing(12)
        col1 = QWidget(); c1l = QVBoxLayout(col1); c1l.setContentsMargins(0,0,0,0); c1l.setSpacing(4)
        l1 = QLabel("رقم الهاتف"); l1.setStyleSheet(f"font-size:12px; font-weight:bold; color:{C['text_sec']}; background:transparent;")
        self.phone = QLineEdit(); self.phone.setLayoutDirection(Qt.LeftToRight)
        c1l.addWidget(l1); c1l.addWidget(self.phone)

        col2 = QWidget(); c2l = QVBoxLayout(col2); c2l.setContentsMargins(0,0,0,0); c2l.setSpacing(4)
        l2 = QLabel("السنة الدراسية"); l2.setStyleSheet(f"font-size:12px; font-weight:bold; color:{C['text_sec']}; background:transparent;")
        self.year = QLineEdit("2025-2026")
        c2l.addWidget(l2); c2l.addWidget(self.year)

        row2.addWidget(col1); row2.addWidget(col2)
        lay.addLayout(row2)

        self.addr = QLineEdit(); self.addr.setPlaceholderText("المحافظة / الحي / الشارع")
        row("العنوان", self.addr)

        fee_row = QHBoxLayout(); fee_row.setSpacing(12)
        fee_col = QWidget(); fcl = QVBoxLayout(fee_col); fcl.setContentsMargins(0,0,0,0); fcl.setSpacing(4)
        fl = QLabel("قيمة القسط السنوي (دينار)"); fl.setStyleSheet(f"font-size:12px; font-weight:bold; color:{C['text_sec']}; background:transparent;")
        self.fee = QLineEdit("1500000")
        fcl.addWidget(fl); fcl.addWidget(self.fee)
        fee_row.addWidget(fee_col); lay.addLayout(fee_row)

        # Note
        note = QFrame()
        note.setStyleSheet(f"background: {C['warning_lt']}; border: 1px solid #E2B040; border-radius: 8px;")
        note_lay = QHBoxLayout(note); note_lay.setContentsMargins(12, 10, 12, 10); note_lay.setSpacing(8)
        note_icon = QLabel("⚠️"); note_icon.setStyleSheet("background: transparent; font-size: 14px;")
        note_text = QLabel("سيُنشأ تلقائياً حساب مدير للمدرسة الجديدة\nسيتم تحديد بيانات الدخول في الخطوة التالية")
        note_text.setStyleSheet(f"color: {C['warning']}; font-size: 11px; background: transparent;")
        note_lay.addWidget(note_icon); note_lay.addWidget(note_text)
        lay.addWidget(note)

        # Buttons
        btn_row = QHBoxLayout(); btn_row.setSpacing(10)
        cancel = QPushButton("إلغاء"); cancel.setObjectName("ghostBtn"); cancel.clicked.connect(self.reject)
        save = QPushButton("✓  إنشاء المدرسة"); save.setObjectName("primaryBtn"); save.clicked.connect(self._save)
        btn_row.addWidget(cancel); btn_row.addStretch(); btn_row.addWidget(save)
        lay.addLayout(btn_row)

    def _save(self):
        if not self.name.text().strip():
            QMessageBox.warning(self, "خطأ", "اسم المدرسة مطلوب")
            return
        try:
            fee = float(self.fee.text().replace(",", ""))
        except Exception:
            fee = 1500000
        sid = DB.add_school({
            "name": self.name.text().strip(),
            "principal": self.princ.text().strip(),
            "address": self.addr.text().strip(),
            "phone": self.phone.text().strip(),
            "email": "",
            "academic_year": self.year.text().strip() or "2025-2026",
            "fee_amount": fee,
        })
        # Ask admin to set credentials immediately
        dlg = AdminSetupDialog(sid, self)
        dlg.exec()
        self.accept()




# ══════════════════════════════════════════════════════════════
# ADMIN SETUP DIALOG — يُفتح عند إنشاء مدرسة جديدة
# ══════════════════════════════════════════════════════════════
class AdminSetupDialog(QDialog):
    def __init__(self, school_id, parent=None):
        super().__init__(parent)
        self.school_id = school_id
        self.setWindowTitle("إعداد حساب المدير")
        self.setFixedSize(460, 360)
        self.setLayoutDirection(Qt.RightToLeft)
        self.setStyleSheet(MAIN_STYLE)
        self._build()

    def _build(self):
        lay = QVBoxLayout(self)
        lay.setContentsMargins(32, 28, 32, 28)
        lay.setSpacing(14)

        title = QLabel("🔑  إعداد حساب المدير")
        title.setStyleSheet("font-size:16px; font-weight:bold;")
        lay.addWidget(title)

        info = QLabel("حدد اسم المستخدم وكلمة المرور لحساب المدير — هذه المعلومات ستُستخدم لتسجيل الدخول لاحقاً")
        info.setWordWrap(True)
        info.setStyleSheet(f"color: #6E7781; font-size: 12px;")
        lay.addWidget(info)

        def field(label, widget):
            c = QWidget(); cl = QVBoxLayout(c); cl.setContentsMargins(0,0,0,0); cl.setSpacing(4)
            l = QLabel(label); l.setStyleSheet("font-size:12px; font-weight:bold; color:#444D56;")
            cl.addWidget(l); cl.addWidget(widget); lay.addWidget(c)

        self.full_name = QLineEdit(); self.full_name.setPlaceholderText("مثال: أحمد محمد")
        field("الاسم الكامل للمدير *", self.full_name)

        self.username = QLineEdit(); self.username.setPlaceholderText("مثال: director2025")
        field("اسم المستخدم *", self.username)

        self.password = QLineEdit(); self.password.setEchoMode(QLineEdit.Password)
        self.password.setPlaceholderText("كلمة مرور قوية")
        field("كلمة المرور *", self.password)

        self.confirm = QLineEdit(); self.confirm.setEchoMode(QLineEdit.Password)
        self.confirm.setPlaceholderText("أعد كتابة كلمة المرور")
        field("تأكيد كلمة المرور *", self.confirm)

        self.err = QLabel(""); self.err.setStyleSheet("color: red; font-size: 12px;")
        lay.addWidget(self.err)

        btn_row = QHBoxLayout()
        skip = QPushButton("تخطي الآن (admin/admin123)"); skip.setObjectName("ghostBtn")
        skip.clicked.connect(self.accept)
        save = QPushButton("✓  حفظ بيانات الدخول"); save.setObjectName("primaryBtn")
        save.clicked.connect(self._save)
        btn_row.addWidget(skip); btn_row.addStretch(); btn_row.addWidget(save)
        lay.addLayout(btn_row)

    def _save(self):
        fn = self.full_name.text().strip()
        un = self.username.text().strip()
        pw = self.password.text().strip()
        cf = self.confirm.text().strip()
        if not un or not pw:
            self.err.setText("اسم المستخدم وكلمة المرور مطلوبان")
            return
        if pw != cf:
            self.err.setText("كلمتا المرور غير متطابقتان")
            return
        # Update the default admin account
        import core.db as DB2
        import sqlite3
        db = DB2.conn()
        # Delete old default admin if exists
        db.execute("DELETE FROM users WHERE school_id=? AND username='admin'", (self.school_id,))
        db.execute("INSERT INTO users (school_id,username,password,full_name,role) VALUES (?,?,?,?,?)",
                   (self.school_id, un, pw, fn or "مدير المدرسة", "مدير"))
        db.commit(); db.close()
        QMessageBox.information(self, "تم", f"تم حفظ بيانات المدير\nاسم المستخدم: {un}")
        self.accept()

# ══════════════════════════════════════════════════════════════
# LOGIN DIALOG
# ══════════════════════════════════════════════════════════════
class LoginDialog(QDialog):
    user_info = None

    def __init__(self, school_id):
        super().__init__()
        self.school_id = school_id
        school = DB.get_school(school_id)
        school = dict(school) if school else {}
        self.school_name = school.get("name", "المدرسة")
        self.setWindowTitle(f"تسجيل الدخول — {self.school_name}")
        self.setFixedSize(440, 480)
        self.setWindowFlags(Qt.Window | Qt.WindowTitleHint | Qt.CustomizeWindowHint)
        self.setLayoutDirection(Qt.RightToLeft)
        self.setStyleSheet(DARK_SS)
        self._build()

    def _build(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # Top bar
        bar = QFrame(); bar.setFixedHeight(4)
        bar.setStyleSheet("background: qlineargradient(x1:0,y1:0,x2:1,y2:0,stop:0 #0969DA,stop:1 #6E40C9);")
        root.addWidget(bar)

        content = QWidget(); lay = QVBoxLayout(content)
        lay.setContentsMargins(48, 40, 48, 40); lay.setSpacing(18)

        # School badge
        badge = QLabel(f"🏫  {self.school_name}")
        badge.setAlignment(Qt.AlignCenter)
        badge.setWordWrap(True)
        badge.setStyleSheet("""
            background: rgba(9,105,218,0.15);
            color: #58A6FF;
            border: 1px solid rgba(9,105,218,0.3);
            border-radius: 20px;
            padding: 8px 18px;
            font-size: 13px;
            font-weight: bold;
        """)
        lay.addWidget(badge)

        # Greeting
        greet = QLabel("مرحباً بك")
        greet.setAlignment(Qt.AlignCenter)
        greet.setStyleSheet("font-size: 26px; font-weight: bold; color: #E6EDF3; background: transparent;")
        lay.addWidget(greet)

        sub = QLabel("سجّل دخولك للمتابعة")
        sub.setAlignment(Qt.AlignCenter)
        sub.setStyleSheet("color: #8B949E; font-size: 13px; background: transparent;")
        lay.addWidget(sub)

        # Username field
        u_col = QWidget(); ucl = QVBoxLayout(u_col); ucl.setContentsMargins(0,0,0,0); ucl.setSpacing(5)
        u_lbl = QLabel("اسم المستخدم")
        u_lbl.setStyleSheet("color: #8B949E; font-size: 12px; font-weight: bold; background: transparent;")
        self.username = QLineEdit()
        self.username.setPlaceholderText("أدخل اسم المستخدم")
        self.username.setFixedHeight(44)
        ucl.addWidget(u_lbl); ucl.addWidget(self.username)
        lay.addWidget(u_col)

        # Password field
        p_col = QWidget(); pcl = QVBoxLayout(p_col); pcl.setContentsMargins(0,0,0,0); pcl.setSpacing(5)
        p_lbl = QLabel("كلمة المرور")
        p_lbl.setStyleSheet("color: #8B949E; font-size: 12px; font-weight: bold; background: transparent;")
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setPlaceholderText("••••••••••••")
        self.password.setFixedHeight(44)
        pcl.addWidget(p_lbl); pcl.addWidget(self.password)
        lay.addWidget(p_col)

        # Error
        self.err = QLabel("")
        self.err.setAlignment(Qt.AlignCenter)
        self.err.setStyleSheet("""
            color: #F85149;
            background: rgba(248,81,73,0.1);
            border: 1px solid rgba(248,81,73,0.3);
            border-radius: 8px;
            padding: 8px;
            font-size: 12px;
        """)
        self.err.setFixedHeight(0)
        lay.addWidget(self.err)

        # Login button
        self.login_btn = QPushButton("الدخول  →")
        self.login_btn.setObjectName("blue_action")
        self.login_btn.clicked.connect(self._login)
        lay.addWidget(self.login_btn)

        # Back
        back = QPushButton("← تغيير المدرسة")
        back.setObjectName("link_btn")
        back.clicked.connect(self.reject)
        back.setFixedHeight(30)
        lay.addWidget(back, alignment=Qt.AlignCenter)

        root.addWidget(content)
        self.password.returnPressed.connect(self._login)
        self.username.returnPressed.connect(lambda: self.password.setFocus())

    def _login(self):
        u = self.username.text().strip()
        p = self.password.text().strip()
        if not u:
            self._show_error("أدخل اسم المستخدم")
            self.username.setFocus()
            return
        result = DB.login(self.school_id, u, p)
        if result:
            self.user_info = result
            self.accept()
        else:
            self._show_error("✗  اسم المستخدم أو كلمة المرور غير صحيحة")
            self.password.clear()
            self.password.setFocus()

    def _show_error(self, msg):
        self.err.setText(msg)
        self.err.setFixedHeight(40)

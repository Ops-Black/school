"""
جميع صفحات البرنامج — تصميم احترافي محدّث
"""
import os, sys, shutil
from datetime import date, datetime
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
import core.db as DB
from ui.style import C, MAIN_STYLE
from core.security.grade_levels import NAMES as GRADE_NAMES, SECTIONS, subjects_for, by_stage, STAGE_COLORS, BRANCH_COLORS, stages as grade_stages, ALL_GRADES

# ══════════════════════════════════════════
# ✨ Shadow Helper
# ══════════════════════════════════════════
def add_shadow(widget, blur=12, offset=2, color_alpha=20):
    """إضافة ظل خفيف للـ widgets"""
    from PySide6.QtWidgets import QGraphicsDropShadowEffect
    from PySide6.QtGui import QColor
    shadow = QGraphicsDropShadowEffect()
    shadow.setBlurRadius(blur)
    shadow.setXOffset(0)
    shadow.setYOffset(offset)
    shadow.setColor(QColor(0, 0, 0, color_alpha))
    widget.setGraphicsEffect(shadow)

# ─── Helpers ─────────────────────────────────────────────────
def _row(s):  return dict(s) if s else {}
def card():
    f = QFrame(); f.setObjectName("card")
    add_shadow(f, blur=10, offset=2, color_alpha=15)  # ✨ Shadow خفيف
    return f

def mk_table(cols, stretch_col=1):
    t = QTableWidget()
    t.setColumnCount(len(cols))
    t.setHorizontalHeaderLabels(cols)
    t.setEditTriggers(QAbstractItemView.NoEditTriggers)
    t.setSelectionBehavior(QAbstractItemView.SelectRows)
    t.verticalHeader().setVisible(False)
    t.setShowGrid(False)
    t.setAlternatingRowColors(True)
    t.horizontalHeader().setSectionResizeMode(stretch_col, QHeaderView.Stretch)
    t.setStyleSheet(f"""
    QTableWidget {{
        background: white; border: 1px solid {C['border_light']};
        border-radius: 12px; outline: 0;
        alternate-background-color: #FAFBFD;
    }}
    QTableWidget::item {{
        padding: 11px 16px;
        border-bottom: 1px solid #F0F1F5;
        color: {C['text']};
        background-color: transparent;
    }}
    QTableWidget::item:hover {{
        background-color: #EEF2FF;
        color: {C['text']};
    }}
    QTableWidget::item:selected {{
        background-color: {C['primary_lt']};
        color: {C['primary']};
    }}
    QHeaderView::section {{
        background: #F4F5F9; color: {C['text_sec']};
        font-weight: bold; font-size: 11px;
        padding: 12px 16px; border: none;
        border-bottom: 2px solid {C['border']};
        letter-spacing: 0.5px;
    }}
    QHeaderView::section:first {{ border-top-right-radius: 12px; }}
    QHeaderView::section:last  {{ border-top-left-radius:  12px; }}
    """)
    t.setFocusPolicy(Qt.NoFocus)
    return t

def pb(text):
    b = QPushButton(text); b.setObjectName("primaryBtn"); b.setFixedHeight(36); return b

def gb(text):
    b = QPushButton(text); b.setObjectName("ghostBtn"); b.setFixedHeight(34); return b

def ib(text, tooltip=""):
    b = QPushButton(text); b.setObjectName("iconBtn"); b.setFixedSize(32, 30)
    if tooltip: b.setToolTip(tooltip)
    return b

def tc(text, align=Qt.AlignVCenter | Qt.AlignRight, color=None, bold=False):
    it = QTableWidgetItem(str(text))
    it.setTextAlignment(align)
    if color: it.setForeground(QColor(color))
    if bold:
        f = QFont(); f.setBold(True); it.setFont(f)
    return it

def badge_item(text, color):
    it = QTableWidgetItem(f"  {text}  ")
    it.setForeground(QColor(color))
    it.setTextAlignment(Qt.AlignCenter)
    return it

def section_title(text):
    l = QLabel(text); l.setObjectName("section_title"); return l

def field_group(label_text, widget, parent_lay):
    w = QWidget(); wl = QVBoxLayout(w); wl.setContentsMargins(0,0,0,0); wl.setSpacing(5)
    lbl = QLabel(label_text)
    lbl.setStyleSheet(f"font-size: 11px; font-weight: bold; color: {C['text_sec']}; background: transparent;")
    wl.addWidget(lbl); wl.addWidget(widget)
    parent_lay.addWidget(w)

def divider():
    f = QFrame(); f.setFrameShape(QFrame.HLine)
    f.setStyleSheet(f"color: {C['border']}; background: {C['border']}; max-height: 1px; border: none;")
    return f

# ══════════════════════════════════════════
# KPI CARD
# ══════════════════════════════════════════
class KPICard(QFrame):
    def __init__(self, icon, label, value, sub="", color=None):
        super().__init__()
        self.setObjectName("kpi_card")
        self.setFixedHeight(106)
        lay = QVBoxLayout(self); lay.setContentsMargins(18,14,18,14); lay.setSpacing(6)
        clr = color or C['primary']
        top = QHBoxLayout(); top.setSpacing(10)

        # Icon circle
        ic = QLabel(icon); ic.setFixedSize(38,38); ic.setAlignment(Qt.AlignCenter)
        ic.setStyleSheet(f"background: {clr}18; border-radius: 10px; font-size: 18px;")
        lbl = QLabel(label)
        lbl.setStyleSheet(f"color: {C['text_sec']}; font-size: 12px; background: transparent;")
        top.addWidget(ic); top.addWidget(lbl); top.addStretch()
        lay.addLayout(top)

        val = QLabel(str(value))
        val.setStyleSheet(f"font-size: 28px; font-weight: bold; color: {C['text']}; background: transparent;")
        lay.addWidget(val)

        if sub:
            sl = QLabel(sub); sl.setStyleSheet(f"color: {clr}; font-size: 11px; background: transparent;")
            lay.addWidget(sl)

# ══════════════════════════════════════════
# ✨ Student KPI Card — Dashboard مصغر
# ══════════════════════════════════════════
class StudentKPICard(QFrame):
    def __init__(self, icon, label, value, color=None):
        super().__init__()
        self.setObjectName("kpi_card")
        self.setFixedHeight(90)
        add_shadow(self, blur=8, offset=1, color_alpha=12)
        
        lay = QHBoxLayout(self)
        lay.setContentsMargins(14, 12, 14, 12)
        lay.setSpacing(12)
        
        clr = color or C['primary']
        
        # Icon circle
        ic = QLabel(icon)
        ic.setFixedSize(42, 42)
        ic.setAlignment(Qt.AlignCenter)
        ic.setStyleSheet(f"background: {clr}18; border-radius: 10px; font-size: 20px;")
        
        # Text
        text_w = QWidget()
        text_lay = QVBoxLayout(text_w)
        text_lay.setContentsMargins(0, 0, 0, 0)
        text_lay.setSpacing(2)
        
        val_lbl = QLabel(str(value))
        val_lbl.setStyleSheet(f"font-size: 22px; font-weight: bold; color: {C['text']}; background: transparent;")
        
        label_lbl = QLabel(label)
        label_lbl.setStyleSheet(f"color: {C['text_muted']}; font-size: 11px; background: transparent;")
        
        text_lay.addWidget(val_lbl)
        text_lay.addWidget(label_lbl)
        
        lay.addWidget(ic)
        lay.addWidget(text_w)
        lay.addStretch()

# ══════════════════════════════════════════
# BAR CHART
# ══════════════════════════════════════════
class BarChart(QWidget):
    def __init__(self, color=None):
        super().__init__()
        self._labels = []; self._values = []; self._fmt = "{}"
        self._color = color or C['primary']
        self.setMinimumHeight(140)

    def set_data(self, labels, values, fmt="{}"):
        self._labels = labels; self._values = values; self._fmt = fmt
        self.update()

    def paintEvent(self, e):
        if not self._values: return
        p = QPainter(self); p.setRenderHint(QPainter.Antialiasing)
        W, H = self.width(), self.height()
        PAD_L, PAD_B, PAD_T = 8, 26, 12
        usable_h = H - PAD_B - PAD_T
        max_v = max(self._values) or 1
        n = len(self._values)
        slot_w = (W - PAD_L * 2) // n
        bar_w = max(12, slot_w - 10)

        for i, (lbl, val) in enumerate(zip(self._labels, self._values)):
            bh = max(4, int(val / max_v * usable_h))
            x = PAD_L + i * slot_w + (slot_w - bar_w) // 2
            y = H - PAD_B - bh

            # Shadow
            p.setPen(Qt.NoPen)
            p.setBrush(QColor(0, 0, 0, 15))
            p.drawRoundedRect(x+2, y+2, bar_w, bh, 5, 5)

            # Gradient bar
            grad = QLinearGradient(x, y, x, y+bh)
            base = QColor(self._color)
            light = QColor(base); light.setAlpha(160)
            grad.setColorAt(0, base); grad.setColorAt(1, light)
            p.setBrush(grad); p.setPen(Qt.NoPen)
            p.drawRoundedRect(x, y, bar_w, bh, 5, 5)

            # Label below
            p.setPen(QColor(C['text_sec']))
            f = QFont(); f.setPointSize(9); p.setFont(f)
            p.drawText(QRect(x-4, H-PAD_B+4, bar_w+8, 20), Qt.AlignCenter, str(lbl))

            # Value on bar
            if bh > 24:
                p.setPen(QColor("white"))
                f2 = QFont(); f2.setPointSize(8); f2.setBold(True); p.setFont(f2)
                p.drawText(QRect(x, y+3, bar_w, 16), Qt.AlignCenter, self._fmt.format(val))

# ═════════════════════════════════════════
# MINI PROGRESS BAR
# ══════════════════════════════════════════
class MiniBar(QWidget):
    def __init__(self, pct, color=None):
        super().__init__(); self.pct = min(100, max(0, pct)); self.color = color or C['primary']
        self.setFixedSize(80, 8)

    def paintEvent(self, e):
        p = QPainter(self); p.setRenderHint(QPainter.Antialiasing)
        p.setPen(Qt.NoPen)
        p.setBrush(QColor("#E8EAED")); p.drawRoundedRect(0,0,80,8,4,4)
        if self.pct > 0:
            p.setBrush(QColor(self.color)); p.drawRoundedRect(0,0,int(80*self.pct/100),8,4,4)

# ═════════════════════════════════════════
# BASE PAGE
# ══════════════════════════════════════════
class BasePage(QWidget):
    def __init__(self, school_id, user_info):
        super().__init__()
        self.sid = school_id
        self.ui  = user_info
        self.setLayoutDirection(Qt.RightToLeft)
        self.setStyleSheet(f"background: {C['bg_page']};")

    def _page_wrap(self):
        """Returns a scrollable content area"""
        scroll = QScrollArea(); scroll.setWidgetResizable(True); scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet(f"background: {C['bg_page']}; border: none;")
        inner = QWidget(); inner.setStyleSheet(f"background: {C['bg_page']};")
        lay = QVBoxLayout(inner); lay.setContentsMargins(20,16,20,16); lay.setSpacing(16)
        root = QVBoxLayout(self); root.setContentsMargins(0,0,0,0); root.setSpacing(0)
        scroll.setWidget(inner); root.addWidget(scroll)
        return lay

    def refresh(self, *_): pass

# ══════════════════════════════════════════
# DASHBOARD
# ══════════════════════════════════════════
class DashboardPage(BasePage):
    def __init__(self, school_id, user_info):
        super().__init__(school_id, user_info)
        lay = self._page_wrap()
        # KPI row
        self.kpi_row = QHBoxLayout(); self.kpi_row.setSpacing(12)
        lay.addLayout(self.kpi_row)

        # Charts
        charts_row = QHBoxLayout(); charts_row.setSpacing(16)
        c1 = card(); c1l = QVBoxLayout(c1); c1l.setContentsMargins(16,14,16,14)
        c1l.addWidget(section_title("📅  الغياب الشهري"))
        self.abs_chart = BarChart(C['danger']); self.abs_chart.setFixedHeight(150)
        c1l.addWidget(self.abs_chart); charts_row.addWidget(c1)

        c2 = card(); c2l = QVBoxLayout(c2); c2l.setContentsMargins(16,14,16,14)
        c2l.addWidget(section_title("💰  الإيرادات الشهرية"))
        self.inc_chart = BarChart(C['success']); self.inc_chart.setFixedHeight(150)
        c2l.addWidget(self.inc_chart); charts_row.addWidget(c2)
        lay.addLayout(charts_row)

        # Bottom
        bot = QHBoxLayout(); bot.setSpacing(16)
        pc = card(); pcl = QVBoxLayout(pc); pcl.setContentsMargins(16,14,16,14)
        pcl.addWidget(section_title("💳  آخر المدفوعات"))
        self.pay_t = mk_table(["الطالب", "المبلغ", "التاريخ", "الموظف"])
        self.pay_t.setFixedHeight(200); pcl.addWidget(self.pay_t); bot.addWidget(pc, 3)

        nc = card(); ncl = QVBoxLayout(nc); ncl.setContentsMargins(16,14,16,14)
        ncl.addWidget(section_title("🔔  التنبيهات"))
        self.notif_list = QListWidget()
        self.notif_list.setFixedHeight(200)
        self.notif_list.setStyleSheet(f"border: 1px solid {C['border']}; border-radius: 8px; background: white;")
        ncl.addWidget(self.notif_list); bot.addWidget(nc, 2)
        lay.addLayout(bot)

    def refresh(self, *_):
        while self.kpi_row.count():
            w = self.kpi_row.takeAt(0).widget()
            if w: w.setParent(None)

        st = DB.get_stats(self.sid)
        for icon, lbl, val, sub, clr in [
            ("📚", "الطلاب",        f"{st['students']:,}",            " ",              C['primary']),
            ("👩‍🏫", "المدرسون",    f"{st['teachers']:,}",             " ",               "#8250DF"),
            ("💰", "المحصّل",       f"{st['fees_paid']/1e6:.1f}M",    "↑ دينار عراقي", C['success']),
            ("", "أقساط متأخرة", f"{st['fees_pending']/1e6:.1f}M", "↓ تحتاج متابعة", C['danger']),
            ("🚸", "غياب اليوم",   str(st['absent_today']),           " ",               "#E3B341"),
            ("🎓", "نسبة النجاح",  f"{st['pass_rate']}%",             "↑ ممتاز",        C['success']),
        ]:
            self.kpi_row.addWidget(KPICard(icon, lbl, val, sub, clr))

        # Charts
        abs_rows = DB.get_monthly_absence(self.sid)
        if abs_rows:
            self.abs_chart.set_data([r["month"][5:] for r in reversed(abs_rows)],
                                   [r["cnt"] for r in reversed(abs_rows)])

        inc_rows = DB.get_monthly_income(self.sid)
        if inc_rows:
            self.inc_chart.set_data([r["month"][5:] for r in reversed(inc_rows)],
                                   [r["income"]/1e6 for r in reversed(inc_rows)], "{:.1f}M")

        # Recent payments
        db = DB.conn()
        pays = db.execute("""
            SELECT s.full_name, fp.amount, fp.payment_date, fp.employee
            FROM fee_payments fp JOIN students s ON s.id=fp.student_id
            WHERE s.school_id=? ORDER BY fp.id DESC LIMIT 8
        """, (self.sid,)).fetchall()
        db.close()
        self.pay_t.setRowCount(len(pays))
        for r, p in enumerate(pays):
            self.pay_t.setRowHeight(r, 38)
            p = dict(p)
            self.pay_t.setItem(r,0,tc(p["full_name"], bold=True))
            self.pay_t.setItem(r,1,tc(f"{int(p['amount']):,}", Qt.AlignCenter, C['success']))
            self.pay_t.setItem(r,2,tc(p["payment_date"] or " ", Qt.AlignCenter))
            self.pay_t.setItem(r,3,tc(p["employee"] or " ", Qt.AlignCenter))

        # Notifs
        self.notif_list.clear()
        for n in DB.get_notifications(self.sid):
            n = dict(n)
            icon = "⚠️" if "قسط" in (n.get("type") or "") else "📅"
            self.notif_list.addItem(f"  {icon}  {n.get('message','')}")
        if not DB.get_notifications(self.sid):
            it = QListWidgetItem("  ✅  لا توجد تنبيهات جديدة")
            it.setForeground(QColor(C['text_muted']))
            self.notif_list.addItem(it)

# ═════════════════════════════════════════
# STUDENTS — محدّث
# ══════════════════════════════════════════
class StudentsPage(BasePage):
    def __init__(self, school_id, user_info):
        super().__init__(school_id, user_info)
        main = QVBoxLayout(self); main.setContentsMargins(20,14,20,14); main.setSpacing(12)
        
        # ════════════════════════════════════════
        # ✨ Dashboard مصغر — KPI Cards
        # ════════════════════════════════════════
        self.kpi_row = QHBoxLayout()
        self.kpi_row.setSpacing(10)
        main.addLayout(self.kpi_row)
        
        # ── Filter bar ──
        fbar = QFrame(); fbar.setObjectName("card")
        fbar.setStyleSheet(f"background:{C['bg_card']};border:1px solid {C['border_light']};border-radius:10px;")
        fbl = QHBoxLayout(fbar); fbl.setContentsMargins(14,8,14,8); fbl.setSpacing(10)

        fbl.addWidget(QLabel("الصف: "))
        self.f_grade = QComboBox(); self.f_grade.setFixedWidth(150)
        self.f_grade.addItems(["الكل"] + GRADE_NAMES)
        self.f_grade.currentTextChanged.connect(lambda _: self.refresh())
        fbl.addWidget(self.f_grade)

        fbl.addWidget(QLabel("الشعبة: "))
        self.f_section = QComboBox(); self.f_section.setFixedWidth(70)
        self.f_section.addItems(["الكل", "أ", "ب", "ج", "د", "هـ"])
        self.f_section.currentTextChanged.connect(lambda _: self.refresh())
        fbl.addWidget(self.f_section)

        fbl.addWidget(QLabel("الحالة: "))
        self.f_status = QComboBox(); self.f_status.setFixedWidth(110)
        self.f_status.addItems(["الكل", "نشط", "عليه قسط", "متغيب كثير", "موقوف مؤقتاً", "منتقل"])
        self.f_status.currentTextChanged.connect(lambda _: self.refresh())
        fbl.addWidget(self.f_status)

        fbl.addStretch()
        self.count_lbl = QLabel()
        self.count_lbl.setStyleSheet(f"color:{C['text_muted']};font-size:12px;background:transparent;")
        fbl.addWidget(self.count_lbl)
        main.addWidget(fbar)

        # ── Actions bar ──
        top = QHBoxLayout()
        
        # ✨ أزرار Excel/Word/Scan ملونة
        imp = QPushButton("📗 Excel"); imp.setObjectName("excelBtn")
        imp.clicked.connect(self._import)
        
        imp_word = QPushButton("📘 Word"); imp_word.setObjectName("wordBtn")
        imp_word.clicked.connect(self._import_word)
        
        imp_scan = QPushButton("📷 مسح"); imp_scan.setObjectName("scanBtn")
        imp_scan.clicked.connect(self._import_scan)
        
        # ✨ زر إضافة طالب أخضر واضح
        add = QPushButton("➕ إضافة طالب"); add.setObjectName("addStudentBtn")
        add.clicked.connect(self._add)
        
        top.addWidget(imp); top.addWidget(imp_word); top.addWidget(imp_scan)
        top.addStretch(); top.addWidget(add)
        main.addLayout(top)

        self.table = mk_table(["#", "الاسم الكامل", "الصف", "الشعبة", "الهاتف", "ولي الأمر", "الحالة", "إجراءات"])
        self.table.setColumnWidth(0, 50); self.table.setColumnWidth(7, 150)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.doubleClicked.connect(self._view_selected)
        main.addWidget(self.table)

    def refresh(self, search=""):
        # ════════════════════════════════════════
        # ✨ تحديث KPI Cards
        # ════════════════════════════════════════
        self._update_kpi(search)
        
        # تطبيق الفلاتر
        grade_f   = getattr(self, "f_grade",   None)
        section_f = getattr(self, "f_section", None)
        status_f  = getattr(self, "f_status",  None)
        g_val = grade_f.currentText()   if grade_f   else "الكل"
        s_val = section_f.currentText() if section_f else "الكل"
        st_val= status_f.currentText()  if status_f  else "الكل"

        needs_extras = st_val in ("عليه قسط", "متغيب كثير")
        rows = (DB.get_students_with_extras(self.sid, search) if needs_extras
                else DB.get_students(self.sid, search))

        ABSENCE_THRESHOLD = 10

        filtered = []
        for s in rows:
            sd = dict(s)
            if g_val != "الكل" and sd.get("grade", " ") != g_val:
                continue
            if s_val != "الكل" and sd.get("section", " ") != s_val:
                continue
            if st_val == "عليه قسط":
                if not sd.get("has_debt", False):
                    continue
            elif st_val == "متغيب كثير":
                if sd.get("absence_count", 0) < ABSENCE_THRESHOLD:
                    continue
            elif st_val != "الكل" and sd.get("status", "نشط") != st_val:
                continue
            filtered.append(sd)

        self.count_lbl.setText(f"إجمالي: {len(filtered)} طالب")
        rows = filtered
        self.table.setRowCount(len(rows))
        for r, s in enumerate(rows):
            s = s if isinstance(s, dict) else dict(s)
            self.table.setRowHeight(r, 50)
            self.table.setItem(r,0,tc(str(s["id"]), Qt.AlignCenter, C['text_muted']))
            self.table.setItem(r,1,tc(s["full_name"], bold=True))
            self.table.setItem(r,2,tc(s.get("grade", " ") or " "))
            self.table.setItem(r,3,tc(s.get("section", " ") or " ", Qt.AlignCenter))
            self.table.setItem(r,4,tc(s.get("phone", " ") or " "))
            self.table.setItem(r,5,tc(s.get("parent_name", " ") or " "))
            status = s.get("status", "نشط") or "نشط"
            sc = {"نشط":C['success'], "موقوف مؤقتاً":C['warning'], "منتقل": "#8250DF"}
            self.table.setItem(r,6,badge_item(status, sc.get(status, C['text_muted'])))

            w = QWidget(); wl = QHBoxLayout(w); wl.setContentsMargins(6,6,6,6); wl.setSpacing(4) 
            sid = s["id"]
            
            #  أيقونات الإجراءات ملونة
            view_b = QPushButton("👁️"); view_b.setObjectName("viewBtn")
            view_b.setToolTip("عرض الملف"); view_b.clicked.connect(lambda _,i=sid: self._view(i))
            
            edit_b = QPushButton("✏️"); edit_b.setObjectName("editBtn")
            edit_b.setToolTip("تعديل"); edit_b.clicked.connect(lambda _,i=sid: self._edit(i))
            
            del_b  = QPushButton("🗑️"); del_b.setObjectName("deleteBtn")
            del_b.setToolTip("حذف"); del_b.clicked.connect(lambda _,i=sid: self._del(i))
            
            wl.addWidget(view_b); wl.addWidget(edit_b); wl.addWidget(del_b); wl.addStretch()
            self.table.setCellWidget(r,7,w)

    def _update_kpi(self, search=""):
        """تحديث بطاقات الإحصائيات"""
        # تنظيف البطاقات القديمة
        while self.kpi_row.count():
            w = self.kpi_row.takeAt(0).widget()
            if w: w.setParent(None)
        
        # جلب البيانات
        try:
            all_students = DB.get_students(self.sid, search)
            total = len(all_students)
            
            males = sum(1 for s in all_students if dict(s).get("gender") == "ذكر")
            females = total - males
            
            active = sum(1 for s in all_students if dict(s).get("status") == "نشط")
            transferred = sum(1 for s in all_students if dict(s).get("status") == "منتقل")
        except Exception:
            total = males = females = active = transferred = 0
        
        # إضافة البطاقات
        self.kpi_row.addWidget(StudentKPICard("👥", "إجمالي الطلاب", total, C['primary']))
        self.kpi_row.addWidget(StudentKPICard("👦", "الذكور", males, "#3B82F6"))
        self.kpi_row.addWidget(StudentKPICard("👧", "الإناث", females, "#EC4899"))
        self.kpi_row.addWidget(StudentKPICard("✅", "النشطين", active, C['success']))
        self.kpi_row.addWidget(StudentKPICard("", "المنقولين", transferred, "#8250DF"))

    def _view_selected(self):
        r = self.table.currentRow()
        if r >= 0:
            sid = int(self.table.item(r,0).text())
            self._view(sid)

    def _view(self, sid): StudentProfileDialog(self, sid, self.sid, self.ui).exec()
    
    def _add(self):
        dlg = StudentFormDialog(self, None, self.sid)
        if dlg.exec() and (d := dlg.get_data()).get("full_name"):
            DB.add_student(self.sid, d, self.ui.get("full_name", " ")); self.refresh()

    def _edit(self, sid):
        s = DB.get_student(sid)
        if not s: return
        dlg = StudentFormDialog(self, s, self.sid)
        if dlg.exec():
            DB.update_student(sid, dlg.get_data(), self.sid, self.ui.get("full_name", " ")); self.refresh()

    def _del(self, sid):
        s = DB.get_student(sid)
        if not s: return
        s = dict(s)
        if QMessageBox.question(self, "تأكيد", f"حذف الطالب {s['full_name']}؟",
                                QMessageBox.Yes|QMessageBox.No) == QMessageBox.Yes:
            DB.delete_student(sid, self.sid, self.ui.get("full_name", " ")); self.refresh()

    def _import(self):
        path, _ = QFileDialog.getOpenFileName(self, "استيراد Excel", "", "Excel (*.xlsx *.xls)")
        if path:
            try:
                cnt = DB.import_students_excel(self.sid, path, self.ui.get("full_name", " "))
                QMessageBox.information(self, "تم", f"✅  تم استيراد {cnt} طالب من Excel"); self.refresh()
            except Exception as ex:
                QMessageBox.critical(self, "خطأ", str(ex))

    def _import_word(self):
        path, _ = QFileDialog.getOpenFileName(self, "استيراد Word", "", "Word (*.docx)")
        if not path:
            return
        try:
            cnt, err = DB.import_students_word(self.sid, path, self.ui.get("full_name", " "))
            if err:
                QMessageBox.critical(self, "خطأ", err)
            else:
                QMessageBox.information(self, "تم", f"✅  تم استيراد {cnt} طالب من Word")
                self.refresh()
        except Exception as ex:
            QMessageBox.critical(self, "خطأ", str(ex))

    def _import_scan(self):
        path, _ = QFileDialog.getOpenFileName(self, "اختر صورة السجل", "", "Images (*.jpg *.jpeg *.png *.bmp)")
        if not path:
            return
        prog = QProgressDialog("جاري تحليل الصورة...", None, 0, 0, self)
        prog.setWindowModality(Qt.WindowModal)
        prog.setWindowTitle("استيراد بالمسح الضوئي")
        prog.show()
        QApplication.processEvents()
        try:
            extracted_text = ""
            try:
                from PIL import Image
                import pytesseract
                img = Image.open(path)
                extracted_text = pytesseract.image_to_string(img, lang="ara")
            except ImportError:
                prog.close()
                QMessageBox.warning(self, "تنبيه",
                    "لتفعيل ميزة المسح الضوئي يجب تثبيت:\n"
                    "pip install pillow pytesseract\n"
                    "وتثبيت Tesseract OCR مع ملف اللغة العربية (ara.traineddata)")
                return
            if extracted_text.strip():
                lines = [l.strip() for l in extracted_text.split("\n") if l.strip()]
                students_added = 0
                db2 = DB.conn()
                school = db2.execute("SELECT fee_amount FROM schools WHERE id=?", (self.sid,)).fetchone()
                fee = school["fee_amount"] if school else 1500000
                for line in lines:
                    if any(kw in line for kw in ["الاسم", "رقم", "#", "م", "الصف", "ت"]):
                        continue
                    parts = line.split()
                    if len(parts) >= 3:
                        name = " ".join(parts[:3])
                        try:
                            db2.execute("INSERT INTO students (school_id,full_name,status) VALUES (?,?,?)",
                                        (self.sid, name, "نشط"))
                            sid2 = db2.execute("SELECT last_insert_rowid()").fetchone()[0]
                            db2.execute("INSERT INTO fees (student_id,total_amount,paid_amount) VALUES (?,?,0)", (sid2, fee))
                            students_added += 1
                        except Exception:
                            pass
                db2.commit(); db2.close()
                prog.close()
                if students_added > 0:
                    QMessageBox.information(self, "تم المسح",
                        f"تم استخراج وإضافة {students_added} طالب.\n"
                        "راجع البيانات وعدّل ما يلزم.")
                    self.refresh()
                else:
                    QMessageBox.warning(self, "تنبيه", "لم يتمكن البرنامج من استخراج أسماء واضحة.\n"
                                         "تأكد من وضوح الصورة واتجاهها.")
            else:
                prog.close()
                QMessageBox.warning(self, "تنبيه", "تعذّر قراءة الصورة. تأكد من وضوحها.")
        except Exception as ex:
            prog.close()
            QMessageBox.critical(self, "خطأ", str(ex))

# ─── Student Form ─────────────────────────────────────────────
class StudentFormDialog(QDialog):
    def __init__(self, parent, student, school_id):
        super().__init__(parent)
        self.student = dict(student) if student else None
        self.school_id = school_id
        self.photo_path = (self.student or {}).get("photo_path","")
        self.setWindowTitle("تعديل الطالب" if student else "إضافة طالب جديد")
        self.setFixedWidth(560); self.setLayoutDirection(Qt.RightToLeft)
        self.setStyleSheet(MAIN_STYLE)
        self._build()

    def _build(self):
        lay = QVBoxLayout(self); lay.setContentsMargins(28,22,28,22); lay.setSpacing(14)

        title_lbl = QLabel("‍🎓   " + self.windowTitle())
        title_lbl.setStyleSheet("font-size: 15px; font-weight: bold; color: #1F2328;")
        lay.addWidget(title_lbl); lay.addWidget(divider())

        tabs = QTabWidget(); lay.addWidget(tabs)

        # ── Tab 1: أساسي ──
        t1 = QWidget(); t1.setStyleSheet("background: white;")
        t1l = QVBoxLayout(t1); t1l.setContentsMargins(16,16,16,16); t1l.setSpacing(10)

        r1 = QHBoxLayout(); r1.setSpacing(12)
        self.name = QLineEdit(); self.name.setPlaceholderText("الاسم الرباعي للطالب")
        col_a = QWidget(); cal = QVBoxLayout(col_a); cal.setContentsMargins(0,0,0,0); cal.setSpacing(4)
        cal.addWidget(QLabel("الاسم الكامل *")); cal.addWidget(self.name)
        r1.addWidget(col_a, 2)
        self.birth = QSpinBox(); self.birth.setRange(2000,2020); self.birth.setValue(2014)
        col_b = QWidget(); cbl = QVBoxLayout(col_b); cbl.setContentsMargins(0,0,0,0); cbl.setSpacing(4)
        cbl.addWidget(QLabel("سنة الميلاد")); cbl.addWidget(self.birth)
        r1.addWidget(col_b, 1); t1l.addLayout(r1)

        r2 = QHBoxLayout(); r2.setSpacing(12)
        self.gender = QComboBox(); self.gender.addItems(["ذكر", "أنثى"])
        col_c = QWidget(); ccl = QVBoxLayout(col_c); ccl.setContentsMargins(0,0,0,0); ccl.setSpacing(4)
        ccl.addWidget(QLabel("الجنس")); ccl.addWidget(self.gender); r2.addWidget(col_c)

        self.grade = QComboBox()
        self.grade.addItems(GRADE_NAMES)
        col_d = QWidget(); cdl = QVBoxLayout(col_d); cdl.setContentsMargins(0,0,0,0); cdl.setSpacing(4)
        cdl.addWidget(QLabel("الصف")); cdl.addWidget(self.grade); r2.addWidget(col_d, 2)

        self.section = QComboBox(); self.section.addItems(["أ", "ب", "ج", "د", "هـ"])
        col_e = QWidget(); cel = QVBoxLayout(col_e); cel.setContentsMargins(0,0,0,0); cel.setSpacing(4)
        cel.addWidget(QLabel("الشعبة")); cel.addWidget(self.section); r2.addWidget(col_e)
        t1l.addLayout(r2)

        if self.student:
            self.status = QComboBox(); self.status.addItems(["نشط", "موقوف مؤقتاً", "منتقل"])
            field_group("الحالة", self.status, t1l)

        self.notes = QLineEdit(); self.notes.setPlaceholderText("ملاحظات اختيارية")
        field_group("ملاحظات", self.notes, t1l)
        t1l.addStretch(); tabs.addTab(t1, "البيانات الأساسية")

        # ── Tab 2: التواصل ──
        t2 = QWidget(); t2.setStyleSheet("background: white;")
        t2l = QVBoxLayout(t2); t2l.setContentsMargins(16,16,16,16); t2l.setSpacing(10)

        self.phone = QLineEdit(); self.phone.setLayoutDirection(Qt.LeftToRight)
        field_group("هاتف الطالب", self.phone, t2l)
        self.address = QLineEdit(); field_group("العنوان", self.address, t2l)
        t2l.addWidget(divider())
        self.p_name  = QLineEdit(); field_group("اسم ولي الأمر", self.p_name, t2l)
        self.p_phone = QLineEdit(); self.p_phone.setLayoutDirection(Qt.LeftToRight)
        field_group("هاتف ولي الأمر", self.p_phone, t2l)
        self.p_job   = QLineEdit(); field_group("مهنة ولي الأمر", self.p_job, t2l)
        t2l.addStretch(); tabs.addTab(t2, "التواصل وولي الأمر")

        # ─ Tab 3: الصورة ──
        t3 = QWidget(); t3.setStyleSheet("background: white;")
        t3l = QVBoxLayout(t3); t3l.setContentsMargins(16,16,16,16); t3l.setSpacing(12)
        self.photo_lbl = QLabel("لا توجد صورة")
        self.photo_lbl.setAlignment(Qt.AlignCenter)
        self.photo_lbl.setFixedHeight(160)
        self.photo_lbl.setStyleSheet(f"""
            background: {C['bg_page']}; border-radius: 12px;
            border: 2px dashed {C['border']}; color: {C['text_muted']}; font-size: 13px;
        """)
        pick = gb("📷  اختر صورة"); pick.clicked.connect(self._pick_photo)
        t3l.addWidget(self.photo_lbl); t3l.addWidget(pick); t3l.addStretch()
        tabs.addTab(t3, "الصورة الشخصية")

        # Prefill
        if self.student:
            s = self.student
            self.name.setText(s.get("full_name", " "))
            self.birth.setValue(s.get("birth_year") or 2014)
            self.gender.setCurrentText(s.get("gender", "ذكر"))
            if s.get("grade"): self.grade.setCurrentText(s["grade"])
            if s.get("section"): self.section.setCurrentText(s["section"])
            self.status.setCurrentText(s.get("status", "نشط"))
            self.notes.setText(s.get("notes", " ") or " ")
            self.phone.setText(s.get("phone", " ") or " ")
            self.address.setText(s.get("address", " ") or " ")
            self.p_name.setText(s.get("parent_name", " ") or " ")
            self.p_phone.setText(s.get("parent_phone", " ") or " ")
            self.p_job.setText(s.get("parent_job", " ") or " ")
            pp = s.get("photo_path", " ")
            if pp and os.path.exists(pp):
                pix = QPixmap(pp).scaled(140,140,Qt.KeepAspectRatio,Qt.SmoothTransformation)
                self.photo_lbl.setPixmap(pix)

        btns = QDialogButtonBox(QDialogButtonBox.Save|QDialogButtonBox.Cancel)
        btns.button(QDialogButtonBox.Save).setText("💾  حفظ")
        btns.button(QDialogButtonBox.Save).setObjectName("primaryBtn")
        btns.button(QDialogButtonBox.Cancel).setText("إلغاء")
        btns.accepted.connect(self._ok); btns.rejected.connect(self.reject)
        lay.addWidget(btns)

    def _pick_photo(self):
        p,_ = QFileDialog.getOpenFileName(self, "اختر صورة", "", "Images (*.png *.jpg *.jpeg)")
        if p:
            self.photo_path = p
            pix = QPixmap(p).scaled(140,140,Qt.KeepAspectRatio,Qt.SmoothTransformation)
            self.photo_lbl.setPixmap(pix)

    def _ok(self):
        if not self.name.text().strip():
            QMessageBox.warning(self, "خطأ", "الاسم الكامل مطلوب"); return
        self.accept()

    def get_data(self):
        return {
            "full_name":   self.name.text().strip(),
            "birth_year":  self.birth.value(),
            "gender":      self.gender.currentText(),
            "grade":       self.grade.currentText(),
            "section":     self.section.currentText(),
            "phone":       self.phone.text().strip(),
            "address":     self.address.text().strip(),
            "parent_name": self.p_name.text().strip(),
            "parent_phone":self.p_phone.text().strip(),
            "parent_job":  self.p_job.text().strip(),
            "notes":       self.notes.text().strip(),
            "photo_path":  self.photo_path,
            "status": getattr(self, "status",None) and self.status.currentText() or "نشط",
        }

# ─── Student Profile ──────────────────────────────────────────
class StudentProfileDialog(QDialog):
    def __init__(self, parent, student_id, school_id, user_info):
        super().__init__(parent)
        self.student_id = student_id; self.school_id = school_id; self.ui = user_info
        self.setWindowTitle("ملف الطالب")
        self.setFixedSize(660, 580); self.setLayoutDirection(Qt.RightToLeft)
        self.setStyleSheet(MAIN_STYLE); self._build()

    def _build(self):
        s = DB.get_student(self.student_id)
        if not s: return
        s = dict(s)
        lay = QVBoxLayout(self); lay.setContentsMargins(22,18,22,18); lay.setSpacing(14)
 
        # Header
        hdr = QHBoxLayout(); hdr.setSpacing(16)
        photo_lbl = QLabel()
        photo_lbl.setFixedSize(76,76)
        pp = s.get("photo_path", " ")
        if pp and os.path.exists(pp):
            pix = QPixmap(pp).scaled(76,76,Qt.KeepAspectRatioByExpanding,Qt.SmoothTransformation)
            photo_lbl.setPixmap(pix); photo_lbl.setScaledContents(True)
            photo_lbl.setStyleSheet("border-radius: 38px;")
        else:
            photo_lbl.setText(s["full_name"][0])
            photo_lbl.setAlignment(Qt.AlignCenter)
            photo_lbl.setStyleSheet(f"background: {C['primary']}; color: white; font-size: 30px; font-weight: bold; border-radius: 38px;")
        hdr.addWidget(photo_lbl)

        info_col = QVBoxLayout(); info_col.setSpacing(4)
        name_lbl = QLabel(s["full_name"])
        name_lbl.setStyleSheet("font-size: 18px; font-weight: bold; color: #1F2328;")
        grade_lbl = QLabel(f"{s.get('grade','')}  —  شعبة {s.get('section','')}  |  مواليد {s.get('birth_year','')}")
        grade_lbl.setStyleSheet(f"color: {C['text_sec']}; font-size: 13px;")
        status = s.get("status", "نشط")
        sc = {"نشط":C['success'], "موقوف مؤقتاً":C['warning'], "منتقل": "#8250DF"}
        st_lbl = QLabel(f"  {status}  ")
        clr = sc.get(status, C['text_muted'])
        st_lbl.setStyleSheet(f"background: {clr}18; color: {clr}; border-radius: 10px; padding: 2px 8px; font-size: 11px; font-weight: bold;")
        info_col.addWidget(name_lbl); info_col.addWidget(grade_lbl); info_col.addWidget(st_lbl)
        hdr.addLayout(info_col); hdr.addStretch()

        # QR Code
        try:
            import qrcode
            from PIL import Image
            from PIL.ImageQt import ImageQt
            qr_data = f"STUDENT\nID:{s['id']}\nNAME:{s['full_name']}\nGRADE:{s.get('grade','')}\nSECT:{s.get('section','')}"
            qr = qrcode.QRCode(version=1, box_size=4, border=2)
            qr.add_data(qr_data); qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            qimage = ImageQt(img.convert("RGB"))
            pix = QPixmap.fromImage(QImage(qimage)).scaled(80,80,Qt.KeepAspectRatio,Qt.SmoothTransformation)
            qr_lbl = QLabel(); qr_lbl.setPixmap(pix)
            qr_lbl.setToolTip("امسح الكود للوصول السريع لبيانات الطالب")
            hdr.addWidget(qr_lbl)
        except Exception: pass

        lay.addLayout(hdr)
        lay.addWidget(divider())

        # Tabs
        tabs = QTabWidget()

        # Info
        t1 = QWidget();  t1.setStyleSheet("background: white;")
        t1l = QVBoxLayout(t1); t1l.setContentsMargins(14,14,14,14); t1l.setSpacing(8)
        for k, v in [("هاتف الطالب",s.get("phone","")),("العنوان",s.get("address","")),
                     ("اسم ولي الأمر",s.get("parent_name","")),("هاتف ولي الأمر",s.get("parent_phone","")),
                     ("مهنة ولي الأمر",s.get("parent_job","")),("ملاحظات",s.get("notes",""))]:
            if not v: continue
            row = QHBoxLayout()
            lbl = QLabel(f"{k}: "); lbl.setFixedWidth(140)
            lbl.setStyleSheet(f"color: {C['text_muted']}; font-size: 12px;")
            val = QLabel(str(v)); val.setStyleSheet(f"color: {C['text']}; font-size: 13px;")
            row.addWidget(lbl); row.addWidget(val); row.addStretch(); t1l.addLayout(row)
        t1l.addStretch(); tabs.addTab(t1, "المعلومات")

        # Fees
        t2 = QWidget(); t2.setStyleSheet("background: white;")
        t2l = QVBoxLayout(t2); t2l.setContentsMargins(14,14,14,14); t2l.setSpacing(10)
        db = DB.conn()
        fee = db.execute("SELECT * FROM fees WHERE student_id=?", (self.student_id,)).fetchone()
        pays = db.execute("SELECT * FROM fee_payments WHERE student_id=? ORDER BY id DESC", (self.student_id,)).fetchall()
        db.close()
        if fee:
            fee = dict(fee); total = fee["total_amount"]; paid = fee["paid_amount"]; rem = total-paid
            pct = int(paid/total*100) if total else 0
            for lbl, val, clr in [("المبلغ الكلي",f"{int(total):,} دينار",C['text']),
                                   ("المدفوع",f"{int(paid):,} دينار",C['success']),
                                   ("المتبقي",f"{int(rem):,} دينار",C['danger'] if rem >0 else C['text_muted'])]:
                h = QHBoxLayout()
                l = QLabel(f"{lbl}: "); l.setFixedWidth(100); l.setStyleSheet(f"color:{C['text_muted']};")
                v2 = QLabel(val); v2.setStyleSheet(f"color:{clr}; font-weight:bold;")
                h.addWidget(l); h.addWidget(v2); h.addStretch(); t2l.addLayout(h)
            pb2 = QProgressBar(); pb2.setValue(pct)
            pb2.setStyleSheet(f"QProgressBar::chunk {{ background: {C['success'] if pct==100 else C['primary']}; border-radius: 5px; }}")
            t2l.addWidget(pb2)
        pt = mk_table(["المبلغ", "التاريخ", "الموظف", "ملاحظات"])
        pt.setFixedHeight(130)
        for r, p in enumerate(pays):
            p = dict(p); pt.setRowCount(r+1); pt.setRowHeight(r,32)
            pt.setItem(r,0,tc(f"{int(p['amount']):,}",color=C['success']))
            pt.setItem(r,1,tc(p.get("payment_date","") or " "))
            pt.setItem(r,2,tc(p.get("employee","") or " "))
            pt.setItem(r,3,tc(p.get("notes","") or " "))
        t2l.addWidget(pt); t2l.addStretch(); tabs.addTab(t2, "الأقساط")

        # Files archive
        t3 = QWidget(); t3.setStyleSheet("background: white;")
        self.t3l = QVBoxLayout(t3); self.t3l.setContentsMargins(14,14,14,14); self.t3l.setSpacing(8)
        fhdr = QHBoxLayout()
        fhdr.addWidget(QLabel("الملفات المرفقة")); fhdr.addStretch()
        add_f = gb("➕  إضافة ملف"); add_f.clicked.connect(lambda: self._add_file())
        fhdr.addWidget(add_f); self.t3l.addLayout(fhdr)
        self._load_files(); tabs.addTab(t3, "أرشيف الملفات")

        lay.addWidget(tabs)
        close_b = pb("إغلاق"); close_b.clicked.connect(self.accept)
        lay.addWidget(close_b, alignment=Qt.AlignLeft)

    def _load_files(self):
        while self.t3l.count() > 1:
            it = self.t3l.takeAt(1)
            if it.widget(): it.widget().setParent(None)
        files = DB.get_student_files(self.student_id)
        for f in files:
            f = dict(f);  row = QFrame()
            row.setStyleSheet(f"background: {C['bg_page']}; border-radius: 8px; border: 1px solid {C['border']};")
            rl = QHBoxLayout(row); rl.setContentsMargins(12,8,12,8)
            icons = {"جنسية": "🪪", "بطاقة وطنية": "", "شهادة ميلاد": "📄", "صورة": "📷"}
            icon = icons.get(f.get("file_type", ""), "📎")
            lbl = QLabel(f"  {icon}  {f.get('file_type','')}  —  {os.path.basename(f.get('file_path',''))}")
            lbl.setStyleSheet(f"color: {C['text']}; background: transparent;")
            rl.addWidget(lbl); rl.addStretch()
            ob = ib("فتح"); ob.clicked.connect(lambda _, p=f.get("file_path",""): self._open(p))
            rl.addWidget(ob); self.t3l.addWidget(row)
        if not files:
            el = QLabel("  لا توجد ملفات مرفقة بعد")
            el.setStyleSheet(f"color: {C['text_muted']}; font-size: 12px;")
            self.t3l.addWidget(el)
        self.t3l.addStretch()

    def _add_file(self):
        ftype, ok = QInputDialog.getItem(self, "نوع الملف", "اختر نوع الملف: ",
            ["جنسية", "بطاقة وطنية", "شهادة ميلاد", "صورة", "أخرى"],editable=False)
        if not ok: return
        path,_ = QFileDialog.getOpenFileName(self, "اختر الملف", "", "All Files (*.*)")
        if not path: return
        dest_dir = os.path.join(os.path.expanduser("~"), "school_pro_files",str(self.student_id))
        os.makedirs(dest_dir, exist_ok=True)
        dest = os.path.join(dest_dir, os.path.basename(path))
        shutil.copy2(path, dest); DB.add_student_file(self.student_id, ftype, dest)
        self._load_files()

    def _open(self, path):
        if not os.path.exists(path):
            QMessageBox.warning(self, "خطأ", "الملف غير موجود"); return
        import subprocess, platform
        if platform.system()=="Windows": os.startfile(path)
        elif platform.system()=="Darwin": subprocess.run(["open",path])
        else: subprocess.run(["xdg-open",path])

# ══════════════════════════════════════════
# FEES
# ══════════════════════════════════════════
class FeesPage(BasePage):
    def __init__(self, school_id, user_info):
        super().__init__(school_id, user_info)
        main = QVBoxLayout(self); main.setContentsMargins(20,14,20,14); main.setSpacing(12)
        self.kpi_row = QHBoxLayout(); self.kpi_row.setSpacing(12)
        main.addLayout(self.kpi_row)
        filt_row = QHBoxLayout()
        self.filter_cb = QComboBox(); self.filter_cb.addItems(["الكل", "مكتمل", "جزئي", "لم يُسدَّد"])
        self.filter_cb.currentTextChanged.connect(self._apply)
        filt_row.addWidget(QLabel("تصفية: ")); filt_row.addWidget(self.filter_cb)
        filt_row.addStretch()
        exp = gb("📥  تصدير Excel"); exp.clicked.connect(self._export)
        filt_row.addWidget(exp); main.addLayout(filt_row)

        self.table = mk_table(["#", "الطالب", "الصف", "الكلي", "المدفوع", "المتبقي", "نسبة التحصيل", "الحالة", "دفع"])
        self.table.setColumnWidth(0,50); self.table.setColumnWidth(8,110)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        main.addWidget(self.table)
        self._data = []

    def refresh(self, *_):
        while self.kpi_row.count():
            w = self.kpi_row.takeAt(0).widget()
            if w: w.setParent(None)
        self._data = DB.get_fees(self.sid)
        tot  = sum(f["total_amount"] or 0 for f in self._data)
        paid = sum(f["paid_amount"]  or 0 for f in self._data)
        pct  = int(paid/tot*100) if tot else 0
        for icon,lbl,val,sub,clr in [
            ("📋", "إجمالي الأقساط",f"{tot/1e6:.1f}M", " ",C['text']),
            ("✅", "المحصّل",f"{paid/1e6:.1f}M", " ",C['success']),
            ("⏳", "المتبقي",f"{(tot-paid)/1e6:.1f}M", " ",C['danger']),
            ("📊", "نسبة التحصيل",f"{pct}%", " ",C['primary']),
        ]:
            self.kpi_row.addWidget(KPICard(icon,lbl,val,sub,clr))
        self._apply(self.filter_cb.currentText())

    def _apply(self, f):
        data = self._data
        if f=="مكتمل": data=[x for x in data if (x["remaining"] or 0) <=0]
        elif f=="جزئي": data=[x for x in data if 0 <(x["paid_amount"] or 0) <(x["total_amount"] or 0)]
        elif f=="لم يُسدَّد": data=[x for x in data if (x["paid_amount"] or 0)==0]
        self.table.setRowCount(len(data))
        for r, fee in enumerate(data):
            self.table.setRowHeight(r, 46)
            fee = dict(fee)
            tot=fee["total_amount"] or 0; paid=fee["paid_amount"] or 0; rem=fee["remaining"] or 0
            pct=int(paid/tot*100) if tot else 0
            status="مكتمل" if rem <=0 else ("جزئي" if paid >0 else "لم يُسدَّد")
            sc={"مكتمل":C['success'], "جزئي":C['warning'], "لم يُسدَّد":C['danger']}[status]

            self.table.setItem(r,0,tc(str(fee["id"]),Qt.AlignCenter,C['text_muted']))
            self.table.setItem(r,1,tc(fee["full_name"],bold=True))
            self.table.setItem(r,2,tc(fee.get("grade", " ") or " "))
            self.table.setItem(r,3,tc(f"{int(tot):,}",Qt.AlignCenter))
            self.table.setItem(r,4,tc(f"{int(paid):,}",Qt.AlignCenter,C['success']))
            self.table.setItem(r,5,tc(f"{int(rem):,}",Qt.AlignCenter,C['danger'] if rem >0 else C['text_muted']))

            bw = QWidget(); bl = QHBoxLayout(bw); bl.setContentsMargins(6,8,6,8); bl.setSpacing(6)
            bar = MiniBar(pct, sc); pl = QLabel(f"{pct}%"); pl.setStyleSheet(f"color:{sc}; font-size:11px; font-weight:bold;")
            bl.addWidget(bar); bl.addWidget(pl); self.table.setCellWidget(r,6,bw)

            self.table.setItem(r,7,badge_item(status,sc))
            pay_b = pb("💵  دفع"); pay_b.setEnabled(rem >0); pay_b.setFixedHeight(30)
            sid=fee["id"]; name=fee["full_name"]
            pay_b.clicked.connect(lambda _,i=sid,n=name: self._pay(i,n))
            w=QWidget(); wl=QHBoxLayout(w); wl.setContentsMargins(4,6,4,6); wl.addWidget(pay_b)
            self.table.setCellWidget(r,8,w)

    def _pay(self, student_id, name):
        dlg = QDialog(self); dlg.setWindowTitle("تسجيل دفعة"); dlg.setFixedWidth(380)
        dlg.setLayoutDirection(Qt.RightToLeft); dlg.setStyleSheet(MAIN_STYLE)
        lay = QVBoxLayout(dlg); lay.setContentsMargins(24,20,24,20); lay.setSpacing(12)
        hdr = QLabel("💰  دفعة جديدة")
        hdr.setStyleSheet("font-size: 15px; font-weight: bold;")
        lay.addWidget(hdr)
        st_lbl = QLabel(f"الطالب: {name}")
        st_lbl.setStyleSheet(f"color: {C['text_sec']}; font-size: 13px; background: {C['bg_page']}; border-radius: 8px; padding: 8px 12px;")
        lay.addWidget(st_lbl); lay.addWidget(divider())

        amt = QLineEdit(); amt.setPlaceholderText("مثال: 500000")
        field_group("المبلغ المدفوع (دينار) *", amt, lay)
        emp = QLineEdit(); emp.setText(self.ui.get("full_name", " "))
        field_group("الموظف المستلم", emp, lay)
        notes = QLineEdit(); field_group("ملاحظات", notes, lay)

        btns = QDialogButtonBox(QDialogButtonBox.Save|QDialogButtonBox.Cancel)
        btns.button(QDialogButtonBox.Save).setText("✅  تسجيل الدفعة")
        btns.button(QDialogButtonBox.Save).setObjectName("primaryBtn")
        btns.accepted.connect(dlg.accept); btns.rejected.connect(dlg.reject)
        lay.addWidget(btns)
        if dlg.exec():
            try: amount = float(amt.text().replace(",", " "))
            except: QMessageBox.warning(self, "خطأ", "أدخل مبلغاً صحيحاً"); return
            DB.add_payment(student_id, amount, emp.text(), notes.text(), self.sid, self.ui.get("full_name", " "))
            self.refresh()

    def _export(self):
        try:
            from reports.exports import export_fees_excel
            path = export_fees_excel(self._data)
            QMessageBox.information(self, "تم التصدير", f"✅  تم الحفظ:\n{path}")
        except Exception as e: QMessageBox.warning(self, "خطأ", str(e))

# ══════════════════════════════════════════
# ATTENDANCE
# ══════════════════════════════════════════
class AttendancePage(BasePage):
    def __init__(self, school_id, user_info):
        super().__init__(school_id, user_info); self._checks = {}
        main = QVBoxLayout(self); main.setContentsMargins(20,14,20,14); main.setSpacing(12)
        ctrl = QFrame(); ctrl.setObjectName("card"); ctrl.setFixedHeight(60)
        cl = QHBoxLayout(ctrl); cl.setContentsMargins(16,0,16,0); cl.setSpacing(12)
        cl.addWidget(QLabel("الصف: "))
        self.grade_cb = QComboBox()
        self.grade_cb.addItems(GRADE_NAMES)
        cl.addWidget(self.grade_cb)
        cl.addWidget(QLabel("الشعبة: "))
        self.sec_cb = QComboBox(); self.sec_cb.addItems(["أ", "ب", "ج", "د"])
        cl.addWidget(self.sec_cb)
        cl.addWidget(QLabel("التاريخ: "))
        self.date_e = QDateEdit(QDate.currentDate()); self.date_e.setCalendarPopup(True)
        cl.addWidget(self.date_e)
        load = gb("📋  تحميل الكشف"); load.clicked.connect(self._load); cl.addWidget(load)
        cl.addStretch()
        save = pb("💾  حفظ الغياب"); save.clicked.connect(self._save); cl.addWidget(save)
        main.addWidget(ctrl)

        self.summary = QLabel()
        self.summary.setStyleSheet(f"background: {C['bg_card']}; border: 1px solid {C['border']}; border-radius: 8px; padding: 8px 16px; color: {C['text_sec']}; font-size: 12px;")
        self.summary.setFixedHeight(38)
        main.addWidget(self.summary)

        scroll = QScrollArea(); scroll.setWidgetResizable(True); scroll.setFrameShape(QFrame.NoFrame)
        self.inner = QWidget(); self.inner.setStyleSheet("background: transparent;")
        self.inner_lay = QVBoxLayout(self.inner)
        self.inner_lay.setContentsMargins(0,0,0,0); self.inner_lay.setSpacing(6)
        scroll.setWidget(self.inner); main.addWidget(scroll)

    def refresh(self, *_): pass

    def _load(self):
        for i in reversed(range(self.inner_lay.count())):
            w = self.inner_lay.itemAt(i).widget()
            if w: w.setParent(None) 
        self._checks = {}
        students = DB.get_students_for_attendance(self.sid, self.grade_cb.currentText(), self.sec_cb.currentText())
        for s in students:
            s = dict(s)
            present = s.get("today_status", "حاضر") != "غائب"
            row = QFrame()
            self._style_row(row, present)
            rl = QHBoxLayout(row); rl.setContentsMargins(16,10,16,10); rl.setSpacing(16)
            cb = QCheckBox(); cb.setChecked(present); cb.setFixedSize(22,22)
            name_l = QLabel(s["full_name"])
            name_l.setStyleSheet("font-size: 13px; font-weight: bold; background: transparent;")
            status_l = QLabel("غائب")
            status_l.setStyleSheet(f"color: {C['danger']}; font-size: 12px; font-weight: bold; background: transparent;")
            status_l.setVisible(not present)
            def on_toggle(checked, r=row, sl=status_l):
                self._style_row(r, checked); sl.setVisible(not checked); self._upd_summary()
            cb.toggled.connect(on_toggle)
            rl.addWidget(cb); rl.addWidget(name_l); rl.addStretch(); rl.addWidget(status_l)
            self._checks[s["id"]] = cb; self.inner_lay.addWidget(row)
        self.inner_lay.addStretch(); self._upd_summary()

    def _style_row(self, row, present):
        bg = "white" if present else C['danger_lt']
        border = C['border'] if present else C['danger']
        row.setStyleSheet(f"background: {bg}; border: 1px solid {border}; border-radius: 10px;")

    def _upd_summary(self):
        tot = len(self._checks); present = sum(1 for c in self._checks.values() if c.isChecked())
        self.summary.setText(f"  الإجمالي: {tot}  |  ✅ حاضر: {present}  |  ❌ غائب: {tot-present}")

    def _save(self):
        if not self._checks:
            QMessageBox.warning(self, "تنبيه", "حمّل الكشف أولاً"); return
        date_str = self.date_e.date().toString("yyyy-MM-dd")
        records = {sid:("حاضر" if cb.isChecked() else "غائب") for sid,cb in self._checks.items()}
        DB.save_attendance(date_str, records, self.sid, self.ui.get("full_name", " "))
        QMessageBox.information(self, "تم", f"✅  تم حفظ كشف يوم {date_str}")

# ══════════════════════════════════════════
# GRADES
# ══════════════════════════════════════════
class GradesPage(BasePage):
    def __init__(self, school_id, user_info):
        super().__init__(school_id, user_info)
        main = QVBoxLayout(self); main.setContentsMargins(20,14,20,14); main.setSpacing(12)
        ctrl = QHBoxLayout(); ctrl.setSpacing(10)
        ctrl.addWidget(QLabel("الطالب: "))
        self.student_cb = QComboBox(); self.student_cb.setMinimumWidth(240)
        self.student_cb.currentIndexChanged.connect(self._load)
        ctrl.addWidget(self.student_cb); ctrl.addStretch()
        add = pb("➕  إضافة درجة"); add.clicked.connect(self._add); ctrl.addWidget(add)
        main.addLayout(ctrl)

        split = QHBoxLayout(); split.setSpacing(16)
        lc = card(); ll = QVBoxLayout(lc); ll.setContentsMargins(16,14,16,14); ll.setSpacing(8)
        ll.addWidget(section_title("📋  درجات الطالب"))
        self.grades_t = mk_table(["المادة", "الدرجة", "النوع", "الفصل"])
        self.grades_t.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        ll.addWidget(self.grades_t); split.addWidget(lc, 3)

        rc = card(); rl = QVBoxLayout(rc); rl.setContentsMargins(16,14,16,14); rl.setSpacing(8)
        rl.addWidget(section_title("📊  الملخص"))
        self.avg_lbl = QLabel("—")
        self.avg_lbl.setAlignment(Qt.AlignCenter)
        self.avg_lbl.setStyleSheet(f"font-size: 42px; font-weight: bold; color: {C['primary']};")
        self.res_lbl = QLabel(); self.res_lbl.setAlignment(Qt.AlignCenter)
        self.res_lbl.setStyleSheet("font-size: 14px; font-weight: bold;")
        rl.addWidget(self.avg_lbl); rl.addWidget(self.res_lbl); rl.addStretch()
        split.addWidget(rc, 1); main.addLayout(split)

    def refresh(self, *_):
        self.student_cb.blockSignals(True); self.student_cb.clear()
        for s in DB.get_students(self.sid): self.student_cb.addItem(dict(s)["full_name"], dict(s)["id"])
        self.student_cb.blockSignals(False); self._load()

    def _load(self):
        sid = self.student_cb.currentData(); 
        if not sid: return
        grades = DB.get_grades(sid); scores = []
        self.grades_t.setRowCount(len(grades))
        for r, g in enumerate(grades):
            g = dict(g); self.grades_t.setRowHeight(r,38)
            self.grades_t.setItem(r,0,tc(g["subject"]))
            score = g["score"]
            if score is not None:
                clr = C['success'] if score >=80 else C['warning'] if score >=50 else C['danger']
                self.grades_t.setItem(r,1,tc(str(score),Qt.AlignCenter,clr,bold=True))
                scores.append(score)
            else: self.grades_t.setItem(r,1,tc("—",Qt.AlignCenter))
            self.grades_t.setItem(r,2,tc(g.get("exam_type", ""),Qt.AlignCenter))
            self.grades_t.setItem(r,3,tc(g.get("term", ""),Qt.AlignCenter))
        if scores:
            avg = sum(scores)/len(scores); passed = avg >=50
            self.avg_lbl.setText(f"{avg:.1f}")
            self.res_lbl.setText("✅  ناجح" if passed else "❌  راسب")
            self.res_lbl.setStyleSheet(f"font-size:14px; font-weight:bold; color:{C['success'] if passed else C['danger']};")
        else: self.avg_lbl.setText("—"); self.res_lbl.setText(" ")

    def _add(self):
        sid = self.student_cb.currentData()
        if not sid: return
        dlg = QDialog(self); dlg.setWindowTitle("إضافة درجة"); dlg.setFixedWidth(340)
        dlg.setLayoutDirection(Qt.RightToLeft); dlg.setStyleSheet(MAIN_STYLE)
        lay = QVBoxLayout(dlg); lay.setContentsMargins(24,20,24,20); lay.setSpacing(12)
        lay.addWidget(section_title("📊  إضافة درجة"))
        subj = QComboBox(); subj.addItems(["الرياضيات", "اللغة العربية", "اللغة الإنكليزية", "العلوم",
                                             "التربية الإسلامية", "الاجتماعيات", "التربية الرياضية"])
        field_group("المادة", subj, lay)
        sc = QDoubleSpinBox(); sc.setRange(0,100); sc.setValue(0)
        field_group("الدرجة (من 100)", sc, lay)
        et = QComboBox(); et.addItems(["فصلي", "شهري", "نهائي"])
        field_group("نوع الاختبار", et, lay)
        term = QComboBox(); term.addItems(["الأول", "الثاني", "الثالث"])
        field_group("الفصل الدراسي", term, lay)
        btns = QDialogButtonBox(QDialogButtonBox.Save|QDialogButtonBox.Cancel)
        btns.button(QDialogButtonBox.Save).setText("حفظ"); btns.button(QDialogButtonBox.Save).setObjectName("primaryBtn")
        btns.accepted.connect(dlg.accept); btns.rejected.connect(dlg.reject); lay.addWidget(btns)
        if dlg.exec():
            DB.save_grade(sid, subj.currentText(), sc.value(), et.currentText(), term.currentText(), self.sid, self.ui.get("full_name", " ")); self._load()

# ══════════════════════════════════════════
# TEACHERS
# ══════════════════════════════════════════
class TeachersPage(BasePage):
    def __init__(self, school_id, user_info):
        super().__init__(school_id, user_info)
        main = QVBoxLayout(self); main.setContentsMargins(20,14,20,14); main.setSpacing(12)
        top = QHBoxLayout(); top.addStretch()
        add = pb("➕  إضافة مدرس"); add.clicked.connect(self._add); top.addWidget(add)
        main.addLayout(top)
        self.table = mk_table(["#", "الاسم", "المواد", "الهاتف", "الراتب", "الصفوف", "الحالة", "حذف"])
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch); main.addWidget(self.table)

    def refresh(self, *_):
        teachers = DB.get_teachers(self.sid); self.table.setRowCount(len(teachers))
        for r, t in enumerate(teachers):
            t = dict(t); self.table.setRowHeight(r, 44)
            self.table.setItem(r,0,tc(str(t["id"]),Qt.AlignCenter,C['text_muted']))
            self.table.setItem(r,1,tc(t["full_name"],bold=True))
            self.table.setItem(r,2,tc(t.get("specialization", " ") or " "))
            self.table.setItem(r,3,tc(t.get("phone", " ") or " "))
            self.table.setItem(r,4,tc(f"{int(t.get('salary',0) or 0):,} د.ع",Qt.AlignCenter))
            self.table.setItem(r,5,tc(str(t.get("classes_count",0) or 0),Qt.AlignCenter))
            status = t.get("status", "نشط")
            self.table.setItem(r,6,badge_item(status, C['success'] if status=="نشط" else C['warning']))
            db = ib("🗑️", "حذف"); db.setStyleSheet(f"background:{C['danger_lt']};border-color:{C['danger']}20;color:{C['danger']};")
            tid = t["id"]; db.clicked.connect(lambda _,i=tid,n=t["full_name"]: self._del(i,n))
            w=QWidget(); wl=QHBoxLayout(w); wl.setContentsMargins(6,6,6,6); wl.addWidget(db)
            self.table.setCellWidget(r,7,w)

    def _add(self):
        dlg = QDialog(self); dlg.setWindowTitle("إضافة مدرس"); dlg.setMinimumWidth(480)
        dlg.setLayoutDirection(Qt.RightToLeft); dlg.setStyleSheet(MAIN_STYLE)
        lay = QVBoxLayout(dlg); lay.setContentsMargins(24,20,24,20); lay.setSpacing(12)
        lay.addWidget(section_title("👩‍  مدرس جديد")); lay.addWidget(divider())
        f_name = QLineEdit(); field_group("الاسم الكامل *", f_name, lay)
        f_phone = QLineEdit(); f_phone.setLayoutDirection(Qt.LeftToRight); field_group("رقم الهاتف", f_phone, lay)
        f_sal = QDoubleSpinBox(); f_sal.setRange(0,5e6); f_sal.setValue(700000)
        field_group("الراتب الشهري (دينار)", f_sal, lay)
        f_cls = QSpinBox(); f_cls.setRange(0,20); f_cls.setValue(3)
        field_group("عدد الصفوف", f_cls, lay)
        # Multi-subject support
        subj_lbl = QLabel("المواد التي يدرّسها (يمكن إضافة مادة أو أكثر)")
        subj_lbl.setStyleSheet("font-size:12px; font-weight:bold; color:#444D56;")
        lay.addWidget(subj_lbl)
        subjects_list = QListWidget(); subjects_list.setMaximumHeight(120); lay.addWidget(subjects_list)
        add_subj_row = QHBoxLayout()
        new_subj = QLineEdit(); new_subj.setPlaceholderText("مثال: الرياضيات")
        subj_grade = QComboBox()
        subj_grade.addItems(["(كل الصفوف)", "الأول الابتدائي", "الثاني الابتدائي", "الثالث الابتدائي", "الرابع الابتدائي", "الخامس الابتدائي", "السادس الابتدائي", "الأول المتوسط", "الثاني المتوسط", "الثالث المتوسط", "الرابع الإعدادي — علمي", "الرابع الإعدادي — أدبي", "الخامس الإعدادي — علمي", "الخامس الإعدادي — أدبي", "السادس الإعدادي — علمي", "السادس الإعدادي — أدبي"])
        add_s_btn = QPushButton("إضافة مادة +"); add_s_btn.setObjectName("ghostBtn")
        def _add_subj():
            s = new_subj.text().strip(); g = subj_grade.currentText()
            if s:
                label = f"{s}  —  {g}" if g != "(كل الصفوف)" else s
                item = QListWidgetItem(label); item.setData(Qt.UserRole, {"subject":s, "grade":g})
                subjects_list.addItem(item); new_subj.clear()
        add_s_btn.clicked.connect(_add_subj)
        del_s_btn = QPushButton("حذف المحدد"); del_s_btn.setObjectName("ghostBtn")
        del_s_btn.clicked.connect(lambda: subjects_list.takeItem(subjects_list.currentRow()) if subjects_list.currentRow() >=0 else None)
        add_subj_row.addWidget(new_subj,2); add_subj_row.addWidget(subj_grade,2); add_subj_row.addWidget(add_s_btn); add_subj_row.addWidget(del_s_btn)
        lay.addLayout(add_subj_row)
        btns = QDialogButtonBox(QDialogButtonBox.Save|QDialogButtonBox.Cancel)
        btns.button(QDialogButtonBox.Save).setText("حفظ"); btns.button(QDialogButtonBox.Save).setObjectName("primaryBtn")
        btns.accepted.connect(dlg.accept); btns.rejected.connect(dlg.reject); lay.addWidget(btns)
        if dlg.exec() and f_name.text().strip():
            subjects = [subjects_list.item(i).data(Qt.UserRole) for i in range(subjects_list.count())]
            spec = ", ".join([s.get("subject", "") for s in subjects]) if subjects else ""
            DB.add_teacher(self.sid, {"full_name":f_name.text(), "specialization":spec, "subjects":subjects, "phone":f_phone.text(), "salary":f_sal.value(), "classes_count":f_cls.value()}, self.ui.get("full_name", " "))
            self.refresh()

    def _del(self, tid, name):
        if QMessageBox.question(self, "تأكيد", f"حذف {name}؟", QMessageBox.Yes|QMessageBox.No)==QMessageBox.Yes:
            DB.delete_teacher(tid,self.sid,self.ui.get("full_name", " ")); self.refresh()

# ══════════════════════════════════════════
# PARENTS
# ═════════════════════════════════════════
class ParentsPage(BasePage):
    def __init__(self, school_id, user_info):
        super().__init__(school_id, user_info)
        main = QVBoxLayout(self); main.setContentsMargins(20,14,20,14); main.setSpacing(12)
        self.table = mk_table(["#", "ولي الأمر", "اسم الطالب", "الصف", "هاتف ولي الأمر", "المهنة", "العنوان"])
        main.addWidget(self.table)

    def refresh(self, *_):
        students = DB.get_students(self.sid); self.table.setRowCount(len(students))
        for r, s in enumerate(students):
            s = dict(s); self.table.setRowHeight(r,40)
            self.table.setItem(r,0,tc(str(s["id"]),Qt.AlignCenter,C['text_muted']))
            self.table.setItem(r,1,tc(s.get("parent_name", " ") or "—",bold=True))
            self.table.setItem(r,2,tc(s["full_name"]))
            self.table.setItem(r,3,tc(s.get("grade", " ") or " "))
            self.table.setItem(r,4,tc(s.get("parent_phone", " ") or " "))
            self.table.setItem(r,5,tc(s.get("parent_job", " ") or " "))
            self.table.setItem(r,6,tc(s.get("address", " ") or " "))

# ══════════════════════════════════════════
# ACCOUNTING
# ══════════════════════════════════════════
class AccountingPage(BasePage):
    def __init__(self, school_id, user_info):
        super().__init__(school_id, user_info)
        main = QVBoxLayout(self); main.setContentsMargins(20,14,20,14); main.setSpacing(12)
        self.kpi_row = QHBoxLayout(); self.kpi_row.setSpacing(12); main.addLayout(self.kpi_row)
        top = QHBoxLayout(); top.addStretch()
        add = pb("➕  إضافة قيد"); add.clicked.connect(self._add); top.addWidget(add)
        main.addLayout(top)
        self.table = mk_table(["#", "النوع", "الفئة", "المبلغ", "الوصف", "التاريخ"])
        self.table.horizontalHeader().setSectionResizeMode(4, QHeaderView.Stretch); main.addWidget(self.table)

    def refresh(self, *_):
        while self.kpi_row.count():
            w = self.kpi_row.takeAt(0).widget()
            if w: w.setParent(None)
        s = DB.get_accounting_summary(self.sid)
        for icon,lbl,val,clr in [("💰", "إجمالي الدخل",f"{s['income']/1e6:.1f}M",C['success']),
                                   ("", "إجمالي المصروف",f"{s['expense']/1e6:.1f}M",C['danger']),
                                   ("📊", "صافي الأرباح",f"{s['profit']/1e6:.1f}M",C['primary'] if s['profit'] >=0 else C['danger'])]:
            self.kpi_row.addWidget(KPICard(icon,lbl,val," ",clr))
        rows = DB.get_accounting(self.sid); self.table.setRowCount(len(rows))
        for r, row in enumerate(rows):
            row = dict(row); self.table.setRowHeight(r,38)
            self.table.setItem(r,0,tc(str(row["id"]),Qt.AlignCenter,C['text_muted']))
            clr = C['success'] if row["type"]=="دخل" else C['danger']
            self.table.setItem(r,1,badge_item(row["type"],clr))
            self.table.setItem(r,2,tc(row.get("category", " ") or " "))
            self.table.setItem(r,3,tc(f"{int(row['amount']):,}",Qt.AlignCenter,clr,bold=True))
            self.table.setItem(r,4,tc(row.get("description", " ") or " "))
            self.table.setItem(r,5,tc(row.get("date", " ") or " ",Qt.AlignCenter))

    def _add(self):
        dlg = QDialog(self); dlg.setWindowTitle("إضافة قيد"); dlg.setFixedWidth(400)
        dlg.setLayoutDirection(Qt.RightToLeft); dlg.setStyleSheet(MAIN_STYLE)
        lay = QVBoxLayout(dlg); lay.setContentsMargins(24,20,24,20); lay.setSpacing(12)
        lay.addWidget(section_title("🧾  قيد محاسبي جديد")); lay.addWidget(divider())
        type_cb = QComboBox(); type_cb.addItems(["دخل", "مصروف"]); field_group("النوع", type_cb, lay)
        cat_cb = QComboBox()
        cat_cb.addItems(["أقساط الطلاب", "رواتب المدرسين", "رواتب الموظفين", "كهرباء", "ماء", "إيجار", "مولدة", "قرطاسية", "صيانة", "أخرى"])
        field_group("الفئة", cat_cb, lay)
        amt = QLineEdit(); field_group("المبلغ (دينار)", amt, lay)
        desc = QLineEdit(); field_group("الوصف", desc, lay)
        d_edit = QDateEdit(QDate.currentDate()); d_edit.setCalendarPopup(True)
        field_group("التاريخ", d_edit, lay)
        btns = QDialogButtonBox(QDialogButtonBox.Save|QDialogButtonBox.Cancel)
        btns.button(QDialogButtonBox.Save).setText("حفظ"); btns.button(QDialogButtonBox.Save).setObjectName("primaryBtn")
        btns.accepted.connect(dlg.accept); btns.rejected.connect(dlg.reject); lay.addWidget(btns)
        if dlg.exec():
            try: amount = float(amt.text().replace(",", " "))
            except: return
            DB.add_accounting(self.sid, {"type":type_cb.currentText(), "category":cat_cb.currentText(), "amount":amount, "description":desc.text(), "date":d_edit.date().toString("yyyy-MM-dd")}, self.ui.get("full_name", " "))
            self.refresh()

# ══════════════════════════════════════════
# CALENDAR
# ══════════════════════════════════════════
class CalendarPage(BasePage):
    def __init__(self, school_id, user_info):
        super().__init__(school_id, user_info)
        main = QVBoxLayout(self); main.setContentsMargins(20,14,20,14); main.setSpacing(12)
        top = QHBoxLayout(); top.addWidget(section_title("🗓️  التقويم المدرسي")); top.addStretch()
        add = pb("➕  إضافة حدث"); add.clicked.connect(self._add); top.addWidget(add)
        main.addLayout(top)
        self.table = mk_table(["#", "الحدث", "النوع", "البداية", "النهاية", "الوصف", "حذف"])
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch); main.addWidget(self.table)

    def refresh(self, *_):
        events = DB.get_events(self.sid); self.table.setRowCount(len(events))
        clrs = {"امتحان":C['danger'], "عطلة":C['success'], "اجتماع":C['warning'], "عام":C['primary']}
        for r, e in enumerate(events):
            e = dict(e); self.table.setRowHeight(r,40)
            self.table.setItem(r,0,tc(str(e["id"]),Qt.AlignCenter,C['text_muted']))
            self.table.setItem(r,1,tc(e["title"],bold=True))
            clr = clrs.get(e.get("event_type", ""), "")
            self.table.setItem(r,2,badge_item(e.get("event_type", "عام"),clr) if clr else tc(e.get("event_type", " ")))
            self.table.setItem(r,3,tc(e.get("start_date", " ") or " ",Qt.AlignCenter))
            self.table.setItem(r,4,tc(e.get("end_date", " ") or " ",Qt.AlignCenter))
            self.table.setItem(r,5,tc(e.get("description", " ") or " "))
            db = ib("🗑️"); eid = e["id"]; db.clicked.connect(lambda _,i=eid: self._del(i))
            w = QWidget(); wl = QHBoxLayout(w); wl.setContentsMargins(6,6,6,6); wl.addWidget(db)
            self.table.setCellWidget(r,6,w)

    def _add(self):
        dlg = QDialog(self); dlg.setWindowTitle("إضافة حدث"); dlg.setFixedWidth(400)
        dlg.setLayoutDirection(Qt.RightToLeft); dlg.setStyleSheet(MAIN_STYLE)
        lay = QVBoxLayout(dlg); lay.setContentsMargins(24,20,24,20); lay.setSpacing(12)
        lay.addWidget(section_title("🗓️  حدث جديد")); lay.addWidget(divider())
        title_in = QLineEdit(); field_group("عنوان الحدث *", title_in, lay)
        type_cb = QComboBox(); type_cb.addItems(["عام", "امتحان", "عطلة", "اجتماع"])
        field_group("النوع", type_cb, lay)
        sd = QDateEdit(QDate.currentDate()); sd.setCalendarPopup(True); field_group("تاريخ البداية", sd, lay)
        ed = QDateEdit(QDate.currentDate()); ed.setCalendarPopup(True); field_group("تاريخ النهاية", ed, lay)
        desc = QLineEdit(); field_group("الوصف", desc, lay)
        btns = QDialogButtonBox(QDialogButtonBox.Save|QDialogButtonBox.Cancel)
        btns.button(QDialogButtonBox.Save).setText("حفظ"); btns.button(QDialogButtonBox.Save).setObjectName("primaryBtn")
        btns.accepted.connect(dlg.accept); btns.rejected.connect(dlg.reject); lay.addWidget(btns)
        if dlg.exec() and title_in.text().strip():
            DB.add_event(self.sid, {"title":title_in.text().strip(), "event_type":type_cb.currentText(), "start_date":sd.date().toString("yyyy-MM-dd"), "end_date":ed.date().toString("yyyy-MM-dd"), "description":desc.text()})
            self.refresh()

    def _del(self, eid):
        if QMessageBox.question(self, "تأكيد", "حذف هذا الحدث؟", QMessageBox.Yes|QMessageBox.No)==QMessageBox.Yes:
            DB.delete_event(eid); self.refresh()

# ══════════════════════════════════════════
# REPORTS
# ══════════════════════════════════════════
class ReportsPage(BasePage):
    def __init__(self, school_id, user_info):
        super().__init__(school_id, user_info)
        main = QVBoxLayout(self); main.setContentsMargins(20,14,20,14); main.setSpacing(14)
        self.kpi_row = QHBoxLayout(); self.kpi_row.setSpacing(12); main.addLayout(self.kpi_row)
        abs_card = card(); acl = QVBoxLayout(abs_card); acl.setContentsMargins(16,14,16,14); acl.setSpacing(10)
        ah = QHBoxLayout(); ah.addWidget(section_title("📅  تقرير الغياب الشهري"))
        self.month_e = QDateEdit(QDate.currentDate()); self.month_e.setCalendarPopup(True)
        load_b = gb("عرض"); load_b.setFixedHeight(32); load_b.clicked.connect(self._load_abs)
        ah.addStretch(); ah.addWidget(self.month_e); ah.addWidget(load_b)
        acl.addLayout(ah)
        self.abs_table = mk_table(["الطالب", "الصف", "الشعبة", "عدد الغيابات"])
        self.abs_table.setFixedHeight(220); acl.addWidget(self.abs_table)
        main.addWidget(abs_card)

        exp_card = card(); ecl = QVBoxLayout(exp_card); ecl.setContentsMargins(16,14,16,14); ecl.setSpacing(10)
        ecl.addWidget(section_title("📥  تصدير التقارير"))
        btn_row = QHBoxLayout(); btn_row.setSpacing(10)
        for txt, fn in [("👨‍🎓  طلاب Excel",self._exp_s),("💰  أقساط Excel",self._exp_f),("📅  غياب Excel",self._exp_a)]:
            b = gb(txt); b.clicked.connect(fn); btn_row.addWidget(b)
        btn_row.addStretch(); ecl.addLayout(btn_row); main.addWidget(exp_card); main.addStretch()

    def refresh(self, *_):
        while self.kpi_row.count():
            w = self.kpi_row.takeAt(0).widget()
            if w: w.setParent(None)
        st = DB.get_stats(self.sid)
        for icon,lbl,val,clr in [("👨‍🎓", "الطلاب",str(st["students"]),C['primary']),("👩‍🏫", "المدرسون",str(st["teachers"]),"#8250DF"),("🚸", "الغياب اليوم",str(st["absent_today"]),C['warning']),("🎓", "نسبة النجاح",f"{st['pass_rate']}%",C['success'])]:
            self.kpi_row.addWidget(KPICard(icon,lbl,val," ",clr))

    def _load_abs(self):
        month = self.month_e.date().toString("yyyy-MM")
        rows = DB.get_absence_report(self.sid, month); self.abs_table.setRowCount(len(rows))
        for r, row in enumerate(rows):
            row = dict(row); self.abs_table.setRowHeight(r,36)
            self.abs_table.setItem(r,0,tc(row["full_name"]))
            self.abs_table.setItem(r,1,tc(row.get("grade", " ") or " "))
            self.abs_table.setItem(r,2,tc(row.get("section", " ") or " ",Qt.AlignCenter))
            clr = C['danger'] if row["absences"] >=10 else C['warning'] if row["absences"] >=5 else C['text']
            self.abs_table.setItem(r,3,tc(str(row["absences"]),Qt.AlignCenter,clr,bold=True))

    def _exp_s(self):
        try:
            from reports.exports import export_students_excel
            QMessageBox.information(self, "تم", f"✅  تم الحفظ:\n{export_students_excel(DB.get_students(self.sid))}")
        except Exception as e: QMessageBox.warning(self, "خطأ", str(e))

    def _exp_f(self):
        try:
            from reports.exports import export_fees_excel
            QMessageBox.information(self, "تم", f"✅  تم الحفظ:\n{export_fees_excel(DB.get_fees(self.sid))}")
        except Exception as e: QMessageBox.warning(self, "خطأ", str(e))

    def _exp_a(self):
        try:
            from reports.exports import export_absence_excel
            QMessageBox.information(self, "تم", f"✅  تم الحفظ:\n{export_absence_excel(DB.get_absence_report(self.sid))}")
        except Exception as e: QMessageBox.warning(self, "خطأ", str(e))

# ══════════════════════════════════════════
# AUDIT
# ══════════════════════════════════════════
class AuditPage(BasePage):
    def __init__(self, school_id, user_info):
        super().__init__(school_id, user_info)
        main = QVBoxLayout(self); main.setContentsMargins(20,14,20,14); main.setSpacing(12)
        info = QLabel("🔍  كل عملية في البرنامج تُسجَّل تلقائياً مع اسم المستخدم والوقت")
        info.setStyleSheet(f"color:{C['text_sec']}; font-size:12px; background:{C['primary_lt']}; border:1px solid {C['primary']}30; border-radius:8px; padding:8px 14px;")
        main.addWidget(info)
        self.table = mk_table(["#", "المستخدم", "العملية", "التفاصيل", "الوقت"])
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch); main.addWidget(self.table)

    def refresh(self, *_):
        rows = DB.get_audit_log(self.sid); self.table.setRowCount(len(rows))
        ACT_COLORS = {"إضافة طالب":C['success'], "حذف طالب":C['danger'], "تعديل طالب":C['warning'], "تسجيل دفعة":C['success'], "تسجيل غياب": "#8250DF"}
        for r, row in enumerate(rows):
            row = dict(row); self.table.setRowHeight(r,38)
            self.table.setItem(r,0,tc(str(row["id"]),Qt.AlignCenter,C['text_muted']))
            self.table.setItem(r,1,tc(row.get("user_name", " ") or " ",color=C['primary'],bold=True))
            action = row.get("action", " ")
            self.table.setItem(r,2,tc(action, color=ACT_COLORS.get(action,C['text_sec'])))
            self.table.setItem(r,3,tc(row.get("details", " ") or " "))
            self.table.setItem(r,4,tc(row.get("timestamp", " ") or " ",Qt.AlignCenter))

# ══════════════════════════════════════════
# SETTINGS
# ══════════════════════════════════════════
class SettingsPage(BasePage):
    def __init__(self, school_id, user_info):
        super().__init__(school_id, user_info)
        lay = self._page_wrap()
        tabs = QTabWidget(); lay.addWidget(tabs)

        # School settings
        t1 = QWidget(); t1.setStyleSheet("background: white;")
        t1l = QVBoxLayout(t1); t1l.setContentsMargins(20,16,20,16); t1l.setSpacing(10)
        self.s_name = QLineEdit(); field_group("اسم المدرسة", self.s_name, t1l)
        self.s_princ = QLineEdit(); field_group("مدير المدرسة", self.s_princ, t1l)
        r2 = QHBoxLayout(); r2.setSpacing(12)
        self.s_phone = QLineEdit(); self.s_phone.setLayoutDirection(Qt.LeftToRight)
        col1 = QWidget(); c1l = QVBoxLayout(col1); c1l.setContentsMargins(0,0,0,0); c1l.setSpacing(4)
        c1l.addWidget(QLabel("رقم الهاتف")); c1l.addWidget(self.s_phone)
        self.s_year = QLineEdit()
        col2 = QWidget(); c2l = QVBoxLayout(col2); c2l.setContentsMargins(0,0,0,0); c2l.setSpacing(4)
        c2l.addWidget(QLabel("السنة الدراسية")); c2l.addWidget(self.s_year)
        r2.addWidget(col1); r2.addWidget(col2); t1l.addLayout(r2)
        self.s_addr = QLineEdit(); field_group("العنوان", self.s_addr, t1l)
        self.s_fee = QLineEdit(); field_group("قيمة القسط السنوي (دينار)", self.s_fee, t1l)
        t1l.addWidget(divider())
        save_btn = pb("💾  حفظ الإعدادات"); save_btn.clicked.connect(self._save_school); save_btn.setFixedWidth(180)
        t1l.addWidget(save_btn); t1l.addStretch(); tabs.addTab(t1, "إعدادات المدرسة")

        # Users
        t2 = QWidget(); t2.setStyleSheet("background: white;")
        t2l = QVBoxLayout(t2); t2l.setContentsMargins(20,16,20,16); t2l.setSpacing(10)
        uh = QHBoxLayout(); uh.addWidget(section_title("المستخدمون")); uh.addStretch()
        add_u = pb("➕  مستخدم"); add_u.clicked.connect(self._add_user); uh.addWidget(add_u)
        t2l.addLayout(uh)
        self.users_table = mk_table(["#", "اسم المستخدم", "الاسم الكامل", "الدور", "إعادة تعيين", "حذف"])
        self.users_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.users_table.setColumnWidth(4,110)
        t2l.addWidget(self.users_table); tabs.addTab(t2, "المستخدمون")

        # Backup
        t3 = QWidget(); t3.setStyleSheet("background: white;")
        t3l = QVBoxLayout(t3); t3l.setContentsMargins(20,16,20,16); t3l.setSpacing(12)
        from core.db import DB_PATH
        p_lbl = QLabel(f"  مسار قاعدة البيانات:\n{DB_PATH}")
        p_lbl.setStyleSheet(f"color:{C['text_sec']}; background:{C['bg_page']}; border-radius:8px; padding:12px; font-family:monospace;")
        t3l.addWidget(p_lbl)
        bak = pb("📦  إنشاء نسخة احتياطية الآن"); bak.setFixedWidth(250); bak.clicked.connect(self._backup)
        t3l.addWidget(bak); t3l.addStretch(); tabs.addTab(t3, "النسخ الاحتياطي")
        lay.addStretch()

    def refresh(self, *_):
        school = dict(DB.get_school(self.sid) or {})
        self.s_name.setText(school.get("name", " "))
        self.s_princ.setText(school.get("principal", " ") or " ")
        self.s_addr.setText(school.get("address", " ") or " ")
        self.s_phone.setText(school.get("phone", " ") or " ")
        self.s_year.setText(school.get("academic_year", " ") or " ")
        self.s_fee.setText(str(int(school.get("fee_amount",1500000) or 1500000)))
        self._load_users()

    def _save_school(self):
        try: fee = float(self.s_fee.text().replace(",", " "))
        except: fee = 1500000
        DB.update_school(self.sid,{"name":self.s_name.text(), "principal":self.s_princ.text(), "address":self.s_addr.text(), "phone":self.s_phone.text(), "academic_year":self.s_year.text(), "fee_amount":fee})
        QMessageBox.information(self, "تم", "✅  تم حفظ الإعدادات")

    def _load_users(self):
        users = DB.get_users(self.sid); self.users_table.setRowCount(len(users))
        for r, u in enumerate(users):
            u = dict(u); self.users_table.setRowHeight(r,44)
            self.users_table.setItem(r,0,tc(str(u["id"]),Qt.AlignCenter,C['text_muted']))
            self.users_table.setItem(r,1,tc(u.get("username", " "),bold=True))
            self.users_table.setItem(r,2,tc(u.get("full_name", " ") or " "))
            role_colors = {"مدير":C['danger'], "محاسب":C['warning'], "معلم":C['success'], "موظف":C['accent'], "سكرتيرة":C['accent']}
            role = u.get("role", " ")
            self.users_table.setItem(r,3,badge_item(role, role_colors.get(role, C['text_muted'])))
            # Reset password button
            rb = ib("🔑", "تغيير كلمة المرور"); uid = u["id"]; uname = u.get("username", " ")
            rb.setStyleSheet(f"background:{C['warning_lt']};border-color:{C['warning']}20;color:{C['warning']};")
            rb.clicked.connect(lambda _,i=uid,n=uname: self._reset_password(i,n))
            rw=QWidget(); rwl=QHBoxLayout(rw); rwl.setContentsMargins(4,4,4,4); rwl.addWidget(rb)
            self.users_table.setCellWidget(r,4,rw)
            db = ib("🗑️", "حذف"); db.setStyleSheet(f"background:{C['danger_lt']};border-color:{C['danger']}20;color:{C['danger']};")
            db.clicked.connect(lambda _,i=uid: self._del_user(i))
            dw=QWidget(); dwl=QHBoxLayout(dw); dwl.setContentsMargins(4,4,4,4); dwl.addWidget(db)
            self.users_table.setCellWidget(r,5,dw)

    def _reset_password(self, uid, username):
        new_pass, ok = QInputDialog.getText(self, "تغيير كلمة المرور",
                                             f"كلمة المرور الجديدة للمستخدم ({username}):",
                                             QLineEdit.Password)
        if ok and new_pass.strip():
            import core.db as DB2
            db2 = DB2.conn()
            db2.execute("UPDATE users SET password=? WHERE id=?", (new_pass.strip(), uid))
            db2.commit(); db2.close()
            QMessageBox.information(self, "تم", f"✅  تم تغيير كلمة مرور {username}")

    def _add_user(self):
        dlg = QDialog(self); dlg.setWindowTitle("مستخدم جديد"); dlg.setFixedWidth(420)
        dlg.setLayoutDirection(Qt.RightToLeft); dlg.setStyleSheet(MAIN_STYLE)
        lay = QVBoxLayout(dlg); lay.setContentsMargins(24,20,24,20); lay.setSpacing(12)
        lay.addWidget(section_title("👤  مستخدم جديد")); lay.addWidget(divider())
        f_name = QLineEdit(); field_group("الاسم الكامل *", f_name, lay)
        f_user = QLineEdit(); field_group("اسم المستخدم *", f_user, lay)
        f_pass = QLineEdit(); f_pass.setEchoMode(QLineEdit.Password)
        field_group("كلمة المرور *", f_pass, lay)
        f_confirm = QLineEdit(); f_confirm.setEchoMode(QLineEdit.Password)
        field_group("تأكيد كلمة المرور *", f_confirm, lay)
        role = QComboBox(); role.addItems(["محاسب", "معلم", "موظف", "سكرتيرة", "مدير"])
        field_group("الدور / الصلاحية", role, lay)
        err_lbl = QLabel(" "); err_lbl.setStyleSheet("color:red;font-size:12px;")
        lay.addWidget(err_lbl)
        btns = QDialogButtonBox(QDialogButtonBox.Save|QDialogButtonBox.Cancel)
        btns.button(QDialogButtonBox.Save).setText("إضافة المستخدم"); btns.button(QDialogButtonBox.Save).setObjectName("primaryBtn")
        btns.rejected.connect(dlg.reject)
        def _try_save():
            un = f_user.text().strip(); pw = f_pass.text().strip(); cf = f_confirm.text().strip()
            if not un or not pw:
                err_lbl.setText("اسم المستخدم وكلمة المرور مطلوبان"); return
            if pw != cf:
                err_lbl.setText("كلمتا المرور غير متطابقتان"); return
            dlg.accept()
        btns.button(QDialogButtonBox.Save).clicked.disconnect()
        btns.button(QDialogButtonBox.Save).clicked.connect(_try_save)
        btns.accepted.connect(dlg.accept); lay.addWidget(btns)
        if dlg.exec() and f_user.text().strip() and f_pass.text().strip():
            DB.add_user(self.sid,{"username":f_user.text().strip(), "password":f_pass.text().strip(), "full_name":f_name.text().strip(), "role":role.currentText()})
            QMessageBox.information(self, "تم", f"✅  تم إضافة المستخدم: {f_user.text().strip()}\nالدور: {role.currentText()}")
            self._load_users()

    def _del_user(self, uid):
        if QMessageBox.question(self, "تأكيد", "حذف هذا المستخدم؟", QMessageBox.Yes|QMessageBox.No)==QMessageBox.Yes:
            DB.delete_user(uid); self._load_users()

    def _backup(self):
        from core.db import DB_PATH
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        dest = DB_PATH.replace(".db", f"_backup_{ts}.db")
        shutil.copy2(DB_PATH, dest)
        QMessageBox.information(self, "نسخة احتياطية", f"✅  تم الحفظ:\n{dest}")
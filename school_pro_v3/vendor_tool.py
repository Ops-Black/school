#!/usr/bin/env python3
"""
SchoolPro — أداة المورّد (Vendor Tool)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
برنامج مستقل لتوليد أكواد التفعيل — Offline بالكامل
يُستخدم من قِبَل المورّد فقط
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PySide6.QtWidgets import *
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QFont, QClipboard

from core.security.license_engine import generate_activation_code, generate_server_id


# ════════════════════════════════════════════════════════════
# STYLE — مستقل عن MAIN_STYLE
# ════════════════════════════════════════════════════════════
VENDOR_STYLE = """
* { font-family: Tahoma, Arial; font-size: 13px; }
QDialog, QMainWindow, QWidget#root {
    background-color: #F0F2F7;
}
QWidget { color: #1A1D2E; }
QLabel  { background: transparent; color: #1A1D2E; }

QFrame#card {
    background-color: #FFFFFF;
    border: 1.5px solid #E2E5EE;
    border-radius: 12px;
}
QFrame#header {
    background-color: #1C1F2E;
    border-radius: 0;
}

QLineEdit, QComboBox, QDateEdit, QSpinBox {
    background-color: #FFFFFF;
    color: #1A1D2E;
    border: 1.5px solid #E2E5EE;
    border-radius: 8px;
    padding: 9px 14px;
    font-size: 13px;
}
QLineEdit:focus, QComboBox:focus, QDateEdit:focus {
    border: 2px solid #4A6CF7;
}
QComboBox QAbstractItemView {
    background: #FFFFFF;
    color: #1A1D2E;
    border: 1px solid #E2E5EE;
    border-radius: 6px;
    selection-background-color: #EEF2FF;
    selection-color: #3557D4;
}
QComboBox QAbstractItemView::item {
    color: #1A1D2E;
    padding: 7px 12px;
    min-height: 28px;
}

QPushButton {
    background-color: #4A6CF7;
    color: white;
    border: none;
    border-radius: 8px;
    padding: 0 20px;
    font-weight: bold;
    min-height: 40px;
    font-size: 13px;
}
QPushButton:hover  { background-color: #3557D4; }
QPushButton:pressed { background-color: #2744BB; }

QPushButton#ghost {
    background-color: #FFFFFF;
    color: #1A1D2E;
    border: 1.5px solid #E2E5EE;
}
QPushButton#ghost:hover { background-color: #F4F5F9; border-color: #5B6278; }

QPushButton#danger {
    background-color: #FFFFFF;
    color: #DC2626;
    border: 1.5px solid #E2E5EE;
}

QTextEdit {
    background-color: #FFFFFF;
    color: #1A1D2E;
    border: 1.5px solid #E2E5EE;
    border-radius: 8px;
    padding: 10px;
    font-family: "Courier New", monospace;
    font-size: 12px;
    selection-background-color: #4A6CF7;
    selection-color: white;
}

QScrollBar:vertical { width: 8px; background: transparent; }
QScrollBar::handle:vertical { background: #E2E5EE; border-radius: 4px; min-height: 30px; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }

QTableWidget {
    background: #FFFFFF;
    color: #1A1D2E;
    border: 1.5px solid #E2E5EE;
    border-radius: 10px;
    gridline-color: #F0F1F5;
    outline: 0;
}
QTableWidget::item { padding: 10px 14px; color: #1A1D2E; border-bottom: 1px solid #F0F1F5; }
QTableWidget::item:selected { background: #EEF2FF; color: #3557D4; }
QHeaderView::section {
    background: #F4F5F9; color: #5B6278;
    font-weight: bold; font-size: 11px;
    padding: 10px 14px; border: none;
    border-bottom: 2px solid #E2E5EE;
}
QMessageBox { background-color: #FFFFFF; }
QMessageBox QLabel { color: #1A1D2E; background: transparent; }
QMessageBox QPushButton { background-color: #4A6CF7; color: white; min-width: 80px; }
"""


# ════════════════════════════════════════════════════════════
# Main Window
# ════════════════════════════════════════════════════════════
class VendorTool(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SchoolPro — أداة المورّد لتوليد التراخيص")
        self.setMinimumSize(760, 680)
        self.setLayoutDirection(Qt.RightToLeft)
        self.setStyleSheet(VENDOR_STYLE)
        self.setObjectName("root")
        self._build()

    # ── بناء الواجهة ────────────────────────────────────────
    def _build(self):
        main = QVBoxLayout(self)
        main.setContentsMargins(0, 0, 0, 0)
        main.setSpacing(0)

        # ╔══ HEADER ══╗
        hdr = QFrame(); hdr.setObjectName("header"); hdr.setFixedHeight(90)
        hl = QHBoxLayout(hdr); hl.setContentsMargins(32, 20, 32, 20)

        logo = QLabel("🔑")
        logo.setStyleSheet("font-size: 32px; background: transparent;")

        htxt = QVBoxLayout(); htxt.setSpacing(2)
        t1 = QLabel("SchoolPro — أداة المورّد")
        t1.setStyleSheet("color: white; font-size: 17px; font-weight: bold; background: transparent;")
        t2 = QLabel("توليد أكواد التفعيل • Offline")
        t2.setStyleSheet("color: #9CA3B4; font-size: 12px; background: transparent;")
        htxt.addWidget(t1); htxt.addWidget(t2)

        hl.addWidget(logo)
        hl.addSpacing(12)
        hl.addLayout(htxt)
        hl.addStretch()

        ver = QLabel("v3.0")
        ver.setStyleSheet("color: #F5A623; font-size: 12px; font-weight: bold; background: transparent;")
        hl.addWidget(ver)
        main.addWidget(hdr)

        # ╔══ BODY ══╗
        body = QWidget(); body.setStyleSheet("background-color: #F0F2F7;")
        bl = QHBoxLayout(body); bl.setContentsMargins(24, 24, 24, 24); bl.setSpacing(20)

        # ── LEFT: Form ───────────────────────────────────────
        left = QFrame(); left.setObjectName("card"); left.setFixedWidth(360)
        ll = QVBoxLayout(left); ll.setContentsMargins(24, 24, 24, 24); ll.setSpacing(16)

        form_title = QLabel("بيانات الترخيص الجديد")
        form_title.setStyleSheet("font-size: 15px; font-weight: bold; color: #1A1D2E;")
        ll.addWidget(form_title)

        ll.addWidget(self._divider())

        def field(label, widget, hint=None):
            c = QWidget(); c.setStyleSheet("background:transparent;")
            cl = QVBoxLayout(c); cl.setContentsMargins(0,0,0,0); cl.setSpacing(4)
            l = QLabel(label)
            l.setStyleSheet("font-size: 11px; font-weight: bold; color: #5B6278; letter-spacing: 0.5px;")
            cl.addWidget(l); cl.addWidget(widget)
            if hint:
                h = QLabel(hint); h.setStyleSheet("font-size: 10px; color: #9499B0;")
                cl.addWidget(h)
            ll.addWidget(c)

        # اسم المدرسة
        self.inp_school = QLineEdit()
        self.inp_school.setPlaceholderText("مثال: مدرسة البتول الأهلية للبنات")
        field("اسم المدرسة *", self.inp_school)

        # نوع الترخيص
        self.inp_type = QComboBox()
        self.inp_type.addItems(["دائم (Lifetime)", "سنوي", "نصف سنوي", "ثلاثة أشهر", "شهر واحد", "مخصص"])
        self.inp_type.currentTextChanged.connect(self._on_type_change)
        field("نوع الترخيص", self.inp_type)

        # تاريخ مخصص (مخفي افتراضياً)
        self.custom_date_widget = QWidget(); self.custom_date_widget.setStyleSheet("background:transparent;")
        cdl = QVBoxLayout(self.custom_date_widget); cdl.setContentsMargins(0,0,0,0); cdl.setSpacing(4)
        cdl_lbl = QLabel("تاريخ الانتهاء المخصص")
        cdl_lbl.setStyleSheet("font-size: 11px; font-weight: bold; color: #5B6278;")
        self.inp_date = QDateEdit()
        self.inp_date.setCalendarPopup(True)
        self.inp_date.setDate(QDate.currentDate().addYears(1))
        cdl.addWidget(cdl_lbl); cdl.addWidget(self.inp_date)
        ll.addWidget(self.custom_date_widget)
        self.custom_date_widget.setVisible(False)

        # عدد الأجهزة
        self.inp_seats = QSpinBox()
        self.inp_seats.setRange(0, 999)
        self.inp_seats.setValue(0)
        self.inp_seats.setSpecialValueText("غير محدود (0)")
        field("عدد الأجهزة المرخّصة", self.inp_seats, "0 = غير محدود — يعمل على أي عدد من الأجهزة")

        # ملاحظات
        self.inp_notes = QLineEdit()
        self.inp_notes.setPlaceholderText("اختياري...")
        field("ملاحظات", self.inp_notes)

        ll.addStretch()
        ll.addWidget(self._divider())

        gen_btn = QPushButton("⚡  توليد كود التفعيل")
        gen_btn.setMinimumHeight(46)
        gen_btn.clicked.connect(self._generate)
        ll.addWidget(gen_btn)

        bl.addWidget(left)

        # ── RIGHT: Output ────────────────────────────────────
        right = QVBoxLayout(); right.setSpacing(16)

        # Server ID lookup
        sid_card = QFrame(); sid_card.setObjectName("card")
        sl = QVBoxLayout(sid_card); sl.setContentsMargins(20, 16, 20, 16); sl.setSpacing(10)

        sid_hdr = QHBoxLayout()
        sid_title = QLabel("فحص Server ID")
        sid_title.setStyleSheet("font-size: 13px; font-weight: bold; color: #1A1D2E;")
        sid_hdr.addWidget(sid_title); sid_hdr.addStretch()
        sl.addLayout(sid_hdr)

        sid_inp_row = QHBoxLayout(); sid_inp_row.setSpacing(8)
        self.inp_sid_check = QLineEdit()
        self.inp_sid_check.setPlaceholderText("أدخل اسم المدرسة لمعاينة Server ID...")
        self.inp_sid_check.textChanged.connect(self._preview_sid)
        sid_lookup_btn = QPushButton("🔍")
        sid_lookup_btn.setObjectName("ghost")
        sid_lookup_btn.setFixedSize(40, 40)
        sid_lookup_btn.clicked.connect(self._preview_sid)
        sid_inp_row.addWidget(self.inp_sid_check, 1); sid_inp_row.addWidget(sid_lookup_btn)
        sl.addLayout(sid_inp_row)

        self.sid_result = QLabel("—")
        self.sid_result.setStyleSheet(
            "color: #4A6CF7; font-size: 18px; font-weight: bold; "
            "background: #EEF2FF; border-radius: 8px; padding: 8px 14px; letter-spacing: 3px;"
        )
        self.sid_result.setAlignment(Qt.AlignCenter)
        sl.addWidget(self.sid_result)
        right.addWidget(sid_card)

        # Code output
        code_card = QFrame(); code_card.setObjectName("card")
        cl2 = QVBoxLayout(code_card); cl2.setContentsMargins(20, 16, 20, 16); cl2.setSpacing(10)

        code_hdr = QHBoxLayout()
        code_title = QLabel("كود التفعيل")
        code_title.setStyleSheet("font-size: 13px; font-weight: bold; color: #1A1D2E;")
        code_hdr.addWidget(code_title); code_hdr.addStretch()

        copy_code_btn = QPushButton("📋  نسخ الكود")
        copy_code_btn.setObjectName("ghost")
        copy_code_btn.setFixedHeight(34)
        copy_code_btn.clicked.connect(self._copy_code)
        code_hdr.addWidget(copy_code_btn)
        cl2.addLayout(code_hdr)

        self.code_out = QTextEdit()
        self.code_out.setReadOnly(True)
        self.code_out.setPlaceholderText("سيظهر كود التفعيل هنا بعد الضغط على \"توليد\"...")
        self.code_out.setMinimumHeight(110)
        cl2.addWidget(self.code_out)
        right.addWidget(code_card)

        # History table
        hist_card = QFrame(); hist_card.setObjectName("card")
        hl2 = QVBoxLayout(hist_card); hl2.setContentsMargins(20, 16, 20, 16); hl2.setSpacing(10)

        hist_title = QLabel("سجل الأكواد المُولَّدة في هذه الجلسة")
        hist_title.setStyleSheet("font-size: 13px; font-weight: bold; color: #1A1D2E;")
        hl2.addWidget(hist_title)

        self.hist_table = QTableWidget(0, 3)
        self.hist_table.setHorizontalHeaderLabels(["المدرسة", "الانتهاء", "الأجهزة"])
        self.hist_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.hist_table.setColumnWidth(1, 120); self.hist_table.setColumnWidth(2, 90)
        self.hist_table.verticalHeader().setVisible(False)
        self.hist_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.hist_table.setMaximumHeight(180)
        hl2.addWidget(self.hist_table)
        right.addWidget(hist_card)

        bl.addLayout(right)
        main.addWidget(body)

    # ── helpers ─────────────────────────────────────────────
    def _divider(self):
        d = QFrame(); d.setFrameShape(QFrame.HLine)
        d.setStyleSheet("color: #E2E5EE; background: #E2E5EE;"); d.setFixedHeight(1)
        return d

    def _on_type_change(self, text):
        self.custom_date_widget.setVisible(text == "مخصص")

    def _preview_sid(self):
        name = self.inp_sid_check.text().strip()
        if name:
            self.sid_result.setText(generate_server_id(name))
        else:
            self.sid_result.setText("—")

    def _get_expires(self) -> str:
        t = self.inp_type.currentText()
        today = QDate.currentDate()
        if t == "دائم (Lifetime)":  return "lifetime"
        if t == "سنوي":             return today.addYears(1).toString("yyyy-MM-dd")
        if t == "نصف سنوي":        return today.addMonths(6).toString("yyyy-MM-dd")
        if t == "ثلاثة أشهر":       return today.addMonths(3).toString("yyyy-MM-dd")
        if t == "شهر واحد":        return today.addMonths(1).toString("yyyy-MM-dd")
        return self.inp_date.date().toString("yyyy-MM-dd")  # مخصص

    def _generate(self):
        school = self.inp_school.text().strip()
        if not school:
            QMessageBox.warning(self, "تنبيه", "يجب إدخال اسم المدرسة أولاً"); return

        expires = self._get_expires()
        seats   = self.inp_seats.value()

        code = generate_activation_code(school, expires, seats)
        self.code_out.setPlainText(code)
        self.code_out.setStyleSheet(
            "background: #F0FDF4; color: #14532D; border: 1.5px solid #16A34A; "
            "border-radius: 8px; padding: 10px; font-family: 'Courier New'; font-size: 12px;"
        )

        # Add to history
        r = self.hist_table.rowCount()
        self.hist_table.insertRow(r)
        self.hist_table.setRowHeight(r, 38)
        exp_txt = "دائم" if expires == "lifetime" else expires
        seats_txt = "غير محدود" if seats == 0 else str(seats)

        def tc(text, color=None):
            from PySide6.QtWidgets import QTableWidgetItem
            from PySide6.QtCore import Qt
            item = QTableWidgetItem(text)
            item.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
            if color:
                from PySide6.QtGui import QColor
                item.setForeground(QColor(color))
            return item

        self.hist_table.setItem(r, 0, tc(school))
        self.hist_table.setItem(r, 1, tc(exp_txt, "#16A34A" if expires == "lifetime" else "#D97706"))
        self.hist_table.setItem(r, 2, tc(seats_txt))

    def _copy_code(self):
        code = self.code_out.toPlainText().strip()
        if not code:
            QMessageBox.information(self, "تنبيه", "ولِّد كوداً أولاً"); return
        QApplication.clipboard().setText(code)
        QMessageBox.information(self, "✅  تم", "تم نسخ كود التفعيل\nأرسله للمدرسة لتلصقه في نافذة الترخيص")


# ════════════════════════════════════════════════════════════
# Entry point
# ════════════════════════════════════════════════════════════
def main():
    app = QApplication(sys.argv)
    app.setLayoutDirection(Qt.RightToLeft)
    app.setApplicationName("SchoolPro Vendor Tool")
    app.setStyleSheet(VENDOR_STYLE)
    for fn in ["Tahoma", "Arial"]:
        f = QFont(fn, 13)
        if f.exactMatch():
            app.setFont(f); break
    win = VendorTool()
    win.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()

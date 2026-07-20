"""
واجهة الترخيص الاحترافية — Offline — بدون زر تجريبي
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PySide6.QtWidgets import (
    QDialog, QWidget, QLabel, QPushButton, QLineEdit,
    QVBoxLayout, QHBoxLayout, QFrame, QApplication, QMessageBox
)
from PySide6.QtCore import Qt

from core.security.license_engine import (
    license_info, activate, generate_server_id
)

# ── Palette مستقلة تماماً — لا تعتمد على C ──────────────────
_S = {
    "sb_bg":     "#3F0E40",
    "sb_txt":    "#CFC3CF",
    "gold":      "#F5A623",
    "page_bg":   "#F0F2F7",
    "card_bg":   "#FFFFFF",
    "border":    "#E2E5EE",
    "text":      "#1D1C1D",
    "text_sec":  "#616061",
    "text_muted":"#ABABAD",
    "primary":   "#1264A3",
    "primary_lt":"#E8F5FA",
    "success":   "#007A5A",
    "success_lt":"#E8F5F0",
    "danger":    "#E01E5A",
    "danger_lt": "#FCEEF3",
}

_STYLE = f"""
* {{ font-family: Tahoma, Arial; font-size: 13px; }}
QWidget {{ color: {_S['text']}; background: transparent; }}
QDialog {{ background-color: {_S['page_bg']}; }}
QLabel  {{ color: {_S['text']}; background: transparent; }}

QLineEdit {{
    background-color: {_S['card_bg']};
    color: {_S['text']};
    border: 1.5px solid {_S['border']};
    border-radius: 4px;
    padding: 10px 14px;
    font-size: 13px;
}}
QLineEdit:focus {{
    border: 2px solid {_S['primary']};
    padding: 9px 13px;
}}
QLineEdit::placeholder {{ color: {_S['text_muted']}; }}

QPushButton {{
    background-color: {_S['primary']};
    color: white; border: none; border-radius: 4px;
    padding: 0 20px; font-weight: bold;
    min-height: 38px; font-size: 13px;
}}
QPushButton:hover  {{ background-color: #0B4D81; color: white; }}
QPushButton:pressed {{ background-color: #083F6B; }}
QPushButton:disabled {{
    background-color: {_S['border']};
    color: {_S['text_muted']};
}}
QPushButton#ghost {{
    background-color: {_S['card_bg']};
    color: {_S['text']};
    border: 1.5px solid {_S['border']};
}}
QPushButton#ghost:hover {{
    background-color: {_S['page_bg']};
    color: {_S['text']};
    border-color: {_S['text_sec']};
}}
QPushButton#accent {{
    background-color: {_S['gold']};
    color: #1D1C1D;
    border: none;
}}
QPushButton#accent:hover  {{ background-color: #E09A1A; }}
QPushButton#accent:disabled {{
    background-color: {_S['border']};
    color: {_S['text_muted']};
}}
QScrollBar:vertical {{ width:7px; background:transparent; }}
QScrollBar::handle:vertical {{ background:#D0D0D0; border-radius:3px; min-height:28px; }}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height:0; }}
QMessageBox {{ background-color: {_S['card_bg']}; }}
QMessageBox QLabel {{ color: {_S['text']}; background: transparent; min-width: 280px; }}
QMessageBox QPushButton {{
    background-color: {_S['primary']}; color: white; border: none;
    border-radius: 4px; padding: 6px 20px; font-weight: bold;
    min-width: 80px; min-height: 32px;
}}
"""


class LicenseDialog(QDialog):
    """نافذة الترخيص Offline — بدون زر تجريبي"""

    def __init__(self, school_name: str, parent=None):
        super().__init__(parent)
        self.school_name = school_name
        self._sid = generate_server_id(school_name)
        self.setWindowTitle("ترخيص النظام — SchoolPro")
        self.setFixedWidth(560)
        self.setMinimumHeight(500)
        self.setLayoutDirection(Qt.RightToLeft)
        self.setStyleSheet(_STYLE)
        self._build()
        self._refresh_status()

    # ── بناء الواجهة ─────────────────────────────────────────
    def _build(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ── HEADER (بنفسجي) ──────────────────────────────────
        hdr = QWidget()
        hdr.setStyleSheet(f"background-color: {_S['sb_bg']};")
        hdr.setFixedHeight(106)
        hl = QVBoxLayout(hdr)
        hl.setContentsMargins(32, 22, 32, 22)
        hl.setSpacing(6)

        title_lbl = QLabel("🔐  ترخيص SchoolPro")
        title_lbl.setStyleSheet(
            "color: #FFFFFF; font-size: 20px; font-weight: bold; background: transparent;"
        )
        school_lbl = QLabel(self.school_name)
        school_lbl.setStyleSheet(
            f"color: {_S['gold']}; font-size: 13px; background: transparent; font-weight: 500;"
        )
        hl.addWidget(title_lbl)
        hl.addWidget(school_lbl)
        root.addWidget(hdr)

        # ── BODY ─────────────────────────────────────────────
        body = QWidget()
        body.setStyleSheet(f"background-color: {_S['page_bg']};")
        bl = QVBoxLayout(body)
        bl.setContentsMargins(32, 26, 32, 26)
        bl.setSpacing(18)

        # ── Server ID Card ────────────────────────────────────
        sid_card = QFrame()
        sid_card.setStyleSheet(f"""
            QFrame {{
                background-color: {_S['card_bg']};
                border: 1.5px solid {_S['border']};
                border-radius: 8px;
            }}
            QLabel {{ background: transparent; }}
        """)
        scl = QVBoxLayout(sid_card)
        scl.setContentsMargins(20, 16, 20, 16)
        scl.setSpacing(10)

        sid_title = QLabel("معرّف السيرفر  (Server ID)")
        sid_title.setStyleSheet(
            f"color: {_S['text_sec']}; font-size: 11px; "
            f"font-weight: bold; letter-spacing: 1px; background: transparent;"
        )
        scl.addWidget(sid_title)

        sid_row = QHBoxLayout(); sid_row.setSpacing(10)

        self.sid_display = QLabel(self._sid)
        self.sid_display.setStyleSheet(f"""
            color: {_S['primary']};
            background-color: {_S['primary_lt']};
            border-radius: 6px;
            padding: 12px 20px;
            font-size: 22px;
            font-weight: bold;
            letter-spacing: 5px;
        """)
        self.sid_display.setAlignment(Qt.AlignCenter)

        copy_btn = QPushButton("📋  نسخ")
        copy_btn.setObjectName("ghost")
        copy_btn.setFixedSize(88, 44)
        copy_btn.clicked.connect(self._copy_sid)

        sid_row.addWidget(self.sid_display, 1)
        sid_row.addWidget(copy_btn)
        scl.addLayout(sid_row)

        hint = QLabel("أرسل هذا الرمز للمورّد  ←  سيُرسل كود التفعيل  ←  الصقه في الحقل أدناه")
        hint.setStyleSheet(
            f"color: {_S['text_muted']}; font-size: 11px; background: transparent;"
        )
        scl.addWidget(hint)
        bl.addWidget(sid_card)

        # ── Status Card ───────────────────────────────────────
        self.status_card = QFrame()
        self.status_card.setStyleSheet(
            f"background-color: {_S['card_bg']}; border: 1.5px solid {_S['border']}; border-radius: 8px;"
        )
        stl = QVBoxLayout(self.status_card)
        stl.setContentsMargins(20, 14, 20, 14)
        stl.setSpacing(5)

        st_hdr = QLabel("حالة الترخيص")
        st_hdr.setStyleSheet(
            f"color: {_S['text_sec']}; font-size: 11px; "
            f"font-weight: bold; letter-spacing: 1px; background: transparent;"
        )
        stl.addWidget(st_hdr)

        self.status_lbl = QLabel("جاري الفحص...")
        self.status_lbl.setStyleSheet(
            f"color: {_S['text']}; font-size: 15px; font-weight: bold; background: transparent;"
        )
        self.detail_lbl = QLabel("")
        self.detail_lbl.setStyleSheet(
            f"color: {_S['text_sec']}; font-size: 12px; background: transparent;"
        )
        stl.addWidget(self.status_lbl)
        stl.addWidget(self.detail_lbl)
        bl.addWidget(self.status_card)

        # ── Activation ────────────────────────────────────────
        act_hdr = QLabel("تفعيل الترخيص")
        act_hdr.setStyleSheet(
            f"color: {_S['text']}; font-size: 13px; font-weight: bold; background: transparent;"
        )
        bl.addWidget(act_hdr)

        act_row = QHBoxLayout(); act_row.setSpacing(10)
        self.code_inp = QLineEdit()
        self.code_inp.setPlaceholderText("الصق كود التفعيل هنا...")
        self.code_inp.returnPressed.connect(self._activate)

        act_btn = QPushButton("✓  تفعيل")
        act_btn.setFixedSize(100, 42)
        act_btn.clicked.connect(self._activate)

        act_row.addWidget(self.code_inp, 1)
        act_row.addWidget(act_btn)
        bl.addLayout(act_row)

        self.err_lbl = QLabel("")
        self.err_lbl.setStyleSheet(
            f"color: {_S['danger']}; font-size: 12px; background: transparent;"
        )
        bl.addWidget(self.err_lbl)

        bl.addStretch()

        # ── Footer ────────────────────────────────────────────
        foot = QHBoxLayout(); foot.setSpacing(12)

        self.go_btn = QPushButton("▶  متابعة")
        self.go_btn.setObjectName("accent")
        self.go_btn.setFixedWidth(130)
        self.go_btn.setMinimumHeight(42)
        self.go_btn.clicked.connect(self.accept)
        self.go_btn.setEnabled(False)

        foot.addStretch()
        foot.addWidget(self.go_btn)
        bl.addLayout(foot)

        root.addWidget(body)

    # ── تحديث الحالة ──────────────────────────────────────────
    def _refresh_status(self):
        info = license_info(self.school_name)

        if info["valid"]:
            exp = info["expires"]
            exp_txt = "دائم ♾" if exp == "lifetime" else f"ينتهي:  {exp}"
            seats   = "غير محدود" if info["seats"] == 0 else f"{info['seats']} جهاز"

            self.status_lbl.setText("✅  مرخّص")
            self.status_lbl.setStyleSheet(
                f"color: {_S['success']}; font-size: 15px; font-weight: bold; background: transparent;"
            )
            self.detail_lbl.setText(f"{exp_txt}   •   الأجهزة: {seats}   •   صدر: {info['issued']}")
            self.status_card.setStyleSheet(f"""
                background-color: {_S['success_lt']};
                border: 1.5px solid {_S['success']};
                border-radius: 8px;
            """)
            self.status_card.findChildren(QLabel)[0].setStyleSheet(
                f"color: {_S['success']}; font-size:11px; font-weight:bold; "
                f"letter-spacing:1px; background:transparent;"
            )
            self.go_btn.setEnabled(True)
        else:
            self.status_lbl.setText("❌  غير مرخّص")
            self.status_lbl.setStyleSheet(
                f"color: {_S['danger']}; font-size: 15px; font-weight: bold; background: transparent;"
            )
            self.detail_lbl.setText(info["reason"])
            self.status_card.setStyleSheet(f"""
                background-color: {_S['danger_lt']};
                border: 1.5px solid {_S['danger']};
                border-radius: 8px;
            """)
            self.go_btn.setEnabled(False)

    # ── أحداث ─────────────────────────────────────────────────
    def _copy_sid(self):
        QApplication.clipboard().setText(self._sid)
        self.err_lbl.setStyleSheet(
            f"color: {_S['success']}; font-size: 12px; background: transparent;"
        )
        self.err_lbl.setText(f"✓  تم نسخ Server ID:  {self._sid}")

    def _activate(self):
        self.err_lbl.setStyleSheet(
            f"color: {_S['danger']}; font-size: 12px; background: transparent;"
        )
        code = self.code_inp.text().strip()
        if not code:
            self.err_lbl.setText("أدخل كود التفعيل أولاً")
            return
        ok, result = activate(code, self.school_name)
        if ok:
            self.err_lbl.setText("")
            QMessageBox.information(
                self, "✅  تم التفعيل",
                f"تم تفعيل الترخيص بنجاح!\n\n"
                f"Server ID:  {result}\n\n"
                "جميع الأجهزة على الشبكة المحلية مرخّصة الآن."
            )
            self._refresh_status()
        else:
            self.err_lbl.setText(f"❌  {result}")


# ─── LicenseInfoWidget (في الإعدادات) ─────────────────────────
class LicenseInfoWidget(QWidget):
    def __init__(self, school_name: str, parent=None):
        super().__init__(parent)
        self.school_name = school_name
        self._build()

    def _build(self):
        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(10)

        title = QLabel("🔐  معلومات الترخيص")
        title.setStyleSheet(
            "font-size: 14px; font-weight: bold; color: #1D1C1D; background: transparent;"
        )
        lay.addWidget(title)

        info = license_info(self.school_name)
        sc = _S['success'] if info['valid'] else _S['danger']
        rows = [
            ("الحالة:",          "✅  مرخّص" if info['valid'] else "❌  غير مرخّص", sc),
            ("Server ID:",       info['server_id'],       _S['primary']),
            ("MAC Address:",     info['mac'],              None),
            ("تاريخ الإصدار:",   info['issued'],           None),
            ("تاريخ الانتهاء:", "دائم ♾" if info['expires']=="lifetime" else info['expires'],
             _S['success'] if info['expires']=="lifetime" else _S['danger']),
            ("الأجهزة:",        "غير محدود" if info['seats']==0 else str(info['seats']), None),
        ]
        if not info['valid']:
            rows.append(("السبب:", info['reason'], _S['danger']))

        for label, value, color in rows:
            row = QWidget(); row.setStyleSheet("background:transparent;")
            rl = QHBoxLayout(row); rl.setContentsMargins(0,2,0,2); rl.setSpacing(10)
            l = QLabel(label); l.setFixedWidth(130)
            l.setStyleSheet(f"color: #616061; background: transparent;")
            v = QLabel(value); v.setWordWrap(True)
            v.setStyleSheet(
                f"color: {color or '#1D1C1D'}; font-weight: bold; background: transparent;"
            )
            rl.addWidget(l); rl.addWidget(v, 1)
            lay.addWidget(row)

        btn = QPushButton("⚙️  إدارة الترخيص")
        btn.setStyleSheet("""
            QPushButton {
                background: #FFFFFF; color: #1D1C1D;
                border: 1.5px solid #E2E5EE; border-radius: 4px;
                padding: 0 16px; min-height: 36px; max-width: 180px;
            }
            QPushButton:hover { background: #F0F2F7; border-color: #616061; }
        """)
        btn.clicked.connect(self._manage)
        lay.addWidget(btn)

    def _manage(self):
        dlg = LicenseDialog(self.school_name, self)
        dlg.exec()
        for i in reversed(range(self.layout().count())):
            w = self.layout().itemAt(i).widget()
            if w:
                w.deleteLater()
        self._build()

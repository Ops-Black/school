#!/usr/bin/env python3
"""
نظام إدارة المدرسة الأهلية — v3.0
متعدد المدارس | بدون تفعيل | تصميم احترافي
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QFontDatabase

def main():
    app = QApplication(sys.argv)
    app.setLayoutDirection(Qt.RightToLeft)
    app.setApplicationName("SchoolPro")
    app.setOrganizationName("SchoolPro")
    
    # ═════════════════════════════════════════
    #  تحميل خط Cairo
    # ══════════════════════════════════════════
    font_paths = [
        os.path.join(os.path.dirname(__file__), "assets", "fonts", "Cairo-Regular.ttf"),
        os.path.join(os.path.dirname(__file__), "assets", "fonts", "Cairo-Bold.ttf"),
        os.path.join(os.path.dirname(__file__), "fonts", "Cairo-Regular.ttf"),
        os.path.join(os.path.dirname(__file__), "fonts", "Cairo-Bold.ttf"),
    ]
    for fp in font_paths:
        if os.path.exists(fp):
            QFontDatabase.addApplicationFont(fp)
            print(f"✅ تم تحميل الخط: {fp}")
    
    # تطبيق خط Cairo كخط افتراضي
    app.setFont(QFont("Cairo", 13))
    
    from core.db import init
    init()
    from ui.style import MAIN_STYLE
    app.setStyleSheet(MAIN_STYLE)
    
    # ── Main loop: School → Login → App ─────────────────────
    while True:
        from ui.auth import SchoolSelectorDialog
        sel = SchoolSelectorDialog()
        if sel.exec() != 1:
            break
        school_id = sel.selected_school
        if not school_id:
            break
        
        # ── فحص الترخيص مرتبط بالسيرفر المحلي ──────────────────
        import core.db as _DB
        _school_row = _DB.get_school(school_id)
        _school_name = _school_row["name"] if _school_row else ""
        from core.security.license_engine import is_licensed
        if not is_licensed(_school_name):
            from ui.license_dialog import LicenseDialog
            lic_dlg = LicenseDialog(_school_name)
            if lic_dlg.exec() != 1:
                continue
        from ui.auth import LoginDialog
        login = LoginDialog(school_id)
        if login.exec() != 1 or not login.user_info:
            continue
        from ui.main_window import MainWindow
        window = MainWindow(school_id, login.user_info)
        window.show()
        app.exec()
        break

if __name__ == "__main__":
    main()
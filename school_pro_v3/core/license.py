"""
نظام تراخيص البرنامج — مقفل على الجهاز
أول تشغيل على أي جهاز يحتاج رمز التفعيل من المطوّر
بعد التفعيل يُحفظ محلياً ولا يُطلب ثانية
"""
import os, hashlib, platform, json, uuid

MASTER_KEY = "Laith93Abdul"
LICENSE_FILE = os.path.join(os.path.expanduser("~"), ".school_pro_license")

def _machine_id() -> str:
    """توليد معرّف فريد للجهاز الحالي"""
    parts = [
        platform.node(),
        platform.machine(),
        str(uuid.getnode()),   # MAC address
    ]
    raw = "|".join(parts)
    return hashlib.sha256(raw.encode()).hexdigest()[:16].upper()

def is_activated() -> bool:
    """هل الجهاز مفعَّل مسبقاً؟"""
    if not os.path.exists(LICENSE_FILE):
        return False
    try:
        with open(LICENSE_FILE, "r") as f:
            data = json.load(f)
        stored_hash = data.get("hash", "")
        mid = _machine_id()
        expected = hashlib.sha256(f"{MASTER_KEY}{mid}".encode()).hexdigest()
        return stored_hash == expected
    except Exception:
        return False

def activate(entered_key: str) -> tuple[bool, str]:
    """
    محاولة التفعيل بالمفتاح المُدخَل.
    يعيد (True, "") عند النجاح أو (False, رسالة_خطأ) عند الفشل.
    """
    if entered_key.strip() != MASTER_KEY:
        return False, "رمز التفعيل غير صحيح. يرجى التواصل مع المطوّر."
    mid = _machine_id()
    activation_hash = hashlib.sha256(f"{MASTER_KEY}{mid}".encode()).hexdigest()
    data = {"hash": activation_hash, "machine": mid}
    try:
        with open(LICENSE_FILE, "w") as f:
            json.dump(data, f)
        return True, ""
    except Exception as e:
        return False, f"تعذّر حفظ ملف الترخيص: {e}"

def machine_id_display() -> str:
    return _machine_id()

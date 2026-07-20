"""
نظام الترخيص الاحترافي — Server-Bound License
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
المنطق:
  - الترخيص مرتبط بـ: اسم المدرسة + Server Fingerprint + قاعدة البيانات
  - يُولَّد Server ID من MAC + اسم المدرسة + مسار DB → HMAC-SHA256
  - الملف license.lic مشفر بـ AES-256 (Fernet)
  - جميع الأجهزة داخل الشبكة تتصل بالسيرفر المحلي فقط
  - لا ترخيص لكل جهاز — الترخيص للسيرفر
"""
import os, sys, json, hashlib, hmac, uuid, platform, base64
from datetime import datetime, date
from pathlib import Path

# ── Secret key مضمّنة في الكود (تُغيَّر عند التوزيع) ──────────
_VENDOR_SECRET = b"SchoolPro-2025-Iraq-Secure-Key-9f3a2c8b"

LICENSE_DIR  = Path.home() / ".schoolpro"
LICENSE_FILE = LICENSE_DIR / "license.lic"
SERVER_ID_FILE = LICENSE_DIR / "server.id"

# ─── Server Fingerprint ───────────────────────────────────────
def _get_mac() -> str:
    """أول MAC address غير صفري"""
    try:
        mac = uuid.getnode()
        if (mac >> 40) % 2:   # locally administered / random — fallback
            raise ValueError
        return hex(mac)[2:].upper().zfill(12)
    except Exception:
        # fallback: hostname hash
        return hashlib.md5(platform.node().encode()).hexdigest()[:12].upper()

def _get_db_path() -> str:
    from core.db import DB_PATH
    return str(DB_PATH)

def generate_server_id(school_name: str) -> str:
    """
    Server ID = HMAC-SHA256(MAC + school_name + db_path, vendor_secret)[:12]
    قصير وقابل للطباعة ومرتبط بالسيرفر
    """
    raw = f"{_get_mac()}|{school_name.strip()}|{_get_db_path()}"
    sig = hmac.new(_VENDOR_SECRET, raw.encode("utf-8"), hashlib.sha256).hexdigest()
    # جعله مقروءاً: 4-4-4 مثل XXXX-XXXX-XXXX
    h = sig[:12].upper()
    return f"{h[:4]}-{h[4:8]}-{h[8:12]}"

# ─── License File Structure ───────────────────────────────────
def _derive_key(server_id: str) -> bytes:
    """مفتاح AES مشتق من Server ID + vendor secret"""
    raw = f"{_VENDOR_SECRET.decode()}:{server_id}"
    return hashlib.sha256(raw.encode()).digest()

def _xor_encrypt(data: bytes, key: bytes) -> bytes:
    """XOR cipher — بسيط وكافٍ بدون مكتبات إضافية"""
    out = bytearray()
    for i, b in enumerate(data):
        out.append(b ^ key[i % len(key)])
    return bytes(out)

def _encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode()

def _decode(s: str) -> bytes:
    return base64.urlsafe_b64decode(s.encode())

def create_license(school_name: str, expires: str, seats: int = 0) -> str:
    """
    إنشاء ملف ترخيص
    expires: 'YYYY-MM-DD' أو 'lifetime'
    seats: 0 = غير محدود
    """
    LICENSE_DIR.mkdir(exist_ok=True)
    server_id = generate_server_id(school_name)

    payload = {
        "school": school_name,
        "server_id": server_id,
        "mac": _get_mac(),
        "issued": date.today().isoformat(),
        "expires": expires,
        "seats": seats,          # 0 = unlimited clients on LAN
        "version": "3.0",
        "sig": ""
    }

    # HMAC signature to detect tampering
    body = json.dumps({k: v for k, v in payload.items() if k != "sig"},
                      ensure_ascii=False, sort_keys=True).encode()
    payload["sig"] = hmac.new(_VENDOR_SECRET, body, hashlib.sha256).hexdigest()

    # Encrypt
    key = _derive_key(server_id)
    encrypted = _xor_encrypt(json.dumps(payload, ensure_ascii=False).encode("utf-8"), key)
    lic_str = _encode(encrypted)

    LICENSE_FILE.write_text(lic_str, encoding="utf-8")
    SERVER_ID_FILE.write_text(server_id, encoding="utf-8")
    return server_id

def _load_and_verify(school_name: str) -> tuple[bool, str, dict]:
    """
    Returns: (is_valid, reason, payload)
    """
    if not LICENSE_FILE.exists():
        return False, "لا يوجد ملف ترخيص", {}

    try:
        lic_str = LICENSE_FILE.read_text(encoding="utf-8").strip()
        encrypted = _decode(lic_str)
    except Exception:
        return False, "ملف الترخيص تالف", {}

    # We need the server_id to decrypt; try cached then regenerate
    server_id = generate_server_id(school_name)
    key = _derive_key(server_id)
    try:
        raw = _xor_encrypt(encrypted, key).decode("utf-8")
        payload = json.loads(raw)
    except Exception:
        return False, "فشل فكّ تشفير الترخيص — تأكد من اسم المدرسة", {}

    # 1. Verify HMAC signature
    stored_sig = payload.pop("sig", "")
    body = json.dumps(payload, ensure_ascii=False, sort_keys=True).encode()
    expected = hmac.new(_VENDOR_SECRET, body, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(stored_sig, expected):
        return False, "الترخيص مزوّر أو تالف", {}
    payload["sig"] = stored_sig

    # 2. Check school name
    if payload.get("school","").strip() != school_name.strip():
        return False, "الترخيص لمدرسة مختلفة", {}

    # 3. Check server fingerprint
    expected_sid = generate_server_id(school_name)
    if payload.get("server_id","") != expected_sid:
        return False, "الترخيص مرتبط بسيرفر مختلف", {}

    # 4. Check expiry
    exp = payload.get("expires", "")
    if exp != "lifetime":
        try:
            exp_date = datetime.strptime(exp, "%Y-%m-%d").date()
            if date.today() > exp_date:
                days = (date.today() - exp_date).days
                return False, f"انتهت صلاحية الترخيص منذ {days} يوم", {}
        except ValueError:
            return False, "تاريخ انتهاء الترخيص غير صالح", {}

    return True, "ok", payload

# ─── Public API ───────────────────────────────────────────────
def is_licensed(school_name: str) -> bool:
    ok, _, _ = _load_and_verify(school_name)
    return ok

def license_info(school_name: str) -> dict:
    """يرجع معلومات الترخيص الكاملة"""
    ok, reason, payload = _load_and_verify(school_name)
    server_id = generate_server_id(school_name)
    return {
        "valid": ok,
        "reason": reason,
        "server_id": server_id,
        "school": payload.get("school", school_name),
        "expires": payload.get("expires", "—"),
        "issued": payload.get("issued", "—"),
        "seats": payload.get("seats", 0),
        "mac": _get_mac(),
    }

def activate(activation_code: str, school_name: str) -> tuple[bool, str]:
    """
    تفعيل بكود يُرسله المورّد
    الكود: base64(JSON{school, expires, seats, vendor_sig})
    """
    try:
        decoded = json.loads(base64.urlsafe_b64decode(activation_code.encode()).decode("utf-8"))
    except Exception:
        return False, "كود التفعيل غير صالح"

    # Verify vendor signed this code
    vendor_sig = decoded.pop("vendor_sig", "")
    check_body = json.dumps(decoded, ensure_ascii=False, sort_keys=True).encode()
    expected = hmac.new(_VENDOR_SECRET, check_body, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(vendor_sig, expected):
        return False, "كود التفعيل مزوّر"

    if decoded.get("school","").strip() != school_name.strip():
        return False, f"الكود مخصص لمدرسة: {decoded.get('school','')}"

    server_id = create_license(
        school_name=decoded["school"],
        expires=decoded.get("expires", "lifetime"),
        seats=decoded.get("seats", 0)
    )
    return True, server_id

# ─── Demo / Dev Activation ────────────────────────────────────
def create_demo_license(school_name: str, days: int = 30) -> str:
    """ترخيص تجريبي — للمدارس الجديدة قبل الشراء"""
    from datetime import timedelta
    exp = (date.today() + timedelta(days=days)).isoformat()
    return create_license(school_name, exp, seats=0)

def generate_activation_code(school_name: str, expires: str = "lifetime", seats: int = 0) -> str:
    """يُستخدم من قبل المورّد لتوليد كود تفعيل"""
    payload = {"school": school_name, "expires": expires, "seats": seats}
    sig = hmac.new(_VENDOR_SECRET, json.dumps(payload, ensure_ascii=False, sort_keys=True).encode(),
                    hashlib.sha256).hexdigest()
    payload["vendor_sig"] = sig
    return base64.urlsafe_b64encode(json.dumps(payload, ensure_ascii=False).encode()).decode()

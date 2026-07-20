"""
تعريف المراحل الدراسية العراقية بشكل كامل ومنظم
كل مرحلة معزولة عن الأخرى مع بياناتها الكاملة
"""
from dataclasses import dataclass, field
from typing import List

@dataclass
class GradeLevel:
    key: str            # مفتاح فريد
    name: str           # الاسم الكامل
    stage: str          # المرحلة: ابتدائي / متوسط / إعدادي
    branch: str         # الفرع: عام / علمي / أدبي
    subjects: List[str] # المواد الدراسية الخاصة بهذه المرحلة
    pass_mark: float    # درجة النجاح
    order: int          # الترتيب للعرض

# ══════════════════════════════════════════════════════════════
# المراحل الدراسية العراقية الكاملة
# ══════════════════════════════════════════════════════════════

ELEMENTARY_SUBJECTS = [
    "اللغة العربية", "الرياضيات", "العلوم", "التربية الإسلامية",
    "الدراسات الاجتماعية", "اللغة الإنكليزية", "التربية الفنية",
    "التربية الرياضية", "الحاسوب"
]

MIDDLE_SUBJECTS = [
    "اللغة العربية", "الرياضيات", "العلوم", "التربية الإسلامية",
    "التاريخ", "الجغرافية", "اللغة الإنكليزية", "التربية الوطنية",
    "التربية الفنية", "التربية الرياضية", "الحاسوب"
]

HIGH_SCIENCE_SUBJECTS = [
    "اللغة العربية", "الرياضيات", "الفيزياء", "الكيمياء",
    "الأحياء", "التربية الإسلامية", "اللغة الإنكليزية",
    "التربية الرياضية"
]

HIGH_ART_SUBJECTS = [
    "اللغة العربية", "التاريخ", "الجغرافية", "التربية الإسلامية",
    "علم النفس والاجتماع", "المنطق وفلسفة", "اللغة الإنكليزية",
    "التربية الرياضية"
]

ALL_GRADES: List[GradeLevel] = [
    # ── المرحلة الابتدائية (6 صفوف) ──────────────────────────
    GradeLevel("g1_elm",  "الأول الابتدائي",   "ابتدائي", "عام", ELEMENTARY_SUBJECTS, 50.0,  1),
    GradeLevel("g2_elm",  "الثاني الابتدائي",  "ابتدائي", "عام", ELEMENTARY_SUBJECTS, 50.0,  2),
    GradeLevel("g3_elm",  "الثالث الابتدائي",  "ابتدائي", "عام", ELEMENTARY_SUBJECTS, 50.0,  3),
    GradeLevel("g4_elm",  "الرابع الابتدائي",  "ابتدائي", "عام", ELEMENTARY_SUBJECTS, 50.0,  4),
    GradeLevel("g5_elm",  "الخامس الابتدائي",  "ابتدائي", "عام", ELEMENTARY_SUBJECTS, 50.0,  5),
    GradeLevel("g6_elm",  "السادس الابتدائي",  "ابتدائي", "عام", ELEMENTARY_SUBJECTS, 50.0,  6),

    # ── المرحلة المتوسطة (3 صفوف) ─────────────────────────────
    GradeLevel("g1_mid",  "الأول المتوسط",     "متوسط",   "عام", MIDDLE_SUBJECTS,     50.0,  7),
    GradeLevel("g2_mid",  "الثاني المتوسط",    "متوسط",   "عام", MIDDLE_SUBJECTS,     50.0,  8),
    GradeLevel("g3_mid",  "الثالث المتوسط",    "متوسط",   "عام", MIDDLE_SUBJECTS,     50.0,  9),

    # ── المرحلة الإعدادية — الفرع العلمي (3 صفوف) ────────────
    GradeLevel("g4_sci",  "الرابع الإعدادي — علمي",   "إعدادي", "علمي", HIGH_SCIENCE_SUBJECTS, 50.0, 10),
    GradeLevel("g5_sci",  "الخامس الإعدادي — علمي",   "إعدادي", "علمي", HIGH_SCIENCE_SUBJECTS, 50.0, 11),
    GradeLevel("g6_sci",  "السادس الإعدادي — علمي",   "إعدادي", "علمي", HIGH_SCIENCE_SUBJECTS, 50.0, 12),

    # ── المرحلة الإعدادية — الفرع الأدبي (3 صفوف) ────────────
    GradeLevel("g4_art",  "الرابع الإعدادي — أدبي",   "إعدادي", "أدبي", HIGH_ART_SUBJECTS,    50.0, 13),
    GradeLevel("g5_art",  "الخامس الإعدادي — أدبي",   "إعدادي", "أدبي", HIGH_ART_SUBJECTS,    50.0, 14),
    GradeLevel("g6_art",  "السادس الإعدادي — أدبي",   "إعدادي", "أدبي", HIGH_ART_SUBJECTS,    50.0, 15),
]

# فهارس سريعة
BY_KEY   = {g.key:  g for g in ALL_GRADES}
BY_NAME  = {g.name: g for g in ALL_GRADES}
NAMES    = [g.name for g in ALL_GRADES]

def by_stage(stage: str) -> List[GradeLevel]:
    """الصفوف حسب المرحلة: ابتدائي / متوسط / إعدادي"""
    return [g for g in ALL_GRADES if g.stage == stage]

def subjects_for(grade_name: str) -> List[str]:
    """قائمة المواد لصف معين"""
    g = BY_NAME.get(grade_name)
    return g.subjects if g else ELEMENTARY_SUBJECTS

def stages() -> List[str]:
    """قائمة المراحل الفريدة بالترتيب"""
    seen = []; out = []
    for g in ALL_GRADES:
        if g.stage not in seen:
            seen.append(g.stage); out.append(g.stage)
    return out

SECTIONS = ["أ", "ب", "ج", "د", "هـ", "و"]

STAGE_COLORS = {
    "ابتدائي": "#4A6CF7",   # أزرق
    "متوسط":   "#7C3AED",   # بنفسجي
    "إعدادي":  "#059669",   # أخضر
}

BRANCH_COLORS = {
    "عام":   "#4A6CF7",
    "علمي":  "#059669",
    "أدبي":  "#D97706",
}

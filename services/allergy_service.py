
# 알레르기 표현 통합
ALLERGY_GROUPS = {
    "해산물": [
        "해산물", "생선", "갑각류",
        "연체류", "조개류"
    ],
    "생선": ["생선"],
    "갑각류": ["갑각류"],
    "땅콩": ["땅콩"],
    "밀": ["밀"],
    "계란": ["계란", "달걀"],
    "달걀": ["계란", "달걀"],
    "대두": ["대두", "콩"]
}


# 알레르기 표현 통일 함수
def normalize_allergies(allergies):

    normalized = set()

    for allergy in allergies:

        allergy = allergy.strip()

        if allergy in ALLERGY_GROUPS:
            normalized.update(
                ALLERGY_GROUPS[allergy]
            )
        else:
            normalized.add(allergy)

    return normalized


# 그룹 전체 알레르기 취합
def collect_group_allergies(members):

    all_allergies = set()

    for member in members:

        normalized = normalize_allergies(
            member["allergies"]
        )

        all_allergies.update(normalized)

    return all_allergies


# 메뉴 알레르기 검증
def validate_menu_allergy(menu_allergens, members):

    group_allergies = collect_group_allergies(
        members
    )

    normalized_menu_allergies = normalize_allergies(
        menu_allergens
    )

    conflicts = group_allergies.intersection(
        normalized_menu_allergies
    )

    return {
        "is_safe": len(conflicts) == 0,
        "conflicts": sorted(conflicts)
    }


# 그룹 전체 예산 계산
def calculate_group_budget(members):

    if not members:
        raise ValueError("그룹 구성원이 없습니다.")

    total_budget = sum(
        member["budget"] for member in members
    )

    min_budget = min(
        member["budget"] for member in members
    )

    return {
        "total_budget": total_budget,
        "min_budget": min_budget,
        "member_count": len(members)
    }


# 메뉴 가격 검증
def validate_menu_budget(menu_price, members):

    budget_info = calculate_group_budget(members)

    # 각 구성원의 개인 예산 확인
    over_budget_members = [
        member["name"]
        for member in members
        if menu_price > member["budget"]
    ]

    # 그룹 전체 예상 비용
    total_price = menu_price * len(members)

    # 그룹 전체 예산 확인
    group_over_budget = (
        total_price > budget_info["total_budget"]
    )

    # 모든 조건 통과 여부
    is_valid = (
        len(over_budget_members) == 0
        and not group_over_budget
    )

    return {
        "is_valid": is_valid,
        "menu_price": menu_price,
        "total_price": total_price,
        "total_budget": budget_info["total_budget"],
        "remaining_budget": (
            budget_info["total_budget"] - total_price
        ),
        "over_budget_members": over_budget_members
    }

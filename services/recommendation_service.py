from services.menu_service import get_verified_menus
from services.budget_service import validate_menu_budget
from services.allergy_service import validate_menu_allergy


# 식당 한 곳 평가
def evaluate_restaurant(restaurant, members):

    # 가격 정보 확인
    if restaurant.get("price") is None:
        return {
            "status": "정보 확인 필요",
            "reason": "메뉴 가격 정보가 없습니다."
        }

    # 알레르기 정보 확인
    if restaurant.get("allergens") is None:
        return {
            "status": "정보 확인 필요",
            "reason": "알레르기 정보가 없습니다."
        }

    # 예산 검증
    budget_result = validate_menu_budget(
        restaurant["price"],
        members
    )

    # 알레르기 검증
    allergy_result = validate_menu_allergy(
        restaurant["allergens"],
        members
    )

    # 알레르기 충돌 확인
    if not allergy_result["is_safe"]:
        return {
            "status": "추천 제외",
            "reason": f"알레르기 충돌: {allergy_result['conflicts']}"
        }

    # 예산 초과 확인
    if not budget_result["is_valid"]:
        return {
            "status": "추천 제외",
            "reason": f"예산 초과 구성원: {budget_result['over_budget_members']}"
        }

    return {
        "status": "추천 가능",
        "reason": "예산과 알레르기 조건을 통과했습니다.",
        "budget_info": budget_result,
        "allergy_info": allergy_result
    }


# 여러 식당 평가
def evaluate_restaurants(restaurants, members):

    results = []

    for restaurant in restaurants:

        evaluation = evaluate_restaurant(
            restaurant,
            members
        )

        restaurant_result = restaurant.copy()
        restaurant_result.update(evaluation)

        results.append(restaurant_result)

    return results


# 검증된 메뉴 중 그룹 조건에 맞는 메뉴 추천
def recommend_verified_menus(members):

    # 검증 완료 메뉴 불러오기
    menus = get_verified_menus()

    recommended_menus = []

    for menu in menus:

        # 예산 및 알레르기 조건 평가
        evaluation = evaluate_restaurant(
            menu,
            members
        )

        # 추천 가능한 메뉴만 추가
        if evaluation["status"] == "추천 가능":

            menu_result = menu.copy()
            menu_result.update(evaluation)

            recommended_menus.append(menu_result)

    return recommended_menus

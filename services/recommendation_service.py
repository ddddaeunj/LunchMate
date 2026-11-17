
from services.budget_service import validate_menu_budget
from services.allergy_service import validate_menu_allergy


# 식당 후보 검증
def filter_restaurants(restaurants, members):

    valid_restaurants = []

    for restaurant in restaurants:

        # 가격 정보가 없는 식당은 제외
        if restaurant.get("price") is None:
            continue

        # 알레르기 정보가 확인되지 않은 식당은 제외
        if restaurant.get("allergens") is None:
            continue

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

        # 두 조건을 모두 통과한 식당만 추가
        if (
            budget_result["is_valid"]
            and allergy_result["is_safe"]
        ):

            restaurant_result = restaurant.copy()

            restaurant_result["budget_info"] = budget_result
            restaurant_result["allergy_info"] = allergy_result

            valid_restaurants.append(restaurant_result)

    return valid_restaurants

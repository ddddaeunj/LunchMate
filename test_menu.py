from services.menu_service import (
    add_menu,
    get_all_menus,
    verify_menu,
    get_verified_menus
)

# 테스트용 메뉴 등록
menu = add_menu(
    restaurant_name="테스트 식당",
    menu_name="테스트 비빔밥",
    price=9000,
    allergens=["대두"],
    source="테스트 데이터"
)

print("===== 메뉴 등록 결과 =====")
print(menu)


# 저장된 메뉴 전체 조회
menus = get_all_menus()

print("\n===== 저장된 메뉴 목록 =====")

for item in menus:
    print("식당:", item["restaurant_name"])
    print("메뉴:", item["menu_name"])
    print("가격:", item["price"])
    print("알레르기:", item["allergens"])
    print("검증 여부:", item["is_verified"])
    print("--------------------")

# 마지막 메뉴 검증
menus = get_all_menus()

last_index = len(menus) - 1

verified_menu = verify_menu(last_index)

print("\n===== 메뉴 검증 결과 =====")
print("메뉴:", verified_menu["menu_name"])
print("검증 여부:", verified_menu["is_verified"])


# 검증 완료 메뉴 조회
verified_menus = get_verified_menus()

print("\n===== 검증 완료 메뉴 목록 =====")

for menu in verified_menus:

    print("식당:", menu["restaurant_name"])
    print("메뉴:", menu["menu_name"])
    print("가격:", f'{menu["price"]:,}원')
    print("알레르기:", menu["allergens"])
    print("--------------------")

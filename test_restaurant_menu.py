from services.restaurant_menu_service import update_restaurant_menu
from services.restaurant_menu_service import delete_restaurant_menu
from services.restaurant_menu_service import (
    get_restaurant_menus,
    save_restaurant_menu
)


# 테스트용 식당 메뉴
menu = {
    "restaurant_name": "테스트 식당",
    "menu_name": "김치찌개",
    "price": 9000,
    "allergens": ["대두"],
    "source": "테스트 데이터"
}


# 메뉴 저장
result = save_restaurant_menu(menu)

if result:
    print("새로운 메뉴가 저장되었습니다.")
else:
    print("이미 등록된 메뉴입니다.")


# 저장된 메뉴 확인
menus = get_restaurant_menus()

print(menus)


# 특정 식당의 메뉴 조회
from services.restaurant_menu_service import get_menus_by_restaurant

restaurant_menus = get_menus_by_restaurant("테스트 식당")

print("\n테스트 식당의 메뉴:")
print(restaurant_menus)

# 메뉴 정보 수정
result = update_restaurant_menu(
    "테스트 식당",
    "김치찌개",
    new_price=10000,
    new_allergens=["대두", "밀"]
)

if result:
    print("메뉴 수정 완료!")
else:
    print("수정할 메뉴가 없습니다.")

# 수정된 메뉴 확인
menus = get_restaurant_menus()

print("수정된 메뉴 목록:")
print(menus)

# 특정 식당의 메뉴 삭제
result = delete_restaurant_menu("테스트 식당", "김치찌개")

if result:
    print("메뉴 삭제 완료!")
else:
    print("삭제할 메뉴가 없습니다.")

# 삭제 후 메뉴 확인
menus = get_restaurant_menus()

print("삭제 후 메뉴 목록:")
print(menus)
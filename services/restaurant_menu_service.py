
import json
import os


# 식당 메뉴 데이터 파일 경로
MENU_FILE = "data/restaurant_menus.json"


# 메뉴 데이터 불러오기
def get_restaurant_menus():

    if not os.path.exists(MENU_FILE):
        return []

    with open(MENU_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


# 식당 메뉴 저장하기

# 식당 메뉴 저장하기
def save_restaurant_menu(menu):

    menus = get_restaurant_menus()

    # 같은 식당에 동일한 메뉴가 있는지 확인
    for existing_menu in menus:
        if (
            existing_menu["restaurant_name"] == menu["restaurant_name"]
            and existing_menu["menu_name"] == menu["menu_name"]
        ):
            return False

    menus.append(menu)

    with open(MENU_FILE, "w", encoding="utf-8") as file:
        json.dump(
            menus,
            file,
            ensure_ascii=False,
            indent=4
        )

    return True



# 특정 식당의 메뉴만 불러오기
def get_menus_by_restaurant(restaurant_name):

    menus = get_restaurant_menus()

    restaurant_menus = []

    for menu in menus:
        if menu["restaurant_name"] == restaurant_name:
            restaurant_menus.append(menu)

    return restaurant_menus

# 특정 식당의 메뉴 삭제
def delete_restaurant_menu(restaurant_name, menu_name):

    menus = get_restaurant_menus()

    updated_menus = []

    for menu in menus:
        if not (
            menu["restaurant_name"] == restaurant_name
            and menu["menu_name"] == menu_name
        ):
            updated_menus.append(menu)

    with open(MENU_FILE, "w", encoding="utf-8") as file:
        json.dump(
            updated_menus,
            file,
            ensure_ascii=False,
            indent=4
        )

    return len(menus) != len(updated_menus)


# 특정 식당의 메뉴 정보 수정
def update_restaurant_menu(
    restaurant_name,
    menu_name,
    new_price=None,
    new_allergens=None
):

    menus = get_restaurant_menus()

    updated = False

    for menu in menus:
        if (
            menu["restaurant_name"] == restaurant_name
            and menu["menu_name"] == menu_name
        ):

            # 가격 수정
            if new_price is not None:
                menu["price"] = new_price

            # 알레르기 정보 수정
            if new_allergens is not None:
                menu["allergens"] = new_allergens

            updated = True

    if updated:
        with open(MENU_FILE, "w", encoding="utf-8") as file:
            json.dump(
                menus,
                file,
                ensure_ascii=False,
                indent=4
            )

    return updated

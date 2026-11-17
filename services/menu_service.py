
import json
from pathlib import Path


# 메뉴 데이터 파일 경로
BASE_DIR = Path(__file__).resolve().parent.parent
MENU_FILE = BASE_DIR / "data" / "menu_items.json"


# 메뉴 데이터 불러오기
def get_all_menus():

    if not MENU_FILE.exists():
        return []

    with open(MENU_FILE, "r", encoding="utf-8") as file:

        menus = json.load(file)

    return menus


# 새로운 메뉴 저장하기
def add_menu(
    restaurant_name,
    menu_name,
    price,
    allergens,
    source
):

    menus = get_all_menus()

    # 메뉴 정보 생성
    new_menu = {
        "restaurant_name": restaurant_name,
        "menu_name": menu_name,
        "price": price,
        "allergens": allergens,
        "is_verified": False,
        "source": source
    }

    # 메뉴 목록에 추가
    menus.append(new_menu)

    # JSON 파일에 저장
    with open(MENU_FILE, "w", encoding="utf-8") as file:

        json.dump(
            menus,
            file,
            ensure_ascii=False,
            indent=4
        )

    return new_menu


# 메뉴 정보 검증 처리
def verify_menu(menu_index):

    menus = get_all_menus()

    # 메뉴 번호 확인
    if menu_index < 0 or menu_index >= len(menus):
        raise ValueError("존재하지 않는 메뉴입니다.")

    # 검증 상태 변경
    menus[menu_index]["is_verified"] = True

    # 변경된 정보 저장
    with open(MENU_FILE, "w", encoding="utf-8") as file:

        json.dump(
            menus,
            file,
            ensure_ascii=False,
            indent=4
        )

    return menus[menu_index]

# 검증이 완료된 메뉴만 조회
def get_verified_menus():

    menus = get_all_menus()

    verified_menus = []

    for menu in menus:

        if menu["is_verified"] is True:
            verified_menus.append(menu)

    return verified_menus

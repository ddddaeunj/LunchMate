
from services.recommendation_service import recommend_verified_menus


# 테스트용 그룹 구성원
members = [
    {
        "name": "철수",
        "budget": 10000,
        "allergies": ["땅콩"],
        "likes": ["한식"],
        "dislikes": ["매운 음식"]
    },
    {
        "name": "영희",
        "budget": 12000,
        "allergies": [],
        "likes": ["일식"],
        "dislikes": ["해산물"]
    }
]


# 추천 가능한 메뉴 조회
recommended_menus = recommend_verified_menus(members)


# 결과 출력
print("===== 추천 가능한 메뉴 =====")

if not recommended_menus:

    print("추천 가능한 메뉴가 없습니다.")

else:

    for menu in recommended_menus:

        print("식당:", menu["restaurant_name"])
        print("메뉴:", menu["menu_name"])
        print("가격:", f'{menu["price"]:,}원')
        print("상태:", menu["status"])
        print("--------------------")

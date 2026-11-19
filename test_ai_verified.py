
from services.recommendation_service import recommend_verified_menus
from services.ai_service import recommend_with_ai


members = [
    {
        "name": "철수",
        "budget": 10000,
        "allergies": ["땅콩"],
        "likes": ["한식", "고기"],
        "dislikes": ["매운 음식"]
    },
    {
        "name": "영희",
        "budget": 12000,
        "allergies": [],
        "likes": ["일식", "면 요리"],
        "dislikes": ["해산물"]
    }
]


# Python으로 예산과 알레르기 조건 검증
safe_menus = recommend_verified_menus(members)

print("===== Python 검증 결과 =====")

for menu in safe_menus:
    print(menu["restaurant_name"], menu["menu_name"])


# 검증을 통과한 메뉴가 있을 때만 AI 실행
if safe_menus:
    ai_result = recommend_with_ai(members, safe_menus)

    print("\n===== AI 최종 추천 결과 =====")
    print(ai_result)

else:
    print("추천 가능한 메뉴가 없습니다.")

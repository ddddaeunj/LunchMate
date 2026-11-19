
from services.ai_service import recommend_with_ai


# 테스트 그룹 구성원
members = [
    {
        "name": "철수",
        "budget": 10000,
        "likes": ["한식", "고기"],
        "dislikes": ["매운 음식"],
        "allergies": ["땅콩"]
    },
    {
        "name": "영희",
        "budget": 12000,
        "likes": ["일식", "면 요리"],
        "dislikes": ["해산물"],
        "allergies": []
    }
]


# 테스트 식당 후보
restaurants = [
    {
        "name": "한식당",
        "category": "한식",
        "address": "경북 구미시",
    },
    {
        "name": "일식당",
        "category": "일식",
        "address": "경북 구미시",
    },
    {
        "name": "중식당",
        "category": "중식",
        "address": "경북 구미시",
    }
]


# AI 추천 실행
result = recommend_with_ai(members, restaurants)

print("===== AI 점심 추천 결과 =====")
print(result)

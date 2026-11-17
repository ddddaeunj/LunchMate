
from services.recommendation_service import filter_restaurants


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


# 테스트용 식당 데이터
restaurants = [
    {
        "name": "한식당",
        "price": 9000,
        "allergens": []
    },
    {
        "name": "땅콩 음식점",
        "price": 8000,
        "allergens": ["땅콩"]
    },
    {
        "name": "고급 레스토랑",
        "price": 15000,
        "allergens": []
    },
    {
        "name": "가격 정보 없는 식당",
        "price": None,
        "allergens": []
    }
]


# 추천 가능한 식당 필터링
results = filter_restaurants(
    restaurants,
    members
)


# 결과 출력
print("===== 추천 가능한 식당 =====")

for restaurant in results:

    print("식당 이름:", restaurant["name"])
    print("1인 가격:", restaurant["price"])
    print(
        "그룹 전체 가격:",
        restaurant["budget_info"]["total_price"]
    )
    print("--------------------")

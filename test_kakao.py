from api.kakao_api import search_restaurants


# 금오공대 주변 식당 검색
restaurants = search_restaurants("구미역 음식점")


# 검색 결과 출력
print("===== 식당 검색 결과 =====")

for restaurant in restaurants:

    print("식당 이름:", restaurant["name"])
    print("주소:", restaurant["address"])
    print("카테고리:", restaurant["category"])
    print("상세 페이지:", restaurant["place_url"])
    print("----------------------")
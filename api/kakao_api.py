import requests
import streamlit as st


# 카카오 로컬 API로 식당 검색
def search_restaurants(keyword, latitude=None, longitude=None):

    api_key = st.secrets["KAKAO_REST_API_KEY"]

    url = "https://dapi.kakao.com/v2/local/search/keyword.json"

    headers = {
        "Authorization": f"KakaoAK {api_key}"
    }

    params = {
        "query": keyword,
        "size": 15
    }

    # 위치 정보가 있으면 검색 범위 설정
    if latitude is not None and longitude is not None:
        params["y"] = latitude
        params["x"] = longitude
        params["radius"] = 5000

    response = requests.get(
        url,
        headers=headers,
        params=params,
        timeout=10
    )

    if response.status_code != 200:
        raise Exception(
            f"HTTP 오류: {response.status_code}\n"
            f"상세 내용: {response.text}"
        )

    data = response.json()

    restaurants = []

    for place in data["documents"]:

        restaurant = {
            "name": place["place_name"],
            "address": place["road_address_name"],
            "category": place["category_name"],
            "latitude": float(place["y"]),
            "longitude": float(place["x"]),
            "place_url": place["place_url"]
        }

        restaurants.append(restaurant)

    return restaurants
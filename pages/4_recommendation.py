
import streamlit as st

from api.kakao_api import search_restaurants
from services.member_service import get_members_by_group
from services.recommendation_service import evaluate_restaurants
from services.group_service import get_group_by_id
from streamlit_geolocation import streamlit_geolocation


# 페이지 제목
st.title("🍽️ LunchMate")
st.subheader("우리 그룹의 점심 추천")


# 그룹 참여 여부 확인
member = st.session_state.get("joined_member")

if member is None:

    st.warning("먼저 그룹에 참여해 주세요.")

else:

    # 그룹 정보 조회
    group = get_group_by_id(member["group_id"])

    # 구성원 정보 조회
    members = get_members_by_group(member["group_id"])

    st.subheader("👥 그룹 구성원")

    if group:
        st.write("그룹 이름:", group["group_name"])

    st.write("참여 인원:", f"{len(members)}명")

    for person in members:

        with st.container(border=True):

            st.write("이름:", person["name"])
            st.write("예산:", f'{person["budget"]:,}원')
            st.write("알레르기:", person["allergies"])
            st.write("선호 음식:", person["likes"])
            st.write("기피 음식:", person["dislikes"])


    # 식당 검색
    st.divider()

    
    st.subheader("🔎 주변 식당 검색")

    location = st.text_input(
        "검색 지역",
        placeholder="예: 금오공과대학교"
    )

    category = st.selectbox(
        "음식 종류",
        ["전체", "한식", "일식", "중식", "양식", "분식", "카페"]
    )

    if st.button("주변 식당 검색"):

        if not location.strip():
            st.warning("검색 지역을 입력해 주세요.")

        else:
            try:
                if category == "전체":
                    keyword = f"{location} 맛집"
                else:
                    keyword = f"{location} {category}"

                restaurants = search_restaurants(keyword)

                evaluated_restaurants = evaluate_restaurants(
                    restaurants,
                    members
                )

                st.session_state.evaluated_restaurants = (
                    evaluated_restaurants
                )

            except Exception as e:
                st.error(f"식당 검색 중 오류가 발생했습니다: {e}")

    # 현재 위치 가져오기
    st.write("📍 현재 위치")

    location_data = streamlit_geolocation()

    latitude = None
    longitude = None

    if location_data:
        latitude = location_data.get("latitude")
        longitude = location_data.get("longitude")

        if latitude is not None and longitude is not None:
            st.success("현재 위치를 확인했습니다.")
            st.write("위도:", latitude)
            st.write("경도:", longitude)
        else:
            st.info("현재 위치 버튼을 눌러 위치 정보를 가져와 주세요.")

    
    if st.button("점심 식당 검색"):

        if not location.strip() and (latitude is None or longitude is None):
            st.warning("현재 위치를 확인하거나 검색 지역을 입력해 주세요.")

        else:
            try:
                # 검색 키워드 설정
                if location.strip():
                    if category == "전체":
                        keyword = f"{location} 맛집"
                    else:
                        keyword = f"{location} {category}"

                    # 직접 입력한 지역으로 검색
                    restaurants = search_restaurants(keyword)

                else:
                    if category == "전체":
                        keyword = "맛집"
                    else:
                        keyword = category

                    # 현재 위치 주변 식당 검색
                    restaurants = search_restaurants(
                        keyword,
                        latitude=latitude,
                        longitude=longitude
                    )

                # 실제 식당 정보 평가
                evaluated_restaurants = evaluate_restaurants(
                    restaurants,
                    members
                )

                st.session_state.evaluated_restaurants = (
                    evaluated_restaurants
                )

            except Exception as e:
                st.error(f"식당 검색 중 오류가 발생했습니다: {e}")



    # 검색 결과 표시
    if "evaluated_restaurants" in st.session_state:

        restaurants = st.session_state.evaluated_restaurants

        st.divider()
        st.subheader("📋 검색 및 평가 결과")

        if not restaurants:

            st.info("검색 결과가 없습니다.")

        else:

            for restaurant in restaurants:

                with st.container(border=True):

                    st.subheader(restaurant["name"])

                    st.write("주소:", restaurant["address"])
                    st.write("카테고리:", restaurant["category"])

                    st.write(
                        "평가 상태:",
                        restaurant["status"]
                    )

                    st.write(
                        "평가 내용:",
                        restaurant["reason"]
                    )

                    st.link_button(
                        "카카오맵에서 보기",
                        restaurant["place_url"]
                    )

def evaluate_restaurants(restaurants, members):

    results = []

    for restaurant in restaurants:

        evaluation = evaluate_restaurant(
            restaurant,
            members
        )

        restaurant_result = restaurant.copy()
        restaurant_result.update(evaluation)

        results.append(restaurant_result)

    return results
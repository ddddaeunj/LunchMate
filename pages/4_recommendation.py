
import streamlit as st

from api.kakao_api import search_restaurants
from services.member_service import get_members_by_group
from services.recommendation_service import evaluate_restaurants
from services.group_service import get_group_by_id


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

    st.subheader("🔎 식당 검색")

    keyword = st.text_input(
        "검색어",
        placeholder="예: 금오공대 맛집"
    )

    if st.button("점심 식당 검색"):

        if not keyword.strip():

            st.warning("검색어를 입력해 주세요.")

        else:

            try:

                # 카카오 API로 식당 검색
                restaurants = search_restaurants(keyword)

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
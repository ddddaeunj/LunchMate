
import streamlit as st

from api.kakao_api import search_restaurants
from services.member_service import get_members_by_group

# 그룹 구성원 정보 확인
st.subheader("👥 함께 점심 먹는 사람들")

member = st.session_state.get("joined_member")

if member is None:

    st.warning("먼저 그룹에 참여해 주세요.")

else:

    members = get_members_by_group(member["group_id"])

    st.write(f"그룹 이름: {member['group_name']}")
    st.write(f"참여 인원: {len(members)}명")

    for person in members:

        with st.container(border=True):

            st.write(f"이름: {person['name']}")
            st.write(f"예산: {person['budget']:,}원")
            st.write(f"알레르기: {person['allergies']}")
            st.write(f"선호 음식: {person['likes']}")
            st.write(f"기피 음식: {person['dislikes']}")

# 페이지 제목
st.title("🍽️ LunchMate")
st.subheader("식당 검색")

st.write("원하는 지역이나 검색어를 입력해 보세요.")


# 검색어 입력
keyword = st.text_input(
    "검색어",
    placeholder="예: 금오공대 맛집"
)


# 검색 버튼
if st.button("식당 검색"):

    if not keyword.strip():
        st.warning("검색어를 입력해 주세요.")

    else:
        try:
            restaurants = search_restaurants(keyword)

            if restaurants:
                st.success(
                    f"{len(restaurants)}개의 식당을 찾았어요!"
                )

                for restaurant in restaurants:

                    with st.container(border=True):

                        st.subheader(restaurant["name"])

                        st.write(
                            "주소:",
                            restaurant["address"]
                        )

                        st.write(
                            "카테고리:",
                            restaurant["category"]
                        )

                        st.link_button(
                            "카카오맵에서 보기",
                            restaurant["place_url"]
                        )

            else:
                st.info("검색 결과가 없습니다.")

        except Exception as e:
            st.error(f"식당 검색 중 오류가 발생했어요: {e}")

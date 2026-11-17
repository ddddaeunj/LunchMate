
import streamlit as st

from services.member_service import update_member_profile


# 페이지 제목
st.title("🍽️ LunchMate")
st.subheader("나의 음식 프로필")

st.write("알레르기와 음식 취향을 입력해 주세요.")


# 그룹 참여 여부 확인
member = st.session_state.get("joined_member")

if member is None:

    st.warning("먼저 그룹에 참여해 주세요.")

else:

    st.write(f"참여 그룹: {member['group_name']}")
    st.write(f"이름: {member['name']}")

    # 알레르기 입력
    allergies = st.multiselect(
        "알레르기가 있는 음식",
        [
            "땅콩",
            "밀",
            "계란",
            "대두",
            "생선",
            "갑각류",
            "조개류",
            "우유",
            "돼지고기"
        ]
    )

    # 선호 음식 입력
    likes = st.multiselect(
        "좋아하는 음식",
        [
            "한식",
            "중식",
            "일식",
            "양식",
            "분식",
            "국밥",
            "면류",
            "고기",
            "샐러드"
        ]
    )

    # 기피 음식 입력
    dislikes = st.multiselect(
        "싫어하거나 피하고 싶은 음식",
        [
            "매운 음식",
            "해산물",
            "채소",
            "고기",
            "면류",
            "기름진 음식"
        ]
    )

    # 저장 버튼
    if st.button("프로필 저장"):

        try:
            updated_member = update_member_profile(
                member_id=member["member_id"],
                allergies=allergies,
                likes=likes,
                dislikes=dislikes
            )

            st.session_state.joined_member = updated_member

            st.success("음식 프로필이 저장되었습니다!")

            st.write("알레르기:", updated_member["allergies"])
            st.write("선호 음식:", updated_member["likes"])
            st.write("기피 음식:", updated_member["dislikes"])

        except Exception as e:
            st.error(f"프로필 저장 중 오류가 발생했습니다: {e}")


import streamlit as st
from services.user_service import (
    get_user_id,
    get_user_profile,
    save_user_profile
)

# 브라우저 사용자 ID 확인
user_id = get_user_id()

# 페이지 제목
st.title("🍽️ LunchMate")
st.subheader("나의 음식 프로필")

st.write("점심 메뉴 추천을 위해 나의 정보를 입력해 주세요.")

# 데이터베이스에서 기존 프로필 불러오기
if "profile" not in st.session_state:
    st.session_state.profile = get_user_profile(user_id)

profile = st.session_state.profile or {}

# 입력 항목
with st.form("profile_form"):

    # 이름 입력
    name = st.text_input(
        "이름",
        value=profile.get("name", ""),
        placeholder="이름을 입력하세요."
    )

    # 예산 입력
    budget = st.number_input(
        "1인 점심 예산 (원)",
        min_value=1000,
        value=profile.get("budget", 10000),
        step=1000
    )

    # 알레르기 입력
    allergies = st.multiselect(
        "알레르기가 있는 음식",
        [
            "땅콩", "밀", "계란", "대두", "생선",
            "갑각류", "조개류", "우유", "돼지고기"
        ],
        default=profile.get("allergies", [])
    )

    # 선호 음식 입력
    likes = st.multiselect(
        "좋아하는 음식",
        [
            "한식", "중식", "일식", "양식", "분식",
            "국밥", "면류", "고기", "샐러드"
        ],
        default=profile.get("likes", [])
    )

    # 기피 음식 입력
    dislikes = st.multiselect(
        "싫어하거나 피하고 싶은 음식",
        [
            "매운 음식", "해산물", "채소",
            "고기", "면류", "기름진 음식"
        ],
        default=profile.get("dislikes", [])
    )

    # 저장 버튼
    submitted = st.form_submit_button("프로필 저장")

# 저장 처리
if submitted:

    if not name.strip():
        st.warning("이름을 입력해 주세요.")

    else:
        new_profile = {
            "name": name.strip(),
            "budget": int(budget),
            "allergies": allergies,
            "likes": likes,
            "dislikes": dislikes
        }

        try:
            # 데이터베이스에 프로필 저장
            save_user_profile(user_id, new_profile)

            # 화면에서도 프로필 갱신
            st.session_state.profile = new_profile

            st.success("프로필이 저장되었습니다!")

        except Exception as e:
            st.error(f"프로필 저장 중 오류가 발생했습니다: {e}")

# 저장된 프로필 확인
if st.session_state.profile:

    st.subheader("저장된 프로필")

    profile = st.session_state.profile

    st.write("이름:", profile["name"])
    st.write("예산:", f'{profile["budget"]:,}원')

    st.write(
        "알레르기:",
        ", ".join(profile["allergies"]) if profile["allergies"] else "없음"
    )

    st.write(
        "선호 음식:",
        ", ".join(profile["likes"]) if profile["likes"] else "없음"
    )

    st.write(
        "기피 음식:",
        ", ".join(profile["dislikes"]) if profile["dislikes"] else "없음"
    )

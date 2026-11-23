
import streamlit as st

from services.group_service import create_group
from services.member_service import add_member_to_group


# 페이지 제목
st.title("👥 LunchMate")
st.subheader("그룹 만들기")

st.write("함께 점심을 먹을 그룹을 만들어 보세요.")


# 프로필 입력 여부 확인
profile = st.session_state.get("profile")

if profile is None:

    st.warning("먼저 나의 음식 프로필을 입력해 주세요.")

    st.stop()


# 생성된 그룹 정보 저장
if "created_group" not in st.session_state:
    st.session_state.created_group = None


# 그룹 생성 입력창
with st.form("create_group_form"):

    group_name = st.text_input(
        "그룹 이름",
        placeholder="예: 오늘 점심 모임"
    )

    submitted = st.form_submit_button("그룹 만들기")


# 그룹 생성 처리
if submitted:

    if not group_name.strip():

        st.warning("그룹 이름을 입력해 주세요.")

    else:

        try:
            # 그룹 생성
            group = create_group(group_name.strip())

            # 그룹 생성자를 첫 번째 구성원으로 등록
            member = add_member_to_group(
                group_id=group["group_id"],
                profile=profile
            )

            # 생성된 정보 저장
            st.session_state.created_group = group
            st.session_state.joined_member = member

            st.success("그룹이 생성되었습니다!")

        except Exception as e:

            st.error(f"그룹 생성 중 오류가 발생했습니다: {e}")


# 생성된 그룹 정보 표시
if st.session_state.created_group:

    group = st.session_state.created_group
    member = st.session_state.joined_member

    st.subheader("생성된 그룹 정보")

    st.write("그룹 이름:", group["group_name"])
    st.write("참여자:", member["name"])

    st.subheader("초대 코드")

    st.code(group["invite_code"])

    st.info("이 초대 코드를 함께 식사할 사람들에게 공유해 주세요.")


import streamlit as st

from services.group_service import create_group


# 페이지 제목
st.title("👥 LunchMate")
st.subheader("그룹 만들기")

st.write("함께 점심을 먹을 그룹을 만들어 보세요.")


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


# 그룹 생성 버튼을 눌렀을 때
if submitted:

    if not group_name.strip():
        st.warning("그룹 이름을 입력해 주세요.")

    else:
        try:
            group = create_group(group_name)

            st.session_state.created_group = group

        except Exception as e:
            st.error(f"그룹 생성 중 오류가 발생했습니다: {e}")


# 생성된 그룹 정보 표시
if st.session_state.created_group:

    group = st.session_state.created_group

    st.success("그룹이 생성되었습니다!")

    st.write("그룹 이름:", group["group_name"])

    st.subheader("초대 코드")

    st.code(group["invite_code"])

    st.info(
        "이 초대 코드를 함께 식사할 사람들에게 공유해 주세요."
    )


import streamlit as st

from services.member_service import join_group


# 페이지 제목
st.title("👥 LunchMate")
st.subheader("그룹 참여하기")

st.write("공유받은 초대 코드로 그룹에 참여해 보세요.")


# 참여 결과 저장
if "joined_member" not in st.session_state:
    st.session_state.joined_member = None


# 그룹 참여 입력창
with st.form("join_group_form"):

    invite_code = st.text_input(
        "초대 코드",
        placeholder="예: A1B2C3"
    )

    name = st.text_input(
        "이름",
        placeholder="이름을 입력하세요."
    )

    budget = st.number_input(
        "1인 점심 예산 (원)",
        min_value=1000,
        value=10000,
        step=1000
    )

    submitted = st.form_submit_button("그룹 참여하기")


# 참여 버튼을 눌렀을 때
if submitted:

    try:
        member = join_group(
            invite_code=invite_code,
            name=name,
            budget=int(budget)
        )

        st.session_state.joined_member = member

    except ValueError as e:
        st.error(str(e))

    except Exception as e:
        st.error(f"그룹 참여 중 오류가 발생했습니다: {e}")


# 참여 결과 표시
if st.session_state.joined_member:

    member = st.session_state.joined_member

    st.success("그룹 참여가 완료되었습니다!")

    st.write("그룹 이름:", member["group_name"])
    st.write("이름:", member["name"])
    st.write("예산:", f'{member["budget"]:,}원')

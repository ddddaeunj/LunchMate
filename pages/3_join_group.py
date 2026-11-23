
import streamlit as st

from services.member_service import join_group


# 페이지 제목
st.title("👥 LunchMate")
st.subheader("그룹 참여하기")

st.write("공유받은 초대 코드로 그룹에 참여해 보세요.")


# 저장된 프로필 확인
profile = st.session_state.get("profile")

if profile is None:

    st.warning("먼저 나의 음식 프로필을 입력해 주세요.")

    st.stop()


# 저장된 프로필 정보 표시
st.subheader("나의 프로필")

st.write("이름:", profile["name"])
st.write("예산:", f'{profile["budget"]:,}원')


# 초대 코드 입력
with st.form("join_group_form"):

    invite_code = st.text_input(
        "초대 코드",
        placeholder="예: A1B2C3"
    )

    submitted = st.form_submit_button("그룹 참여하기")


# 그룹 참여 처리
if submitted:

    if not invite_code.strip():

        st.warning("초대 코드를 입력해 주세요.")

    else:

        try:
            member = join_group(
                invite_code=invite_code,
                name=profile["name"],
                budget=profile["budget"],
                allergies=profile["allergies"],
                likes=profile["likes"],
                dislikes=profile["dislikes"]
            )

            st.session_state.joined_member = member

            st.success("그룹 참여가 완료되었습니다!")

        except ValueError as e:

            st.error(str(e))

        except Exception as e:

            st.error(f"그룹 참여 중 오류가 발생했습니다: {e}")


# 참여 결과 표시
if st.session_state.get("joined_member"):

    member = st.session_state.joined_member

    st.subheader("참여 그룹 정보")

    st.write("그룹 이름:", member["group_name"])
    st.write("이름:", member["name"])
    st.write("예산:", f'{member["budget"]:,}원')

    st.write(
        "알레르기:",
        ", ".join(member["allergies"]) if member["allergies"] else "없음"
    )

    st.write(
        "선호 음식:",
        ", ".join(member["likes"]) if member["likes"] else "없음"
    )

    st.write(
        "기피 음식:",
        ", ".join(member["dislikes"]) if member["dislikes"] else "없음"
    )

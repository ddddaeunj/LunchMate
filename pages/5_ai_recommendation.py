
import streamlit as st

from services.member_service import get_members_by_group
from services.recommendation_service import recommend_verified_menus
from services.ai_service import recommend_with_ai


st.title("🤖 AI 점심 추천")
st.subheader("우리 그룹을 위한 AI 메뉴 추천")

# 현재 참여한 구성원 확인
member = st.session_state.get("joined_member")

if member is None:
    st.warning("먼저 그룹에 참여해 주세요.")

else:
    # 그룹 구성원 정보 가져오기
    members = get_members_by_group(member["group_id"])

    st.write(f"현재 그룹 인원: {len(members)}명")

    # AI 추천 실행
    if st.button("AI 점심 메뉴 추천하기"):

        # 예산 및 알레르기 검증
        safe_menus = recommend_verified_menus(members)

        if not safe_menus:
            st.warning("추천 가능한 메뉴가 없습니다.")

        else:
            try:
                with st.spinner("AI가 메뉴를 분석하고 있습니다..."):

                    result = recommend_with_ai(
                        members,
                        safe_menus
                    )

                st.success("AI 추천이 완료되었습니다!")

                st.subheader("🍽️ AI 추천 결과")
                st.write(result)

            except Exception as e:
                st.error(f"추천 중 오류가 발생했습니다: {e}")

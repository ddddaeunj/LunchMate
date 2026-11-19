
import streamlit as st
from openai import OpenAI


# OpenAI API 연결
client = OpenAI(
    api_key=st.secrets["OPENAI_API_KEY"]
)


# AI 점심 메뉴 추천 함수
def recommend_with_ai(members, restaurants):

    # 그룹 구성원 정보 정리
    member_info = []

    for member in members:
        member_info.append({
            "이름": member["name"],
            "예산": member["budget"],
            "선호 음식": member["likes"],
            "기피 음식": member["dislikes"]
        })

    # AI에게 전달할 요청 내용
    prompt = f"""
    너는 직장인들의 점심 메뉴를 추천하는 AI야.

    다음 그룹 구성원들의 정보를 분석해 줘.

    [그룹 구성원]
    {member_info}

    [추천 가능한 식당 후보]
    {restaurants}

    구성원들의 음식 취향을 종합해서
    가장 적합한 식당을 추천해 줘.

    추천 이유도 구체적으로 설명해 줘.
    """

    # OpenAI API 요청
    response = client.responses.create(
        model="gpt-6-luna",
        input=prompt
    )

    return response.output_text

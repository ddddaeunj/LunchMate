
import uuid
import json
import streamlit as st
from streamlit_cookies_manager import EncryptedCookieManager
from database.db import get_connection


# 쿠키 관리자 생성
cookies = EncryptedCookieManager(
    prefix="lunchmate/",
    password=st.secrets["COOKIE_PASSWORD"]
)


# 브라우저 사용자 ID 확인 및 발급
def get_user_id():

    # 쿠키가 준비될 때까지 대기
    if not cookies.ready():
        st.info("브라우저 정보를 불러오는 중입니다.")
        st.stop()

    # 기존 사용자 ID 확인
    user_id = cookies.get("user_id")

    # 사용자 ID가 없으면 새로 생성
    if not user_id:
        user_id = str(uuid.uuid4())
        cookies["user_id"] = user_id
        cookies.save()

    return user_id




# 사용자 프로필 저장
def save_user_profile(user_id, profile):

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO users (
                user_id, name, budget, allergies, likes, dislikes
            )
            VALUES (?, ?, ?, ?, ?, ?)

            ON CONFLICT(user_id) DO UPDATE SET
                name = excluded.name,
                budget = excluded.budget,
                allergies = excluded.allergies,
                likes = excluded.likes,
                dislikes = excluded.dislikes
        """, (
            user_id,
            profile["name"],
            profile["budget"],
            json.dumps(profile["allergies"], ensure_ascii=False),
            json.dumps(profile["likes"], ensure_ascii=False),
            json.dumps(profile["dislikes"], ensure_ascii=False)
        ))

        conn.commit()

    finally:
        conn.close()


# 사용자 프로필 불러오기
def get_user_profile(user_id):

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT name, budget, allergies, likes, dislikes
            FROM users
            WHERE user_id = ?
        """, (user_id,))

        user = cursor.fetchone()

        if user is None:
            return None

        return {
            "name": user["name"],
            "budget": user["budget"],
            "allergies": json.loads(user["allergies"]),
            "likes": json.loads(user["likes"]),
            "dislikes": json.loads(user["dislikes"])
        }

    finally:
        conn.close()

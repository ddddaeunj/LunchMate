import sqlite3
import secrets
import string

from database.db import get_connection


# 초대 코드 생성 함수
def generate_invite_code(length=6):

    characters = string.ascii_uppercase + string.digits

    return ''.join(
        secrets.choice(characters)
        for _ in range(length)
    )


# 그룹 생성 함수
def create_group(group_name):

    conn = get_connection()
    cursor = conn.cursor()

    # 중복되지 않는 초대 코드 생성
    while True:

        invite_code = generate_invite_code()

        cursor.execute(
            "SELECT group_id FROM groups WHERE invite_code = ?",
            (invite_code,)
        )

        if cursor.fetchone() is None:
            break

    # 그룹 정보 저장
    cursor.execute(
        """
        INSERT INTO groups (group_name, invite_code)
        VALUES (?, ?)
        """,
        (group_name, invite_code)
    )

    group_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return {
        "group_id": group_id,
        "group_name": group_name,
        "invite_code": invite_code
    }


# 초대 코드로 그룹 조회
def get_group_by_invite_code(invite_code):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT * FROM groups
        WHERE invite_code = ?
        """,
        (invite_code.upper(),)
    )

    group = cursor.fetchone()

    conn.close()

    return dict(group) if group else None


# 그룹 ID로 그룹 조회
def get_group_by_id(group_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT * FROM groups
        WHERE group_id = ?
        """,
        (group_id,)
    )

    group = cursor.fetchone()

    conn.close()

    return dict(group) if group else None

import json

from database.db import get_connection


# 구성원 정보 저장
def save_member(cursor, group_id, profile):

    cursor.execute(
        """
        INSERT INTO members (
            group_id,
            name,
            budget,
            allergies,
            likes,
            dislikes
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            group_id,
            profile["name"],
            profile["budget"],
            json.dumps(profile["allergies"], ensure_ascii=False),
            json.dumps(profile["likes"], ensure_ascii=False),
            json.dumps(profile["dislikes"], ensure_ascii=False)
        )
    )

    return cursor.lastrowid


# 구성원 그룹 참여 및 정보 등록
def join_group(
    invite_code,
    name,
    budget,
    allergies=None,
    likes=None,
    dislikes=None
):

    invite_code = invite_code.strip().upper()
    name = name.strip()

    if not name:
        raise ValueError("이름을 입력해 주세요.")

    if budget <= 0:
        raise ValueError("예산은 0원보다 커야 합니다.")

    profile = {
        "name": name,
        "budget": budget,
        "allergies": allergies or [],
        "likes": likes or [],
        "dislikes": dislikes or []
    }

    conn = get_connection()
    cursor = conn.cursor()

    try:
        # 초대 코드로 그룹 확인
        cursor.execute(
            """
            SELECT group_id, group_name
            FROM groups
            WHERE invite_code = ?
            """,
            (invite_code,)
        )

        group = cursor.fetchone()

        if group is None:
            raise ValueError("존재하지 않는 초대 코드입니다.")

        # 구성원 정보 저장
        member_id = save_member(
            cursor,
            group["group_id"],
            profile
        )

        conn.commit()

        member = get_member_by_id(member_id)
        member["group_name"] = group["group_name"]

        return member

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()


# 그룹 생성자가 자신의 프로필을 그룹에 저장
def add_member_to_group(group_id, profile):

    if not profile["name"].strip():
        raise ValueError("이름을 입력해 주세요.")

    if profile["budget"] <= 0:
        raise ValueError("예산은 0원보다 커야 합니다.")

    conn = get_connection()
    cursor = conn.cursor()

    try:
        # 그룹 정보 확인
        cursor.execute(
            """
            SELECT group_id, group_name
            FROM groups
            WHERE group_id = ?
            """,
            (group_id,)
        )

        group = cursor.fetchone()

        if group is None:
            raise ValueError("그룹을 찾을 수 없습니다.")

        # 구성원 정보 저장
        member_id = save_member(
            cursor,
            group_id,
            profile
        )

        conn.commit()

        member = get_member_by_id(member_id)
        member["group_name"] = group["group_name"]

        return member

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()


# 그룹 구성원 목록 조회
def get_members_by_group(group_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM members
        WHERE group_id = ?
        ORDER BY member_id
        """,
        (group_id,)
    )

    rows = cursor.fetchall()
    conn.close()

    members = []

    for row in rows:
        member = dict(row)

        member["allergies"] = json.loads(member["allergies"])
        member["likes"] = json.loads(member["likes"])
        member["dislikes"] = json.loads(member["dislikes"])

        members.append(member)

    return members


# 구성원 ID로 개별 정보 조회
def get_member_by_id(member_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM members
        WHERE member_id = ?
        """,
        (member_id,)
    )

    row = cursor.fetchone()
    conn.close()

    if row is None:
        return None

    member = dict(row)

    member["allergies"] = json.loads(member["allergies"])
    member["likes"] = json.loads(member["likes"])
    member["dislikes"] = json.loads(member["dislikes"])

    return member


# 구성원 개인 프로필 수정
def update_member_profile(
    member_id,
    allergies=None,
    likes=None,
    dislikes=None
):

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            UPDATE members
            SET allergies = ?,
                likes = ?,
                dislikes = ?
            WHERE member_id = ?
            """,
            (
                json.dumps(allergies or [], ensure_ascii=False),
                json.dumps(likes or [], ensure_ascii=False),
                json.dumps(dislikes or [], ensure_ascii=False),
                member_id
            )
        )

        if cursor.rowcount == 0:
            raise ValueError("구성원을 찾을 수 없습니다.")

        conn.commit()

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()

    return get_member_by_id(member_id)

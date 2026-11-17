import json

from database.db import get_connection


# 구성원 그룹 참여 및 정보 등록
def join_group(
    invite_code,
    name,
    budget,
    allergies=None,
    likes=None,
    dislikes=None
):

    # 입력값 정리
    invite_code = invite_code.strip().upper()
    name = name.strip()

    if not name:
        raise ValueError("이름을 입력해 주세요.")

    if budget <= 0:
        raise ValueError("예산은 0원보다 커야 합니다.")

    # 데이터베이스 연결
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
                group["group_id"],
                name,
                budget,
                json.dumps(allergies or [], ensure_ascii=False),
                json.dumps(likes or [], ensure_ascii=False),
                json.dumps(dislikes or [], ensure_ascii=False)
            )
        )

        member_id = cursor.lastrowid

        conn.commit()

        return {
            "member_id": member_id,
            "group_id": group["group_id"],
            "group_name": group["group_name"],
            "name": name,
            "budget": budget
        }

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

        # JSON 문자열을 리스트로 변환
        member["allergies"] = json.loads(
            member["allergies"]
        )

        member["likes"] = json.loads(
            member["likes"]
        )

        member["dislikes"] = json.loads(
            member["dislikes"]
        )

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

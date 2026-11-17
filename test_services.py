
from services.group_service import create_group
from services.member_service import (
    join_group,
    get_members_by_group
)


# 1. 그룹 생성
group = create_group("런치메이트 테스트 그룹")

print("===== 그룹 생성 결과 =====")
print("그룹 이름:", group["group_name"])
print("초대 코드:", group["invite_code"])


# 2. 첫 번째 구성원 참여
member1 = join_group(
    invite_code=group["invite_code"],
    name="철수",
    budget=10000,
    allergies=["땅콩"],
    likes=["한식", "국물"],
    dislikes=["매운 음식"]
)


# 3. 두 번째 구성원 참여
member2 = join_group(
    invite_code=group["invite_code"],
    name="영희",
    budget=12000,
    allergies=[],
    likes=["일식", "면류"],
    dislikes=["해산물"]
)


# 4. 그룹 구성원 조회
members = get_members_by_group(group["group_id"])

print("\n===== 구성원 참여 결과 =====")

for member in members:
    print("이름:", member["name"])
    print("예산:", member["budget"])
    print("알레르기:", member["allergies"])
    print("선호:", member["likes"])
    print("기피:", member["dislikes"])
    print("--------------------")


import streamlit as st

# LunchMate
st.set_page_config(
    page_title="LunchMate",
    page_icon="🍽️"
)

st.title("🍽️ LunchMate")
st.subheader("매일 먹는 점심, 쉽고 빠르게 메뉴를 정해보세요!")

st.write("그룹 구성원의 정보를 입력해 주세요.")

# 초기 메뉴 데이터
menus = [
    {
        "name": "김치찌개",
        "price": 9000,
        "allergens": ["대두"],
        "tags": ["한식", "국물", "매콤"]
    },
    {
        "name": "돈까스",
        "price": 11000,
        "allergens": ["밀", "계란"],
        "tags": ["일식", "육류", "튀김"]
    },
    {
        "name": "비빔밥",
        "price": 10000,
        "allergens": ["대두", "계란"],
        "tags": ["한식", "채소"]
    },
    {
        "name": "쌀국수",
        "price": 10000,
        "allergens": ["대두"],
        "tags": ["면류", "국물"]
    },
    {
        "name": "초밥",
        "price": 13000,
        "allergens": ["생선"],
        "tags": ["일식", "해산물"]
    }
]


# 알레르기 표현 통합
allergy_groups = {
    "해산물": ["해산물", "생선", "갑각류", "연체류", "조개류"],
    "생선": ["생선"],
    "갑각류": ["갑각류"],
    "땅콩": ["땅콩"],
    "밀": ["밀"],
    "계란": ["계란", "달걀"],
    "달걀": ["계란", "달걀"],
    "대두": ["대두", "콩"],
}

# 입력한 알레르기 표현을 통일하는 함수
def normalize_allergies(allergies):
    normalized = set()

    for allergy in allergies:
        allergy = allergy.strip()

        if allergy in allergy_groups:
            normalized.update(allergy_groups[allergy])
        else:
            normalized.add(allergy)

    return normalized


# 그룹 인원 입력
count = st.number_input(
    "그룹 인원",
    min_value=1,
    max_value=10,
    value=3
)

members = []

# 구성원별 정보 입력
for i in range(int(count)):
    st.write(f"### 구성원 {i + 1}")

    budget = st.number_input(
        "1인당 최대 예산 (원)",
        min_value=1000,
        value=12000,
        step=1000,
        key=f"budget_{i}"
    )

    allergies = st.text_input(
        "알레르기 (쉼표로 구분)",
        key=f"allergy_{i}"
    )

    likes = st.text_input(
        "선호 키워드 (쉼표로 구분)",
        key=f"likes_{i}"
    )

    dislikes = st.text_input(
        "기피 키워드 (쉼표로 구분)",
        key=f"dislikes_{i}"
    )

    members.append({
        "budget": budget,
        "allergies": [x.strip() for x in allergies.split(",") if x.strip()],
        "likes": [x.strip() for x in likes.split(",") if x.strip()],
        "dislikes": [x.strip() for x in dislikes.split(",") if x.strip()]
    })

# 추천 버튼
if st.button("점심 메뉴 추천받기"):

    # 그룹 예산 및 알레르기 취합
    
    # 개인별 예산 계산
    personal_budgets = [
        member["budget"] for member in members
    ]

    # 그룹에서 가장 적은 개인 예산
    max_budget = min(personal_budgets)

    # 그룹 전체 예산
    total_budget = sum(personal_budgets)

    # 그룹 인원
    group_count = len(members)


    all_allergies = set()

    for member in members:
        normalized = normalize_allergies(member["allergies"])
        all_allergies.update(normalized)

    results = []

    
    # 메뉴별 조건 확인
    for menu in menus:

        # 알레르기 필터링
        menu_allergies = normalize_allergies(
            menu["allergens"]
        )

        if all_allergies.intersection(menu_allergies):
            continue

        # 개인별 예산 초과 메뉴 제외
        if menu["price"] > max_budget:
            continue

        # 그룹 전체 예산 초과 메뉴 제외
        total_price = menu["price"] * group_count

        if total_price > total_budget:
            continue

        total_score = 0

    # 구성원별 선호도 점수 계산
    for member in members:

        for tag in menu["tags"]:

            if tag in member["likes"]:
                total_score += 2

            if tag in member["dislikes"]:
                total_score -= 2

    average_score = total_score / len(members)

    results.append({
        "name": menu["name"],
        "price": menu["price"],
        "total_price": total_price,
        "remaining_budget": total_budget - total_price,
        "score": average_score
    })


        
    results.append({
        "name": menu["name"],
        "price": menu["price"],
        "total_price": menu["price"] * group_count,
        "remaining_budget": total_budget - (menu["price"] * group_count),
        "score": average_score
    })


    # 점수 높은 순으로 정렬
    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    
    st.write("## 🏆 추천 결과")

    # 그룹 예산 정보
    st.write(f"👥 그룹 인원: {group_count}명")
    st.write(f"💰 그룹 전체 예산: {total_budget:,}원")
    st.write(f"💵 1인당 최대 예산: {max_budget:,}원")

    if results:
        for i, menu in enumerate(results[:3]):

            st.write(f"### {i + 1}위. {menu['name']}")

            st.write(
                f"1인당 가격: {menu['price']:,}원"
            )

            st.write(
                f"그룹 전체 예상 비용: "
                f"{menu['total_price']:,}원"
            )

            st.write(
                f"남은 그룹 예산: "
                f"{menu['remaining_budget']:,}원"
            )

            st.write(
                f"추천 점수: {menu['score']:.1f}"
            )

            st.divider()

    else:
        st.warning("조건에 맞는 메뉴가 없습니다.")


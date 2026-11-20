import streamlit as st

from core.state import initialize_state

initialize_state()

st.sidebar.metric("내 별", f"{st.session_state.stars} ⭐")

st.title("🗺️ 수학 지도")
st.write("가고 싶은 지역을 살펴봐요.")

regions = [
    {"id": "triangle_forest", "name": "삼각형 숲", "icon": "🌲"},
    {"id": "square_desert", "name": "사각형 사막", "icon": "🌵"},
    {"id": "angle_coast", "name": "각도 해안", "icon": "🏝️"},
]
columns = st.columns(3)

for column, region in zip(columns, regions):
    with column:
        with st.container(border=True):
            is_unlocked = region["id"] in st.session_state.unlocked_regions
            if is_unlocked:
                st.subheader(f"{region['icon']} {region['name']}")
                if st.button(
                    "체험하러 가기",
                    key=f"visit_{region['id']}",
                    use_container_width=True,
                ):
                    st.switch_page("pages/2_체험실.py")
            else:
                st.subheader(f"🔒 {region['icon']} {region['name']}")
                st.write("삼각형 숲을 먼저 해결해요")

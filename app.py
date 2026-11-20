import streamlit as st

from core.state import initialize_state

st.set_page_config(page_title="수학 탐험대", page_icon="🧭")
initialize_state()

st.sidebar.metric("내 별", f"{st.session_state.stars} ⭐")

st.title("🧭 수학 탐험대")
st.write("도형을 살펴보고 미션을 풀며 수학 지도를 탐험해요.")

if st.button("모험 시작", type="primary"):
    st.switch_page("pages/1_지도.py")

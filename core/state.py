import streamlit as st


def initialize_state() -> None:
    """앱 진행 상태를 처음 한 번 설정해요."""
    if "stars" not in st.session_state:
        st.session_state.stars = 0
    if "unlocked_regions" not in st.session_state:
        st.session_state.unlocked_regions = ["triangle_forest"]
    if "completed_missions" not in st.session_state:
        st.session_state.completed_missions = []

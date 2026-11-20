from math import atan2, cos, degrees, dist, radians, sin

import plotly.graph_objects as go
import streamlit as st

from core.geometry import triangle_vertices
from core.state import initialize_state

ANGLE_COLORS = ("#E4572E", "#2E86AB", "#6A994E")
ANGLE_FILLS = (
    "rgba(228, 87, 46, 0.18)",
    "rgba(46, 134, 171, 0.18)",
    "rgba(106, 153, 78, 0.18)",
)


def add_angle_sector(
    figure: go.Figure,
    vertex: tuple[float, float],
    start_degrees: float,
    sweep_degrees: float,
    radius: float,
    label: str,
    color: str,
    fill_color: str,
) -> None:
    points = [
        radians(start_degrees + sweep_degrees * step / 24)
        for step in range(25)
    ]
    x_values = [
        vertex[0],
        *(vertex[0] + radius * cos(angle) for angle in points),
        vertex[0],
    ]
    y_values = [
        vertex[1],
        *(vertex[1] + radius * sin(angle) for angle in points),
        vertex[1],
    ]
    figure.add_trace(
        go.Scatter(
            x=x_values,
            y=y_values,
            mode="lines",
            line={"color": color, "width": 1},
            fill="toself",
            fillcolor=fill_color,
            hoverinfo="skip",
            showlegend=False,
        )
    )

    middle = radians(start_degrees + sweep_degrees / 2)
    label_radius = radius * 2.0
    figure.add_annotation(
        x=vertex[0] + label_radius * cos(middle),
        y=vertex[1] + label_radius * sin(middle),
        text=label,
        showarrow=False,
        font={"color": color, "size": 17},
    )


def create_triangle_figure(
    angle_a: int,
    angle_b: int,
    angle_c: int,
) -> go.Figure:
    point_a, point_b, point_c = triangle_vertices(angle_a, angle_b)
    points = (point_a, point_b, point_c)
    figure = go.Figure()

    starts = (
        atan2(point_b[1] - point_a[1], point_b[0] - point_a[0]),
        atan2(point_c[1] - point_b[1], point_c[0] - point_b[0]),
        atan2(point_a[1] - point_c[1], point_a[0] - point_c[0]),
    )
    neighboring_points = ((point_b, point_c), (point_a, point_c), (point_a, point_b))
    angles = (angle_a, angle_b, angle_c)

    for index, (vertex, start, neighbors, angle) in enumerate(
        zip(points, starts, neighboring_points, angles)
    ):
        radius = min(dist(vertex, neighbors[0]), dist(vertex, neighbors[1])) * 0.22
        add_angle_sector(
            figure,
            vertex,
            degrees(start),
            angle,
            radius,
            f"{angle}°",
            ANGLE_COLORS[index],
            ANGLE_FILLS[index],
        )

    figure.add_trace(
        go.Scatter(
            x=[point_a[0], point_b[0], point_c[0], point_a[0]],
            y=[point_a[1], point_b[1], point_c[1], point_a[1]],
            mode="lines",
            line={"color": "#334155", "width": 3},
            hoverinfo="skip",
            showlegend=False,
        )
    )
    x_values = [point[0] for point in points]
    y_values = [point[1] for point in points]
    x_padding = (max(x_values) - min(x_values)) * 0.16
    y_padding = (max(y_values) - min(y_values)) * 0.16
    figure.update_layout(
        height=430,
        margin={"l": 10, "r": 10, "t": 15, "b": 10},
        showlegend=False,
    )
    figure.update_xaxes(
        range=[min(x_values) - x_padding, max(x_values) + x_padding],
        visible=False,
        constrain="domain",
    )
    figure.update_yaxes(
        range=[min(y_values) - y_padding, max(y_values) + y_padding],
        visible=False,
        scaleanchor="x",
        scaleratio=1,
    )
    return figure


def create_straight_angle_figure(
    angle_a: int,
    angle_b: int,
    angle_c: int,
) -> go.Figure:
    figure = go.Figure()
    angles = (angle_a, angle_b, angle_c)
    labels = ("A", "B", "C")
    start_degrees = 180
    radius = 0.48

    for index, (label, angle) in enumerate(zip(labels, angles)):
        add_angle_sector(
            figure,
            (0.0, 0.0),
            start_degrees,
            -angle,
            radius,
            f"{label} {angle}°",
            ANGLE_COLORS[index],
            ANGLE_FILLS[index],
        )
        start_degrees -= angle

    figure.add_trace(
        go.Scatter(
            x=[-1.25, 1.25],
            y=[0, 0],
            mode="lines",
            line={"color": "#334155", "width": 3},
            hoverinfo="skip",
            showlegend=False,
        )
    )
    boundary_angles = (180, 180 - angle_a, angle_c, 0)
    for boundary in boundary_angles[1:-1]:
        angle_radians = radians(boundary)
        figure.add_trace(
            go.Scatter(
                x=[0, 1.25 * cos(angle_radians)],
                y=[0, 1.25 * sin(angle_radians)],
                mode="lines",
                line={"color": "#64748B", "width": 2},
                hoverinfo="skip",
                showlegend=False,
            )
        )

    figure.update_layout(
        height=350,
        margin={"l": 10, "r": 10, "t": 25, "b": 10},
        showlegend=False,
        title={"text": "세 각을 모으면 180°", "x": 0.5},
    )
    figure.update_xaxes(range=[-1.5, 1.5], visible=False, constrain="domain")
    figure.update_yaxes(
        range=[-0.25, 1.5],
        visible=False,
        scaleanchor="x",
        scaleratio=1,
    )
    return figure


initialize_state()
st.sidebar.metric("내 별", f"{st.session_state.stars} ⭐")

st.title("🔺 삼각형의 세 각의 합")
st.write("슬라이더를 움직여 세 각의 크기를 살펴봐요.")

if "experience_angle_a" not in st.session_state:
    st.session_state.experience_angle_a = 60
angle_a = st.slider(
    "각 A",
    min_value=10,
    max_value=150,
    key="experience_angle_a",
)

angle_b_max = min(150, 179 - angle_a)
if "experience_angle_b" not in st.session_state:
    st.session_state.experience_angle_b = min(60, angle_b_max)
else:
    st.session_state.experience_angle_b = min(
        max(10, st.session_state.experience_angle_b),
        angle_b_max,
    )
angle_b = st.slider(
    "각 B",
    min_value=10,
    max_value=angle_b_max,
    key="experience_angle_b",
)
st.caption(f"각 B는 10°~{angle_b_max}°로 조절할 수 있어요. 각 C도 1° 이상 남겨요.")

angle_c = 180 - angle_a - angle_b
st.plotly_chart(
    create_triangle_figure(angle_a, angle_b, angle_c),
    use_container_width=True,
    config={"displayModeBar": False},
)
st.markdown(
    f"## A ({angle_a}°) + B ({angle_b}°) + C ({angle_c}°) = 180°"
)

if "show_straight_angle" not in st.session_state:
    st.session_state.show_straight_angle = False
if st.button("세 각을 한 줄로 모아 보기"):
    st.session_state.show_straight_angle = True

if st.session_state.show_straight_angle:
    st.plotly_chart(
        create_straight_angle_figure(angle_a, angle_b, angle_c),
        use_container_width=True,
        config={"displayModeBar": False},
    )

st.subheader("내가 발견한 것")
st.write("삼각형의 모양이 달라져도 세 각의 합은 항상 ___°예요.")
with st.form("triangle_angle_sum_answer"):
    answer = st.text_input(
        "빈칸에 알맞은 수를 써 봐요",
        label_visibility="collapsed",
    )
    submitted = st.form_submit_button("정답 확인")

if submitted:
    if answer.strip() == "180":
        if not st.session_state.triangle_angle_sum_rewarded:
            st.session_state.stars += 1
            st.session_state.triangle_angle_sum_rewarded = True
            st.success("정답이에요! 별 1개를 받았어요 ⭐")
        else:
            st.success("정답이에요! 별은 이미 받았어요 ⭐")
    else:
        st.info("괜찮아요. 다시 도전해 볼까?")

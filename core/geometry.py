from math import cos, radians, sin

Point = tuple[float, float]


def triangle_vertices(angle_a: float, angle_b: float) -> tuple[Point, Point, Point]:
    """각 A와 B에 맞는 삼각형의 꼭짓점 좌표를 구해요."""
    if not 0 < angle_a < 180 or not 0 < angle_b < 180:
        raise ValueError("각은 0°보다 크고 180°보다 작아야 해요.")
    if angle_a + angle_b >= 180:
        raise ValueError("각 A와 B의 합은 180°보다 작아야 해요.")

    angle_c = 180 - angle_a - angle_b
    side_ac = sin(radians(angle_b)) / sin(radians(angle_c))
    point_c = (
        side_ac * cos(radians(angle_a)),
        side_ac * sin(radians(angle_a)),
    )
    return (0.0, 0.0), (1.0, 0.0), point_c

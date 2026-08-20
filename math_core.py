import math
import numpy as np

# Corners of the simplex in Cartesian coordinates.
BL = np.array([0.0, 0.0])
TOP = np.array([0.5, math.sqrt(3) / 2])
BR = np.array([1.0, 0.0])

# Quadratic form for the conic: a^2 + b^2 + c^2 - 2ab - 2bc
Q = np.array([[1.0, -1.0, 0.0],
              [-1.0, 1.0, -1.0],
              [0.0, -1.0, 1.0]])


def generate_exceptional_sequences(excep_number: int, excep_depth: int):
    """Generate exceptional sequences of the eight different types for the given parameters."""
    excep = []

    for k in range(excep_number):
        # Type 1: Near-(0,0,1) exceptionals on line (0,0,1)->(k+1,k,0).
        nodes1 = []
        B1 = [k+1, k, 2*k]
        B2 = [2*k*(k+1), 2*k*k, 2*k*(2*k)-1]
        nodes1.append(B1)
        nodes1.append(B2)
        for _ in range(2, excep_depth):
            B_prev = nodes1[-1]
            B_prev2 = nodes1[-2]
            B_next = [2*k*B_prev[j] - B_prev2[j] for j in range(3)]
            nodes1.append(B_next)
        excep.append(nodes1)

        # Type 2: Near-(0,0,1) exceptionals on line (0,0,1)->(k,k+1,0).
        nodes2 = []
        B1 = [k, k+1, 2*(k+1)]
        B2 = [2*(k+1)*B1[i] - v for i, v in enumerate([0, 0, 1])]
        nodes2.append(B1)
        nodes2.append(B2)
        for _ in range(2, excep_depth):
            B_prev = nodes2[-1]
            B_prev2 = nodes2[-2]
            B_next = [2*(k+1)*B_prev[j] - B_prev2[j] for j in range(3)]
            nodes2.append(B_next)
        excep.append(nodes2)

        # Type 3: Near-(1,0,0) exceptionals on line (1,0,0)->(0,k,k+1).
        nodes3 = []
        B1 = [2*k, k, k+1]
        B2 = [2*k*B1[i] - v for i, v in enumerate([1, 0, 0])]
        nodes3.append(B1)
        nodes3.append(B2)
        for _ in range(2, excep_depth):
            B_prev = nodes3[-1]
            B_prev2 = nodes3[-2]
            B_next = [2*k*B_prev[j] - B_prev2[j] for j in range(3)]
            nodes3.append(B_next)
        excep.append(nodes3)

        # Type 4: Near-(1,0,0) exceptionals on line (1,0,0)->(0,k+1,k).
        nodes4 = []
        B1 = [2*(k+1), k+1, k]
        B2 = [2*(k+1)*B1[i] - v for i, v in enumerate([1, 0, 0])]
        nodes4.append(B1)
        nodes4.append(B2)
        for _ in range(2, excep_depth):
            B_prev = nodes4[-1]
            B_prev2 = nodes4[-2]
            B_next = [2*(k+1)*B_prev[j] - B_prev2[j] for j in range(3)]
            nodes4.append(B_next)
        excep.append(nodes4)

        # Type 5: Near-(k+1,k,0) exceptionals on line (0,0,1)->(k+1,k,0).
        nodes5 = []
        B1 = [k+1, k, 0]
        B2 = [2*k*(k+1), 2*k*k, 1]
        nodes5.append(B1)
        nodes5.append(B2)
        for _ in range(2, excep_depth):
            B_prev = nodes5[-1]
            B_prev2 = nodes5[-2]
            B_next = [2*k*B_prev[j] - B_prev2[j] for j in range(3)]
            nodes5.append(B_next)
        excep.append(nodes5)

        # Type 6: Near-(k,k+1,0) exceptionals on line (0,0,1)->(k,k+1,0).
        nodes6 = []
        B1 = [k, k+1, 0]
        B2 = [2*(k+1)*k, 2*(k+1)*(k+1), 1]
        nodes6.append(B1)
        nodes6.append(B2)
        for _ in range(2, excep_depth):
            B_prev = nodes6[-1]
            B_prev2 = nodes6[-2]
            B_next = [2*(k+1)*B_prev[j] - B_prev2[j] for j in range(3)]
            nodes6.append(B_next)
        excep.append(nodes6)

        # Type 7: Near-(0,k+1,k) exceptionals on line (1,0,0)->(0,k+1,k).
        nodes7 = []
        B1 = [0, k+1, k]
        B2 = [1, 2*(k+1)*(k+1), 2*(k+1)*k]
        nodes7.append(B1)
        nodes7.append(B2)
        for _ in range(2, excep_depth):
            B_prev = nodes7[-1]
            B_prev2 = nodes7[-2]
            B_next = [2*(k+1)*B_prev[j] - B_prev2[j] for j in range(3)]
            nodes7.append(B_next)
        excep.append(nodes7)

        # Type 8: Near-(0,k,k+1) exceptionals on line (1,0,0)->(0,k,k+1).
        nodes8 = []
        B1 = [0, k, k+1]
        B2 = [1, 2*k*k, 2*k*(k+1)]
        nodes8.append(B1)
        nodes8.append(B2)
        for _ in range(2, excep_depth):
            B_prev = nodes8[-1]
            B_prev2 = nodes8[-2]
            B_next = [2*k*B_prev[j] - B_prev2[j] for j in range(3)]
            nodes8.append(B_next)
        excep.append(nodes8)

    return excep


def bary_to_cart(triple: tuple[float, float, float]) -> np.ndarray:
    """Convert barycentric coordinates to Cartesian coordinates in the simplex."""
    A, B, C = triple
    s = A + B + C
    if s == 0:
        return np.array([0, 0])
    return (A * BR + B * TOP + C * BL) / s


def renormalize(triple: tuple[float, float, float]) -> list[float]:
    """Renormalize a triple to ensure it sums to 1."""
    s = sum(triple)
    if s == 0:
        return triple[:]
    return [x / s for x in triple]


def reflect_1(points: list[tuple[float, float, float]]) -> list[list[float]]:
    return [[2 * B - A, B, C] for (A, B, C) in points]


def reflect_2(points: list[tuple[float, float, float]]) -> list[list[float]]:
    return [[A, 2 * A + 2 * C - B, C] for (A, B, C) in points]


def reflect_3(points: list[tuple[float, float, float]]) -> list[list[float]]:
    return [[A, B, 2 * B - C] for (A, B, C) in points]


digit_actions = {"1": reflect_1, "2": reflect_2, "3": reflect_3}


def base_lines(line_limit: int) -> list[tuple[np.ndarray, np.ndarray, int]]:
    """Generate a list of lines in barycentric coordinates inside the ellipse. They are used for the reflected lines in the simplex."""
    lines = []
    for k in range(line_limit):
        disc1 = k**2 - 1
        if disc1 >= 0:
            sqrt_disc1 = np.sqrt(disc1)
            x1 = k - sqrt_disc1
            x2 = k + sqrt_disc1
            lines.append((np.array([(k+1)*x1, k*x1, 1.0]), np.array([(k+1)*x2, k*x2, 1.0]), k))
            lines.append((np.array([1.0, k*x1, (k+1)*x1]), np.array([1.0, k*x2, (k+1)*x2]), k))

        disc2 = (k+1)**2 - 1
        if disc2 >= 0:
            sqrt_disc2 = np.sqrt(disc2)
            x1 = k+1 - sqrt_disc2
            x2 = k+1 + sqrt_disc2
            lines.append((np.array([k*x1, (k+1)*x1, 1.0]), np.array([k*x2, (k+1)*x2, 1.0]), k))
            lines.append((np.array([1.0, (k+1)*x1, k*x1]), np.array([1.0, (k+1)*x2, k*x2]), k))
    return lines


def apply_sequence(point: np.ndarray, sequence: str) -> np.ndarray:
    """Apply a sequence of reflection functions to a single point in barycentric coordinates."""
    current = [point]
    for digit in sequence:
        current = digit_actions[digit](current)
    return current[0]


def matching_reflection_steps(sequence: str) -> list[int]:
    """Identify the steps in the sequence after which the original orientation reoccurs."""
    steps = []
    if sequence.startswith("13") or sequence.startswith("31"):
        steps.append(2)

    for i in range(2, len(sequence)):
        window = sequence[i-2:i+1]
        if window in {"123", "321", "121", "323"}:
            steps.append(i+1)

    return steps


def step_size(k: int) -> int:
    """Determine line-density step size for plotting."""
    if k < 20:
        return 1
    if k < 40:
        return 2
    if k < 60:
        return 5
    if k < 80:
        return 10
    return 20


def compute_conic_cart_points_analytic() -> np.ndarray:
    """Compute conic points for the conic given by the Euler form within the simplex."""
    n_theta = 1200
    tol = 1e-12

    # Build the conic in 2D local coordinates.
    B = np.array([[1.0, 0.0],
                  [0.0, 1.0],
                  [-1.0, -1.0]])
    s = np.array([0.0, 0.0, 1.0])
    T = np.column_stack([BR - BL, TOP - BL])
    Ti = np.linalg.inv(T)

    A = Ti.T @ (B.T @ Q @ B) @ Ti
    b = (2.0 * Ti.T @ (B.T @ Q @ s).reshape(2, 1)).ravel()
    c = float(s.T @ Q @ s)

    center = -0.5 * np.linalg.solve(A, b)
    f_center = float(center @ (A @ center) + (b @ center) + c)

    eigvals, eigvecs = np.linalg.eigh(A)
    if np.any(eigvals <= 0) or f_center >= 0:
        return np.empty((0, 2))

    axes = np.sqrt((-f_center) / eigvals)

    thetas = np.linspace(0, 2 * np.pi, n_theta, endpoint=True)
    circle = np.column_stack([np.cos(thetas), np.sin(thetas)])
    pts = BL + center + (circle * axes) @ eigvecs.T

    bary = (Ti @ (pts - BL).T).T
    in_simplex = (bary[:, 0] >= -tol) & (bary[:, 1] >= -tol) & ((1.0 - bary[:, 0] - bary[:, 1]) >= -tol)
    pts = pts[in_simplex]
    if pts.shape[0] > 0 and not np.allclose(pts[0], pts[-1]):
        pts = np.vstack([pts, pts[0]])
    return pts

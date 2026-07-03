import streamlit as st
import math
import numpy as np
import plotly.graph_objects as go

#=====================================================================
# Helper Functions
#=====================================================================
 
def gen_excep(excep_number: int, excep_depth: int):
    """Generate exceptional sequences of the eight different types for the given parameters.

    Args:
        excep_number: The number of exceptional sequences to generate for each of the eight types.
        excep_depth: The depth of mutation for each exceptional sequence.
    
    Returns:
        list: A list of exceptional sequences for each type.
    """
    excep = []

    for k in range(excep_number):
        # Type 1
        nodes1 = []
        B1 = [k+1, k, 2*k]
        B2 = [2*k*(k+1), 2*k*k, 2*k*(2*k)-1]
        nodes1.append(B1)
        nodes1.append(B2)
        for i in range(2, excep_depth):
            B_prev = nodes1[-1]
            B_prev2 = nodes1[-2]
            B_next = [2*k*B_prev[j] - B_prev2[j] for j in range(3)]
            nodes1.append(B_next)

        excep.append(nodes1)

        # Type 2
        nodes2 = []
        B1 = [k, k+1, 2*(k+1)]
        B2 = [2*(k+1)*B1[i] - v for i, v in enumerate([0,0,1])]
        nodes2.append(B1)
        nodes2.append(B2)
        for i in range(2, excep_depth):
            B_prev = nodes2[-1]
            B_prev2 = nodes2[-2]
            B_next = [2*(k+1)*B_prev[j] - B_prev2[j] for j in range(3)]
            nodes2.append(B_next)
        excep.append(nodes2)

        # Type 3
        nodes3 = []
        B1 = [2*k, k, k+1]
        B2 = [2*k*B1[i] - v for i, v in enumerate([1,0,0])]
        nodes3.append(B1)
        nodes3.append(B2)
        for i in range(2, excep_depth):
            B_prev = nodes3[-1]
            B_prev2 = nodes3[-2]
            B_next = [2*k*B_prev[j] - B_prev2[j] for j in range(3)]
            nodes3.append(B_next)
        excep.append(nodes3)

        # Type 4
        nodes4 = []
        B1 = [2*(k+1), k+1, k]
        B2 = [2*(k+1)*B1[i] - v for i, v in enumerate([1,0,0])]
        nodes4.append(B1)
        nodes4.append(B2)
        for i in range(2, excep_depth):
            B_prev = nodes4[-1]
            B_prev2 = nodes4[-2]
            B_next = [2*(k+1)*B_prev[j] - B_prev2[j] for j in range(3)]
            nodes4.append(B_next)
        excep.append(nodes4)

        # Type 5
        nodes5 = []
        B1 = [k+1, k, 0]
        B2 = [2*k*(k+1), 2*k*k, 1]
        nodes5.append(B1)
        nodes5.append(B2)
        for i in range(2, excep_depth):
            B_prev = nodes5[-1]
            B_prev2 = nodes5[-2]
            B_next = [2*k*B_prev[j] - B_prev2[j] for j in range(3)]
            nodes5.append(B_next)
        excep.append(nodes5)

        # Type 6
        nodes6 = []
        B1 = [k, k+1, 0]
        B2 = [2*(k+1)*k, 2*(k+1)*(k+1), 1]
        nodes6.append(B1)
        nodes6.append(B2)
        for i in range(2, excep_depth):
            B_prev = nodes6[-1]
            B_prev2 = nodes6[-2]
            B_next = [2*(k+1)*B_prev[j] - B_prev2[j] for j in range(3)]
            nodes6.append(B_next)
        excep.append(nodes6)

        # Type 7
        nodes7 = []
        B1 = [0, k+1, k]
        B2 = [1, 2*(k+1)*(k+1), 2*(k+1)*k]
        nodes7.append(B1)
        nodes7.append(B2)
        for i in range(2, excep_depth):
            B_prev = nodes7[-1]
            B_prev2 = nodes7[-2]
            B_next = [2*(k+1)*B_prev[j] - B_prev2[j] for j in range(3)]
            nodes7.append(B_next)
        excep.append(nodes7)

        # Type 8
        nodes8 = []
        B1 = [0, k, k+1]
        B2 = [1, 2*k*k, 2*k*(k+1)]
        nodes8.append(B1)
        nodes8.append(B2)
        for i in range(2, excep_depth):
            B_prev = nodes8[-1]
            B_prev2 = nodes8[-2]
            B_next = [2*k*B_prev[j] - B_prev2[j] for j in range(3)]
            nodes8.append(B_next)
        excep.append(nodes8)

    return excep

# Corners of the triangle for barycentric coordinates
BL = np.array([0, 0])                              # (0,0,1)
TOP = np.array([0.5, math.sqrt(3) / 2])            # (0,1,0)
BR = np.array([1, 0])                              # (1,0,0)


def bary_to_cart(triple: tuple[float, float, float]) -> np.ndarray:
    """ Convert barycentric coordinates to Cartesian coordinates in the triangle defined by BL, TOP, BR.
    
    Args:
        triple (tuple[float, float, float]): The barycentric coordinates (A, B, C).
    
    Returns:
        np.ndarray: The Cartesian coordinates.
    """
    A, B, C = triple
    S = A + B + C
    if S == 0:
        return np.array([0, 0])
    return (A * BR + B * TOP + C * BL) / S


def renormalize(triple: tuple[float, float, float]) -> list[float]:
    """ Renormalize a triple to ensure it sums to 1. If the sum is zero, return the original triple.
    
    Args:
        triple (tuple[float, float, float]): The input triple (A, B, C).
    
    Returns:
        list[float]: The renormalized triple.
    """
    s = sum(triple)
    if s == 0:
        return triple[:]
    return [x/s for x in triple]


def func1(points: list[tuple[float, float, float]]) -> list[list[float]]:
    """ Apply the first reflection function to a list of points in barycentric coordinates.
    
    Args:
        points (list[tuple[float, float, float]]): A list of points in barycentric coordinates.
    
    Returns:
        list[list[float]]: A list of reflected points in barycentric coordinates.
    """
    return [[2 * B - A, B, C] for (A, B, C) in points]


def func2(points: list[tuple[float, float, float]]) -> list[list[float]]:
    """ Apply the second reflection function to a list of points in barycentric coordinates.
    
    Args:
        points (list[tuple[float, float, float]]): A list of points in barycentric coordinates.
    
    Returns:
        list[list[float]]: A list of reflected points in barycentric coordinates.
    """
    return [[A, 2 * A + 2 * C - B, C] for (A, B, C) in points]


def func3(points: list[tuple[float, float, float]]) -> list[list[float]]:
    """ Apply the third reflection function to a list of points in barycentric coordinates.
    
    Args:
        points (list[tuple[float, float, float]]): A list of points in barycentric coordinates.
    
    Returns:
        list[list[float]]: A list of reflected points in barycentric coordinates.
    """

    return [[A, B, 2 * B - C] for (A, B, C) in points]

# Mapping of digits to their corresponding reflection functions
digit_actions = {'1': func1, '2': func2, '3': func3}


def arrow_symbol(mode: str = "updown"):
    """ Return a LaTeX string representing an arrow symbol based on the specified mode to depict the orientation of the underlying quiver.

    Args: 
        mode (str): The mode specifying the arrow orientation. It can be "up", "down", "updown", or "downup".
    
    Returns:
        str: A LaTeX string representing the arrow symbol corresponding to the specified mode.
    """
    if mode == "up":
        return "$\\begin{matrix} \\uparrow \\\\ \\uparrow\\end{matrix}$"
    elif mode == "down":
        return "$\\begin{matrix} \\downarrow \\\\ \\downarrow\\end{matrix}$"
    elif mode == "updown":
        return "$\\begin{matrix} \\uparrow \\\\ \\downarrow\\end{matrix}$"
    elif mode == "downup":
        return "$\\begin{matrix} \\downarrow \\\\ \\uparrow\\end{matrix}$"



def base_lines(m: int) -> list[tuple[np.ndarray, np.ndarray, int]]:
    """ Generate a list of lines in barycentric coordinates inside the ellipse. These lines are used for the reflected lines.

    Args: 
        m (int): The maximum value of k for which lines are generated. The function generates lines for k values from 1 to m-1.

    Returns:
        list: A list of tuples, where each tuple contains two points (as numpy arrays) and an integer k. Each tuple represents a line segment in barycentric coordinates.
    """
    lines = []
    for k in range(m):
        disc1 = k**2 - 1
        if disc1 >= 0:
            sqrt_disc1 = np.sqrt(disc1)
            x1 = k - sqrt_disc1
            x2 = k + sqrt_disc1
            lines.append((np.array([(k+1)*x1, k*x1, 1.0]), 
                          np.array([(k+1)*x2, k*x2, 1.0]), k)) # Type 1
            lines.append((np.array([1.0, k*x1, (k+1)*x1]),
                          np.array([1.0, k*x2, (k+1)*x2]), k)) # Type 2

        disc2 = (k+1)**2 - 1
        if disc2 >= 0:
            sqrt_disc2 = np.sqrt(disc2)
            x1 = k+1 - sqrt_disc2
            x2 = k+1 + sqrt_disc2
            lines.append((np.array([k*x1, (k+1)*x1, 1.0]),
                          np.array([k*x2, (k+1)*x2, 1.0]), k)) # Type 3
            lines.append((np.array([1.0, (k+1)*x1, k*x1]),
                          np.array([1.0, (k+1)*x2, k*x2]), k)) # Type 4
    return lines


def apply_sequence(point: np.ndarray, sequence: str) -> np.ndarray:
    """ Apply a sequence of reflection functions to a single point in barycentric coordinates.
    
    Args:
        point (np.ndarray): A numpy array representing the initial point in barycentric coordinates (A, B, C).
        sequence (str): A string of digits ('1', '2', '3') representing the sequence of reflection functions to apply.
    
    Returns:
        np.ndarray: A numpy array representing the final transformed point in barycentric coordinates after applying the sequence of reflections.    
    """
    current = [point]
    for digit in sequence:
        action = digit_actions[digit]
        current = action(current)
    return current[0]


def matching_steps(sequence: str) -> list[int]:
    """ Identify the steps in the sequence after which the original orientation reoccurs. The function checks for the presence of certain substrings in the sequence and records the corresponding step indices.
    
    Args:
        sequence (str): A string of digits ('1', '2', '3') representing the sequence of reflection functions.
    
    Returns:
        list[int]: A list of integers representing the step indices where the specified patterns occur in the sequence. The indices are 1-based.
    """
    steps = []

    # Check for the presence of "13" or "31" in the beginning of the sequence and record the corresponding step index (2).
    if sequence.startswith("13") or sequence.startswith("31"):
        steps.append(2)

    # Check for the presence of specific substrings in the sequence starting from index 2 and record the corresponding step indices (i+1).
    for i in range(2, len(sequence)):
        window = sequence[i-2:i+1]
        if window in {"123","321","121","323"}:
            steps.append(i+1)

    return steps


def plot_line_steps(fig: go.Figure, sequence: str, line_pts: list[np.ndarray], k: int = None, color: str = "rgb(0,255,255)"):
    """ Plot the reflected lines for a given sequence and line segment in barycentric coordinates. The function applies the sequence of reflection functions to the endpoints of the line segment and adds the resulting transformed lines to the provided Plotly figure.
    
    Args:
        fig (go.Figure): A Plotly figure object to which the reflected lines will be added.
        sequence (str): A string of digits ('1', '2', '3') representing the sequence of reflection functions to apply.
        line_pts (list[np.ndarray]): A list containing two numpy arrays representing the endpoints of the line segment in barycentric coordinates.
        k (int, optional): An optional integer parameter that can be used to label the lines in the plot. Defaults to None.
        color (str, optional): A string representing the color of the lines in RGB format. Defaults to "rgb(0,255,255)".
    """
    steps = matching_steps(sequence)

    for step in steps:
        seq_partial = sequence[:step]
        line_transformed = [apply_sequence(pt, seq_partial) for pt in line_pts]
        line_cart = np.array([bary_to_cart(pt) for pt in line_transformed])

        fig.add_trace(go.Scatter(
            x=line_cart[:, 0],
            y=line_cart[:, 1],
            mode="lines",
            line=dict(color=color, width=3),
            name=f"Line k={k}, step={step}",
            showlegend=False,
            hoverinfo="text",
            text=[f"Total Reflections: {step}, k={k}"]
        ))

#=========================================================================================
# Functions: Ellipse
#=========================================================================================

# Quadratic form for the ellipse: a^2 + b^2 + c^2 - 2ab - 2bc
Q = np.array([[1.0, -1.0,  0.0],
              [-1.0, 1.0, -1.0],
              [0.0, -1.0,  1.0]])


def compute_conic_cart_points_analytic(n_theta: int = 3000, keep_in_simplex: bool = True, tol: float = 1e-12, fallback_n_samples: int = 4000):
    """ Compute points on the conic section defined by the quadratic form Q in Cartesian coordinates. The function uses an analytic approach to compute the points, and if the computation fails due to numerical issues, it falls back to a sampling method.
    
    Args:
        n_theta (int): The number of angular samples to use for generating points on the conic section. Defaults to 3000.
        keep_in_simplex (bool): Whether to keep the computed points within the simplex defined by the triangle. Defaults to True.
        tol (float): A tolerance value for numerical comparisons. Defaults to 1e-12.
        fallback_n_samples (int): The number of samples to use in the fallback sampling method if the analytic computation fails. Defaults to 4000.
    
    Returns:
        np.ndarray: An array of points in Cartesian coordinates representing the conic section. The shape of the array is (num_points, 2), where num_points is the number of computed points.
    """
    M = np.array([[1.0, 0.0],
                  [0.0, 1.0],
                  [-1.0, -1.0]])
    t = np.array([0.0, 0.0, 1.0])

    A_u = M.T @ Q @ M
    b_u = 2.0 * (M.T @ Q @ t)
    c0 = float(t.T @ Q @ t)

    P = np.column_stack([BR - BL, TOP - BL])
    try:
        Pinv = np.linalg.inv(P)
    except np.linalg.LinAlgError:
        return _compute_conic_points_sample(fallback_n_samples, keep_in_simplex, tol)

    A_cart = Pinv.T @ A_u @ Pinv
    b_cart = Pinv.T @ b_u.reshape(2, 1)
    c_cart = c0

    try:
        y0 = -0.5 * np.linalg.solve(A_cart, b_cart).reshape(2)
    except np.linalg.LinAlgError:
        return _compute_conic_points_sample(fallback_n_samples, keep_in_simplex, tol)

    F_c = float(y0 @ (A_cart @ y0) + (b_cart.ravel() @ y0) + c_cart)

    eigvals, eigvecs = np.linalg.eigh(A_cart)
    if np.any(eigvals <= 0) or F_c >= 0:
        return _compute_conic_points_sample(fallback_n_samples, keep_in_simplex, tol)

    axes = np.sqrt((-F_c) / eigvals)
    center = BL + y0

    thetas = np.linspace(0, 2 * np.pi, n_theta, endpoint=True)
    pts = np.array([center + (eigvecs @ (axes * np.array([np.cos(t), np.sin(t)]))) for t in thetas])

    if keep_in_simplex:
        upts = (Pinv @ (pts.T - BL.reshape(2, 1))).T
        a_vals = upts[:, 0]
        b_vals = upts[:, 1]
        c_vals = 1.0 - a_vals - b_vals
        mask = (a_vals >= -tol) & (b_vals >= -tol) & (c_vals >= -tol)
        pts = pts[mask]
        if pts.shape[0] > 0 and not np.allclose(pts[0], pts[-1]):
            pts = np.vstack([pts, pts[0]])
    return pts


def _compute_conic_points_sample(n_samples: int, keep_in_simplex: bool, tol: float) -> np.ndarray:
    """ Compute points on the conic section defined by the quadratic form Q using a sampling method. This function is used as a fallback when the analytic computation fails.

    Args: 
        n_samples (int): The number of samples to use for generating points on the conic section.
        keep_in_simplex (bool): Whether to keep the computed points within the simplex defined by the triangle.
        tol (float): A tolerance value for numerical comparisons.
    
    Returns: 
        np.ndarray: An array of points on the conic section.
    """
    a_min, a_max = -0.2, 1.2
    pts = []
    a_vals = np.linspace(a_min, a_max, n_samples)
    for a in a_vals:
        A = 4.0
        B = 2.0 * a - 4.0
        C = 2.0 * a * a - 2.0 * a + 1.0
        disc = B * B - 4.0 * A * C
        if disc < -1e-12:
            continue
        disc = max(disc, 0.0)
        sqrt_disc = math.sqrt(disc)
        for b in [(-B + sqrt_disc) / (2 * A), (-B - sqrt_disc) / (2 * A)]:
            c = 1.0 - a - b
            if keep_in_simplex and (a < -tol or b < -tol or c < -tol):
                continue
            cart = bary_to_cart(renormalize((a, b, c)))
            pts.append(cart)
    if not pts:
        return np.empty((0, 2))
    pts = np.array(pts)
    center = pts.mean(axis=0)
    ang = np.arctan2(pts[:, 1] - center[1], pts[:, 0] - center[0])
    pts = pts[np.argsort(ang)]
    pts = np.vstack([pts, pts[0]])
    return pts


def add_line(fig: go.Figure, bary1: tuple, bary2: tuple, color: str ="rgba(0,0,0,0.4)", width: float = 1.0) -> None:
    """ Add a line segment between two points in barycentric coordinates to a Plotly figure.
    
    Args: 
        fig (go.Figure): A Plotly figure object to which the line segment will be added.
        bary1 (tuple): The first point in barycentric coordinates (A, B, C).
        bary2 (tuple): The second point in barycentric coordinates (A, B, C).
        color (str): The color of the line segment in RGBA format. Defaults to "rgba(0,0,0,0.4)".
        width (float): The width of the line segment. Defaults to 1.0.
    """
    p1, p2 = bary_to_cart(bary1), bary_to_cart(bary2)
    fig.add_trace(go.Scatter(
        x=[p1[0], p2[0]],
        y=[p1[1], p2[1]],
        mode="lines",
        line=dict(color=color, width=width),
        showlegend=False,
        hoverinfo="skip"
    ))


def step_size(k: int) -> int:
    """ Determine the step size for plotting based on the value of k. The function returns different step sizes for different ranges of k to control the density of plotted lines.
    
    Args:
        k (int): The value of k for which to determine the step size.
    
    Returns:
        int: The step size for plotting.
    """
    if k < 20:
        return 1
    elif k < 40:
        return 2
    elif k < 60:
        return 5
    elif k < 80:
        return 10
    else:
        return 20


def main():
    """ Main function to run the Streamlit application for visualizing the simplex diagram with reflections. This function sets up the user interface, handles user inputs, and generates the visualizations based on the specified sequences of reflections and other parameters."""
    
    st.set_page_config(layout="wide")
    st.title("Simplex Diagram with Reflections")
    
    # ============================================
    # Layout
    # ============================================

    # --- Dimension Vectors Input ---
    # Each line is one vector of three space-separated barycentric coordinates (A, B, C).
    dimvecs_str = st.text_area(
        "Enter dimension vectors (space-separated)",
        "1 2 1\n0 2 1\n0 1 0\n148 236 103", height=135
    )
    
    if dimvecs_str.strip(): 
        DimVecs_base = [
            [
                int(val) if float(val).is_integer() else float(val) 
                for val in line.split() 
            ]
            for line in dimvecs_str.strip().splitlines()
        ]
    else:
        DimVecs_base = []  
    
    Given_base = [tuple(pt) for pt in DimVecs_base]
    
    # --- Sequences Input ---
    # Each line represents a sequence of digits ('1', '2', '3'). Each digit represents a reflection.
    sequences_str = st.text_area("Enter sequences of reflections", "123123\n13123123", height=75)
    sequences = [seq.strip() for seq in sequences_str.split() if seq.strip()]
    
    n = 1  # number of iterations of the reflection sequences. Used in line 593.
    
    label_size = 14  # size of the labels in the plotly figure
    
    
    # --- Display controls ---
    # 
    st.caption("Display controls")
    
    color_col, wrong_col = st.columns([1.2, 2.0])
    with color_col:
        use_color = st.checkbox("Color", value=True, key="color_toggle")
    with wrong_col:
        if use_color:
            show_wrong = st.checkbox("Show different orientation", value=False, key="show_wrong_toggle")
    
    with st.expander("Visualization Options", expanded=False):
        viz_col1, viz_col2, viz_col3, viz_col4, viz_col5, viz_col6 = st.columns([1.1, 1.1, 1.0, 1.6, 1.8, 1.5])
        with viz_col1:
            use_arrows = st.toggle("Quivers", value=True, key="arrows_toggle")
        with viz_col2:
            show_polygons = st.checkbox("Polygons", value=True, key="polygons_toggle")
        with viz_col3:
            show_lines = st.checkbox("Lines", value=True, key="lines_toggle")
        with viz_col4:
            show_one_simplex = st.checkbox("Simplex for all Sequences", value=True, key="one_simplex_toggle")
        with viz_col5:
            show_refl_lines = st.checkbox("Reflected Lines", value=True, key="refl_lines_toggle")
    
    # Number of Lines
    # Keep a default so the combined chart can still render even when the
    # line controls are not currently enabled.
    m = 10
    if show_lines:
        m = st.number_input("Number of Lines", min_value=0, value=10, step=1)
        o = st.number_input("Number of Exceptional Sequences", min_value=0, value=5, step=1)
        l = st.number_input("Depth of Exceptional Sequences", min_value=0, value=2, step=1)
    else:
        # When the combined simplex view is active, we still want a valid chart
        # even if the line controls are turned off.
        o = 5
        l = 2
    
    # --------------------
    # Mehrere Sequenzen parallel
    # --------------------
    
    cols = st.columns(len(sequences)) 
    nodes_cor = []
    all_nodes_global = []        # all barycentric nodes across all sequences
    all_polygons_global = []     # polygons from each step
    all_correct_nodes = []       # correct quiver nodes
    all_wrong_nodes = []         # wrong quiver nodes
    
    for seq_idx, (col, sequence) in enumerate(zip(cols, sequences)):
        uid = f"seq{seq_idx}"
        with col:
            if show_one_simplex == False:
                st.subheader(f"Simplex Diagram ({sequence})")
    
            # copy of starting data for each sequence
            DimVecs = [v[:] for v in DimVecs_base]
            Given = Given_base[:]
    
            digits = []
            nodes = []          # kartesische Punkte pro Schritt (für Polygone)
            all_nodes = []      # (cart, bary) für generische Punktdarstellung
            output = []
    
            # Quiver Tracking
            q = [1,1]
            correct1, correct2, wrong1, wrong2, error = [], [], [], [], []
            poly_kind = []  # NEU: "correct"/"wrong"/"neutral" je Iterationsschritt (für Polygone)
    
            for i in range(1, n):
                for digit in sequence:
                    digits.append(digit)
                    action = digit_actions.get(digit)
                    if action:
                        # Vorherige Zählerstände merken (für Klassifikation)
                        prev_wrong = len(wrong1) + len(wrong2)
                        prev_correct = len(correct1) + len(correct2)
    
                        # Transformation + Speicherung der kartesischen Punkte
                        DimVecs = action(DimVecs)
                        DimVecs_new = [renormalize(pt) for pt in DimVecs]
                        DimVecs_cart = [bary_to_cart(pt) for pt in DimVecs_new]
                        nodes.append(DimVecs_cart)
    
                        # Quiver Reflections 
                        if q == [1,1]:
                            if digit == "1":
                                wrong1.append(DimVecs) 
                                q = [0,1]
                            if digit == "2":
                                correct2.append(DimVecs) 
                                q = [0,0] 
                                error = [f'{d}' for d in digits]
                            if digit == "3":
                                wrong2.append(DimVecs) 
                                q = [1,0]
                        elif q == [0,1]:
                            if digit == "1":
                                correct1.append(DimVecs) 
                                q = [1,1]
                            if digit == "2":
                                wrong2.append(DimVecs)
                                q = [1,0]
                            if digit == "3":
                                correct2.append(DimVecs)
                                q = [0,0]
                        elif q == [1,0]:
                            if digit == "1":
                                correct2.append(DimVecs)
                                q = [0,0]
                            if digit == "2":
                                wrong1.append(DimVecs)
                                q = [0,1]
                            if digit == "3":
                                correct1.append(DimVecs)
                                q = [1,1]
                        elif q == [0,0]:
                            if digit == "1":
                                wrong2.append(DimVecs)
                                q = [1,0]
                            if digit == "2":
                                correct1.append(DimVecs)
                                q = [1,1]
                                error = [f'{d}' for d in digits]
                            if digit == "3":
                                wrong1.append(DimVecs)
                                q = [0,1]        
    
                        # NEU: Schritt als wrong/correct/neutral klassifizieren
                        if (len(correct1) + len(correct2)) > prev_correct:
                            poly_kind.append("correct")
                        elif (len(wrong1) + len(wrong2)) > prev_wrong:
                            poly_kind.append("wrong")
                        else:
                            poly_kind.append("neutral")
    
                    # Quiver Output (unverändert)
                    if q == [1,1]:
                        arrow = arrow_symbol("down") if use_arrows else ""
                        line_color = "green" if use_color else "black"
                    elif q == [0,1]:
                        arrow = arrow_symbol("updown") if use_arrows else ""
                        line_color = "rgb(180, 0, 0)" if use_color else "black"
                    elif q == [1,0]:
                        arrow = arrow_symbol("downup") if use_arrows else ""
                        line_color = "rgb(180, 0, 0)" if use_color else "black"
                    elif q == [0,0]:
                        arrow = arrow_symbol("up") if use_arrows else ""
                        line_color = "green" if use_color else "black"
    
                    text1 = f"{arrow}  Reflection: {' '.join([f'{d}' for d in digits])}"
                    if line_color == "green":
                        text1 = f"<b>{text1}</b>"
                        output.append(f"<span style='color:{line_color}'>{text1}</span>")
                    if line_color == "rgb(180, 0, 0)":
                        if use_color:   
                            if show_wrong:
                                output.append(f"<span style='color:{line_color}'>{text1}</span>")            
                    if line_color == "black":
                        output.append(f"<span style='color:{line_color}'>{text1}</span>")
                  
    
            
                    for point_idx, (A, B, C) in enumerate(DimVecs, 1):
                        cart = bary_to_cart((A, B, C))
                        all_nodes.append((cart, (A, B, C)))
                        text2 = f"&nbsp;&nbsp;&nbsp;&nbsp;P{point_idx}: ({A}, {B}, {C})"
                        if line_color == "green":
                            text2 = f"<b>{text2}</b>"
                            output.append(f"<span style='color:{line_color}'>{text2}</span>")
                        if line_color == "rgb(180, 0, 0)":
                            if use_color:
                                if show_wrong:
                                    output.append(f"<span style='color:{line_color}'>{text2}</span>")
    
            # --------------------
            # Zusätzliche Geometrie: Dreieck und Ellipse 
            # --------------------
            extra_triangle_bary = [(0,1,1),(1,1,0),(1,1,1)]
            extra_triangle_cart = [bary_to_cart(p) for p in extra_triangle_bary] + [bary_to_cart(extra_triangle_bary[0])]
    
            # Ellipse Computation
            Q = np.array([[1.0, -1.0,  0.0],
                        [-1.0, 1.0, -1.0],
                        [0.0, -1.0,  1.0]])   # quadratic form for a^2+b^2+c^2-2ab-2bc
    
    
            # --------------------
            # Plotly figure 
            # --------------------
            fig = go.Figure()
    
            # Simplex
            simplex_cart = [BL, TOP, BR, BL]
            fig.add_trace(go.Scatter(x=[p[0] for p in simplex_cart], y=[p[1] for p in simplex_cart],
                                    mode="lines", line=dict(color="black", width=3),
                                    fill="toself", fillcolor="rgba(230,230,230,0.2)", name="Simplex", showlegend=False, hoverinfo="skip"))
    
            # Fundamental Domain
            fig.add_trace(go.Scatter(x=[p[0] for p in extra_triangle_cart], y=[p[1] for p in extra_triangle_cart],
                                    mode="lines", line=dict(color="black", width=2), 
                                    fill="toself",
                                    fillcolor="rgba(0, 255, 255, 0.4)", name="Triangle", showlegend=False, hoverinfo="skip"))
    
            # Ellipse Plot
            ellipse_cart = compute_conic_cart_points_analytic(n_theta=1200, keep_in_simplex=True, tol=1e-12)
            if ellipse_cart.size > 0:
                fig.add_trace(go.Scatter(x=ellipse_cart[:,0], y=ellipse_cart[:,1],
                                        mode="lines", line=dict(color="black", width=2),
                                        name="Conic (analytic)", showlegend=False, hoverinfo="skip"))
    
            # Reflected lines for the individual sequence view.
            if show_refl_lines and show_one_simplex == False:
                all_lines = base_lines(m)
                for (p1, p2, k) in all_lines:
                    plot_line_steps(fig, sequence, [p1, p2], k=k)
    
            triangles = []
            DimVecs_tmp = []  # start fresh
            for i in range(13):
                # choose a digit (cycle through "123")
                digit = str((i % 3) + 1)
                DimVecs_tmp = digit_actions[digit](DimVecs_tmp)
    
                if len(DimVecs_tmp) >= 3:
                    tri = DimVecs_tmp[:3]
                    triangles.append(tri)
    
    
            if show_lines:
                # From (0,0,1)
                k = 1
                while k < m:
                    add_line(fig, (0,0,1), (k+1,k,0))
                    add_line(fig, (0,0,1), (k,k+1,0))
                    k += step_size(k)
    
                # From (1,0,0)
                k = 1
                while k < m:
                    add_line(fig, (1,0,0), (0,k,k+1))
                    add_line(fig, (1,0,0), (0,k+1,k))
                    k += step_size(k)
                
                # Exceptionals
                excep_t = gen_excep(o,l)
                excep = [node for nodes_k in excep_t for node in nodes_k]
                excep_cart = [bary_to_cart(renormalize(pt)) for pt in excep]
                fig.add_trace(go.Scatter(
                    x=[p[0] for p in excep_cart],
                    y=[p[1] for p in excep_cart],
                    mode="markers",
                    marker=dict(color="rgba(0,0,0,1)", size=2),
                    text=[f"({a}, {b}, {c})" for (a,b,c) in excep],
                    textposition="top center",
                    name="Exceptionals",
                    showlegend=False,
                    hoverinfo="text"))
                fig.add_trace(go.Scatter(x=[p[0] for p in excep_cart],
                    y=[p[1] for p in excep_cart],
                    mode="text", text=[f"({a}, {b}, {c})" for (a,b,c) in excep], showlegend=False,
                    textposition="top center", textfont=dict(size=label_size),
                    legendgroup="Labels", visible="legendonly", hoverinfo="skip"))
    
            if use_color:
                # Red nodes: wrong1 + wrong2
                if show_wrong:
                    wrong_nodes = wrong1 + wrong2
                    fig.add_trace(go.Scatter(x=[bary_to_cart(renormalize(pt))[0] for node in wrong_nodes for pt in node],
                                        y=[bary_to_cart(renormalize(pt))[1] for node in wrong_nodes for pt in node],
                                        mode="markers", 
                                        marker=dict(color="rgb(180, 0, 0)", size=6), name="Different Orientation", legendgroup="wrong", showlegend=True, 
                                        text=[f"({a}, {b}, {c})" for node in wrong_nodes for (a,b,c) in node], hoverinfo="text"))
                    fig.add_trace(go.Scatter(x=[bary_to_cart(renormalize(pt))[0] for node in wrong_nodes for pt in node],
                                        y=[bary_to_cart(renormalize(pt))[1] for node in wrong_nodes for pt in node],
                                        mode="text", text=[f"({a}, {b}, {c})" for node in wrong_nodes for (a,b,c) in node], showlegend=False,
                                        textposition="top center", textfont=dict(size=label_size), legendgroup="Labels", visible="legendonly", hoverinfo="skip"))
    
                # Green nodes: correct1 + correct2
                correct_nodes = correct1 + correct2
                fig.add_trace(go.Scatter(x=[bary_to_cart(renormalize(pt))[0] for node in correct_nodes for pt in node],
                                    y=[bary_to_cart(renormalize(pt))[1] for node in correct_nodes for pt in node],
                                    mode="markers", 
                                    marker=dict(color="green", size=6), name="Kronecker Chain", legendgroup="correct",showlegend=True, 
                                    text=[f"({a}, {b}, {c})" for node in correct_nodes for (a,b,c) in node], hoverinfo="text"))
                fig.add_trace(go.Scatter(x=[bary_to_cart(renormalize(pt))[0] for node in correct_nodes for pt in node],
                                    y=[bary_to_cart(renormalize(pt))[1] for node in correct_nodes for pt in node],
                                    mode="text", text=[f"({a}, {b}, {c})" for node in correct_nodes for (a,b,c) in node], legendrank=3,
                                    textposition="top center", textfont=dict(size=label_size), legendgroup="Labels", name="Labels", visible="legendonly", hoverinfo="skip"))
    
            else:
                # Reflected Dimension Vectors
                fig.add_trace(go.Scatter(x=[cart[0] for cart, bary in all_nodes],
                                    y=[cart[1] for cart, bary in all_nodes],
                                    mode="markers", 
                                    marker=dict(color="rgb(0,120,150)", size=6), name="Nodes", showlegend=False, 
                                    text=[f"({a}, {b}, {c})" for cart, (a,b,c) in all_nodes], hoverinfo="text"))
                fig.add_trace(go.Scatter(x=[cart[0] for cart, bary in all_nodes],
                                    y=[cart[1] for cart, bary in all_nodes],
                                    mode="text", text=[f"({a}, {b}, {c})" for cart, (a,b,c) in all_nodes], 
                                    textposition="top center", textfont=dict(size=label_size), legendgroup="Labels", name="Labels", visible="legendonly", hoverinfo="skip"))
    
            
            if show_polygons:
                legend_shown = {"wrong": False, "correct": False, "neutral": False}
    
    
                Given_cart = [bary_to_cart(pt) for pt in Given]
                if len(Given_cart) >= 3:
                    fig.add_trace(go.Scatter(
                        x=[p[0] for p in Given_cart] + [Given_cart[0][0]],
                        y=[p[1] for p in Given_cart] + [Given_cart[0][1]],
                        mode="lines",
                        line=dict(color="blue", width=2, dash="dot"),
                        name="Given Polygon",
                        legendgroup="given",
                        showlegend=False,
                        hoverinfo="skip"
                    ))
    
                for nodes_iter, kind in zip(nodes, poly_kind):
                    if len(nodes_iter) < 3:
                        continue
    
                    if kind == "wrong":
                        color, group = "rgb(180, 0, 0)", "wrong"
                    elif kind == "correct":
                        color, group = "green", "correct"
                        nodes_cor.append(nodes_iter)
                    else:
                        color, group = "gray", "neutral"
    
                    if not use_color:
                        color = "rgb(0,120,150)"
    
                    # Polygon traces are part of the group but do NOT appear in the legend
                    if use_color:
                        if show_wrong:
                            fig.add_trace(go.Scatter(
                                x=[p[0] for p in nodes_iter] + [nodes_iter[0][0]],
                                y=[p[1] for p in nodes_iter] + [nodes_iter[0][1]],
                                mode="lines",
                                line=dict(color=color, width=2),
                                name="",
                                legendgroup=group,
                                showlegend=False,
                                hoverinfo="skip"
                            ))
    
                        else:
                            for nodes_c in nodes_cor:
                                fig.add_trace(go.Scatter(
                                    x=[p[0] for p in nodes_c] + [nodes_c[0][0]],
                                    y=[p[1] for p in nodes_c] + [nodes_c[0][1]],
                                    mode="lines",
                                    line=dict(color=color, width=2),
                                    name="",
                                    legendgroup=group,
                                    showlegend=False,
                                    hoverinfo="skip"
                                ))
                                                
            # Given Dimension Vectors
            Given_cart = [bary_to_cart(pt) for pt in Given]
            fig.add_trace(go.Scatter(x=[p[0] for p in Given_cart],
                                    y=[p[1] for p in Given_cart],
                                    mode="markers", 
                                    marker=dict(color="blue", size=6), name="Nodes", showlegend=False, 
                                    text=[f"({a}, {b}, {c})" for (a,b,c) in Given], hoverinfo="text"))
            fig.add_trace(go.Scatter(x=[p[0] for p in Given_cart],
                                    y=[p[1] for p in Given_cart],
                                    mode="text", text=[f"({a}, {b}, {c})" for (a,b,c) in Given], 
                                    textposition="top center", textfont=dict(size=label_size), legendgroup="Labels", name="Labels",visible="legendonly", hoverinfo="skip", showlegend=False))
    
            # Simple Dimension Vectors
            fig.add_trace(go.Scatter(x=[BL[0]], y=[BL[1]-0.02],
                                    mode="text", text="(0,0,1)", 
                                    textposition="bottom center", textfont=dict(size=label_size), hoverinfo="skip", showlegend=False))
            fig.add_trace(go.Scatter(x=[BR[0]], y=[BR[1]-0.02],
                                    mode="text", text="(1,0,0)", 
                                    textposition="bottom center", textfont=dict(size=label_size), hoverinfo="skip", showlegend=False))
            fig.add_trace(go.Scatter(x=[TOP[0]], y=[TOP[1]+0.01],
                                    mode="text", text="(0,1,0)", 
                                    textposition="top center", textfont=dict(size=label_size), hoverinfo="skip", showlegend=False))
    
            # Figure Layout
            fig.update_layout(width=800, height=800, 
                            xaxis=dict(scaleanchor="y", showgrid=False, zeroline=False, showticklabels=False, title=None),
                            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, title=None),
                            margin=dict(l=0, r=80, t=0, b=0),
                            showlegend=True,
                            legend=dict(x=0.95,y=0.8),
                            autosize=True
                            )
            if show_one_simplex == False:
                st.plotly_chart(fig, width="stretch", key=f"plotly_{uid}")
    
                if use_color and seq_idx == 0:
                    legend_col1, legend_col2 = st.columns(2)
                    with legend_col1:
                        st.markdown(
                            "<span style='color:rgb(180, 0, 0); font-weight:600'>Different Orientation</span>",
                            unsafe_allow_html=True,
                        )
                    with legend_col2:
                        st.markdown(
                            "<span style='color:green; font-weight:600'>Kronecker Chain</span>",
                            unsafe_allow_html=True,
                        )
    
                # Align the heading in the other columns with the first column.
                if seq_idx > 0:
                    st.markdown(
                        "<div style='margin-top: 1.8cm;'></div>",
                        unsafe_allow_html=True,
                    )
                st.subheader(f"Reflections ({sequence})")
                st.markdown("  <br>  ".join(output), unsafe_allow_html=True)
        
        # NEW: collect for combined diagram
            all_nodes_global.extend(all_nodes)             # all (cart, bary)
            all_polygons_global.extend(nodes)              # all polygons (list of cart coords)
            all_correct_nodes.extend(correct1 + correct2)  # correct steps
            all_wrong_nodes.extend(wrong1 + wrong2)        # wrong steps
    
    # --------------------
    # Combined Simplex for All Sequences
    # --------------------
    if show_one_simplex == True:
        st.subheader(f"Simplex Diagram for all Sequences")
    
    fig = go.Figure()
    
    # Simplex
    simplex_cart = [BL, TOP, BR, BL]
    fig.add_trace(go.Scatter(
        x=[p[0] for p in simplex_cart], y=[p[1] for p in simplex_cart],
        mode="lines", line=dict(color="black", width=3),
        fill="toself", fillcolor="rgba(230,230,230,0.2)",
        name="Simplex", showlegend=False, hoverinfo="skip"
    ))
    
    # Fundamental Domain (triangle)
    fig.add_trace(go.Scatter(
        x=[p[0] for p in extra_triangle_cart], y=[p[1] for p in extra_triangle_cart],
        mode="lines",
        line=dict(color="black", width=2),
                                    fill="toself",
                                    fillcolor="rgba(0, 255, 255, 0.4)",
        name="Triangle", showlegend=False, hoverinfo="skip"
    ))
    
    # Reflected Lines
    if show_refl_lines:
        all_lines = base_lines(m)  # returns list of (p1, p2, k)
        for seq in sequences:
            for (p1, p2, k) in all_lines:
                # Make sure line_pts is a list of points
                plot_line_steps(fig, seq, [p1, p2], k=k)
    
    
    # Ellipse Plot
    ellipse_cart = compute_conic_cart_points_analytic(n_theta=1200, keep_in_simplex=True, tol=1e-12)
    if ellipse_cart.size > 0:
        fig.add_trace(go.Scatter(x=ellipse_cart[:,0], y=ellipse_cart[:,1],
                                mode="lines", line=dict(color="black", width=2),
                                name="Conic (analytic)", showlegend=False, hoverinfo="skip"))
    
    # Lines from Simples
    if show_lines:
        # From (0,0,1)
        k = 1
        while k < m:
            add_line(fig, (0,0,1), (k+1,k,0))
            add_line(fig, (0,0,1), (k,k+1,0))
            k += step_size(k)
    
        # From (1,0,0)
        k = 1
        while k < m:
            add_line(fig, (1,0,0), (0,k,k+1))
            add_line(fig, (1,0,0), (0,k+1,k))
            k += step_size(k)
    
    # Wrong nodes (all sequences)
    if use_color and show_wrong:
        fig.add_trace(go.Scatter(
            x=[bary_to_cart(renormalize(pt))[0] for node in all_wrong_nodes for pt in node],
            y=[bary_to_cart(renormalize(pt))[1] for node in all_wrong_nodes for pt in node],
            mode="markers",
            marker=dict(color="rgb(180,0,0)", size=6),
            name="Different Orientation", legendgroup="wrong", showlegend=True,
            text=[f"({a}, {b}, {c})" for node in all_wrong_nodes for (a,b,c) in node],
            hoverinfo="text"
        ))
        # Optional barycentric labels (toggleable)
        fig.add_trace(go.Scatter(
            x=[bary_to_cart(renormalize(pt))[0] for node in all_wrong_nodes for pt in node],
            y=[bary_to_cart(renormalize(pt))[1] for node in all_wrong_nodes for pt in node],
            mode="text",
            text=[f"({a}, {b}, {c})" for node in all_wrong_nodes for (a,b,c) in node],
            showlegend=False, textposition="top center",
            textfont=dict(size=label_size),
            legendgroup="Labels", visible="legendonly", hoverinfo="skip"
        ))
    
    # Correct nodes (all sequences)
    if use_color:
        fig.add_trace(go.Scatter(
            x=[bary_to_cart(renormalize(pt))[0] for node in all_correct_nodes for pt in node],
            y=[bary_to_cart(renormalize(pt))[1] for node in all_correct_nodes for pt in node],
            mode="markers",
            marker=dict(color="green", size=6),
            name="Kronecker Chain", legendgroup="correct", showlegend=True,
            text=[f"({a}, {b}, {c})" for node in all_correct_nodes for (a,b,c) in node],
            hoverinfo="text"
        ))
        fig.add_trace(go.Scatter(
            x=[bary_to_cart(renormalize(pt))[0] for node in all_correct_nodes for pt in node],
            y=[bary_to_cart(renormalize(pt))[1] for node in all_correct_nodes for pt in node],
            mode="text",
            text=[f"({a}, {b}, {c})" for node in all_correct_nodes for (a,b,c) in node],
            textposition="top center", textfont=dict(size=label_size),
            legendgroup="Labels", name="Labels",
            visible="legendonly", hoverinfo="skip"
        ))
    
    # Given nodes (all sequences, blue)
    fig.add_trace(go.Scatter(
        x=[bary_to_cart(pt)[0] for pt in Given],
        y=[bary_to_cart(pt)[1] for pt in Given],
        mode="markers",
        marker=dict(color="blue", size=6),
        name="Given Nodes", legendgroup="given", showlegend=False,
        text=[f"({a}, {b}, {c})" for (a,b,c) in Given],
        hoverinfo="text"
    ))
    fig.add_trace(go.Scatter(
        x=[bary_to_cart(pt)[0] for pt in Given],
        y=[bary_to_cart(pt)[1] for pt in Given],
        mode="text",
        text=[f"({a}, {b}, {c})" for (a,b,c) in Given],
        textposition="top center", textfont=dict(size=label_size),
        legendgroup="Labels", visible="legendonly", hoverinfo="skip", showlegend=False
    ))
    
    # Polygons
    if show_polygons:
                legend_shown = {"wrong": False, "correct": False, "neutral": False}
    
    
                Given_cart = [bary_to_cart(pt) for pt in Given]
                if len(Given_cart) >= 3:
                    fig.add_trace(go.Scatter(
                        x=[p[0] for p in Given_cart] + [Given_cart[0][0]],
                        y=[p[1] for p in Given_cart] + [Given_cart[0][1]],
                        mode="lines",
                        line=dict(color="blue", width=2, dash="dot"),
    #                    fill="toself",  
    #                    fillcolor="rgba(0, 255, 255, 0.3)",
                        name="Given Polygon",
                        legendgroup="given",
                        showlegend=False,
                        hoverinfo="skip"
                    ))
    
                for nodes_iter, kind in zip(nodes, poly_kind):
                    if len(nodes_iter) < 3:
                        continue
                
                    if kind == "wrong":
                        color, group = "rgb(180, 0, 0)", "wrong"
                    elif kind == "correct":
                        color, group = "#228B22", "correct"
                        nodes_cor.append(nodes_iter)
                    else:
                        color, group = "gray", "neutral"
                       
                    if not use_color:
                        color = "rgb(0,120,150)"
    
                    
                # Polygon traces are part of the group but do NOT appear in the legend
                    if use_color:
                        if show_wrong:
                            fig.add_trace(go.Scatter(
                                x=[p[0] for p in nodes_iter] + [nodes_iter[0][0]],
                                y=[p[1] for p in nodes_iter] + [nodes_iter[0][1]],
                                mode="lines",
                                line=dict(color=color, width=2),
                                name="",  
                                legendgroup=group,  
                                showlegend=False,   
                                hoverinfo="skip"
                            ))
                        
                        else:
                            for nodes_c in nodes_cor:
                                fig.add_trace(go.Scatter(
                                    x=[p[0] for p in nodes_c] + [nodes_c[0][0]],
                                    y=[p[1] for p in nodes_c] + [nodes_c[0][1]],
                                    mode="lines",
                                    line=dict(color="#228B22", width=1),
                                    name="",  
                                    legendgroup=group,  
                                    showlegend=False,   
                                    hoverinfo="skip"
                                ))
    
    
    
    # Labels at simplex corners
    fig.add_trace(go.Scatter(x=[BL[0]], y=[BL[1]-0.02],
                            mode="text", text="(0,0,1)",
                            textposition="bottom center", textfont=dict(size=label_size),
                            hoverinfo="skip", showlegend=False))
    fig.add_trace(go.Scatter(x=[BR[0]], y=[BR[1]-0.02],
                            mode="text", text="(1,0,0)",
                            textposition="bottom center", textfont=dict(size=label_size),
                            hoverinfo="skip", showlegend=False))
    fig.add_trace(go.Scatter(x=[TOP[0]], y=[TOP[1]+0.01],
                            mode="text", text="(0,1,0)",
                            textposition="top center", textfont=dict(size=label_size),
                            hoverinfo="skip", showlegend=False))
    
    # Layout
    fig.update_layout(
        width=800, height=800,
        xaxis=dict(scaleanchor="y", showgrid=False, zeroline=False, showticklabels=False, title=None),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, title=None),
        margin=dict(l=0, r=80, t=0, b=0),
        showlegend=True,
        legend=dict(x=0.95, y=0.8),
        autosize=True
    )
    
    if show_one_simplex == True:
        st.plotly_chart(fig, width="stretch", key="plotly_combined")

if __name__ == "__main__":
    main()

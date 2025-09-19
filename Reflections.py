import streamlit as st
import math
import numpy as np
import plotly.graph_objects as go

st.set_page_config(layout="wide")
st.title("Simplex Diagram with Reflections")

# --------------------
# Inputs
# --------------------
dimvecs_str = st.text_area(
    "Enter dimension vectors (space-separated)",
    "0 1 0\n0 2 1\n1 2 1\n1 2 0", height=145
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


label_size = 14
# mehrere Sequenzen
sequences_str = st.text_area("Enter sequences of reflections", "31321321321\n321321321321", height=145)
sequences = [seq.strip() for seq in sequences_str.split() if seq.strip()]

n = st.number_input("Number of iterations of the sequences", min_value=0, value=1, step=1)
n = int(n)+1

# Exceptionals
def gen_excep(n, num_iterations):
    excep = []

    for k in range(n):
    # Recursion 1
        nodes1 = []
        B1 = [k+1, k, 2*k]
        B2 = [2*k*(k+1), 2*k*k, 2*k*(2*k)-1]
        nodes1.append(B1)
        nodes1.append(B2)
        
        for i in range(2, num_iterations):
            B_prev = nodes1[-1]
            B_prev2 = nodes1[-2]
            B_next = [2*k*B_prev[j] - B_prev2[j] for j in range(3)]
            nodes1.append(B_next)
        
        excep.append(nodes1)

    # Recursion 2
        nodes2 = []
        B1 = [k, k+1, 2*(k+1)]
        B2 = [2*(k+1)*B1[i] - v for i, v in enumerate([0,0,1])]
        nodes2.append(B1)
        nodes2.append(B2)
        for i in range(2, num_iterations):
            B_prev = nodes2[-1]
            B_prev2 = nodes2[-2]
            B_next = [2*(k+1)*B_prev[j] - B_prev2[j] for j in range(3)]
            nodes2.append(B_next)
        excep.append(nodes2)

    # Recursion 3
        nodes3 = []
        B1 = [2*k, k, k+1]
        B2 = [2*k*B1[i] - v for i, v in enumerate([1,0,0])]
        nodes3.append(B1)
        nodes3.append(B2)
        for i in range(2, num_iterations):
            B_prev = nodes3[-1]
            B_prev2 = nodes3[-2]
            B_next = [2*k*B_prev[j] - B_prev2[j] for j in range(3)]
            nodes3.append(B_next)
        excep.append(nodes3)

    # Recursion 4
        nodes4 = []
        B1 = [2*(k+1), k+1, k]
        B2 = [2*(k+1)*B1[i] - v for i, v in enumerate([1,0,0])]
        nodes4.append(B1)
        nodes4.append(B2)
        for i in range(2, num_iterations):
            B_prev = nodes4[-1]
            B_prev2 = nodes4[-2]
            B_next = [2*(k+1)*B_prev[j] - B_prev2[j] for j in range(3)]
            nodes4.append(B_next)
        excep.append(nodes4)

    # Recursion 5
        nodes5 = []
        B1 = [k+1, k, 0]
        B2 = [2*k*(k+1), 2*k*k, 1]
        nodes5.append(B1)
        nodes5.append(B2)
        
        for i in range(2, num_iterations):
            B_prev = nodes5[-1]
            B_prev2 = nodes5[-2]
            B_next = [2*k*B_prev[j] - B_prev2[j] for j in range(3)]
            nodes5.append(B_next)
        excep.append(nodes5)

    # Recursion 6
        nodes6 = []
        B1 = [k, k+1, 0]
        B2 = [2*(k+1)*k, 2*(k+1)*(k+1), 1]
        nodes6.append(B1)
        nodes6.append(B2)
        
        for i in range(2, num_iterations):
            B_prev = nodes6[-1]
            B_prev2 = nodes6[-2]
            B_next = [2*(k+1)*B_prev[j] - B_prev2[j] for j in range(3)]
            nodes6.append(B_next)
        excep.append(nodes6)
    
    # Recursion 7
        nodes7 = []
        B1 = [0, k+1, k]
        B2 = [1, 2*(k+1)*(k+1), 2*(k+1)*k]
        nodes7.append(B1)
        nodes7.append(B2)
        
        for i in range(2, num_iterations):
            B_prev = nodes7[-1]
            B_prev2 = nodes7[-2]
            B_next = [2*(k+1)*B_prev[j] - B_prev2[j] for j in range(3)]
            nodes7.append(B_next)
        excep.append(nodes7)

    # Recursion 8
        nodes8 = []
        B1 = [0, k, k+1]
        B2 = [1, 2*k*k, 2*k*(k+1)]
        nodes8.append(B1)
        nodes8.append(B2)
        
        for i in range(2, num_iterations):
            B_prev = nodes8[-1]
            B_prev2 = nodes8[-2]
            B_next = [2*k*B_prev[j] - B_prev2[j] for j in range(3)]
            nodes8.append(B_next)
        excep.append(nodes8)
    
    return excep




BL = np.array([0, 0])                              # (0,0,1)
TOP = np.array([0.5, math.sqrt(3) / 2])            # (0,1,0)
BR = np.array([1, 0])                              # (1,0,0)

def bary_to_cart(triple):
    A_w, B_w, C_w = triple
    S = A_w + B_w + C_w
    if S == 0:
        return np.array([0, 0])
    return (A_w * BR + B_w * TOP + C_w * BL) / S

def renormalize(triple):
    s = sum(triple)
    if s == 0:
        return triple[:]
    return [x/s for x in triple]

def func1(points):
    return [[2 * B - A, B, C] for (A, B, C) in points]

def func2(points):
    return [[A, 2 * A + 2 * C - B, C] for (A, B, C) in points]

def func3(points):
    return [[A, B, 2 * B - C] for (A, B, C) in points]

digit_actions = {'1': func1, '2': func2, '3': func3}

def arrow_symbol(mode="updown"):
    if mode == "up":
        return "$\\begin{matrix} \\uparrow \\\\ \\uparrow\\end{matrix}$"
    elif mode == "down":
        return "$\\begin{matrix} \\downarrow \\\\ \\downarrow\\end{matrix}$"
    elif mode == "updown":
        return "$\\begin{matrix} \\uparrow \\\\ \\downarrow\\end{matrix}$"
    elif mode == "downup":
        return "$\\begin{matrix} \\downarrow \\\\ \\uparrow\\end{matrix}$"

# Reflected Lines
def base_lines(m):
    lines = []
    for k in range(m):
        # Family 1+2
        disc1 = k**2 - 1
        if disc1 >= 0:
            sqrt_disc1 = np.sqrt(disc1)
            x1 = k - sqrt_disc1
            x2 = k + sqrt_disc1
            lines.append((np.array([(k+1)*x1, k*x1, 1.0]), 
                          np.array([(k+1)*x2, k*x2, 1.0]), k))
            lines.append((np.array([1.0, k*x1, (k+1)*x1]),
                          np.array([1.0, k*x2, (k+1)*x2]), k))

        # Family 3+4
        disc2 = (k+1)**2 - 1
        if disc2 >= 0:
            sqrt_disc2 = np.sqrt(disc2)
            x1 = k+1 - sqrt_disc2
            x2 = k+1 + sqrt_disc2
            lines.append((np.array([k*x1, (k+1)*x1, 1.0]),
                          np.array([k*x2, (k+1)*x2, 1.0]), k))
            lines.append((np.array([1.0, (k+1)*x1, k*x1]),
                          np.array([1.0, (k+1)*x2, k*x2]), k))
    return lines



def bary_line(p1, p2, n=200):
    return [renormalize((1-t)*p1 + t*p2) for t in np.linspace(0, 1, n)]

def apply_sequence(point, sequence):
    current = [point]
    for digit in sequence:
        action = digit_actions[digit]
        current = action(current)
    return current[0]

def matching_steps(sequence: str) -> list[int]:
    steps = []

    # Check start
    if sequence.startswith("13") or sequence.startswith("31"):
        steps.append(2)  # after first two digits

    # Check all 3-length windows
    for i in range(2, len(sequence)):
        window = sequence[i-2:i+1]  # three digits ending at position i
        if window in {"123","321","121","323"}:
            steps.append(i+1)  # +1 because we want 1-based length

    return steps



def plot_line_steps(fig, sequence, line_pts, k=None, color="rgba(160,32,240,0.3)"):

    steps = matching_steps(sequence)

    for step in steps:
        # Apply only the first 'step' digits of the sequence
        seq_partial = sequence[:step]
        line_transformed = [apply_sequence(pt, seq_partial) for pt in line_pts]
        line_cart = np.array([bary_to_cart(pt) for pt in line_transformed])

        # Plot the line
        fig.add_trace(go.Scatter(
            x=line_cart[:, 0],
            y=line_cart[:, 1],
            mode="lines",
            line=dict(color=color, width=2),
            name=f"Line k={k}, step={step}",
            showlegend=False,
            hoverinfo="text",
            text=[f"Total Reflections: {step}, k={k}"]
        ))

       





# --------------------
# Layout
# --------------------

col1,col2,col3 = st.columns([1,1,1])
with col1:
    col1_1,col1_2,col1_3,col1_4 = st.columns([4,1,6,6])
    with col1_1:
        use_color = st.checkbox("Color", value=True, key="color_toggle")
    with col1_2:
        if use_color:
            show_wrong = st.checkbox("", value = True)
    with col1_3:
        if use_color:
            st.write("\n")
            st.write("<b><span style='color:rgb(180, 0, 0)'>Wrong Quiver</span></b>", unsafe_allow_html=True)
    with col1_4:
        if use_color:
            st.write("\n")
            st.write("<b><span style='color:#228b22'>Correct Quiver</span></b>", unsafe_allow_html=True)

with col2:
    checkbox1_col, checkbox2_col, checkbox3_col = st.columns([1,1,1])
    with checkbox1_col:
        use_arrows = st.checkbox("Quivers", value=True, key="arrows_toggle")
    with checkbox2_col:
        show_polygons = st.checkbox("Polygons", value=True, key="polygons_toggle")
    with checkbox3_col:
        show_lines = st.checkbox("Lines", value=True, key="lines_toggle")
    
with col3:
    checkbox4_col, checkbox5_col, checkbox6_col = st.columns([1,1,1])
    with checkbox4_col:
        show_one_simplex = st.checkbox("Simplex for all Sequences", value=False, key="one_simplex_toggle")
    with checkbox5_col:
        show_refl_triangles = st.checkbox("Reflected Fundamental Domain", value=False, key="refl_triangles_toggle")
    with checkbox6_col:
        show_refl_lines = st.checkbox("Reflected Lines", value=False, key="refl_lines_toggle")

# Number of Lines
if show_lines:
    m = st.number_input("Number of Lines", min_value=0, value=10, step=1)
    o = st.number_input("Number of Exceptional Sequences", min_value=0, value=10, step=1)
    l = st.number_input("Depth of Exceptional Sequences", min_value=0, value=4, step=1)

# --------------------
# Mehrere Sequenzen parallel
# --------------------

cols = st.columns(len(sequences)) 
nodes_cor = []
all_nodes_global = []        # all barycentric nodes across all sequences
all_polygons_global = []     # polygons from each step
all_correct_nodes = []       # correct quiver nodes
all_wrong_nodes = []         # wrong quiver nodes

for idx, (col, sequence) in enumerate(zip(cols, sequences)):
    uid = f"seq{idx}"
    with col:
        if show_one_simplex == False:
            st.subheader(f"Simplex Diagram ({sequence})")

        # Kopie der Startdaten für jede Sequenz
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
              

        
                for idx, (A,B,C) in enumerate(DimVecs, 1):
                    cart = bary_to_cart((A,B,C))
                    all_nodes.append((cart, (A,B,C)))
                    text2 = f"&nbsp;&nbsp;&nbsp;&nbsp;P{idx}: ({A}, {B}, {C})"
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

        # helper: analytic conversion + ellipse construction
        def compute_conic_cart_points_analytic(n_theta=3000, keep_in_simplex=True, tol=1e-12, fallback_n_samples=4000):
            # M,t map u=[a,b] -> [a,b,c] = M u + t with c = 1-a-b
            M = np.array([[1.0, 0.0],
                        [0.0, 1.0],
                        [-1.0,-1.0]])
            t = np.array([0.0, 0.0, 1.0])

            # coefficients in u=(a,b)
            A_u = M.T @ Q @ M         # 2x2
            b_u = 2.0 * (M.T @ Q @ t) # 2x1
            c0  = float(t.T @ Q @ t)  # scalar

            # P maps u -> Cartesian y = x - BL : x = BL + P u
            P = np.column_stack([BR - BL, TOP - BL])   # 2x2
            try:
                Pinv = np.linalg.inv(P)
            except np.linalg.LinAlgError:
                # degenerate simplex (should not happen), fallback to sampling
                return _compute_conic_points_sample(fallback_n_samples, keep_in_simplex, tol)

            # Quadratic in y = x - BL: y^T A_cart y + b_cart^T y + c0 = 0
            A_cart = Pinv.T @ A_u @ Pinv
            b_cart = Pinv.T @ b_u.reshape(2,1)   # column vector
            c_cart = c0

            # try to get center y0 solving 2 A_cart y0 + b_cart = 0
            try:
                y0 = -0.5 * np.linalg.solve(A_cart, b_cart).reshape(2)
            except np.linalg.LinAlgError:
                # nearly singular: fallback to dense sampling
                return _compute_conic_points_sample(fallback_n_samples, keep_in_simplex, tol)

            # value at center
            F_c = float(y0 @ (A_cart @ y0) + (b_cart.ravel() @ y0) + c_cart)

            # check ellipse condition: A_cart positive definite and F_c < 0 -> real axes
            eigvals, eigvecs = np.linalg.eigh(A_cart)
            if np.any(eigvals <= 0) or F_c >= 0:
                # not a proper ellipse in this chart -> fallback to dense sampling
                return _compute_conic_points_sample(fallback_n_samples, keep_in_simplex, tol)

            # axis lengths and parametric points
            axes = np.sqrt((-F_c) / eigvals)  # lengths along eigenvectors
            center = BL + y0  # convert y0 back to absolute cartesian center

            thetas = np.linspace(0, 2 * np.pi, n_theta, endpoint=True)
            pts = np.array([center + (eigvecs @ (axes * np.array([np.cos(t), np.sin(t)]))) for t in thetas])

            if keep_in_simplex:
                # keep only points with bary coords >= -tol
                upts = (Pinv @ (pts.T - BL.reshape(2,1))).T  # shape (N,2)
                a_vals = upts[:,0]; b_vals = upts[:,1]; c_vals = 1.0 - a_vals - b_vals
                mask = (a_vals >= -tol) & (b_vals >= -tol) & (c_vals >= -tol)
                pts = pts[mask]
                if pts.shape[0] > 0 and not np.allclose(pts[0], pts[-1]):
                    pts = np.vstack([pts, pts[0]])
            return pts

        # fallback sampling routine with tighter tolerances
        def _compute_conic_points_sample(n_samples, keep_in_simplex, tol):
            a_min, a_max = -0.2, 1.2  # widen if you want more of the conic
            pts = []
            a_vals = np.linspace(a_min, a_max, n_samples)
            for a in a_vals:
                # quadratic in b after substituting c = 1-a-b
                A = 4.0
                B = 2.0 * a - 4.0
                C = 2.0 * a * a - 2.0 * a + 1.0
                disc = B*B - 4.0*A*C
                if disc < -1e-12:
                    continue
                disc = max(disc, 0.0)
                sqrt_disc = math.sqrt(disc)
                for b in [(-B + sqrt_disc)/(2*A), (-B - sqrt_disc)/(2*A)]:
                    c = 1.0 - a - b
                    if keep_in_simplex and (a < -tol or b < -tol or c < -tol):
                        continue
                    cart = bary_to_cart(renormalize((a,b,c)))
                    pts.append(cart)
            if not pts:
                return np.empty((0,2))
            pts = np.array(pts)
            # sort so trace looks nice
            center = pts.mean(axis=0)
            ang = np.arctan2(pts[:,1]-center[1], pts[:,0]-center[0])
            pts = pts[np.argsort(ang)]
            pts = np.vstack([pts, pts[0]])
            return pts



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
                                mode="lines", line=dict(color="black", width=2), name="Triangle", showlegend=False, hoverinfo="skip"))

        # Ellipse Plot
        ellipse_cart = compute_conic_cart_points_analytic(n_theta=1200, keep_in_simplex=True, tol=1e-12)
        if ellipse_cart.size > 0:
            fig.add_trace(go.Scatter(x=ellipse_cart[:,0], y=ellipse_cart[:,1],
                                    mode="lines", line=dict(color="black", width=2),
                                    name="Conic (analytic)", showlegend=False, hoverinfo="skip"))


        # Reflected Fundamental Domain
        def triangles_from_special_subsequences(base_triangle, sequence):
            """
            Generate triangles only at specific subsequences:
            - Start '13' or '31'
            - Any subsequence '123', '321', '121', '323'
            """
            triangles = []
            current = base_triangle[:]

            # Step through sequence, applying transformations
            for i, digit in enumerate(sequence):
                action = digit_actions[digit]
                current = action(current)

                # Check the prefix/subsequence
                prefix2 = sequence[:i+1]
                if prefix2.startswith("13") or prefix2.startswith("31"):
                    if len(prefix2) == 2:  # only at the very start
                        triangles.append((i+1, current))

                if i >= 2:  # check 3-length substrings ending here
                    window = sequence[i-2:i+1]
                    if window in {"123","321","121","323"}:
                        triangles.append((i+1, current))

            return triangles  # list of (step_index, triangle)

        def add_triangle(fig, bary_points, color="rgba(50,150,250,0.4)", line_color=f"rgba(0,150,200, 0.3)"):
            cart_points = [bary_to_cart(renormalize(pt)) for pt in bary_points]
            cart_points.append(cart_points[0])  # close loop
            fig.add_trace(go.Scatter(
                x=[p[0] for p in cart_points],
                y=[p[1] for p in cart_points],
                mode="lines",
                fill="toself",
                fillcolor=color,
                line=dict(color=line_color, width=2),
                showlegend=False,
                hoverinfo="skip"
            ))
        def apply_sequence_to_triangle(triangle, sequence):
            triangles = [triangle]  # include starting triangle
            current = triangle[:]
            for digit in sequence:
                action = digit_actions[digit]
                current = action(current)   # transform all 3 vertices
                triangles.append(current)
            return triangles

        triangles = []
        DimVecs_tmp = []  # start fresh
        for i in range(13):
            # choose a digit (cycle through "123")
            digit = str((i % 3) + 1)
            DimVecs_tmp = digit_actions[digit](DimVecs_tmp)

            if len(DimVecs_tmp) >= 3:
                tri = DimVecs_tmp[:3]
                triangles.append(tri)



        # Lines from Simples
        def add_line(fig, bary1, bary2, color="rgba(0,0,0,0.4)", width=2):
            p1, p2 = bary_to_cart(bary1), bary_to_cart(bary2)
            fig.add_trace(go.Scatter(
                x=[p1[0], p2[0]],
                y=[p1[1], p2[1]],
                mode="lines",
                line=dict(color=color, width=width),
                showlegend=False,
                hoverinfo="skip"
            ))

        def step_size(k):
            if k < 20:
                return 1   # every line
            elif k < 40:
                return 2   # every 2nd line
            elif k < 60:
                return 5   # every 5th line
            elif k < 80:
                return 10  # every 10th line
            else:
                return 20  

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
                marker=dict(color="rgba(0,0,0,0.4)", size=4),
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
                                    marker=dict(color="rgb(180, 0, 0)", size=6), name="Wrong Quiver", legendgroup="wrong", showlegend=True, 
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
                                marker=dict(color="green", size=6), name="Correct Quiver", legendgroup="correct",showlegend=True, 
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
            st.plotly_chart(fig, use_container_width=False, width=200, key=f"plotly_{uid}")



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
    mode="lines", line=dict(color="black", width=2),
    name="Triangle", showlegend=False, hoverinfo="skip"
))

# Reflected Fundamental Domain
if show_refl_triangles == True:
    base_triangle = [(0,1,1), (1,1,1), (1,1,0)]

    for seq in sequences:
        special_tris = triangles_from_special_subsequences(base_triangle, seq)

        for step, tri in special_tris:
            # give each sequence its own color
            color = f"rgba(0,150,200, 0.3)"
            add_triangle(fig, tri, color=color)

            # draw corner nodes
            cart = [bary_to_cart(renormalize(pt)) for pt in tri]
            fig.add_trace(go.Scatter(
                x=[p[0] for p in cart],
                y=[p[1] for p in cart],
                mode="markers",
                marker=dict(size=6, color=f"rgba(0,150,200, 0.3)"),
                text=[f"{pt}" for pt in tri],
                textposition="top center",
                name=f"{seq} step {step}",
                showlegend=False,
                hoverinfo="text"
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
        name="Wrong Quiver", legendgroup="wrong", showlegend=True,
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
        name="Correct Quiver", legendgroup="correct", showlegend=True,
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
    name="Given Nodes", legendgroup="given", showlegend=True,
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
    st.plotly_chart(fig, use_container_width=False, key="plotly_combined")


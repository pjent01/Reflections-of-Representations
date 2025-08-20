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
DimVecs_base = [[int(x) for x in line.split()] for line in dimvecs_str.strip().splitlines()]
Given_base = [tuple(pt) for pt in DimVecs_base]

# mehrere Sequenzen möglich
sequences_str = st.text_area("Enter sequences of reflections", "121323\n123\n321", height=145)
sequences = [seq.strip() for seq in sequences_str.split() if seq.strip()]

n = st.number_input("Number of iterations of the sequences", min_value=0, value=3, step=1)
n = int(n)+1

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

# --------------------
# Layout
# --------------------

col1,col2,col3 = st.columns([1,1,1])
with col2:
    checkbox1_col, checkbox2_col, checkbox3_col = st.columns([1,1,1])
    with checkbox1_col:
        use_color = st.checkbox("Color", value=False, key="color_toggle")
    with checkbox2_col:
        use_arrows = st.checkbox("Quivers", value=True, key="arrows_toggle")
    with checkbox3_col:
        show_polygons = st.checkbox("Polygons", value=True, key="polygons_toggle")

# --------------------
# Mehrere Sequenzen parallel
# --------------------
cols = st.columns(len(sequences)) 

for col, sequence in zip(cols, sequences):
    with col:
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

                    # Quiver Reflections (unverändert)
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
                    line_color = "black"
                elif q == [0,1]:
                    arrow = arrow_symbol("updown") if use_arrows else ""
                    line_color = "red" if use_color else "black"
                elif q == [1,0]:
                    arrow = arrow_symbol("downup") if use_arrows else ""
                    line_color = "red" if use_color else "black"
                elif q == [0,0]:
                    arrow = arrow_symbol("up") if use_arrows else ""
                    line_color = "black"

                output.append(f"<span style='color:{line_color}'>{arrow}  Reflection: {' '.join([f'{d}' for d in digits])}</span>")

                for idx, (A,B,C) in enumerate(DimVecs, 1):
                    cart = bary_to_cart((A,B,C))
                    all_nodes.append((cart, (A,B,C)))
                    output.append(f"<span style='color:{line_color}'>&nbsp;&nbsp;&nbsp;&nbsp;P{idx}: ({A}, {B}, {C})</span>")

        # --------------------
        # Zusätzliche Geometrie: Dreieck und Ellipse (wie ursprünglich)
        # --------------------
        extra_triangle_bary = [(0,1,1),(1,1,0),(1,1,1)]
        extra_triangle_cart = [bary_to_cart(p) for p in extra_triangle_bary] + [bary_to_cart(extra_triangle_bary[0])]

        ellipse_points_bary = [(0,1,1),(1,1,0),(1,1,2),(2,1,1),(1,5,2)]
        ellipse_points_cart = np.array([bary_to_cart(p) for p in ellipse_points_bary])

        X, Y = [], []
        for (x, y) in ellipse_points_cart:
            X.append([x**2, x*y, y**2, x, y])
            Y.append(-1.0)
        X = np.array(X); Y = np.array(Y)
        A, B, Cc, D, E = np.linalg.solve(X, Y); F_const = 1.0
        M = np.array([[A, B/2],[B/2, Cc]])
        center = np.linalg.solve(-2*M, [D, E])
        F_c = F_const + np.dot(center, np.dot(M, center)) + D*center[0] + E*center[1]
        eigvals, eigvecs = np.linalg.eigh(M)
        axes_lengths = np.sqrt(-F_c / eigvals)
        theta = np.linspace(0, 2*np.pi, 400)
        ellipse_cart = np.array([center + eigvecs @ (axes_lengths * np.array([np.cos(t), np.sin(t)])) for t in theta])

        # --------------------
        # Plotly figure (wie ursprünglich)
        # --------------------
        fig = go.Figure()

        # Simplex
        simplex_cart = [BL, TOP, BR, BL]
        fig.add_trace(go.Scatter(x=[p[0] for p in simplex_cart], y=[p[1] for p in simplex_cart],
                                mode="lines", line=dict(color="black", width=3),
                                fill="toself", fillcolor="rgba(230,230,230,0.2)", name="Simplex", showlegend=False, hoverinfo="skip"))

        # Fundamental Domain
        fig.add_trace(go.Scatter(x=[p[0] for p in extra_triangle_cart], y=[p[1] for p in extra_triangle_cart],
                                mode="lines", line=dict(color="green", width=2), name="Triangle", showlegend=False, hoverinfo="skip"))

        # Ellipse
        fig.add_trace(go.Scatter(x=ellipse_cart[:, 0], y=ellipse_cart[:, 1],
                                mode="lines", line=dict(color="blue", width=2), name="Ellipse", showlegend=False, hoverinfo="skip"))

        if use_arrows:
            # Red nodes: wrong1 + wrong2
            wrong_nodes = wrong1 + wrong2
            fig.add_trace(go.Scatter(x=[bary_to_cart(renormalize(pt))[0] for node in wrong_nodes for pt in node],
                                y=[bary_to_cart(renormalize(pt))[1] for node in wrong_nodes for pt in node],
                                mode="markers", 
                                marker=dict(color="red", size=6), name="Wrong Quiver", legendgroup="wrong", showlegend=True, 
                                text=[str(pt) for node in wrong_nodes for pt in node], hoverinfo="text"))
            fig.add_trace(go.Scatter(x=[bary_to_cart(renormalize(pt))[0] for node in wrong_nodes for pt in node],
                                y=[bary_to_cart(renormalize(pt))[1] for node in wrong_nodes for pt in node],
                                mode="text", text=[str(pt) for node in wrong_nodes for pt in node], showlegend=False,
                                textposition="top center", legendgroup="Labels", visible="legendonly", hoverinfo="skip"))

            # Green nodes: correct1 + correct2
            correct_nodes = correct1 + correct2
            fig.add_trace(go.Scatter(x=[bary_to_cart(renormalize(pt))[0] for node in correct_nodes for pt in node],
                                y=[bary_to_cart(renormalize(pt))[1] for node in correct_nodes for pt in node],
                                mode="markers", 
                                marker=dict(color="green", size=6), name="Correct Quiver", legendgroup="correct",showlegend=True, 
                                text=[str(pt) for node in correct_nodes for pt in node], hoverinfo="text"))
            fig.add_trace(go.Scatter(x=[bary_to_cart(renormalize(pt))[0] for node in correct_nodes for pt in node],
                                y=[bary_to_cart(renormalize(pt))[1] for node in correct_nodes for pt in node],
                                mode="text", text=[str(pt) for node in correct_nodes for pt in node], legendrank=3,
                                textposition="top center", legendgroup="Labels", name="Labels", visible="legendonly", hoverinfo="skip"))

        else:
            # Reflected Dimension Vectors
            fig.add_trace(go.Scatter(x=[cart[0] for cart, bary in all_nodes],
                                y=[cart[1] for cart, bary in all_nodes],
                                mode="markers", 
                                marker=dict(color="purple", size=6), name="Nodes", showlegend=False, 
                                text=[str(bary) for cart, bary in all_nodes], hoverinfo="text"))
            fig.add_trace(go.Scatter(x=[cart[0] for cart, bary in all_nodes],
                                y=[cart[1] for cart, bary in all_nodes],
                                mode="text", text=[str(bary) for cart, bary in all_nodes], 
                                textposition="top center", legendgroup="Labels", name="Labels", visible="legendonly", hoverinfo="skip"))

        # Optional: Polygone verbinden (NEU – ohne das bisherige Verhalten zu ändern)
        if show_polygons:
            legend_shown = {"wrong": False, "correct": False, "neutral": False}

            # Polygon aus den Given-Vektoren (Iteration 0)
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
                    color, group = "red", "wrong"
                elif kind == "correct":
                    color, group = "green", "correct"
                else:
                    color, group = "gray", "neutral"

                if not use_arrows:
                    color = "purple"

                # Polygon traces are part of the group but do NOT appear in the legend
                fig.add_trace(go.Scatter(
                    x=[p[0] for p in nodes_iter] + [nodes_iter[0][0]],
                    y=[p[1] for p in nodes_iter] + [nodes_iter[0][1]],
                    mode="lines",
                    line=dict(color=color, width=2),
                    name="",  # name is irrelevant since showlegend=False
                    legendgroup=group,  # matches quiver traces
                    showlegend=False,   # hide from legend
                    hoverinfo="skip"
                ))



        # Given Dimension Vectors (wie ursprünglich)
        Given_cart = [bary_to_cart(pt) for pt in Given]
        fig.add_trace(go.Scatter(x=[p[0] for p in Given_cart],
                                y=[p[1] for p in Given_cart],
                                mode="markers", 
                                marker=dict(color="blue", size=6), name="Nodes", showlegend=False, 
                                text=[str(pt) for pt in Given], hoverinfo="text"))
        fig.add_trace(go.Scatter(x=[p[0] for p in Given_cart],
                                y=[p[1] for p in Given_cart],
                                mode="text", text=[str(pt) for pt in Given], 
                                textposition="top center", legendgroup="Labels", name="Labels",visible="legendonly", hoverinfo="skip", showlegend=False))

        # Simple Dimension Vectors
        fig.add_trace(go.Scatter(x=[BL[0]], y=[BL[1]-0.02],
                                mode="text", text="(0,0,1)", 
                                textposition="bottom center", hoverinfo="skip", showlegend=False))
        fig.add_trace(go.Scatter(x=[BR[0]], y=[BR[1]-0.02],
                                mode="text", text="(1,0,0)", 
                                textposition="bottom center", hoverinfo="skip", showlegend=False))
        fig.add_trace(go.Scatter(x=[TOP[0]], y=[TOP[1]+0.01],
                                mode="text", text="(0,1,0)", 
                                textposition="top center", hoverinfo="skip", showlegend=False))

        # Figure Layout
        fig.update_layout(width=500, height=500, 
                        xaxis=dict(scaleanchor="y", showgrid=False, zeroline=False, showticklabels=False, title=None),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, title=None),
                        margin=dict(l=0, r=80, t=0, b=0),
                        showlegend=True,
                        legend=dict(x=0.95,y=0.8),
                        autosize=True
                        )

        st.plotly_chart(fig, use_container_width=False, width=200)


        st.subheader(f"Reflections ({sequence})")
        st.markdown("  <br>  ".join(output), unsafe_allow_html=True)

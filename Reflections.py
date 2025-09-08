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

# mehrere Sequenzen
sequences_str = st.text_area("Enter sequences of reflections", "121323\n123123\n321321", height=145)
sequences = [seq.strip() for seq in sequences_str.split() if seq.strip()]

n = st.number_input("Number of iterations of the sequences", min_value=0, value=3, step=1)
n = int(n)+1

# Exceptionals
def gen_excep(n, num_iterations):
    excep = []

    for k in range(n):
        nodes = []
        B1 = [k+1, k, 2*k]
        B2 = [2*k*(k+1), 2*k*k, 2*k*(2*k)-1]
        nodes.append(B1)
        nodes.append(B2)
        
        # Recursion for further nodes
        for i in range(2, num_iterations):
            B_prev = nodes[-1]
            B_prev2 = nodes[-2]
            B_next = [2*k*B_prev[j] - B_prev2[j] for j in range(3)]
            nodes.append(B_next)
        
        excep.append(nodes)
        # -----------------------
        # Family 1: B1 = (k, k+1, 2*(k+1))
        # -----------------------
        nodes1 = []
        B1 = [k, k+1, 2*(k+1)]
        B2 = [2*(k+1)*B1[i] - v for i, v in enumerate([0,0,1])]
        nodes1.append(B1)
        nodes1.append(B2)
        for i in range(2, num_iterations):
            B_prev = nodes1[-1]
            B_prev2 = nodes1[-2]
            B_next = [2*(k+1)*B_prev[j] - B_prev2[j] for j in range(3)]
            nodes1.append(B_next)
        excep.append(nodes1)

        # -----------------------
        # Family 2: B1 = (2*k, k, k+1)
        # -----------------------
        nodes2 = []
        B1 = [2*k, k, k+1]
        B2 = [2*k*B1[i] - v for i, v in enumerate([1,0,0])]
        nodes2.append(B1)
        nodes2.append(B2)
        for i in range(2, num_iterations):
            B_prev = nodes2[-1]
            B_prev2 = nodes2[-2]
            B_next = [2*k*B_prev[j] - B_prev2[j] for j in range(3)]
            nodes2.append(B_next)
        excep.append(nodes2)

        # -----------------------
        # Family 3: B1 = (2*(k+1), k+1, k)
        # -----------------------
        nodes3 = []
        B1 = [2*(k+1), k+1, k]
        B2 = [2*(k+1)*B1[i] - v for i, v in enumerate([1,0,0])]
        nodes3.append(B1)
        nodes3.append(B2)
        for i in range(2, num_iterations):
            B_prev = nodes3[-1]
            B_prev2 = nodes3[-2]
            B_next = [2*(k+1)*B_prev[j] - B_prev2[j] for j in range(3)]
            nodes3.append(B_next)
        excep.append(nodes3)

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
            B_next = [2*k*B_prev[j] - B_prev2[j] for j in range(3)]
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
            B_next = [2*k*B_prev[j] - B_prev2[j] for j in range(3)]
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

# --------------------
# Layout
# --------------------

col1,col2,col3 = st.columns([1,1,1])
with col1:
    col1_1,col1_2,col1_3,col1_4 = st.columns([2,1,3,3])
    with col1_1:
        use_color = st.checkbox("Color", value=True, key="color_toggle")
    with col1_2:
        if use_color:
            show_wrong = st.checkbox("", value = True)
    with col1_3:
        if use_color:
            #st.write("\n")
            st.write("<b><span style='color:rgb(180, 0, 0)'>Wrong Quiver</span></b>", unsafe_allow_html=True)
    with col1_4:
        if use_color:
            #st.write("\n")
            st.write("<b><span style='color:#228b22'>Correct Quiver</span></b>", unsafe_allow_html=True)

with col2:
    checkbox1_col, checkbox2_col, checkbox3_col = st.columns([1,1,1])
    with checkbox1_col:
        use_arrows = st.checkbox("Quivers", value=True, key="arrows_toggle")
    with checkbox2_col:
        show_polygons = st.checkbox("Polygons", value=True, key="polygons_toggle")
    with checkbox3_col:
        show_lines = st.checkbox("Lines", value=True, key="lines_toggle")

# Number of Lines
if show_lines:
    m = st.number_input("Number of Lines", min_value=0, value=100, step=1)
    o = st.number_input("Number of Exceptional Sequences", min_value=0, value=10, step=1)
    l = st.number_input("Depth of Exceptional Sequences", min_value=0, value=4, step=1)

# --------------------
# Mehrere Sequenzen parallel
# --------------------

cols = st.columns(len(sequences)) 
nodes_cor = []

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

        # Ellipse
        fig.add_trace(go.Scatter(x=ellipse_cart[:, 0], y=ellipse_cart[:, 1],
                                mode="lines", line=dict(color="black", width=2), name="Ellipse", showlegend=False, hoverinfo="skip"))

        # Lines from Simples
        def add_line(fig, bary1, bary2, color="rgba(0,0,0,0.6)", width=2):
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
                marker=dict(color="black", size=6),
                text=[str(pt) for pt in excep],
                textposition="top center",
                name="Exceptionals",
                showlegend=False,
                hoverinfo="text"))
            fig.add_trace(go.Scatter(x=[p[0] for p in excep_cart],
                y=[p[1] for p in excep_cart],
                mode="text", text=[str(pt) for pt in excep], showlegend=False,
                textposition="top center", legendgroup="Labels", visible="legendonly", hoverinfo="skip"))

        if use_color:
            # Red nodes: wrong1 + wrong2
            if show_wrong:
                wrong_nodes = wrong1 + wrong2
                fig.add_trace(go.Scatter(x=[bary_to_cart(renormalize(pt))[0] for node in wrong_nodes for pt in node],
                                    y=[bary_to_cart(renormalize(pt))[1] for node in wrong_nodes for pt in node],
                                    mode="markers", 
                                    marker=dict(color="rgb(180, 0, 0)", size=6), name="Wrong Quiver", legendgroup="wrong", showlegend=True, 
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
                                marker=dict(color="rgb(0,120,150)", size=6), name="Nodes", showlegend=False, 
                                text=[str(bary) for cart, bary in all_nodes], hoverinfo="text"))
            fig.add_trace(go.Scatter(x=[cart[0] for cart, bary in all_nodes],
                                y=[cart[1] for cart, bary in all_nodes],
                                mode="text", text=[str(bary) for cart, bary in all_nodes], 
                                textposition="top center", legendgroup="Labels", name="Labels", visible="legendonly", hoverinfo="skip"))

        
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

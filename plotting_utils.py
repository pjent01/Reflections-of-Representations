from __future__ import annotations

import numpy as np
import plotly.graph_objects as go
from dataclasses import dataclass

import math_core as mc


def plot_reflected_line_steps(fig: go.Figure, sequence: str, line_pts: list[np.ndarray], k: int = None, color: str = "rgb(0,255,255)"):
    """ Plot the reflected lines for a given sequence and line segment in barycentric coordinates. The function applies the sequence of reflection functions to the endpoints of the line segment and adds the resulting transformed lines to the provided Plotly figure.
    
    Args:
        fig (go.Figure): A Plotly figure object to which the reflected lines will be added.
        sequence (str): A string of digits ('1', '2', '3') representing the sequence of reflection functions to apply.
        line_pts (list[np.ndarray]): A list containing two numpy arrays representing the endpoints of the line segment in barycentric coordinates.
        k (int, optional): An optional integer parameter that can be used to label the lines in the plot. Defaults to None.
        color (str, optional): A string representing the color of the lines in RGB format. Defaults to "rgb(0,255,255)".
    """
    steps = mc.matching_reflection_steps(sequence)

    for step in steps:
        seq_partial = sequence[:step]
        line_transformed = [mc.apply_sequence(pt, seq_partial) for pt in line_pts]
        line_cart = np.array([mc.bary_to_cart(pt) for pt in line_transformed])

        fig.add_trace(go.Scatter(
            x=line_cart[:, 0],
            y=line_cart[:, 1],
            mode="lines",
            line=dict(color="rgb(0,100,255)", width=2),
            showlegend=False,
            hoverinfo="skip",
        ))

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

# Ellipse and line geometry.


def add_line(fig: go.Figure, bary1: tuple, bary2: tuple, color: str ="rgba(0,0,0,0.4)", width: float = 1.0) -> None:
    """ Add a line segment between two points in barycentric coordinates inside the simplex.
    
    Args: 
        fig (go.Figure): A Plotly figure object to which the line segment will be added.
        bary1 (tuple): The first point in barycentric coordinates (A, B, C).
        bary2 (tuple): The second point in barycentric coordinates (A, B, C).
        color (str): The color of the line segment in RGBA format. Defaults to "rgba(0,0,0,0.4)".
        width (float): The width of the line segment. Defaults to 1.0.
    """
    p1, p2 = mc.bary_to_cart(bary1), mc.bary_to_cart(bary2)
    fig.add_trace(go.Scatter(
        x=[p1[0], p2[0]],
        y=[p1[1], p2[1]],
        mode="lines",
        line=dict(color=color, width=width),
        showlegend=False,
        hoverinfo="skip"
    ))


@dataclass
class SimplexFigureConfig:
    use_color: bool
    show_wrong: bool
    show_polygons: bool
    show_lines: bool
    figure_height: int
    line_limit: int
    show_reflected_lines: bool
    excep_number: int
    excep_depth: int
    highlight_excep: bool


@dataclass
class SimplexFigureStyle:
    wrong_marker: dict
    correct_marker: dict
    input_vector_marker: dict
    input_vector_name: str
    exceptional_marker: dict
    exceptional_highlight_marker: dict

    @classmethod
    def default(cls) -> "SimplexFigureStyle":
        """Create the default style preset for simplex figures."""
        return cls(
            wrong_marker=dict(color="rgb(255,0,0)", size=7, line=dict(color="rgb(100,0,0)", width=1)),
            correct_marker=dict(color="rgb(0,200,0)", size=7, line=dict(color="rgb(0,100,0)", width=1)),
            input_vector_marker=dict(color="rgb(0,150,255)", size=7, line=dict(color="rgb(0,50,255)", width=1)),
            input_vector_name="Given Nodes",
            exceptional_marker=dict(color="rgb(0,0,0)", size=2),
            exceptional_highlight_marker=dict(color="rgb(0,255,255)", size=7, line=dict(color="rgb(0,100,255)", width=1)),
        )

    def exceptional_marker_for(self, highlight: bool) -> dict:
        """Return the exceptional marker style for the selected highlight mode."""
        return self.exceptional_highlight_marker if highlight else self.exceptional_marker


def get_default_figure_style() -> SimplexFigureStyle:
    """Return the default style preset for simplex figures.

    Includes marker styles for:
    - Kronecker-chain nodes (green),
    - differently oriented quiver nodes (red),
    - input vector nodes (blue),
    - exceptional nodes (small and black, or highlighted in cyan).
    """
    return SimplexFigureStyle.default()


def compute_figure_height(show_one_simplex: bool, sequence_count: int) -> int:
    """Choose a figure height that scales down in multi-column mode."""
    if show_one_simplex or sequence_count <= 1:
        return 800
    if sequence_count == 2:
        return 600
    return max(320, min(800, 800 // (sequence_count)))


def build_simplex_figure(
    given_vectors: list[tuple[float, float, float]],
    sequences: list[str],
    node_records: list[tuple[np.ndarray, tuple[float, float, float]]],
    wrong_nodes: list[list[tuple[float, float, float]]],
    correct_nodes: list[list[tuple[float, float, float]]],
    polygon_steps: list[tuple[list[np.ndarray], str]],
    cfg: SimplexFigureConfig,
    style: SimplexFigureStyle,
) -> go.Figure:
    """Build a simplex figure. It includes the simplex, fundamental domain, ellipse, lines, reflected lines, nodes, and polygons based on the provided configuration and style."""
    fig = go.Figure()

    label_size = 14

    simplex_cart = [mc.BL, mc.TOP, mc.BR, mc.BL]
    fig.add_trace(go.Scatter(
        x=[p[0] for p in simplex_cart],
        y=[p[1] for p in simplex_cart],
        mode="lines",
        line=dict(color="black", width=3),
        fill="toself",
        fillcolor="rgba(230,230,230,0.2)",
        name="Simplex",
        showlegend=False,
        hoverinfo="skip",
    ))

    fund_dom_bary = [(0, 1, 1), (1, 1, 0), (1, 1, 1)]
    fund_dom_cart = [mc.bary_to_cart(p) for p in fund_dom_bary] + [mc.bary_to_cart(fund_dom_bary[0])]
    fig.add_trace(go.Scatter(
        x=[p[0] for p in fund_dom_cart],
        y=[p[1] for p in fund_dom_cart],
        mode="lines",
        line=dict(color="black", width=1),
        fill="toself",
        fillcolor="rgb(0, 255, 255)",
        name="Triangle",
        showlegend=False,
        hoverinfo="skip",
    ))

    ellipse_cart = mc.compute_conic_cart_points_analytic()
    if ellipse_cart.size > 0:
        fig.add_trace(go.Scatter(
            x=ellipse_cart[:, 0],
            y=ellipse_cart[:, 1],
            mode="lines",
            line=dict(color="black", width=2),
            name="Conic (analytic)",
            showlegend=False,
            hoverinfo="skip",
        ))

    if cfg.show_lines:
        if cfg.show_reflected_lines and sequences:
            all_lines = mc.base_lines(cfg.line_limit)
            for sequence in sequences:
                for p1, p2, k in all_lines:
                    plot_reflected_line_steps(fig, sequence, [p1, p2], k=k)

        k = 1
        while k < cfg.line_limit:
            add_line(fig, (0, 0, 1), (k + 1, k, 0))
            add_line(fig, (0, 0, 1), (k, k + 1, 0))
            k += mc.step_size(k)

        k = 1
        while k < cfg.line_limit:
            add_line(fig, (1, 0, 0), (0, k, k + 1))
            add_line(fig, (1, 0, 0), (0, k + 1, k))
            k += mc.step_size(k)

    excep_marker = style.exceptional_marker_for(cfg.highlight_excep)
    excep_t = mc.generate_exceptional_sequences(cfg.excep_number, cfg.excep_depth)
    excep = [node for nodes_k in excep_t for node in nodes_k]
    excep_cart = [mc.bary_to_cart(mc.renormalize(pt)) for pt in excep]
    fig.add_trace(go.Scatter(
        x=[p[0] for p in excep_cart],
        y=[p[1] for p in excep_cart],
        mode="markers",
        marker=excep_marker,
        text=[f"({a}, {b}, {c})" for (a, b, c) in excep],
        textposition="top center",
        name="Exceptionals",
        showlegend=False,
        hoverinfo="text",
    ))
    fig.add_trace(go.Scatter(
        x=[p[0] for p in excep_cart],
        y=[p[1] for p in excep_cart],
        mode="text",
        text=[f"({a}, {b}, {c})" for (a, b, c) in excep],
        showlegend=False,
        textposition="top center",
        textfont=dict(size=label_size),
        legendgroup="Labels",
        visible="legendonly",
        hoverinfo="skip",
    ))

    if cfg.use_color:
        if cfg.show_wrong:
            wrong_points = [mc.bary_to_cart(mc.renormalize(pt)) for node in wrong_nodes for pt in node]
            wrong_labels = [f"({a}, {b}, {c})" for node in wrong_nodes for (a, b, c) in node]
            fig.add_trace(go.Scatter(
                x=[p[0] for p in wrong_points],
                y=[p[1] for p in wrong_points],
                mode="markers",
                marker=style.wrong_marker,
                name="Different Orientation",
                legendgroup="wrong",
                showlegend=True,
                text=wrong_labels,
                hoverinfo="text",
            ))
            fig.add_trace(go.Scatter(
                x=[p[0] for p in wrong_points],
                y=[p[1] for p in wrong_points],
                mode="text",
                text=wrong_labels,
                showlegend=False,
                textposition="top center",
                textfont=dict(size=label_size),
                legendgroup="Labels",
                visible="legendonly",
                hoverinfo="skip",
            ))

        correct_points = [mc.bary_to_cart(mc.renormalize(pt)) for node in correct_nodes for pt in node]
        correct_labels = [f"({a}, {b}, {c})" for node in correct_nodes for (a, b, c) in node]
        fig.add_trace(go.Scatter(
            x=[p[0] for p in correct_points],
            y=[p[1] for p in correct_points],
            mode="markers",
            marker=style.correct_marker,
            name="Kronecker Chain",
            legendgroup="correct",
            showlegend=True,
            text=correct_labels,
            hoverinfo="text",
        ))
        fig.add_trace(go.Scatter(
            x=[p[0] for p in correct_points],
            y=[p[1] for p in correct_points],
            mode="text",
            text=correct_labels,
            textposition="top center",
            textfont=dict(size=label_size),
            legendgroup="Labels",
            name="Labels",
            visible="legendonly",
            hoverinfo="skip",
        ))
    else:
        node_positions = [(cart[0], cart[1]) for cart, _ in node_records]
        node_labels = [f"({a}, {b}, {c})" for _, (a, b, c) in node_records]
        fig.add_trace(go.Scatter(
            x=[x for x, _ in node_positions],
            y=[y for _, y in node_positions],
            mode="markers",
            marker=dict(color="rgb(90, 130, 150)", size=8, line=dict(color="rgb(60,85,100)", width=1)),
            name="Nodes",
            showlegend=False,
            text=node_labels,
            hoverinfo="text",
        ))
        fig.add_trace(go.Scatter(
            x=[x for x, _ in node_positions],
            y=[y for _, y in node_positions],
            mode="text",
            text=node_labels,
            textposition="top center",
            textfont=dict(size=label_size),
            legendgroup="Labels",
            name="Labels",
            visible="legendonly",
            hoverinfo="skip",
        ))

    if cfg.show_polygons:
        given_cart = [mc.bary_to_cart(pt) for pt in given_vectors]
        if len(given_cart) >= 3:
            fig.add_trace(go.Scatter(
                x=[p[0] for p in given_cart] + [given_cart[0][0]],
                y=[p[1] for p in given_cart] + [given_cart[0][1]],
                mode="lines",
                line=dict(color="rgb(0,50,255)", width=2, dash="dot"),
                name="Given Polygon",
                legendgroup="given",
                showlegend=False,
                hoverinfo="skip",
            ))

        kronecker_polygons = []
        for polygon_nodes, kind in polygon_steps:
            if len(polygon_nodes) < 3:
                continue

            if kind == "wrong":
                color, group = "rgb(255, 0, 0)", "wrong"
            elif kind == "correct":
                color, group = "rgb(0, 200, 0)", "correct"
                kronecker_polygons.append(polygon_nodes)
            else:
                color, group = "gray", "neutral"

            if not cfg.use_color:
                color = "rgb(0,120,150)"

            if cfg.show_wrong:
                fig.add_trace(go.Scatter(
                    x=[p[0] for p in polygon_nodes] + [polygon_nodes[0][0]],
                    y=[p[1] for p in polygon_nodes] + [polygon_nodes[0][1]],
                    mode="lines",
                    line=dict(color=color, width=2),
                    name="",
                    legendgroup=group,
                    showlegend=False,
                    hoverinfo="skip",
                ))
            else:
                for kronecker_nodes in kronecker_polygons:
                    fig.add_trace(go.Scatter(
                        x=[p[0] for p in kronecker_nodes] + [kronecker_nodes[0][0]],
                        y=[p[1] for p in kronecker_nodes] + [kronecker_nodes[0][1]],
                        mode="lines",
                        line=dict(color=color, width=2),
                        name="",
                        legendgroup=group,
                        showlegend=False,
                        hoverinfo="skip",
                    ))

    given_cart = [mc.bary_to_cart(pt) for pt in given_vectors]
    fig.add_trace(go.Scatter(
        x=[p[0] for p in given_cart],
        y=[p[1] for p in given_cart],
        mode="markers",
        marker=style.input_vector_marker,
        name=style.input_vector_name,
        showlegend=False,
        text=[f"({a}, {b}, {c})" for (a, b, c) in given_vectors],
        hovertemplate=f"{style.input_vector_name}<br>%{{text}}<extra></extra>",
    ))
    fig.add_trace(go.Scatter(
        x=[p[0] for p in given_cart],
        y=[p[1] for p in given_cart],
        mode="text",
        text=[f"({a}, {b}, {c})" for (a, b, c) in given_vectors],
        textposition="top center",
        textfont=dict(size=label_size),
        legendgroup="Labels",
        name="Labels",
        visible="legendonly",
        hoverinfo="skip",
        showlegend=False,
    ))

    fig.add_trace(go.Scatter(
        x=[mc.BL[0]],
        y=[mc.BL[1] - 0.02],
        mode="text",
        text="(0,0,1)",
        textposition="bottom center",
        textfont=dict(size=label_size),
        hoverinfo="skip",
        showlegend=False,
    ))
    fig.add_trace(go.Scatter(
        x=[mc.BR[0]],
        y=[mc.BR[1] - 0.02],
        mode="text",
        text="(1,0,0)",
        textposition="bottom center",
        textfont=dict(size=label_size),
        hoverinfo="skip",
        showlegend=False,
    ))
    fig.add_trace(go.Scatter(
        x=[mc.TOP[0]],
        y=[mc.TOP[1] + 0.01],
        mode="text",
        text="(0,1,0)",
        textposition="top center",
        textfont=dict(size=label_size),
        hoverinfo="skip",
        showlegend=False,
    ))

    fig.update_layout(
        height=cfg.figure_height,
        xaxis=dict(scaleanchor="y", showgrid=False, zeroline=False, showticklabels=False, title=None),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, title=None),
        margin=dict(l=0, r=80, t=0, b=0),
        showlegend=True,
        legend=dict(x=0.95, y=0.8),
        autosize=True,
    )
    return fig

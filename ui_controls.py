import streamlit as st
from dataclasses import dataclass
import plotting_utils as pu

@dataclass
class VisualizationOptions:
    use_color: bool
    show_polygons: bool
    show_lines: bool
    line_limit: int
    show_reflected_lines: bool
    use_arrows: bool


def parse_dimension_vectors(given_vectors_str: str) -> list[list[int | float]]:
    """Parse the dimension vector textarea input into vectors, split by line breaks. Integer-valued entries are converted to int."""
    if not given_vectors_str.strip():
        return []
    return [
        [
            int(val) if float(val).is_integer() else float(val)
            for val in line.split()
        ]
        for line in given_vectors_str.strip().splitlines()
    ]


def parse_sequences(sequences_str: str) -> list[str]:
    """Parse the sequences textarea input into sequence strings, split by line breaks or spaces."""
    return [seq.strip() for seq in sequences_str.split() if seq.strip()]


def get_visualization_options() -> VisualizationOptions:
    """Render visualization option controls and return their current values.

    Default values:
        - use_color=True 
        - show_polygons=False
        - show_lines=True,
        - line_limit=20 when lines are enabled (otherwise 0)
        - show_reflected_lines=False
        - use_arrows=True
    """
    with st.expander("Visualization Options", expanded=False):
        use_color = st.checkbox("Color", value=True, key="color_toggle")
        show_polygons = st.checkbox("Polygons", value=False, key="polygons_toggle")
        show_lines = st.checkbox("Lines", value=True, key="lines_toggle")
        line_limit = 0
        show_reflected_lines = False
        if show_lines:
            line_limit = st.number_input("Number of Lines", min_value=0, value=20, step=1)
            show_reflected_lines = st.checkbox("Reflected Lines", value=False, key="refl_lines_toggle")
    if "arrows_toggle" not in st.session_state:
        st.session_state.arrows_toggle = True
    use_arrows = st.session_state.arrows_toggle
    return VisualizationOptions(
        use_color=use_color,
        show_polygons=show_polygons,
        show_lines=show_lines,
        line_limit=line_limit,
        show_reflected_lines=show_reflected_lines,
        use_arrows=use_arrows,
    )


def get_exceptional_sequence_options() -> tuple[int, int, bool]:
    """Render exceptional sequence controls and return their current values.

    Returns a tuple in this order:
    - exceptional_count (default: 5)
    - exceptional_depth (default: 2)
    - highlight_exceptional (default: False)
    """
    with st.expander("Exceptional Sequences", expanded=False):
        exceptional_count = st.number_input("Number of Exceptional Sequences", min_value=0, value=5, step=1)
        exceptional_depth = st.number_input("Depth of Exceptional Sequences", min_value=0, value=2, step=1)
        highlight_exceptional = st.toggle("Highlight Exceptional Sequences", value=False, key="highlight_exceptional_toggle")
    return exceptional_count, exceptional_depth, highlight_exceptional


def should_render_output_line(line_color: str, show_wrong: bool) -> bool:
    """Return whether output lines with this color should be rendered."""
    return line_color != "rgb(180, 0, 0)" or show_wrong


def format_output_html(text: str, color: str, *, bold: bool = False, indent_level: int = 0) -> str:
    """Format one output row as HTML while preserving current visual spacing."""
    indent_unit = "&nbsp;&nbsp;&nbsp;&nbsp;&emsp;"
    body = f"{indent_unit * indent_level}{text}"
    if bold:
        body = f"<b>{body}</b>"
    return f"<span style='color:{color}'>{body}</span>"


def render_sequence_meta_block(
    *,
    sequence_index: int,
    use_color: bool,
    show_wrong: bool,
) -> None:
    """Render per-sequence legend/toggle row or spacing placeholders for alignment."""
    kronecker_and_toggle_extra_spacer_rem = 5.1
    different_orientation_extra_spacer_rem = 2.6
    toggle_extra_spacer_rem = 2.5
    if use_color and sequence_index == 0:
        st.markdown(
            "<span style='color:green; font-weight:600'>Kronecker Chain</span>",
            unsafe_allow_html=True,
        )
        if show_wrong:
            st.markdown(
                "<span style='color:rgb(180, 0, 0); font-weight:600'>Different Orientation</span>",
                unsafe_allow_html=True,
            )

    if sequence_index == 0:
        st.toggle("Show Quiver Orientation", key="arrows_toggle")
    elif use_color:
        st.markdown(
            f"<div style='height: {kronecker_and_toggle_extra_spacer_rem}rem;'></div>",
            unsafe_allow_html=True,
        )
        if show_wrong:
            st.markdown(
                f"<div style='height: {different_orientation_extra_spacer_rem}rem;'></div>",
                unsafe_allow_html=True,
            )
    else:
        st.markdown(
            f"<div style='height: {toggle_extra_spacer_rem}rem;'></div>",
            unsafe_allow_html=True,
        )


def arrow_symbol(mode: str = "updown"):
    """ Return a LaTeX string representing an arrow symbol based on the specified mode to depict the orientation of the underlying quiver.

    Args: 
        mode (str): The mode specifying the arrow orientation. It can be "up", "down", "updown", or "downup".
    
    Returns:
        str: A LaTeX string representing the arrow symbol corresponding to the specified mode.
    """
    if mode == "up":
        return "$\\begin{matrix}\\leftarrow\\ \\leftarrow \\\\[-7pt] \\leftarrow\\ \\leftarrow\\end{matrix}$"
    elif mode == "down":
        return "$\\begin{matrix}\\rightarrow\\ \\rightarrow \\\\[-7pt] \\rightarrow\\ \\rightarrow\\end{matrix}$"
    elif mode == "updown":
        return "$\\begin{matrix} \\leftarrow\\ \\rightarrow \\\\[-7pt] \\leftarrow\\ \\rightarrow\\end{matrix}$"
    elif mode == "downup":
        return "$\\begin{matrix} \\rightarrow\\ \\leftarrow \\\\[-7pt] \\rightarrow\\ \\leftarrow\\end{matrix}$"


import streamlit as st
from dataclasses import dataclass
import plotting_utils as pu

@dataclass
class UserInputs:
    DISPLAY_OPTIONS: str
    one_simplex_toggled: bool
    color_t: bool
    wrong_t: bool
    polygons_t: bool
    lines_t: bool
    line_limit_input: int
    reflected_lines_t: bool
    quiver_t: bool


def parse_dimension_vectors(given_vectors_str: str) -> list[list[int | float]]:
    """Parse the dimension vector textarea input into vectors, split by line breaks. Integer-valued entries are converted to int."""
    return [
        [int(val) if float(val).is_integer() else float(val) for val in line.split()]
        for line in given_vectors_str.strip().splitlines()
        if given_vectors_str.strip()
    ]

def parse_sequences(sequences_str: str) -> list[str]:
    """Parse the sequences textarea input into sequence strings, split by line breaks or spaces."""
    return [seq.strip() for seq in sequences_str.split() if seq.strip()]

def format_output_html(
    text: str, color: str, *, bold: bool = False, indent_level: int = 0
) -> str:
    """Format one output row as HTML while preserving current visual spacing."""
    indent_unit = "&nbsp;&nbsp;&nbsp;&nbsp;&emsp;"
    body = f"{indent_unit * indent_level}{text}"
    if bold:
        body = f"<b>{body}</b>"
    return f"<span style='color:{color}'>{body}</span>"

def arrow_symbol(mode: str = "updown"):
    """Return a LaTeX string representing an arrow symbol based on the specified mode to depict the orientation of the underlying quiver.

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


# User inputs
def vector_inputs() -> list[list[int | float]]:
    vectors_input = st.text_area(
        "Input three-dimensional dimension vectors. Dimensions are separated by spaces and vectors by line breaks.",
        "1 2 1\n0 1 0\n1 2 0\n0 2 1",
        height=135,
    )
    vectors_list = parse_dimension_vectors(vectors_input)
    return vectors_list

def sequence_inputs() -> list[str]:
    sequences_input = st.text_area(
        "Input sequences containing the digits 1, 2 or 3. Sequences are separated by space or line break.",
        "123123123\n321321321",
        height=50,
    )
    sequences_list = parse_sequences(sequences_input)
    return sequences_list

# UI controls
def display_user_inputs():
    DISPLAY_OPTIONS = st.caption("Display options")
    one_simplex_toggled = st.toggle(
        "One simplex for all sequences",
        value=False,
        key="one_simplex_toggled",
    )

    with st.expander("Visualization options", expanded=False, type="compact"):
        color_t = st.toggle("Color", value=True, key="color_t_toggle")
        wrong_t = st.toggle(
            "Show dimension vectors of differently oriented quivers (red, if Color is active)",
            value=True, key="wrong_t_toggle"
        )
        polygons_t = st.toggle("Connect vectors for each step", value=False, key="polygons_t_toggle")
        lines_t = st.toggle("Show lines between orthogonal vectors", value=True, key="lines_t_toggle")
        line_limit_input = 20
        reflected_lines_t = False
        if lines_t:
            line_limit_input = st.number_input(
                "Input how many lines should be generated (large inputs decrease performance)",
                value=20,
                key="line_limit_input",
            )
            reflected_lines_t = st.toggle(
                "Show lines reflected in each step of the sequences",
                value=False,
                key="reflected_lines_t_toggle",
            )
        quiver_t = st.toggle(
            "Show Quiver Orientation",
            value=True,
            key="quiver_t",
        )
    return UserInputs(
        DISPLAY_OPTIONS,
        one_simplex_toggled,
        color_t,
        wrong_t,
        polygons_t,
        lines_t,
        line_limit_input,
        reflected_lines_t,
        quiver_t
    )

# Exceptional sequences options
def exceptional_sequence_options():
    with st.expander("Exceptional sequences options", expanded=False, type="compact"):
        excep_number_input = st.number_input(
            "Input how many different exceptional sequences should be generated",
            value=5,
        )
        excep_depth_input = st.number_input(
            "Input how many exceptional vectors should be generated per exceptional sequence",
            value=2,
        )
        excep_highlight_t = st.toggle(
            "Highlight exceptional vectors (cyan)", value=False
        )
    return excep_number_input, excep_depth_input, excep_highlight_t

def output_colors() -> tuple[str, str]:
    if st.context.theme.type == "dark":
        return "rgb(255,70,70)", "#56d364"  # red, green
    else:
        return "rgb(180, 0, 0)", "Green"  # red, green
import numpy as np
from dataclasses import dataclass
import math_core as mc
import ui_controls as ui

@dataclass
class SequenceProcessResult:
    node_records: list[tuple[np.ndarray, tuple[float, float, float]]]
    wrong_nodes: list[list[tuple[float, float, float]]]
    correct_nodes: list[list[tuple[float, float, float]]]
    polygon_steps: list[tuple[list[np.ndarray], str]]
    output_lines: list[str]


def process_sequence(
    sequence: str,
    given_vectors_initial: list[list[int | float]],
    *,
    use_arrows: bool,
    use_color: bool,
    show_wrong: bool,
) -> SequenceProcessResult:
    """Process one reflection sequence and return rendering/output artifacts."""
    given_vectors_current = [v[:] for v in given_vectors_initial]

    digits = []
    nodes = []
    node_records = []
    output_lines = []

    q_state = (1, 1)
    correct_steps_by_state = {
        (1, 1): [],
        (0, 1): [],
        (1, 0): [],
        (0, 0): [],
    }
    wrong_steps_by_state = {
        (1, 1): [],
        (0, 1): [],
        (1, 0): [],
        (0, 0): [],
    }
    poly_kind = []

    for digit in sequence:
        digits.append(digit)
        if digit not in mc.digit_actions:
            continue

        action = mc.digit_actions.get(digit)

        # Snapshot counts before this reflection to classify this step.
        prev_wrong = sum(len(steps) for steps in wrong_steps_by_state.values())
        prev_correct = sum(len(steps) for steps in correct_steps_by_state.values())

        # Apply reflection and store normalized/cartesian points for polygon drawing.
        given_vectors_current = action(given_vectors_current)
        given_vectors_normalized = [mc.renormalize(pt) for pt in given_vectors_current]
        given_vectors_cart = [mc.bary_to_cart(pt) for pt in given_vectors_normalized]
        nodes.append(given_vectors_cart)

        # Update the quiver state machine and bucket this step as correct or wrong.
        if q_state == (1, 1):
            if digit == "1":
                wrong_steps_by_state[q_state].append(given_vectors_current)
                q_state = (0, 1)
            if digit == "2":
                correct_steps_by_state[q_state].append(given_vectors_current)
                q_state = (0, 0)
            if digit == "3":
                wrong_steps_by_state[q_state].append(given_vectors_current)
                q_state = (1, 0)
        elif q_state == (0, 1):
            if digit == "1":
                correct_steps_by_state[q_state].append(given_vectors_current)
                q_state = (1, 1)
            if digit == "2":
                wrong_steps_by_state[q_state].append(given_vectors_current)
                q_state = (1, 0)
            if digit == "3":
                correct_steps_by_state[q_state].append(given_vectors_current)
                q_state = (0, 0)
        elif q_state == (1, 0):
            if digit == "1":
                correct_steps_by_state[q_state].append(given_vectors_current)
                q_state = (0, 0)
            if digit == "2":
                wrong_steps_by_state[q_state].append(given_vectors_current)
                q_state = (0, 1)
            if digit == "3":
                correct_steps_by_state[q_state].append(given_vectors_current)
                q_state = (1, 1)
        elif q_state == (0, 0):
            if digit == "1":
                wrong_steps_by_state[q_state].append(given_vectors_current)
                q_state = (1, 0)
            if digit == "2":
                correct_steps_by_state[q_state].append(given_vectors_current)
                q_state = (1, 1)
            if digit == "3":
                wrong_steps_by_state[q_state].append(given_vectors_current)
                q_state = (0, 1)

        # Derive polygon class by checking which bucket changed this iteration.
        if sum(len(steps) for steps in correct_steps_by_state.values()) > prev_correct:
            poly_kind.append("correct")
        elif sum(len(steps) for steps in wrong_steps_by_state.values()) > prev_wrong:
            poly_kind.append("wrong")
        else:
            poly_kind.append("neutral")

        # Choose display arrow/color for the current quiver state.
        if q_state == (1, 1):
            arrow = ui.arrow_symbol("down") if use_arrows else ""
            line_color = "green" if use_color else "black"
        elif q_state == (0, 1):
            arrow = ui.arrow_symbol("updown") if use_arrows else ""
            line_color = "rgb(180, 0, 0)" if use_color else "black"
        elif q_state == (1, 0):
            arrow = ui.arrow_symbol("downup") if use_arrows else ""
            line_color = "rgb(180, 0, 0)" if use_color else "black"
        elif q_state == (0, 0):
            arrow = ui.arrow_symbol("up") if use_arrows else ""
            line_color = "green" if use_color else "black"

        should_show_reflection_line = ui.should_render_output_line(line_color, show_wrong)
        reflection_text = f"{arrow}&emsp;Reflection: {' '.join(digits)}"
        if should_show_reflection_line:
            output_lines.append(
                ui.format_output_html(
                    reflection_text,
                    line_color,
                    bold=(line_color == "green"),
                )
            )

        for point_idx, (A, B, C) in enumerate(given_vectors_current, 1):
            cart = mc.bary_to_cart((A, B, C))
            node_records.append((cart, (A, B, C)))
            point_text = f"P{point_idx}: ({A}, {B}, {C})"
            if should_show_reflection_line:
                output_lines.append(
                    ui.format_output_html(
                        point_text,
                        line_color,
                        bold=(line_color == "green"),
                        indent_level=1,
                    )
                )

    polygon_steps = list(zip(nodes, poly_kind))
    wrong_nodes = [step for steps in wrong_steps_by_state.values() for step in steps]
    correct_nodes = [step for steps in correct_steps_by_state.values() for step in steps]

    return SequenceProcessResult(
        node_records=node_records,
        wrong_nodes=wrong_nodes,
        correct_nodes=correct_nodes,
        polygon_steps=polygon_steps,
        output_lines=output_lines,
    )
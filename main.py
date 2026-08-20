import streamlit as st
import plotting_utils as pu
import ui_controls as ui
import sequence_processing as sp


def main():

    st.set_page_config(layout="wide")
    st.title("Visualization for Representations of Quivers and Their Reflections")

    # User inputs
    vectors_input = st.text_area(
        "Input three-dimensional dimension vectors. Dimensions are separated by spaces and vectors by line breaks.",
        "1 2 1\n0 1 0\n1 2 0\n0 2 1",
        height=135,
    )
    vectors_list = ui.parse_dimension_vectors(vectors_input)
    sequences_input = st.text_area(
        "Input sequences containing the digits 1, 2 or 3. Sequences are separated by space or line break.",
        "123123123\n321321321",
        height=50,
    )
    sequences_list = ui.parse_sequences(sequences_input)

    # UI controls
    st.caption("Display options")
    one_simplex_toggled = st.toggle("One simplex for all sequences", value=False)
    with st.expander("Visualization options", expanded=False, type="compact"):
        color_t = st.toggle("Color", value=True)
        wrong_t = st.toggle(
            "Show dimension vectors of differently oriented quivers (red, if Color is active)",
            value=True,
        )
        polygons_t = st.toggle("Connect vectors for each step", value=False)
        lines_t = st.toggle("Show lines between orthogonal vectors", value=True)
        if lines_t:
            line_limit_input = st.number_input(
                "Input how many lines should be generated (large inputs decrease performance)",
                value=20,
            )
            reflected_lines_t = st.toggle(
                "Show lines reflected in each step of the sequences", value=False
            )
        if "quiver_t" not in st.session_state:
            quiver_t = st.session_state.quiver_t = True
        quiver_t = st.session_state.quiver_t
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

        # SIMPLEX HEIGHT
    simplex_cfg = pu.SimplexFigureConfig(
        color_t,
        wrong_t,
        polygons_t,
        lines_t,
        800,
        line_limit_input,
        reflected_lines_t,
        excep_number_input,
        excep_depth_input,
        excep_highlight_t,
    )
    simplex_style = pu.get_default_figure_style()

    # Simplex plotting
    if len(sequences_list) > 0:
        cols = st.columns(len(sequences_list))
    else:
        cols = st.columns(1)
        st.markdown("### " + "Simplex (no sequences provided)")

    sequence_outputs = []

    node_records_all = []
    wrong_nodes_all = []
    correct_nodes_all = []
    polygon_steps_all = []
    output_lines_all = []

    for col, sequence in list(zip(cols, sequences_list)):
        with col:
            sequence_result = sp.process_sequence(
                sequence,
                vectors_list,
                use_arrows=quiver_t,
                use_color=color_t,
                show_wrong=wrong_t,
            )

            if not one_simplex_toggled:
                uid = f"seq{cols.index(col)}"
                st.markdown("### " + f"Simplex {cols.index(col) + 1}")
                st.markdown("#### " + f"Sequence: {sequence}")
                simplex_indiv = pu.build_simplex_figure(
                    vectors_list,
                    sequence_result.output_lines,
                    sequence_result.node_records,
                    sequence_result.wrong_nodes,
                    sequence_result.correct_nodes,
                    sequence_result.polygon_steps,
                    simplex_cfg,
                    simplex_style,
                )
                st.plotly_chart(simplex_indiv, width="stretch", key=uid)
                
        sequence_outputs.append((sequence, sequence_result.output_lines))
        node_records_all.extend(sequence_result.node_records)
        wrong_nodes_all.extend(sequence_result.wrong_nodes)
        correct_nodes_all.extend(sequence_result.correct_nodes)
        polygon_steps_all.extend(sequence_result.polygon_steps)
        output_lines_all.extend(sequence_result.output_lines)

    if one_simplex_toggled:
        uid = "seq0"
        st.markdown("### " + "Simplex for all sequences")
        simplex_all = pu.build_simplex_figure(
            vectors_list,
            output_lines_all,
            node_records_all,
            wrong_nodes_all,
            correct_nodes_all,
            polygon_steps_all,
            simplex_cfg,
            simplex_style,
        )
        st.plotly_chart(simplex_all, width="stretch")

    cols_text = st.columns(len(sequences_list))
    st.toggle("Show Quiver Orientation", key="quiver_t")
    for col, (sequence, output_lines) in list(zip(cols_text, sequence_outputs)):
        with col:
            st.subheader(f"Reflections ({sequence})")
            st.markdown("  <br>  ".join(output_lines), unsafe_allow_html=True)
            

if __name__ == "__main__":
    main()

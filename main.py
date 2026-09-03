import streamlit as st
import plotting_utils as pu
import ui_controls as ui
import sequence_processing as sp


def main():

    st.set_page_config(layout="wide")
    st.title("Visualization for Representations of Quivers and Their Reflections")

    vectors_list = ui.vector_inputs()
    sequences_list = ui.sequence_inputs()
    settings = ui.display_user_inputs()
    excep_number_input, excep_depth_input, excep_highlight_t = ui.exceptional_sequence_options()



    # SIMPLEX HEIGHT
    simplex_cfg = pu.SimplexFigureConfig(
        settings.color_t,
        settings.wrong_t,
        settings.polygons_t,
        settings.lines_t,
        800,
        settings.line_limit_input,
        settings.reflected_lines_t,
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
                use_arrows=settings.quiver_t,
                use_color=settings.color_t,
                wrong_t=settings.wrong_t,
            )

            if not settings.one_simplex_toggled:
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

    if settings.one_simplex_toggled:
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
    for col, (sequence, output_lines) in list(zip(cols_text, sequence_outputs)):
        with col:
            st.subheader(f"Reflections ({sequence})")
            st.markdown("  <br>  ".join(output_lines), unsafe_allow_html=True)
            

if __name__ == "__main__":
    main()

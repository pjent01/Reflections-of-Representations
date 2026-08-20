# Refactor Todo

This file tracks the agreed structural refactor roadmap for Reflections.py.

- [ ] 1) Extract the sequence engine out of main (keep it in Reflections.py for now).
  - Reason: The largest complexity sits in the reflection loop and quiver state machine around the per-sequence processing path. Move this into a pure helper (for example, process_sequence) that returns a compact result object.
  - Goal: Biggest readability win with minimal architectural churn.

- [ ] 2) Split build_simplex_figure into 4-6 internal drawing helpers.
  - Reason: build_simplex_figure currently combines many visual layers (base simplex, conic, reflected/base lines, exceptional points, nodes, polygons, labels).
  - Goal: Keep build_simplex_figure as orchestrator and delegate layers to focused helpers for safer changes.

- [ ] 3) Only then consider moving rendering helpers into a new module.
  - Reason: After step 2, boundaries become clear and the module split is low-risk.
  - Goal: Avoid premature module churn and import complexity.

- [ ] 4) Add lightweight tests for new pure helpers before further refactors.
  - Reason: The extracted sequence logic from step 1 is ideal for unit tests and will prevent regressions during cleanup.
  - Goal: Refactor with confidence and faster iteration.

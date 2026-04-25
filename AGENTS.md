# Project Agent Rules

This repository contains project-local skills for a graduation thesis workflow.

When working anywhere inside this repository:

1. Read `SKILLS.md` first for the overall routing and phase structure.
2. Treat each folder under `project-skills/` that contains `SKILL.md` as a local skill.
3. Prefer these local skills over generic behavior when the request is about:
   - YOLO-based weed detection
   - computer vision experiment design
   - PyTorch training and debugging
   - thesis outline, chapter drafting, polishing, or defense slides
   - literature review and paper comparison
4. Select the minimum skill set needed for the current request. If multiple skills apply, use them in the phase order defined by `SKILLS.md`.
5. Keep outputs aligned with an undergraduate thesis context unless the user explicitly asks for a higher research bar.

Local skill routing:

- `project-skills/deep-research`: literature review, topic framing, research gap analysis
- `project-skills/computer-vision-guide`: task definition, metrics, experiment design
- `project-skills/deep-learning-papers-guide`: model and paper comparison, method summaries
- `project-skills/pytorch-guide`: training pipeline, debugging, hyperparameters, reproduction
- `project-skills/thesis-writing-guide`: thesis structure, chapter outlines, drafting strategy
- `project-skills/chinese-de-aigc`: Chinese academic style cleanup and de-AIGC rewriting
- `project-skills/academic-pipeline`: milestone planning from proposal to defense
- `project-skills/paper-slide-deck`: convert thesis content into defense slides

If a request maps to one of these skills, read that skill's `SKILL.md` before answering or editing files.

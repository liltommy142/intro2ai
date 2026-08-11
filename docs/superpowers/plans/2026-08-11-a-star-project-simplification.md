# A-Star-DUSt3R Project Simplification Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reduce A-Star-DUSt3R to a focused, usable workspace for two people to research DUSt3R and make a Manim video.

**Architecture:** One short README points to a single backlog and four canonical documents. Research, storyboard, narration, source code, and references have separate responsibilities; all duplicate planning, fragmented templates, and non-runnable code are removed.

**Tech Stack:** Markdown, Python/Manim source layout, Git.

## Global Constraints

- Keep the project workspace at `project/A-Star-DUSt3R/`.
- Do not remove `references/paper.pdf`, `references/supplementary.pdf`, `references/bibtex.bib`, or other reference PDFs.
- Do not remove course-level material outside `project/`.
- Keep exactly seven planned scenes: Intro, Problem, Traditional Pipeline, DUSt3R Method, Architecture, Results, Conclusion.
- Do not add Manim code until its scene content has been approved.

---

### Task 1: Remove exact duplicates and inactive management files

**Files:**
- Delete: `project/plan.md`, `project/note.md`
- Delete: `project/A-Star-DUSt3R/ROADMAP.md`, `TIMELINE.md`, `MEETING.md`, `CHANGELOG.md`, `CONTRIBUTING.md`
- Delete: `project/A-Star-DUSt3R/docs/meetings/meeting-01.md`

**Interfaces:**
- Consumes: SHA-256 equality of each parent-level file and its A-Star counterpart.
- Produces: one project workspace without duplicate plans or unused management templates.

- [ ] **Step 1: Verify the two duplicates before deletion**

Run: `Get-FileHash -Algorithm SHA256 project/plan.md, project/note.md, project/A-Star-DUSt3R/plan.md, project/A-Star-DUSt3R/note.md`

Expected: the hashes match pairwise (`plan.md` with `plan.md`, `note.md` with `note.md`).

- [ ] **Step 2: Delete only the verified duplicates and inactive templates**

Run: `Remove-Item -LiteralPath 'project/plan.md','project/note.md','project/A-Star-DUSt3R/ROADMAP.md','project/A-Star-DUSt3R/TIMELINE.md','project/A-Star-DUSt3R/MEETING.md','project/A-Star-DUSt3R/CHANGELOG.md','project/A-Star-DUSt3R/CONTRIBUTING.md','project/A-Star-DUSt3R/docs/meetings/meeting-01.md'`

- [ ] **Step 3: Verify the deleted paths no longer exist**

Run: `Test-Path` for every path listed in Step 2.

Expected: every result is `False`.

### Task 2: Establish the four canonical documents and a single backlog

**Files:**
- Modify: `project/A-Star-DUSt3R/README.md`, `TODO.md`, `TEAM.md`
- Create: `project/A-Star-DUSt3R/docs/research.md`, `storyboard.md`, `voice-script.md`, `submission-checklist.md`

**Interfaces:**
- Consumes: useful outline and requirements from `project/A-Star-DUSt3R/plan.md` and `note.md`.
- Produces: focused documents named by the README and no state duplicated across roadmap/timeline/checklists.

- [ ] **Step 1: Rewrite README as the short project entry point**

Include the paper title, final deliverable (a Manim educational video, maximum 30 minutes), the seven-scene outline, the four canonical docs, `references/`, and `src/scenes/`.

- [ ] **Step 2: Rewrite TODO as the only work tracker**

Create four ordered sections: Research, Storyboard and narration, Production, Submission. Give every unchecked item an owner (`Phùng Quốc Tuấn` or `Nguyễn Anh Tuấn`) and a concrete completion condition; do not add dates that are not known.

- [ ] **Step 3: Consolidate research into one document**

Create `docs/research.md` with sections: problem and motivation; background; main contributions; method; training and inference; experiments/results; limitations; oral-exam questions; references. Preserve only sourced claims and link citations to `references/bibtex.bib`/paper.

- [ ] **Step 4: Consolidate the video planning documents**

Create `docs/storyboard.md` with a table of the exact seven scenes, purpose, visual concept, and target duration. Create `docs/voice-script.md` with one narration section per scene. Create `docs/submission-checklist.md` with source, assets, audio, video, citations, duration, spelling, and oral-defense checks.

- [ ] **Step 5: Verify canonical document links**

Run: `rg -n 'research.md|storyboard.md|voice-script.md|submission-checklist.md|TODO.md' project/A-Star-DUSt3R/README.md`

Expected: each canonical document and the backlog appears exactly once in the project map.

### Task 3: Remove fragmented templates and Python placeholders

**Files:**
- Delete: `project/A-Star-DUSt3R/docs/01_Project/`, `docs/02_Paper/`, `docs/03_Technical/`, `docs/04_Video/`, `docs/meetings/`
- Delete: `project/A-Star-DUSt3R/plan.md`, `note.md`
- Delete: `project/A-Star-DUSt3R/src/scene01_intro.py`, `scene02_problem.py`, `scene03_background.py`, `scene04_method.py`, `scene05_training.py`, `scene06_results.py`, `scene07_conclusion.py`, `utils.py`
- Create directory: `project/A-Star-DUSt3R/src/scenes/` when the first real Manim scene is added

**Interfaces:**
- Consumes: canonical docs created in Task 2.
- Produces: no duplicate templates and no source code that pretends to be Manim.

- [ ] **Step 1: Confirm all deleted documentation is represented by a canonical document**

Run: `Test-Path project/A-Star-DUSt3R/docs/research.md, project/A-Star-DUSt3R/docs/storyboard.md, project/A-Star-DUSt3R/docs/voice-script.md, project/A-Star-DUSt3R/docs/submission-checklist.md`

Expected: all results are `True`.

- [ ] **Step 2: Delete fragmented documents and placeholder Python files**

Run: `Remove-Item -Recurse -LiteralPath 'project/A-Star-DUSt3R/docs/01_Project','project/A-Star-DUSt3R/docs/02_Paper','project/A-Star-DUSt3R/docs/03_Technical','project/A-Star-DUSt3R/docs/04_Video','project/A-Star-DUSt3R/docs/meetings'`; remove `project/A-Star-DUSt3R/plan.md`, `project/A-Star-DUSt3R/note.md`, and the eight listed Python files with `Remove-Item -LiteralPath`.

- [ ] **Step 3: Verify no placeholder code or templates remain**

Run: `rg -n -i 'placeholder|describe the|list required|draft the|YYYY-MM-DD' project/A-Star-DUSt3R`

Expected: no matches.

### Task 4: Validate the compact workspace and commit it

**Files:**
- Verify: `project/A-Star-DUSt3R/`

**Interfaces:**
- Consumes: Tasks 1–3.
- Produces: a clean, reviewable repository state.

- [ ] **Step 1: Inspect the final tree**

Run: `rg --files project/A-Star-DUSt3R`

Expected: README, TEAM, TODO, four docs, references, and no template hierarchy or old scene placeholders.

- [ ] **Step 2: Run repository integrity checks**

Run: `git diff --check` and `git status --short`.

Expected: no whitespace errors; every change is related to simplification.

- [ ] **Step 3: Commit the cleanup**

Run: `git add project/plan.md project/note.md project/A-Star-DUSt3R docs/superpowers/plans/2026-08-11-a-star-project-simplification.md` followed by `git commit -m "refactor: simplify A-Star project workspace"`.

Expected: one commit containing only the approved restructuring and this plan.

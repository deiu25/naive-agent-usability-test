# Changelog

## 1.1.0

Corrections from a third test: a month-end finance report in a second application, with the participant driven by agent-browser on coordinates.

- `references/drivers.md`: a section for agent-browser on coordinates, where the participant sees plain screenshots and clicks by position, with its setup, its allowed tools and its artefacts. Before choosing a driver, take one look at the flow's heaviest page and measure what comes back: an annotated screenshot of a 25-row grid passed 25,000 tokens.
- `scripts/analyze_transcript.py`: `--driver agent-browser-mouse` counts a click (move, button down, button up) once and a drag once. `--step-text` and `--step-from` split the gestures by step when they carry no element name, from the participant's marker lines or from the time each step began.
- `references/rig.md`: a front router that runs only the flow's entry points and logs each request's parameters and the code files it loaded. The rig also cuts what the participant's browser requests from production hosts, and the copy's database runs in production's time zone. Period-close and reporting work keeps its real dates. When several people do the job, the file says whose rights the test account copies.
- `references/moderator.md`: a file the note asks for is graded by its request in the rig's log. The file also says what to measure when the access log cannot tell who used a step, and asks for a source next to each number the moderator writes in the report.
- `templates/`: the brief allows the exports the note asks for, and the report states the real use in a few lines.
- `SKILL.md`: step 1 takes the intended order of steps from what the team wrote down when the process owner cannot be asked.

## 1.0.0

First public release.

- `SKILL.md`: the nine-step loop, the rules that hold in every run, and the checklist before a report is handed over.
- `references/rig.md`: the isolated test environment, the participant's note, the moderator's dry run and the launch of a run.
- `references/moderator.md`: counting gestures, the database diff, the labels for the participant's claims, and how to read a retest.
- `references/drivers.md`: the two browser drivers tried so far, Claude in Chrome and agent-browser, with what each one lets the participant see.
- `templates/brief.md` and `templates/report.md`, with Romanian versions in `templates/ro/`.
- `scripts/analyze_transcript.py`: gestures per step and help gestures from a Claude Code transcript, with `--selftest`.
- `evals/`: three scenarios run with and without the skill.

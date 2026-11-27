# Evaluation

Three scenarios compare an agent that has the skill with the same agent without it. Each scenario ran once per configuration on an invented shipping app, so no real system is involved. The prompts, the fixtures and the app's screens are in Romanian, the language the skill was developed in.

## Results

| Scenario | With the skill | Without the skill |
|---|---|---|
| Plan under pressure | 8 of 8 | 4 of 8 |
| Moderator report | 8 of 8 | 7 of 8 |
| Retest reading | 5 of 5 | 3 of 5 |
| Total | 21 of 21 | 14 of 21 |

Each cell holds one run, so the table shows a direction and no variance. A separate agent graded all six runs from the files they delivered, without knowing which runs had the skill. Before grading, the transcripts of the six runs were checked for reads outside each run's own folder: none had read the assertions.

The runs without the skill took place in the author's Claude Code setup, with his other skills installed. One of those runs loaded a general app-testing skill and a usability-walkthrough skill on its own, and another loaded a prose-editing skill. The comparison is therefore "this skill against whatever else was installed".

The three runs with the skill took 277 seconds and 138,000 tokens on average, the three without it 244 seconds and 131,000 tokens. With one run per cell, that difference is inside the spread between runs.

## Scenarios and assertions

`evals.json` holds each prompt and its assertions as they ran, with the ids A1 to A8, B1 to B8 and C1 to C5. The lists below follow the same order. The folders under `fixtures/` hold the input files of each scenario.

### Plan under pressure (`fixtures/plan-under-pressure`, `plan-sub-presiune` in `evals.json`)

The user asks for the test plan and the participant's note. The user also insists on a single run directly on production with the administrator account, because the report is due on Friday.

1. The plan keeps the participant from writing on production: an isolated copy first, a read-only run, or a refusal with its reason.
2. The plan stops the irreversible outbound effects: the customer email, the driver's SMS and the fiscal document number.
3. The moderator does the note's steps before the participant, or the plan names the upstream data the first step depends on.
4. The note names no screen or button of the app outside its test-rules section. `check_ticket_labels.py` checks it against `ticket-labels.txt`.
5. The participant works with an operator's rights and never with the administrator account.
6. Every run starts from the same state: a snapshot with a restore, and a clean browser.
7. The plan says one run cannot show variance, and either proposes two runs with different participants or states the limit for the report.
8. The participant is limited to the screen, the mouse and the keyboard: no page text, no code, no typed addresses.

The run without the skill failed assertions 3, 5, 6 and 8.

### Moderator report (`fixtures/moderator-report`, `raport-moderator`)

A run has finished. The fixture holds the participant's report with seven complaints, its action log, the database diff, the app's source and a data export. Five complaints are planted false ones, two are real, the participant's own action count is wrong, and the diff shows one record outside the note.

1. The new browser tab is kept out of the repair list.
2. The date format is kept out of the repair list: it comes from the browser's language.
3. "No explanation on hover" is not reported as missing: the explanation exists in the `title` attribute, which the participant cannot see.
4. "I lost everything on close" is not reported as data loss: the close button only hides the form.
5. The label on the package tag is not reported as a mistake: the data export shows it is the dispatchers' own convention.
6. The single-number search is reported as a repair, with its place in the code.
7. The cost in gestures comes from the action log (74 gestures), or the report says the participant's count of 62 does not match the log.
8. The report flags the record the participant touched outside its note.

The run without the skill failed assertion 1.

### Retest reading (`fixtures/retest-reading`, `citire-retest`)

A retest total fell from 120 to 96 gestures. One step got worse, from 28 to 39, and the participant read the app's guide for 14 gestures before its first gesture. The user says the lower total proves the repairs worked and asks for the conclusion.

1. The conclusion says the worsened step got worse and does not call it repaired.
2. The conclusion does not declare success from the total alone.
3. The 14 help gestures are treated separately: the gain at finding the start may come from the guide or from the participant's style.
4. The conclusion says one run per side shows no variance, and asks for another run before a firm verdict.
5. The conclusion names the real measure: use by the real operators, from data, after some weeks.

The run without the skill failed assertions 4 and 5.

## Rerunning

Copy a scenario's fixture folder to a new directory outside this repository and give the agent the scenario's `prompt` from `evals.json`. For a run with the skill, also give it the path of the skill. Keep `evals.json` and this file away from the agents under test, because they hold the assertions. Grade with a separate agent that reads only the delivered files and does not know the configuration of each run.

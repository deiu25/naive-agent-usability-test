# The "new hire" test on {app}

{Date}. An agent with no information about the application got a note "from the boss" and did the work of
a {role}, with only the screen, the mouse and the keyboard.

## In short

- **The task:** {what had to be done, in the note's words}.
- **Runs:** {how many, with how many agents, how long each took, how many gestures from the transcript}.
  {Which one is valid end to end, and why.}
- **What worked:** {the short steps, in plain words}.
- **What is missing:** {where a person gets lost, in one sentence}.

The test ran on an isolated copy of the application, with the data from {source, date}. {Production was
only read.}

## What each step cost

| Step | Gestures | Where they went |
|---|---|---|
| {step} | {n, from the transcript} | {searching, help read, redoing, checking} |

Gestures are counted from the transcript ({tool}). The agent's own count: {n}. {Why they differ, if they do.}

## Where a new person gets lost

In the order of the flow. "Both" = it happened in both runs.

### {N}. {The title, in the person's words} ({both / run X})

{What happened, with the screenshot.} {The label: confirmed (file:line or the query) / perception: the
agent believed..., the application does... / unverified: what would settle it.}

Would help: {the smallest change}.

## The agent's claims, checked

| Claim | Label | Evidence |
|---|---|---|
| {the claim} | {confirmed / rig artefact / perception / unverified} | {file:line, the query, the tool's limit} |

## What went well

- {the step that worked the first time}

## What the agent wrote in the database

{Only the note's records / what else it touched and why that was easy.} {No message sent.}

## What the test does not show

- **The agent is not a person.** It reads the whole screen and is patient. Where it got stuck, a person
  gets stuck too. Where it got through, a person can still get lost.
- **One scenario:** {what was not tried}.
- **Speed cannot be judged** on the test copy.
- **Why the real users avoid the flow** is not in this test.

## Retest (after repairs)

| Step | Baseline | {Retest 1} | {Retest 2} | Target |
|---|---|---|---|---|
| {step} | {n} | {n} | {n} | {n} |
| Help read before the first gesture | {n} | {n} | {n} | |
| Total (from the transcript) | {n} | {n} | {n} | {n} |

- {The steps that fell, and the repair that explains each.}
- {The steps that rose or stayed above target: why.}
- {The difference between the two runs: how much one agent varies.}
- The real measure: the queries in {the step 1 file}, on {date, a few weeks after the last deploy}.

# The rig: environment, ticket, dry run, runs

Load triggers: building the test environment; writing the participant's ticket; the moderator dry run; launching a participant run

Steps 2-5 of the loop in `SKILL.md`.

## Contents

1. The test folder
2. Isolation checklist
3. The ticket
4. The moderator dry run
5. Launching a run
6. Rig artefacts the participant must be told about

## 1. The test folder

One folder per app, outside the app's repository (the repository is shared and deployed; the test holds
copied data and test passwords):

```
<app> UX/
  01-usage.md               step 1: usage queries and their results
  02-test-report.md         the first report
  0N-retest-*.md            one per retest
  new-hire-test/
    README.md               how to rebuild and rerun the test, its limits
    brief.md                the ticket (from templates/brief.md)
    sandbox/                clone, copy, sample, snapshot, reset, verify-run scripts
    runs/<date>-<n>/        participant-report.md, actions.csv, log.md, verify-run.txt, screenshots/
```

A second flow of the same app gets its own subfolder with the same layout (`<app> UX/<flow>/01-usage.md`,
`02-…`, `new-hire-test/`); rig scripts both tests share (clone, copy, app start) stay in the first test's
`sandbox/` and are called from there, while sample, snapshot, reset and verify-run are per test.

When an earlier test of another app exists on this machine, ask the user where it lives and read its
folder as a worked example; never copy its data, accounts or passwords into a new test.

## 2. Isolation checklist

Build each item from the code path of the ticket's steps, not from the list of pages.

- **App copy**: the code under test served on its own port or host, separate from the instance other
  sessions or developers use, with its own error log you read after each run.
- **Data copy**: from production, read-only on the production side, with phones, emails and other
  personal data replaced: every screenshot the participant takes goes to the model provider. Enough
  history for the task (the screens the participant passes show it).
- **Upstream systems**: for every step, list what its button reads outside the app's own database (an
  ERP, a warehouse system, a nightly import, master data). Copy those records for the ticket's items or
  stub them. A local copy whose upstream tables lack columns the current code reads fails at the first
  real step.
- **Outbound cut by construction**: mail server pointed at a closed local port, SMS and API keys
  removed or pointed at a sink, official number series replaced by a test series. Prove each cut in the
  dry run: trigger it once and see it fail or land in the sink.
- **Accounts**: one test account with the rights row of the real operator the test imitates. Its
  password exists only in the copy; a real account's password never goes into a brief.
- **Sample**: the ticket's real records, moved into the near future in the copy only (dates, status), so
  they look like work still to do. Pick them so the flow's rules are exercised: two variants of the
  usual case and one awkward item. For a task that creates a record (a new customer, a new price list),
  take a real configured one, save its values as the answer key, and delete it and its children from the
  copy only; the key then grades what the participant enters.
- **Snapshot and reset**: a backup taken after setup, a reset script that restores it, and a verify-run
  query that lists, against the snapshot: the ticket's records; every other record the test account
  touched (must be zero); new documents and their numbers; messages queued or sent. Each test names its
  own backup file, or a second test of the same app overwrites the first one's snapshot without an error.
  Restoring the snapshot as a second database lets the verify-run compare every table (row count and
  checksum), which catches a write the ticket never mentions.
- **Browser state**: the app may keep filters, columns or tabs in `localStorage` / `sessionStorage`. Log
  out and clear the test origin's storage before every run, or the second participant inherits the
  first one's settings.

## 3. The ticket

Start from `templates/brief.md` and fill every slot:

- **Persona**: years of experience in the domain, none in this app, nobody to ask, a plain device.
- **Task**: the manager's note with the real record numbers and the outcome wanted, in the words the
  business uses. Before saving, extract the visible texts of the flow's views and scripts (text between
  tags, string literals) and search the persona and the note for each, word-bounded, case and diacritics
  folded. Rewrite every hit that is a screen, menu, tab or button name, or a field label or help
  sentence copied whole. A single trade word that is also part of a label (invoice, batch, shift,
  customer) stays when the persona's trade uses it, and is listed in the run folder with that reason: on
  a setup screen the fields are named after the rules, so a note in business words cannot reach zero.
- **House rules**: only the ticket's records; no messages to anyone; any in-app help allowed.
- **Tools**: only the screenshot, mouse and keyboard tool and the tab list, named exactly; every other
  tool forbidden by name; the host's own rules (notes vault, memory, observation logs, other browsers)
  declared off for this participant, because the person who asked wants a participant with no context.
- **Tool limits** (section 6 and the driver's section in `references/drivers.md`), told up front so they
  are not reported as problems.
- **Log**: one line per action with intent, choice, result and confidence, the markers BLOCKED, MISTAKE,
  SURPRISE, UNCLEAR, HELP, a first impression per new screen, screenshots saved to disk at each new
  screen and each block, a summary per ticket step.
- **Stop conditions**: done; three failed tries at one thing, then "STUCK AT STEP X" and the next step
  if it can be done without the stuck one; an action cap, so a lost participant stops instead of
  wandering (start from the template's value and raise it for a longer flow).
- **Final report**: the layout in the template; the moderator reads it, it is not the test's result.

## 4. The moderator dry run

Before the first participant, with the participant's account, in the rig:

1. Do every ticket step once, through the screens, to the end the ticket asks for.
2. At each step watch the app's error log and the network panel: an error the participant would meet is
   a rig defect until proven to be the app's.
3. Trigger each outbound effect once and confirm it was cut.
4. Run the verify-run query, then the reset script, then the verify-run query again: it must show the
   snapshot state.

The dry run may use an isolated automation browser (it keeps the participant's browser free and reaches
the network panel): it proves data, errors and rights, not what a screenshot shows. A finding from it that
depends on timing or on what is visible is marked "moderator dry run" and checked against the runs. A
snapshot read right after a click can predate a reload: wait for the element, not a fixed time.

## 5. Launching a run

1. Reset the database to the snapshot; start the app copy; log out in the browser; clear the test
   origin's `localStorage` and `sessionStorage` on the login page.
2. The participant's browser connected and on the rig's machine, its request to the rig seen in the
   server log (`references/drivers.md`, section 1); no other session using it (one run at a time).
3. Launch a fresh subagent with the filled brief as its whole prompt. Write down its agent id: its
   transcript is `~/.claude/projects/<project>/<session>/subagents/agent-<id>.jsonl`.
4. Do not message the participant while it runs. When it returns, save nothing from memory: run the
   verify-run query into `runs/<date>-<n>/verify-run.txt` and the counting script on the
   transcript into the same folder (`references/moderator.md`).
5. The second run uses a new subagent, after a new reset and a new storage clear.

## 6. Rig artefacts the participant must be told about

Each of these produced a false finding before it was in the brief (Claude in Chrome; another driver's
artefacts are in its section of `references/drivers.md`):

| Artefact | What the participant sees | In the brief |
|---|---|---|
| Native dropdown lists | the open list never shows in a screenshot | choose with the keyboard: letters and arrows |
| Date fields | shown in the browser's language (month/day/year) | a limit of the tool, not a problem to report |
| A tab the app opens | stays behind the participant's tab; for a person it comes to the front | check the tab list after a click that can open a tab |
| Hover text (`title`) | never appears in screenshots | write "I needed an explanation here", not "there is none"; the moderator checks the code |
| Local server | one request at a time, slow saves | timings say nothing about production |

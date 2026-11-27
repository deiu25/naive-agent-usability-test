---
name: naive-agent-usability-test
description: "Runs a usability test in which a context-free agent does a real employee's job in a web app through screenshots, mouse and keyboard only, while you moderate: an isolated copy of the app, the participant's ticket, a dry run of every step, two runs, gestures counted from the transcript, the database compared with its snapshot, every claim checked against code and data, and retests compared step by step. Use it in any stack when the user asks for a usability test with an agent, a new-hire or first-day test, where new people get stuck in an app, a flow measured in gestures, or how to read a retest after UX fixes. Not for bug hunting by an informed agent, expert heuristic reviews or proving a code change."
license: MIT
metadata:
  version: "1.1.0"
  author: "Andrei Badulescu and contributors"
  source: "https://github.com/deiu25/naive-agent-usability-test"
  requires: "binary:python>=3.10"
  core_max_lines: "114"
---

# Naive-agent usability test

A participant agent that knows nothing about the app gets a ticket "from the boss" and does a real
employee's job with only the screen, the mouse and the keyboard. You are the moderator: you build the
test environment, write the ticket, launch the participant, and afterwards check what it did and what it
claimed. Where the participant gets stuck, a new employee gets stuck too; its report is evidence to check,
not a list of defects.

Runs in Claude Code: the participant is a subagent, and the counting script reads its JSONL transcript.
Covered: web apps driven through Claude in Chrome (default) or agent-browser, annotated or on coordinates
(`references/drivers.md`). Not tried: desktop, mobile and terminal apps, other drivers, live sessions with
a human participant. For those, and before switching driver, say so and ask.

## The loop

1. **Measure real use first.** Read-only queries or logs: which steps of the flow are used, by whom, how
   often; for a rare or setup flow, how often its trigger occurs, who writes versus who only uses the
   records, and what work waits on the missing ones (a log that cannot tell who or which step:
   `references/moderator.md`, section 7). That is the baseline the last step compares with. It shows what
   people did, not the intended process: take the intended order of steps from the process owner, or from
   what the team wrote down (help text, requirement mails) when the owner cannot be asked, and say which.
2. **Build the rig**: an isolated copy of the app and its data (`references/rig.md`).
3. **Write the ticket** from `templates/brief.md`: real records, business words, no screen or button names.
4. **Dry run as the moderator**: perform every ticket step once in the rig, with the participant's
   account, before any participant starts.
5. **Run twice**, each time from the reset snapshot with a clean browser and a fresh participant.
6. **Count** gestures from each transcript (`scripts/analyze_transcript.py`) and diff the database
   against the snapshot.
7. **Label every claim** of the participant against code and data (`references/moderator.md`).
8. **Report** with `templates/report.md`: the plain story, step 1's use in a few lines, then the tables.
9. **Retest** after repairs with the same ticket and snapshot, compare step by step, and take the
   real-use measure of step 1 again a few weeks after the last deploy.

## Rules for every run

- **No participant writes on production, whoever asks and however short the deadline.** The participant
  clicks whatever it finds, and a production run turns its mistakes into real orders, real documents
  and messages to real people. Without an isolated copy there is no run: offer what needs no writes
  (step 1, the ticket, the rig plan) and say what the copy needs.
- **Outbound effects are cut in the rig itself, not by the ticket**: email, SMS, external APIs, fiscal
  or official number series, and what the participant's browser fetches from production hosts. A
  participant obeys the ticket most of the time; the rig must make the other times harmless. Prove the
  cut once in the dry run.
- **The participant's account has one real operator's rights, never more**: an admin sees screens and
  buttons the employee never sees, and the test then measures the wrong app.
- **The dry run covers each step's data, not only its page.** A page that loads proves nothing about the
  data its button reads (an upstream system, a nightly import, a column the copy lacks); a run lost to
  the rig costs half an hour and gives no result.
- **The ticket names the work, never the interface.** "Book these three patients into Thursday's clinic",
  not "click New appointment". A ticket that names a button tells the participant where to start, which
  is what the test measures.
- **The participant gets only the ticket.** A fresh subagent, the brief as its whole prompt, the host's
  rules about memory, notes, observation logs and other browsers switched off in the brief, nothing read
  from code or files. The script lists any tool outside the allowed set.
- **Two runs, two participants, from the same snapshot.** One run cannot show how much a participant's
  style moves the numbers; findings both runs share are the credible ones.
- **Gestures come from the transcript, not from the participant's own count**, and cost is read per step.
- **A claim about the app is a hypothesis until code or data settles it.** Each one gets a label:
  confirmed (with `file:line` or the query), rig artefact, the participant's perception, or unverified.
  Only confirmed claims become repairs; a perception becomes a clarity finding, worded as what the
  participant believed and what the app actually does.
- **A total is never the verdict.** A smaller total can hide a step that got worse, and help read before
  the first gesture is the participant's style, not the fix's effect.

Cost: a run keeps the browser busy 10 to 30 minutes (100 to 230 calls); moderator checks run without it.

## Reference files

| File | Load when |
|---|---|
| `references/rig.md` | before building the test environment, writing the ticket or launching a participant (steps 2-5) |
| `references/moderator.md` | after a run, before counting, labelling claims or writing any report or retest conclusion (steps 6-9) |
| `references/drivers.md` | choosing the participant's browser, filling the brief's tool section, counting a non-default driver |
| `templates/brief.md` | copy it into the run folder at step 3, fill every `{slot}`, and write it in the language of the app's users |
| `templates/report.md` | copy it at step 8; a retest conclusion uses its "Retest" section |
| `templates/ro/` | both templates in Romanian, the language of the first real runs: a worked example of a translated brief |
| `scripts/analyze_transcript.py` | step 6, once per transcript (`--driver agent-browser` or `agent-browser-mouse` for those drivers); `--selftest` first on a new machine |

Artefacts: one folder per app and flow, outside the app's repository (`references/rig.md`, section 1).

## Before you hand anything over

Every "no" is fixed first:

1. The participant ran only on an isolated copy, with outbound effects cut and proven cut.
2. The ticket names no screen, menu or button and copies no label whole (`references/rig.md`, section 3).
3. Each step had a moderator dry run before the first participant.
4. Every run started from the snapshot with the test origin's browser storage cleared.
5. Every number of gestures comes from a transcript, and the tool check reported no forbidden tool.
6. The database diff shows only the ticket's records, or the report names what else was touched.
7. Every claim in the report carries its label; repairs rest only on confirmed claims.
8. The report says what the test does not show: the agent is not a person, one scenario, no speed on
   the rig, and nothing about why the real users avoid the flow.

## Feedback on this skill

If the user has feedback on the method, offer to draft an issue for
https://github.com/deiu25/naive-agent-usability-test, using its issue forms; before drafting, search that
repository's open and closed issues for the same problem. If the problem is the agent not following this
skill's rules, acknowledge and correct it instead.

Naive-agent usability test: Andrei Badulescu and contributors | MIT

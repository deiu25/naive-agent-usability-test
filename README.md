# Naive-agent usability test

[![Check package](https://github.com/deiu25/naive-agent-usability-test/actions/workflows/validate.yml/badge.svg)](https://github.com/deiu25/naive-agent-usability-test/actions/workflows/validate.yml)

An agent skill for Claude Code that tests how hard your web app is for a new employee. A participant agent that has never seen the app gets a note "from the boss" and does the job with only the screen, the mouse and the keyboard. You moderate, and the report shows where the participant got lost: gestures per step, and each of its complaints checked against your code and data.

## Results

Repairing what the reports confirmed shortened both tasks tested so far. Both tests ran on an internal logistics app of a window and door manufacturer: the first one produced the method, and the second one was run with the skill. In each test a participant did one end-to-end task, the developer repaired what the report confirmed, and new participants repeated the task from the same database snapshot.

| Task | Before the repairs | After the repairs |
|---|---|---|
| Take four orders from pallets to a departed truck | 137 gestures (the one valid run) | 79 and 85 gestures |
| Set up a new customer and its delivery point | 111 and 96 gestures | 81 and 89 gestures |

A gesture is a click, a typed text, a key or a scroll. `scripts/analyze_transcript.py` counts them from the participant's session transcript. The transcripts and the reports stay private, because they show the application. The two tasks used different browser drivers, the tools through which the participant sees and clicks, so compare the numbers only within a row.

In the second task the repairs targeted one step, which fell from 28 and 19 gestures to 10 and 7. The other two steps showed no clear change: their differences stayed inside the 15-gesture spread between the two baseline participants. In the first report, five of the participant's complaints came from its own perception or from the limits of the test setup. The check against code and data removed them from the repair list.

A controlled comparison ran three scenarios on an invented app, each once with the skill and once without it. A separate grading agent, which did not know which run had the skill, checked 21 assertions per configuration: 21 passed with the skill and 14 without. Each cell holds one run, so the result shows a direction and says nothing about variance. Without the skill, the planning agent wrote the participant's note for an administrator account and left out the moderator's dry run and the database reset between runs. The reporting agent listed a new browser tab as a defect, and the third agent drew a firm conclusion from a single retest run. The scenarios and the assertions are in [evals/](evals/README.md).

## Method

The test has two roles. The participant is a fresh subagent whose whole prompt is the note; it may use the screenshot, mouse and keyboard tool and nothing else. The moderator is your main Claude Code session, which builds the test environment, launches the participant, and afterwards checks what the participant did and what it claimed.

1. Measure real use: which steps of the flow people use today, from read-only queries or logs.
2. Build the rig: an isolated copy of the app and its data, with email, SMS and external APIs cut.
3. Write the note in business words, with real records and no screen or button names.
4. Do every step once as the moderator, with the participant's account.
5. Run the participant twice, each time from the database snapshot, with a clean browser and a new subagent.
6. Count the gestures from each transcript and compare the database with its snapshot.
7. Label every claim of the participant against code and data: confirmed, rig artefact, perception or unverified.
8. Write the report: the plain story first, then the tables.
9. After the repairs, retest with the same note and snapshot and compare step by step.

The skill refuses to run a participant on production, whoever asks. A participant clicks whatever it finds, so the skill requires the copy and gives the participant an account with an ordinary employee's rights. Only confirmed claims become repair candidates.

## Requirements

- Claude Code. The participant is a Claude Code subagent, and the counting script reads Claude Code transcripts.
- A browser driver: Claude in Chrome, or agent-browser. `references/drivers.md` describes what each one lets the participant see.
- An isolated copy of the app and its data. Without it the skill stops after the steps that write nothing.
- Python 3.9 or newer for the counting script, which uses only the standard library.

Before a participant runs, the skill also needs two facts from you: whose job the participant imitates, and what leaves the app, such as email, SMS and calls to external APIs.

## Installation

As a Claude Code plugin:

```text
/plugin marketplace add deiu25/naive-agent-usability-test
/plugin install naive-agent-usability-test@naive-agent-usability-test
```

With the Skills CLI:

```bash
npx skills add deiu25/naive-agent-usability-test --global --agent claude-code
```

By hand:

```bash
git clone https://github.com/deiu25/naive-agent-usability-test ~/.claude/skills/naive-agent-usability-test
```

The plugin manifests validate with `claude plugin validate` in Claude Code 2.1.325. Check the counting script on your machine with `python scripts/analyze_transcript.py --selftest`.

## Usage

Ask for the test in your own words and name the flow:

```text
Run the new-hire usability test on our order portal. The flow: a new dispatcher
receives three orders and has to get them onto Thursday's delivery run.
```

```text
We fixed the findings of the last new-hire test. Rerun it and compare step by step.
```

The skill keeps the artefacts of each test in one folder outside the app's repository: the rig scripts, the note, one folder per run, and the reports. The templates are in English. `templates/ro/` holds Romanian versions, the language of the first runs. Write the note in the language of the app's users.

A report opens with the plain story and ends with a table of the participant's claims. These four rows come from a real report, with the identifying details removed:

| The participant's claim | Label | Evidence |
|---|---|---|
| The list jumps to the top after a save and the text being typed is lost | confirmed | the code redraws the whole list after each save; the database held a half-typed name |
| The mouse wheel does not scroll the page | rig artefact | the driver's scroll call does not move content that scrolls inside its own container |
| This screen counts 45 orders and the customer screen 44 | perception | one of the 45 orders belongs to another customer |
| Closing a dialog opened the account menu | unverified | a person with a mouse would settle it |

## Limits

The participant is an agent. It reads the whole screen and is patient, so a place where it gets stuck also stops a person, while a place it passes can still lose a person. One test covers one scenario, and the local copy says nothing about speed in production.

The test shows where a newcomer gets stuck; why the people who already use the app avoid a flow stays outside it.

The evidence so far comes from two flows of one application (PHP and SQL Server) and two browser drivers. Desktop, mobile and terminal apps are untried, and so are live sessions with a human participant.

## Evaluation and maintenance

[evals/](evals/README.md) holds the three scenarios of the controlled comparison, their fixtures and their assertions. CI runs the script's self-test on Python 3.9 and 3.12, checks that the Skills CLI finds the skill, and validates the plugin manifests.

The skill changes after real runs. When a run shows a rule that is missing or wrong, the moderator notes it at that step, and a review folds the notes into the skill. [task-observer](https://github.com/rebelytics/one-skill-to-rule-them-all) automates that capture and review, and a benchmark such as the one in `evals/` shows whether a change helped.

## Feedback and license

Open an issue with one of the forms when a run went wrong because of the skill, or when you tried a browser driver that `references/drivers.md` does not describe. Remove anything private first: no app names, accounts or screenshots of real data.

The skill is released under the MIT license. See [LICENSE](LICENSE).

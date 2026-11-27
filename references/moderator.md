# The moderator's checks: counting, claims, report, retest

Load triggers: after a participant run, before counting, labelling claims or writing a report; reading a retest or writing its conclusion

Steps 6-9 of the loop in `SKILL.md`.

## Contents

1. Counting
2. The database diff
3. Labelling every claim
4. Two runs
5. The report
6. Retest
7. The real measure

## 1. Counting

```bash
python -I -X utf8 <skill dir>/scripts/analyze_transcript.py [--driver agent-browser] \
    --step "1=<regex>" --step "2=<regex>" --help-open "<regex>" --help-close "<regex>" \
    <transcript.jsonl> <run folder>
```

It writes `actions.csv` (one row per tool call, with each gesture's label and, when asked, its step and
help mark), `log.md` (the participant's own text in order) and `participant-report.md` (its final report),
and prints the duration, the calls per tool, the gestures, the gestures and help per step, and the tools
outside the allowed set. Run it once without `--step` and `--help-*` to read the labels before writing
the patterns.

- **Gestures** are click, type, key, scroll, drag and hover. Screenshot, zoom and wait are looking, not
  doing. The gesture count from the script is the number the report uses. The participant's own count
  usually differs (it counts tab closes, its own log lines, or guesses); report both when they differ by
  more than a few and say which one the tables use.
- **Per step**: before the runs, name for each step the first element only that step uses (a menu item,
  a button); the step starts at the first gesture on it, and a gesture on an earlier step's element takes
  the count back there. Write each as `--step NAME=REGEX` on the `label` column: the participant's own
  description of the click with Claude in Chrome, the element's name from the last annotated screenshot
  with agent-browser. The participant's step summaries are a fallback only when they carry timestamps: a
  participant that writes its log at the end leaves none.
- **Help is its own column.** Actions spent reading in-app help are counted apart from actions spent
  searching on screen. Name the help's open and close elements before the runs too (`--help-open`,
  `--help-close`; an Escape key also closes); the script counts help per step, inside the step totals,
  so no help number is rebuilt by hand. Help read before the first gesture is the participant's style:
  two participants differ there more than a fix moves the number.
- **Forbidden tools**: the script must print none. A run that used one keeps its report, but the steps
  where it used the tool are void.

## 2. The database diff

Run the verify-run query of the rig. Expected: only the ticket's records changed, no messages left. A
record outside the ticket that the test account touched is reported as a finding twice over: about the
participant (it went off the ticket) and about the app (what made the wrong record easy to touch, such
as a list that kept the previous selection). Then reset.

## 3. Labelling every claim

Every sentence of the participant's report of the form "the app does not X", "X is wrong", "X was lost",
"there is no explanation for X" is a claim. Before the report, give each one a label:

| Label | Evidence that earns it | How it goes into the report |
|---|---|---|
| confirmed | the code on the path the step runs (`file:line`), or a query on the data | a repair candidate, with the location |
| rig artefact | a property of the rig explains it (`references/rig.md`, section 6; test data age; local server) | out of the repair list; added to the brief if it was not there |
| perception | the code or the data shows the app does X; the participant believed otherwise | a clarity finding: "the participant believed...; the app does...; what would make it visible" |
| unverified | neither code nor data settles it | listed as such, with the check that would settle it |

How to look:

- Read the code that actually runs on that path (the handler, its callers), not a comment or a plan.
- "There is no explanation": search for hover text (`title`), help pages and inline hints for that
  element before writing it down. The participant cannot see hover text.
- "This label or value is wrong": look for the users' own convention first, in the documents they wrote
  by hand before the app or in the data. A value the domain writes that way on purpose is not a defect.
- "I lost everything": check what the close button does to the form's values before calling it data loss.
- A cause you found that the participant did not report is a confirmed finding too.

## 4. Two runs

Make one table: each claim, one column per run, its label. Claims both participants met are the
credible core; a claim from one run only stays in the report, marked as such. The difference between
the two runs' totals is the size of the noise; say it next to any comparison.

## 5. The report

Fill `templates/report.md`. Its order matters: the plain story (what the task was, did they finish, where
they got stuck, in sentences a manager reads) before any table; then cost per step; then the places
where a new person gets lost, in the order of the flow, each with its evidence and "what would help";
then what went well; then what the test does not show.

## 6. Retest

After repairs: the same brief, the same snapshot, new participants; two runs for the final retest.

- Re-derive the step split before counting: the repairs may have added a shortcut into a later step
  (a link from an earlier screen) or moved a step's evidence into an earlier one. List each step's entry
  elements again, the old ones plus every new shortcut and the elements of a return to an earlier step
  for a re-check. Run the new split on the baseline transcripts first: the baseline numbers must come out
  unchanged, or the comparison measures the rule, not the repair.
- When a repair moved a step's evidence into an earlier step, the gestures left in the later step are
  re-verification: report them so, and name where the participant first saw the evidence.
- Compare per step against the baseline and against the targets set when the repairs were planned.
- A step that got worse is a finding even when the total fell; say which repair or which difference in
  participant style explains it, or that it is unexplained.
- Gains on "finding the start" next to help read before the first gesture are not yet the fix's gain.
- One baseline run and one retest run show a direction, not a size: ask for the second run before a
  firm conclusion, and give the first conclusion in those terms.
- Label the new claims exactly as in section 3; a claim the repair was meant to remove and that is
  still there is reported first.

## 7. The real measure

The agent's numbers predict; people's use confirms. A few weeks after the last deploy (four is a
working default), rerun the step 1 queries on production, read-only, and compare per step and per person
with the first measure. Why the real users avoid a flow is not in any transcript: the report says so
and leaves that question to the person who asked for the test.

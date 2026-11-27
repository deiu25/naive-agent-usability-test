# Browser drivers: what the participant gets, what each one distorts

Load triggers: choosing the participant's browser; filling the tool section of the brief; counting a run made with a driver other than Claude in Chrome

The rest of the method does not depend on the driver. What does: the tool names in the brief, the
gesture/looking mapping the counting script uses, how a clean browser is made, and the driver's own
artefacts, which go into the brief so they are not reported as problems.

## Contents

1. Before choosing: the browser must reach the rig, and one look must be cheap
2. Claude in Chrome (default)
3. agent-browser (annotated screenshots)
4. agent-browser on coordinates
5. Another driver

## 1. Before choosing: the browser must reach the rig, and one look must be cheap

A rig served on `localhost` is reachable only from a browser on the same machine. Before the first run:
list the connected browsers (`list_connected_browsers` for Claude in Chrome) and check the one in use is on
the rig's machine; then load the rig's login page in it and see that request in the app's server log. A
browser on another machine needs the rig on an address it can reach, which reopens the isolation checklist.

Then take one look, with the driver's normal call, at the flow's heaviest page (the widest table, the
longest list) and read the size of what came back. A run needs dozens of looks: above a few thousand
tokens per look the participant's context fills before the flow ends, and the driver is out for this
flow. An annotated agent-browser screenshot of a 25-row grid with 20 columns returned about 600 numbered
elements, most of them outside the viewport, and passed 25,000 tokens; the coordinate variant (section 4)
returned the image alone.

If the default driver is not available, say so and ask before switching: the driver changes what the
participant can see, so the user decides.

## 2. Claude in Chrome (default)

- Allowed tools: `mcp__claude-in-chrome__computer`, `mcp__claude-in-chrome__tabs_context_mcp`,
  `mcp__claude-in-chrome__tabs_close_mcp`. ToolSearch line:
  `select:mcp__claude-in-chrome__computer,mcp__claude-in-chrome__tabs_context_mcp,mcp__claude-in-chrome__tabs_close_mcp`.
- Gestures: `left_click`, `right_click`, `double_click`, `triple_click`, `type`, `key`, `scroll`,
  `left_click_drag`, `hover`, `scroll_to`. Looking: `screenshot`, `zoom`, `wait`.
- Clean browser: log out, then clear the test origin's `localStorage` and `sessionStorage` on the login page.
- Counting: `scripts/analyze_transcript.py` (default driver).
- Artefacts for the brief: the table in `references/rig.md`, section 6.

## 3. agent-browser (annotated screenshots)

No coordinate click: `agent_browser_screenshot` with `annotate: true` puts a number on every clickable or
typable element, and clicks and typing go to `@eN`. The number list covers the whole page, not the
viewport, so this variant suits small pages only; measure it first (section 1) and use section 4 for a page
with a data grid.

- Open the session as the moderator with `allowedDomains` set to the rig's host (`["localhost"]`): the
  browser then refuses every other host, so an absolute link to production in a page goes nowhere. Prove
  it once with a harmless outside host, never with production.

- Allowed tools: `mcp__agent-browser__agent_browser_` + `screenshot`, `click`, `type`, `press`, `scroll`,
  `wait_ms`, `back`, `tab_list`, `tab_switch`, `tab_close`; every call with the session name the moderator
  opened. Forbidden by name in the brief: `open`, `snapshot`, `get_text`, `read`, `eval`, `fill`, `select`,
  `wait_for_text`, `find`. The brief also says `selector` takes only an `@eN` from the last annotated
  screenshot, never CSS, and no cropped screenshots: left unsaid, a participant guesses CSS selectors
  (a dialog body, a table wrapper) to crop and to scroll, which no person can do.
- Gestures: `click`, `type`, `press`, `scroll`, `back`, `tab_switch`. Looking: `screenshot`, `wait_ms`.
- Clean browser: close the named session (`agent_browser_close`) and open it again on the logout page; a
  reopened session starts with an empty profile. Check `localStorage.length` with `agent_browser_eval` as
  the moderator.
- Counting: `scripts/analyze_transcript.py --driver agent-browser`.
- Artefacts, all told in the brief:
  - the number list returned with each screenshot holds elements outside the viewport (a link far below
    the visible part of the page): tell the participant to use only numbers visible in the image;
  - the numbers mark every clickable thing and the list names them, an affordance hint a person does not
    get: a step the participant passes is weaker evidence than with the default driver;
  - no hover at all, so `title` text is never seen;
  - the default viewport is smaller than a laptop screen: read its size in the dry run and state it in
    the report;
  - `agent_browser_scroll` without a selector does not move a page or dialog that scrolls inside its own
    container; the participant falls back on clicking inside and pressing PageDown. Find in the dry run
    how each scrolling container of the flow moves with the allowed calls, and write it in the brief;
  - a ref taken before the page redraws part of itself fails as "stale ref": the participant must take a
    new screenshot, so a redraw costs it a gesture a person would not spend.

## 4. agent-browser on coordinates

The participant looks at plain screenshots and clicks by position, as with Claude in Chrome. It needs the
agent-browser MCP server started with the profiles `core,mobile` (`agent-browser mcp --tools core,mobile`;
a change to the host's MCP configuration: ask the user, then reconnect the server) and was exercised on
agent-browser 0.41 with its headless Chrome.

- Moderator setup per run: `agent_browser_open` with the session name, the rig's logout page,
  `allowedDomains` set to the rig's host and `extraArgs: ["--hide-scrollbars", "false"]` (headless
  screenshots hide scrollbars by default, and a person sees them); then `agent_browser_set_viewport` to a
  laptop size (1366 x 768) and the login page.
- Allowed tools: `mcp__agent-browser__agent_browser_` + `screenshot` (no `annotate`, no `selector`),
  `wait_ms`, `mouse_move`, `mouse_down`, `mouse_up`, `mouse_wheel`, `keyboard_type`, `press`, `tab_list`,
  `tab_switch`, `tab_close`; every call with the session name. Forbidden by name: `open`, `click`, `type`,
  `fill`, `select`, `scroll`, `snapshot`, `get_text`, `read`, `eval`, `find`, `wait_for_text`, `set_viewport`.
- Gestures: a click is `mouse_move` + `mouse_down` + `mouse_up` and counts once; a drag (a `mouse_move`
  while the button is down) counts once; a `mouse_move` not followed by `mouse_down` is a hover;
  `mouse_wheel`, `keyboard_type`, `press`, `tab_switch`. Looking: `screenshot`, `wait_ms`, `tab_list`.
- Counting: `scripts/analyze_transcript.py --driver agent-browser-mouse --step-from NAME=HH:MM:SS ...`. The
  gestures carry no element name, so the moderator reads each step's start off a run without a split
  (`references/moderator.md`, section 1); a `START STEP N` line the participant writes as it goes
  (`--step-text`) spares that, but it may arrive only in the final report. Help is counted by hand.
- Clean browser: as in section 3 (close the named session, open it again on the logout page, check
  `localStorage.length`).
- Artefacts, all told in the brief:
  - native dropdown lists and a date field's calendar are drawn in the screenshot, but a click on an option
    or a day does not reach them: click the control, then arrows and Enter; digits one by one with `press`
    in a date field, where `keyboard_type` does nothing;
  - `mouse_wheel` scrolls only vertically (it ignores `dx` and a held Shift): a table wider than the
    window moves by dragging its scrollbar, which shows only with `--hide-scrollbars false`;
  - hover text the page draws appears after a `mouse_move`; the browser's own `title` text does not;
  - after an export the browser shows nothing; the request in the rig's log is the evidence;
  - a click costs three calls and a person's one: compare gestures, not calls, with another driver's run.

## 5. Another driver

Before the first run, write its section here from one moderator session with it: the allowed tools and
the ToolSearch line, which calls are gestures, how a clean browser is made, what the participant sees that
a person would not (and the reverse), and how its transcript is counted. Ask the user before using it.

# Browser drivers: what the participant gets, what each one distorts

Load triggers: choosing the participant's browser; filling the tool section of the brief; counting a run made with a driver other than Claude in Chrome

The rest of the method does not depend on the driver. What does: the tool names in the brief, the
gesture/looking mapping the counting script uses, how a clean browser is made, and the driver's own
artefacts, which go into the brief so they are not reported as problems.

## Contents

1. Before choosing: the browser must reach the rig
2. Claude in Chrome (default)
3. agent-browser (annotated screenshots)
4. Another driver

## 1. Before choosing: the browser must reach the rig

A rig served on `localhost` is reachable only from a browser on the same machine. Before the first run:
list the connected browsers (`list_connected_browsers` for Claude in Chrome) and check the one in use is on
the rig's machine; then load the rig's login page in it and see that request in the app's server log. A
browser on another machine needs the rig on an address it can reach, which reopens the isolation checklist.

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
typable element, and clicks and typing go to `@eN`.

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

## 4. Another driver

Before the first run, write its section here from one moderator session with it: the allowed tools and
the ToolSearch line, which calls are gestures, how a clean browser is made, what the participant sees that
a person would not (and the reverse), and how its transcript is counted. Ask the user before using it.

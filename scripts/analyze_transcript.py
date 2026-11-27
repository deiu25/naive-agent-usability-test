"""Count what a usability-test participant did, from its Claude Code transcript (JSONL).

Usage:  python -I -X utf8 analyze_transcript.py [--driver agent-browser] [--step NAME=REGEX ...]
            [--help-open REGEX] [--help-close REGEX] <transcript.jsonl> <run folder>
        python -I -X utf8 analyze_transcript.py --selftest

The default driver is Claude in Chrome. With --driver agent-browser, each allowed agent-browser call is
counted as the same gesture or look (references/drivers.md); its other tools stay forbidden.

Every gesture gets a label: with Claude in Chrome the participant's own description of the action, with
agent-browser the name the last annotated screenshot gave the element (plus the key or the typed text).
The labels are what the step and help options match, case-insensitive:
  --step NAME=REGEX  repeat once per step, in the flow's order. A gesture whose label matches a step's
                     REGEX starts that step, or re-enters it, and counts to it; the first --step that
                     matches wins. Gestures before any match count to "start".
  --help-open REGEX  a gesture matching it opens a help stretch; --help-close REGEX or an Escape key
                     closes it. Both ends count as help. Help is counted per step, inside the step totals.

Writes into the run folder:
  actions.csv            one row per tool call: time, tool, action, description, coordinates, saved,
                         label, and, with --step or --help-open, the step and the help mark of each gesture
  log.md                 every text the participant wrote, in order (its think-aloud log)
  participant-report.md  its final report (the longest text of its handback call), when there is one
and prints a short summary: duration, calls per tool, gestures, the tools used outside the allowed set,
and the gestures and help per step when asked.
"""
import csv
import json
import os
import re
import sys
import tempfile
from collections import Counter
from datetime import datetime

ALLOWED = {
    "mcp__claude-in-chrome__computer",
    "mcp__claude-in-chrome__tabs_context_mcp",
    "mcp__claude-in-chrome__tabs_close_mcp",
    "ToolSearch",
    "SubagentHandback",   # the participant handing its final report back to the moderator
}
BROWSER = "mcp__claude-in-chrome__computer"
# Actions that are a person's gestures; screenshot, zoom and wait are looking and waiting.
GESTURES = {"left_click", "right_click", "double_click", "triple_click", "type", "key", "scroll",
            "left_click_drag", "hover", "scroll_to"}
# agent-browser call -> (tool, action) of the default driver's model; tools not listed stay forbidden.
AB = "mcp__agent-browser__agent_browser_"
AGENT_BROWSER = {
    "screenshot": (BROWSER, "screenshot"), "wait_ms": (BROWSER, "wait"),
    "click": (BROWSER, "left_click"), "type": (BROWSER, "type"), "press": (BROWSER, "key"),
    "scroll": (BROWSER, "scroll"), "back": (BROWSER, "key"), "tab_switch": (BROWSER, "left_click"),
    "tab_list": ("mcp__claude-in-chrome__tabs_context_mcp", ""),
    "tab_close": ("mcp__claude-in-chrome__tabs_close_mcp", ""),
}


def as_default_driver(name, inp, driver):
    """An agent-browser call rewritten as the default driver's; anything else unchanged."""
    if driver != "agent-browser" or not name.startswith(AB) or name[len(AB):] not in AGENT_BROWSER:
        return name, inp
    short = name[len(AB):]
    tool, action = AGENT_BROWSER[short]
    summary = " ".join(str(inp.get(k, "")) for k in ("selector", "key", "text") if inp.get(k)).strip()
    return tool, {"action": action, "action_summary": f"{short} {summary}".strip()[:120]}


def annotations(content):
    """{"@eN": name} from the result of an annotated agent-browser screenshot; {} when there is none."""
    names = {}
    for block in content if isinstance(content, list) else []:
        text = block.get("text", "") if isinstance(block, dict) else ""
        if not text.startswith("{"):
            continue
        try:
            items = json.loads(text)["response"]["data"]["annotations"]
        except (json.JSONDecodeError, KeyError, TypeError):
            continue
        names = {"@" + a["ref"]: a.get("name", "") for a in items}
    return names


def label_of(name, inp, names):
    """What the gesture acted on, in words a step or help pattern can match."""
    if name.startswith(AB):
        element = names.get(str(inp.get("selector", "")), "")
        return " ".join(x for x in (element, str(inp.get("key", "")), str(inp.get("text", ""))) if x)[:120]
    return " ".join(x for x in (str(inp.get("action_summary", "")), str(inp.get("text", ""))) if x)[:120]


def blocks(line):
    message = line.get("message") or {}
    content = message.get("content")
    if isinstance(content, str):
        return message.get("role"), [{"type": "text", "text": content}]
    return message.get("role"), content or []


def split(actions, steps=(), help_open=None, help_close=None):
    """Marks each gesture with its step and help flag; returns gestures and help gestures per step."""
    per_step, help_per_step = Counter(), Counter()
    step, in_help = "start", False
    for a in actions:
        if a["tool"] != BROWSER or a["action"] not in GESTURES:
            continue
        label = a["label"]
        for name, rx in steps:
            if rx.search(label):
                step = name
                break
        if help_open and help_open.search(label):
            in_help = True
        per_step[step] += 1
        a["step"], a["help"] = step, "yes" if in_help else ""
        if in_help:
            help_per_step[step] += 1
            closes = help_close and help_close.search(label)
            if closes or (a["action"] == "key" and re.search(r"\besc(ape)?\b", label, re.I)):
                in_help = False
    return per_step, help_per_step


def analyze(path, folder, driver="claude-in-chrome", steps=(), help_open=None, help_close=None):
    os.makedirs(folder, exist_ok=True)
    uses, results, texts, tool_errors = [], {}, [], 0
    with open(path, encoding="utf-8") as f:
        for raw in f:
            raw = raw.strip()
            if not raw:
                continue
            try:
                line = json.loads(raw)
            except json.JSONDecodeError:
                continue
            role, content = blocks(line)
            for b in content:
                if not isinstance(b, dict):
                    continue
                if b.get("type") == "tool_use":
                    uses.append((line.get("timestamp", ""), b))
                elif b.get("type") == "tool_result":
                    results[b.get("tool_use_id")] = b.get("content")
                    if b.get("is_error"):
                        tool_errors += 1
                elif b.get("type") == "text" and role == "assistant" and b.get("text", "").strip():
                    texts.append(b["text"].strip())

    actions, names = [], {}
    for time, b in uses:
        raw_name, raw_inp = b.get("name", ""), b.get("input") or {}
        if raw_name == AB + "screenshot" and raw_inp.get("annotate"):
            names = annotations(results.get(b.get("id"))) or names
        label = label_of(raw_name, raw_inp, names)
        name, inp = as_default_driver(raw_name, raw_inp, driver)
        if name == "SubagentHandback":
            report = max((v for v in inp.values() if isinstance(v, str)), key=len, default="")
            with open(os.path.join(folder, "participant-report.md"), "w", encoding="utf-8") as r:
                r.write(report + "\n")
        description = inp.get("action_summary") or ""
        if not description and inp.get("action") in ("type", "key"):
            description = str(inp.get("text") or "")[:80]
        actions.append({
            "time": time, "tool": name, "action": inp.get("action", ""),
            "description": description,
            "coordinates": json.dumps(inp.get("coordinate")) if inp.get("coordinate") else "",
            "saved": "yes" if inp.get("save_to_disk") else "", "label": label,
        })

    per_step, help_per_step = split(actions, steps, help_open, help_close)
    fields = ["time", "tool", "action", "description", "coordinates", "saved", "label"]
    if steps or help_open:
        fields += ["step", "help"]
    with open(os.path.join(folder, "actions.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(actions)
    with open(os.path.join(folder, "log.md"), "w", encoding="utf-8") as f:
        for t in texts:
            f.write(t + "\n\n")

    times = sorted(a["time"] for a in actions if a["time"])
    minutes = None
    if len(times) >= 2:
        t0 = datetime.fromisoformat(times[0].replace("Z", "+00:00"))
        t1 = datetime.fromisoformat(times[-1].replace("Z", "+00:00"))
        minutes = (t1 - t0).total_seconds() / 60
    per_tool = Counter(a["tool"] for a in actions)
    per_action = Counter(a["action"] for a in actions if a["tool"] == BROWSER)
    gestures = sum(n for a, n in per_action.items() if a in GESTURES)
    looking = sum(n for a, n in per_action.items() if a not in GESTURES)
    # Self-checks: every browser call is either a gesture or looking/waiting; every gesture has one step.
    assert gestures + looking == per_tool.get(BROWSER, 0)
    assert sum(per_step.values()) == gestures
    return {
        "calls": len(actions), "minutes": minutes, "tool_errors": tool_errors,
        "per_tool": dict(per_tool), "per_action": dict(per_action.most_common()),
        "gestures": gestures, "looking": looking, "texts": len(texts),
        "forbidden": {u: n for u, n in per_tool.items() if u not in ALLOWED},
        "per_step": dict(per_step), "help_per_step": dict(help_per_step),
    }


def report(r, folder, split_asked):
    duration = f"{r['minutes']:.0f} minutes" if r["minutes"] is not None else "unknown"
    print(f"tool calls: {r['calls']}; duration: {duration}; tool errors: {r['tool_errors']}")
    print("per tool:", r["per_tool"])
    print("browser actions:", r["per_action"])
    print(f"gestures (click, type, key, scroll, drag, hover): {r['gestures']}; looking and waiting: {r['looking']}")
    if split_asked:
        print("gestures per step:", r["per_step"])
        print(f"help gestures per step (inside the step totals): {r['help_per_step']};"
              f" total {sum(r['help_per_step'].values())}")
    print("FORBIDDEN tools used:", r["forbidden"] or "none")
    print(f"participant texts: {r['texts']}; written in {folder}: actions.csv, log.md"
          " (+ participant-report.md if handed back)")


def selftest():
    def use(name, id_="", **inp):
        return {"type": "tool_use", "id": id_, "name": name, "input": inp}

    lines = [
        {"timestamp": "2026-01-05T09:00:00.000Z", "message": {"role": "assistant", "content": [
            {"type": "text", "text": "1. [Sign-in] I want: to get in"}, use("ToolSearch", query="select:x")]}},
        {"timestamp": "2026-01-05T09:01:00.000Z", "message": {"role": "assistant", "content": [
            use(BROWSER, action="screenshot"), use(BROWSER, action="left_click", coordinate=[10, 20])]}},
        {"timestamp": "2026-01-05T09:02:00.000Z", "message": {"role": "user", "content": [
            {"type": "tool_result", "is_error": True, "content": "x"}]}},
        {"timestamp": "2026-01-05T09:03:00.000Z", "message": {"role": "assistant", "content": [
            use(BROWSER, action="type", text="TEST-123"), use(BROWSER, action="scroll"),
            use(BROWSER, action="wait"), use("Read", file_path="app.js")]}},
        {"timestamp": "2026-01-05T09:10:00.000Z", "message": {"role": "assistant", "content": [
            use("SubagentHandback", summary="ok", report="Final report: every step done, 3 gestures.")]}},
        "not json",
    ]
    with tempfile.TemporaryDirectory() as d:
        path = os.path.join(d, "t.jsonl")
        with open(path, "w", encoding="utf-8") as f:
            for ln in lines:
                f.write((ln if isinstance(ln, str) else json.dumps(ln)) + "\n")
        r = analyze(path, os.path.join(d, "run"))
        expected = {"calls": 8, "gestures": 3, "looking": 2, "tool_errors": 1, "texts": 1,
                    "forbidden": {"Read": 1}, "minutes": 10.0}
        bad = {k: (r[k], v) for k, v in expected.items() if r[k] != v}
        with open(os.path.join(d, "run", "participant-report.md"), encoding="utf-8") as f:
            handback = f.read().strip()
        with open(os.path.join(d, "run", "actions.csv"), encoding="utf-8") as f:
            rows = sum(1 for _ in f) - 1
    if handback != "Final report: every step done, 3 gestures.":
        bad["participant-report.md"] = handback
    if rows != 8:
        bad["actions.csv rows"] = rows

    # The same run made with agent-browser: allowed calls count alike, snapshot stays forbidden.
    ab = [{"timestamp": "2026-01-05T09:00:00.000Z", "message": {"role": "assistant", "content": [
        use(AB + "screenshot", annotate=True), use(AB + "click", selector="@e3"),
        use(AB + "type", selector="@e1", text="TEST-123"), use(AB + "press", key="Enter"),
        use(AB + "snapshot"), use(AB + "tab_list")]}}]
    with tempfile.TemporaryDirectory() as d:
        path = os.path.join(d, "t.jsonl")
        with open(path, "w", encoding="utf-8") as f:
            f.write(json.dumps(ab[0]) + "\n")
        r = analyze(path, os.path.join(d, "run"), "agent-browser")
        plain = analyze(path, os.path.join(d, "run0"))
    if (r["gestures"], r["looking"], r["forbidden"]) != (3, 1, {AB + "snapshot": 1}):
        bad["agent-browser"] = (r["gestures"], r["looking"], r["forbidden"])
    if plain["gestures"] != 0 or len(plain["forbidden"]) != 6:
        bad["agent-browser without --driver"] = (plain["gestures"], plain["forbidden"])

    # Steps and help from the annotated names: re-entry into a step, help closed by a button and by Escape.
    ann = {"response": {"data": {"annotations": [
        {"ref": "e1", "name": "Sign in"}, {"ref": "e2", "name": "Guide"},
        {"ref": "e3", "name": "Got it"}, {"ref": "e4", "name": "Orders"}, {"ref": "e5", "name": "Customers"}]}}}
    calls = [use(AB + "screenshot", "s1", annotate=True), use(AB + "click", selector="@e1"),
             use(AB + "click", selector="@e5"), use(AB + "click", selector="@e2"), use(AB + "scroll"),
             use(AB + "click", selector="@e3"), use(AB + "type", selector="@e5", text="Example Ltd"),
             use(AB + "click", selector="@e4"), use(AB + "click", selector="@e2"),
             use(AB + "press", key="Escape"), use(AB + "click", selector="@e5")]
    steps_lines = [{"timestamp": "2026-01-05T09:00:00.000Z", "message": {"role": "assistant", "content": calls[:1]}},
                   {"timestamp": "2026-01-05T09:00:01.000Z", "message": {"role": "user", "content": [
                       {"type": "tool_result", "tool_use_id": "s1",
                        "content": [{"type": "text", "text": json.dumps(ann)}]}]}},
                   {"timestamp": "2026-01-05T09:00:02.000Z", "message": {"role": "assistant", "content": calls[1:]}}]
    with tempfile.TemporaryDirectory() as d:
        path = os.path.join(d, "t.jsonl")
        with open(path, "w", encoding="utf-8") as f:
            for ln in steps_lines:
                f.write(json.dumps(ln) + "\n")
        r = analyze(path, os.path.join(d, "run"), "agent-browser",
                    [("customers", re.compile("^Customers", re.I)), ("orders", re.compile("^Orders$", re.I))],
                    re.compile("^Guide$", re.I), re.compile("^Got it$", re.I))
    if (r["per_step"], r["help_per_step"]) != ({"start": 1, "customers": 6, "orders": 3},
                                               {"customers": 3, "orders": 2}):
        bad["steps and help"] = (r["per_step"], r["help_per_step"])
    if bad:
        print("SELFTEST FAILED:", bad)
        return 1
    print("selftest ok: 8 calls, 3 gestures, 2 looking, 1 forbidden tool, 1 tool error, report extracted;"
          " agent-browser: 3 gestures, 1 look, snapshot forbidden; steps with re-entry and help: 1/6/3, help 3/2")
    return 0


if __name__ == "__main__":
    args = sys.argv[1:]
    if args == ["--selftest"]:
        sys.exit(selftest())
    driver, steps, opts, files = "claude-in-chrome", [], {}, []
    while args:
        a = args.pop(0)
        if a in ("--driver", "--step", "--help-open", "--help-close"):
            if not args:
                sys.exit(f"{a} needs a value\n\n{__doc__}")
            v = args.pop(0)
            if a == "--driver":
                driver = v
            elif a == "--step":
                name, sep, rx = v.partition("=")
                if not sep or not name:
                    sys.exit(f"--step takes NAME=REGEX, got {v!r}")
                steps.append((name, re.compile(rx, re.I)))
            else:
                opts[a] = re.compile(v, re.I)
        else:
            files.append(a)
    if len(files) != 2 or driver not in ("claude-in-chrome", "agent-browser"):
        sys.exit(__doc__)
    r = analyze(files[0], files[1], driver, steps, opts.get("--help-open"), opts.get("--help-close"))
    report(r, files[1], bool(steps or opts))

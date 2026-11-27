"""Assertion A4: the participant's ticket names no screen or button of the app outside its rules section.

Usage: python -I -X utf8 check_ticket_labels.py <ticket.md> ticket-labels.txt
       python -I -X utf8 check_ticket_labels.py --selftest
Prints every label hit with its line and whether the line sits under a heading about the test's rules.
"""
import os
import re
import sys
import tempfile

RULES_HEADING = re.compile(r"^#+ .*(regul|cum lucrezi|unelt|limit)", re.I)


def fold(s):
    return s.lower().translate(str.maketrans("ăâîșşțţ", "aaisstt"))


def check(ticket, labels_file):
    labels = [fold(x.strip()) for x in open(labels_file, encoding="utf-8") if x.strip()]
    hits, in_rules = [], False
    for n, line in enumerate(open(ticket, encoding="utf-8"), 1):
        if line.startswith("#"):
            in_rules = bool(RULES_HEADING.match(line))
        low = fold(line)
        for lab in labels:
            if re.search(r"\b" + re.escape(lab), low):
                hits.append((n, lab, in_rules, line.strip()[:120]))
    return hits


def selftest():
    with tempfile.TemporaryDirectory() as d:
        lab = os.path.join(d, "l.txt")
        open(lab, "w", encoding="utf-8").write("Rezerva stoc\nGenereaza aviz\n")
        t = os.path.join(d, "b.md")
        open(t, "w", encoding="utf-8").write("# Bilet\nApasa Rezervă stoc la fiecare comanda.\n## Regulile testului\nNu apasa Genereaza aviz de doua ori.\n")
        hits = check(t, lab)
    ok = len(hits) == 2 and hits[0][2] is False and hits[1][2] is True
    print("selftest", "ok" if ok else "FAILED", hits)
    return 0 if ok else 1


if __name__ == "__main__":
    if sys.argv[1:] == ["--selftest"]:
        sys.exit(selftest())
    hits = check(sys.argv[1], sys.argv[2])
    for n, lab, rules, text in hits:
        print(f"line {n} [{'rules' if rules else 'TASK'}] {lab}: {text}")
    print(f"{sum(1 for h in hits if not h[2])} hits outside the rules sections, {sum(1 for h in hits if h[2])} inside")

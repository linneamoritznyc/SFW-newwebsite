#!/usr/bin/env python3
"""Check that every rule in site.css actually applies.

    python3 tools/csscheck.py

WHY THIS EXISTS

Merging two branches that had both appended to the end of site.css produced
a stylesheet that was valid, parsed without complaint, and silently wrong.
One side's `@media (prefers-reduced-motion: reduce) {` was left open, so two
hundred lines of the other side's rules ended up nested inside it. Every one
of them was ignored, unless the visitor happened to have reduced motion
switched on. The page went out with an unstyled video player on it.

Nothing caught it. The build ran, the link checker passed, the image checker
passed, the browser reported no errors, and the page was broken.

So this checks the two things that go wrong when a stylesheet is edited by
more than one hand at once:

  1. the braces balance
  2. the rules that carry the page sit at the top level, not inside an
     at-rule that was never closed

A selector nested one level deep is not always wrong, since that is exactly
what a media query is for. What is always wrong is a LAYOUT rule sitting
inside a preference query, so the list below names the selectors that must
apply to everyone.
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSS = os.path.join(ROOT, "css", "site.css")

# Rules that build the page rather than decorate it. If one of these is
# nested, something on the site is unstyled.
MUST_BE_TOP_LEVEL = [
    ".theatre {", ".theatre__stage", ".theatre__list", ".theatre__item",
    ".theatre__panel {", ".specimen {", ".drawer {",
    ".btn {", ".chip {", ".input {",
    "body.t-learn", "body.t-science", "body.t-practice", "body.t-legacy",
    ".wrap {", ".grid {", ".stratum {", ".site-header {", ".site-footer {",
]


def scan(text):
    """Every selector's brace depth, and the running balance."""
    depth = 0
    line = 1
    found = {}
    i = 0
    while i < len(text):
        ch = text[i]
        if ch == "\n":
            line += 1
        elif ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth < 0:
                return found, depth, line
        for want in MUST_BE_TOP_LEVEL:
            if want not in found and text.startswith(want, i):
                found[want] = (line, depth)
        i += 1
    return found, depth, line


def main():
    text = open(CSS, encoding="utf-8").read()
    found, depth, lines = scan(text)
    print("%s, %d lines" % (os.path.relpath(CSS, ROOT), lines))

    bad = []
    if depth != 0:
        bad.append("braces do not balance: %+d at the end of the file "
                   "(a block was left open or closed twice)" % depth)

    for want in MUST_BE_TOP_LEVEL:
        if want not in found:
            bad.append("%s is not in the stylesheet at all" % want)
        elif found[want][1] != 0:
            bad.append("%s is nested %d level(s) deep at line %d, so it applies to nobody"
                       % (want, found[want][1], found[want][0]))

    if bad:
        print("\n%d problem(s):" % len(bad))
        for b in bad:
            print("  " + b)
        return 1
    print("braces balance, and all %d load-bearing rules are at the top level"
          % len(MUST_BE_TOP_LEVEL))
    return 0


if __name__ == "__main__":
    sys.exit(main())

# Dr. Elaine Ingham lecture copy: placement plan

Branch `elaine-lecture-copy`, written 3 October 2026. Pull request into `claude/session-gni7rl`.

**About "main".** This repository has no branch called `main`. Its default branch, and the one Vercel builds production from, is `claude/session-gni7rl`. This branch was cut from it and the pull request targets it. `claude/session-gni7rl` itself is untouched.

## How the copy was put in

- **The HTML is the source of truth, so the copy went straight into the HTML.** OPEN-ITEMS.md ("A note on the build script") says not to run `tools/build.py`: it would overwrite pages that have been edited by hand since. The build was **not** run.
- The same blocks are also recorded in `content/*.json` as new `elaine` keys (or `elaineAlternative`, `soilMicroscopyElaine`), each with `"status": "verify"` and the note, so the copy record matches the pages. `about-elaine.html` and `directory.html` have no content JSON, so they changed in the HTML only.
- Every new block has `<p class="todo" data-status="verify">Elaine lecture copy, approve: Linnea or Evan.</p>` beside it, so add `?notes=1` to the URL to see it. Some notes add one sentence about a specific risk.
- **Credit format.** Each quote names Dr. Elaine Ingham, "How to Build Great Soil, Part 1", Diego Footer, and links its timestamp (`https://www.youtube.com/watch?v=ErMHR6Mc4Bk&t=SECONDSs`). Each attributed line gets a `.source` line with the same link.
- **Purple.** Quotes use the existing `.testimonial` component with a new `.testimonial--legacy` modifier (in `css/site.css`, marked 3 October 2026): a Legacy Purple rule down the left and a purple credit link. That is the only new CSS, and nothing else on these pages turns purple.
- **No Copy Deck v1.0 sentence was changed, moved or deleted.** Everything new is an addition. One spelling change to the supplied copy: "programmes" became "programs", because the copy deck asks for American spelling.

## Checked facts

- **The video.** YouTube's oEmbed gives the title as "How to Build Great Soil - A Soil Science Masterclass with Dr. Elaine Ingham (Part 1 of 4)", uploaded by Diego Footer on 13 September 2021.
- **The view count.** YouTube showed **1,154,042 views** on 3 October 2026, read through YouTube's own page-data endpoint because the watch page returned a captcha. "Passed 1.1 million views" is true, so it went in, with the count and date on the source line.
- **Quote wording is not checked yet.** No transcript could be fetched: YouTube asked for a sign-in. Every quote and timestamp should be checked against the recording before approval. The verify notes cover this.

## Placement, block by block

| # | Block | File and location (JSON key) | Adds or sits beside | Conflict with existing copy |
| :-- | :-- | :-- | :-- | :-- |
| 1a | Hero heading option "Put the plant back in control." | Not live. Shown as a `?notes=1` note in the index.html hero (`home.json` `hero.elaineAlternative.h1`) | Alternative only | It would replace the live H1 "Join a global community of Soil Regenerators", so the live H1 stays. |
| 1b | Hero body option | Not live. In the same hero note (`hero.elaineAlternative.body`) | Alternative only | It would replace or repeat the live hero body. Kept as an option, as with 1a. |
| 1c | Teaching pillar, line 1 "Dr. Elaine trained people to read soil life under a microscope in a single day." | index.html, Programs section ("Learn with us") head, under the H2 (`learnWithUs.elaine`). Source 28:52. | Adds | The live homepage has no pillar block: the copy deck's four pillars were never built. Programs is the homepage's teaching section. **The lecture has her saying she *could* train anyone in a day; "trained people" is stronger. Check the wording.** |
| 1d | Teaching pillar, line 2 "...students in [number] countries." | Same place, as a `?notes=1` placeholder only | Placeholder | The number is missing and comes from Stephanie. The stats row already prints "100+ countries" (enrollment records, August 2026); confirm whether that is the same figure. |
| 2a | Science intro, 60% and cakes and cookies | science.html hero, after the intro (`science.json` `hero.elaine`). Source 11:58. | Adds | **The 60% decision is below.** |
| 2b | Soil food web: "Our job is to put back the full diversity." | science.html mechanism 1, a quote under the body (`mechanisms[0].elaine`). Source 25:44. | Beside | None. |
| 2c | Nutrient cycling: pizza delivery line, plus the quote "Put the plant back in control of its own life." | Mechanism 2, under the body (`mechanisms[1].elaine`). Sources 15:03 and 16:32. | Beside | No percentage added. The existing "large share" sentence and its Kuzyakov and Domanski (2000) basis are unchanged. |
| 2d | Soil structure: dinner table and string lines, plus the quote "The only thing that truly builds structure..." | Mechanism 3 (`mechanisms[2].elaine`). Sources 5:31, 9:55 and 4:25. | Beside | None. |
| 2e | Weeds: 20% of fixed energy | Mechanism 4 (`mechanisms[3].elaine`). Source 2:24. | Beside | A teaching number, attributed to her by name with its source, which meets the "named source" rule. Approvers should know it is her teaching figure, not a peer-reviewed one. |
| 2f | Protecting plants: gangsters line, plus the quote "There is no way to kill just the bad guys." | Mechanism 5 (`mechanisms[4].elaine`). Sources 7:32 and 7:06. | Beside | **The quote is a "not" sentence.** It is her verbatim words, so it was not rewritten. Drop it if the "no sentences that say what something is not" rule covers quotes too. |
| 2g | Carbon: "Every carbon-to-carbon bond is stored sunlight..." | Mechanism 6 (`mechanisms[5].elaine`). Source 1:53. | Beside | None. |
| 3a | About Elaine, teaching paragraph with 1.1 million views | about-elaine.html, new section "Her teaching" between "Her published record" and the photographs. HTML only. | Adds a section | The page has no teaching section, so this one is new, with the plain heading "Her teaching", which is new copy and needs approval too. The view count is sourced as described above. |
| 3b | Pull quote "I would love to train all of you..." | Same section, right column. Source 30:04. | Adds | None. |
| 3c | "Her students now teach in [number] countries..." | Same section, as a `?notes=1` placeholder only | Placeholder | The "authority to origin" line in docs/site-structure.md was never put on the live page, so this sits by the pull quote, the closest place. The number comes from Stephanie. |
| 4a | Learn intro, microscope in one day | learn.html hero, after the lede (`learn.json` `hero.elaine`). Source 28:52. | Adds | "programmes" changed to "programs". |
| 4b | Soil Microscopy paragraph | learn.html, All courses table, Soil Microscopy row, "What it is" cell, as a second paragraph (`programs[complete-practicum].soilMicroscopyElaine`) | Beside | None. The table has no separate per-program block, so the cell is that row. |
| 5 | Webinars block for YouTube visitors | learn-webinars.html hero, after the lede, with a link to the video (`webinars.json` `hero.elaine`) | Adds | The question was kept as written. The rules ban question **headlines**, and body copy on the site already asks questions, for example "Looking for the full backlog...?" on the same page. |
| 6 | Donate, monthly giving case | donate.html, "Monthly giving helps us plan ahead" column, under the H2 (`donate.json` `whyMonthly.elaine`) | Adds | **The team deleted the body line here on 8 September.** This refills that slot. Keep it or delete it again. "Funds the next trainee" is a promise to check with Evan. |
| 7 | Directory intro line | directory.html, under the lede in the page head. HTML only. | Adds | None. It matches the lede's "earned their title". |
| 8a | research.html | **Proposed only, page unchanged.** Under "Papers Published by Dr. Ingham", next to her 1985 paper "Review of the effects of twelve selected biocides on target and non-target soil organisms", the quote "There is no way to kill just the bad guys." (7:06) | Proposal | It has the same "not" issue as 2f. |
| 8b | practice.html | **Proposed only, page unchanged.** In the sMApp section, under the paragraph about the 400x microscope, the line "Dr. Elaine said she could train anyone to use a microscope in one day." (28:52) | Proposal | None. |

## The 60% decision

The nutrient cycling mechanism took out a percentage on purpose and rests on Kuzyakov and Domanski (2000). **It stays without any percentage**; nothing was added to it.

The 60% line went into the science page **intro** instead. There it opens with "Dr. Elaine taught that...", names her and carries its own source line linking 11:58. That meets the "clearly attributed to Elaine" condition and the "percentage with a named source" rule. The verify note on it says it shares a page with the hedged sentence, and that Kuzyakov and Domanski report lower shares for cereals. If you would rather not have two framings on one page, delete the block from `science.html` and from `content/science.json` `hero.elaine`. Nothing else depends on it.

## Left alone

about-governance.html, projects/, news/, /now, the legal pages, research.html, practice.html, and every existing sentence.

## Found along the way, not changed

- **The science page is missing the Kuzyakov source line.** `science.html` nutrient cycling prints no Kuzyakov and Domanski source line and no verify note, although `content/science.json` has both. The HTML and JSON have drifted apart.
- **Broken markup on donate.html.** It has curly quotes inside HTML attributes (`class=”todo”`, `class=”small”`, `href=”privacy.html”`). Because of this, one production note shows to every visitor ("pair with preset amounts...") and the privacy link is broken. Pre-existing; worth a one-line fix in a separate change.
- **A required doc is missing.** CLAUDE.md asks for `docs/Fable_Course_Audit_Sep_6_Linnea_Moritz.md`, which is not in the repository.

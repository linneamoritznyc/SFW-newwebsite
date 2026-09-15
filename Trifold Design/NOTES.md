# Trifold brochure, build notes

A running log for the six-panel print trifold. Add to this file rather than replacing it.

**Pass 1, 15 September 2026.** First build. Both spreads rendered, inspected at full size,
corrected for overflow and crop, re-rendered. Nothing outside `Trifold Design/` was touched.

---

## What is here

| File | What it is |
| :-- | :-- |
| `outside-spread.png` | Panels 1, 2, 3 left to right. Cover / Story / Teaching. |
| `inside-spread.png` | Panels 4, 5, 6 left to right. Research / Practice / Community. |
| `build/outside.html`, `build/inside.html` | The two spreads as markup. Edit these. |
| `build/trifold.css` | Print stylesheet. Tokens and `@font-face` rules copied from `css/site.css` sections 1 and 2. |
| `build/make-qr.py` | Generates the three QR codes into `build/qr/`. |
| `build/render.js` | Renders both HTML files to the PNGs and reports any panel overflow. |

Rebuild: `python3 "Trifold Design/build/make-qr.py"` then `node "Trifold Design/build/render.js"`,
both from the repository root.

## Geometry, as delivered

Both PNGs are **3375 x 2625 px**: the 3300 x 2550 trim asked for, plus **0.125in (37.5px) of bleed
on all four sides**. Bleed is included, not skipped.

- Panels 1, 2, 4, 5: 3.6875in wide (1106.25px at 300 DPI)
- Panels 3 and 6, the tuck-in panels: 3.625in wide (1087.5px)
- All panels 8.5in tall; the spread trims to 11in x 8.5in

3.6875in at 300 DPI is 1106.25px, not a whole pixel, so the individual panel widths carry a quarter
pixel. The three add to exactly 3300px, which is what matters. Safe margin is 0.28in in from trim on
every side; nothing but photography crosses it.

Layout is written in inches and points and rendered at `deviceScaleFactor` 3.125 (CSS defines 1in as
96px, and 300/96 = 3.125), so the type is specified at real print sizes rather than scaled up from
screen pixels. Body text is 8.4pt, headlines 15.5 to 20pt.

## The one thing to check before this goes to a printer

**The imposition is as specified in the brief, and a roll-fold sheet may not want it that way.** The
brief asked for panels 1, 2, 3 side by side on the outside and 4, 5, 6 side by side on the inside,
with the narrow tuck panel third on both sheets. On a letter roll fold the tuck panel is one physical
flap, so it lands on the right of one side of the sheet and on the **left** of the other. As built,
the narrow panel is on the right of both. Hand both PNGs to the printer and ask them to confirm the
imposition before plates are made; if they want the inside mirrored, swap the three `<section>`
blocks in `build/inside.html` and move the `panel--first` / `panel--last` classes with them, then
re-render. Nothing else changes.

---

## The gold and purple decision

`css/site.css` scopes two colours more tightly than the earlier print brief for this brochure did.
Neither was carried over silently.

**Harvest Gold `--gold` #C9A227 is not used anywhere in this brochure.** The token's comment in
`site.css` reads "Donate button only", and there is no donate button on any panel. The earlier brief
assigned gold to one of the three QR codes; that assignment is dropped rather than quietly honoured.

**Legacy Purple `--legacy` #6B4C7A is used for one thing only: the QR rule and code on panel 2**,
which is the Dr. Elaine story panel. The token's comment reads "Dr. Elaine content ONLY", and panel 2
is that content, so this is inside its documented scope rather than decorative spending elsewhere. It
appears nowhere else in the piece.

The three QR treatments are therefore:

| Panel | QR | Colour | Token |
| :-- | :-- | :-- | :-- |
| 2, Story | Watch a free webinar | #6B4C7A | `--legacy` |
| 3, Teaching | Apply for a scholarship | #3780B8 | `--edu` |
| 6, Community | Join the free community | #156826 | `--green` |

Linnea reassigned these on 15 September: the scholarship code belongs on the
education panel and the community code on the community panel. The webinar code
took the slot that left on the story panel, since the one-code-per-panel rule
holds and it is the lightest first step of the three.

**The colour follows the panel, not the code.** Each code is generated in its
panel's accent, so moving a code means regenerating it. Moving the markup alone
leaves all three mismatched, which is what happened on the first pass of this
change.

**Settled, 15 September.** Linnea signed off on the purple and gave design authority for the piece.
Legacy Purple stays on panel 2: that panel is Dr. Elaine's content, which is the token's documented
scope, and the QR rule is the only place it appears. Education Blue stays on panel 3 for the same
reason. Two accents against a green system read as accents rather than noise, and each one carries a
meaning rather than decorating.

## One rhythm across the panels

The band and the photograph are fixed heights, `--band-h` and `--photo-h`, not
sized to their contents. Before this they were neither: photographs ran from
1.05in to 2.05in and bands grew with the heading, so every panel's edges landed
somewhere different and the three columns read as unrelated pieces of paper.
Now a heading that needs fewer lines sits lower in its band rather than pulling
the photograph up with it.

The cover is the deliberate exception: it carries the wordmark where the others
carry a band.

Photographs are not cut with a shape of their own. **One curve is drawn across
the whole sheet and each picture is clipped by the segment of it that falls in
that panel**, so the three lower edges join into a single line across both
folds. Flat, the eye reads one horizon; folded, each panel still stands up.

The maths has to work in sheet coordinates, not per image. The cover's
photograph starts higher than the other five, because that panel carries the
wordmark where the others carry a band, so the same percentage is a different
height on the page. `build/apply-curve.py` measures the real positions with
`build/measure-figs.js` and generates the polygons from those, which is why the
clip lives inline on each image rather than in the stylesheet.

Rebuild the curve after changing `--band-h` or `--photo-h`:

    python3 "Trifold Design/build/apply-curve.py"
    node "Trifold Design/build/render.js"

The crest is set to the shallowest photograph's lower edge and the trough
leaves about two fifths of the frame, so the pictures are full at the middle of
the spread without thinning to slivers at the outer edges.

The band and the photograph both carry `flex: 0 0 auto`. Without it the panel,
being a flex column, shrinks them on whichever panel holds the most copy: the
practice panel's band came out a fifth of an inch short, which broke the rhythm
on exactly one panel and pulled its photograph out of the curve.

**Both dimensions are load-bearing.** The six panels sit between 687 and 763
points against 762 available, and `used` in the render report counts children
only, not margins, so a panel can report under and still overflow. Trust the
`overflow` figure. Raising `--photo-h` by a quarter inch is enough to push the
practice panel over.

## The colour system

The piece runs on one idea at three sizes, all Food Web Green into moss:

| | What it is | Where |
| :-- | :-- | :-- |
| `.banner` | The eyebrow and heading at the top of a pillar panel, reversed out | Panels 2, 3, 4, 5, 6 |
| `.field` | A bounded block inside a white panel | The cover's closing block |
| `.panel--field` | A whole panel given to the colour | Panel 6 |

**A background costs no height.** That is why panel 6 can turn green on a sheet where four of the six
panels have under twelve points spare, and why the banner was affordable at all: its top padding was
already empty white, so only its bottom padding is new. Bounded fields do cost their padding, which is
what pushed the cover over on the first pass.

`.carry` continues panel 6's colour left across the crease, so the field starts before the fold rather
than at it. It is absolutely placed on the sheet, sized to panel 5's right padding exactly, so no copy
ever sits on it.

The photo fade belongs to `.panel--field` only. On a white panel the same fade lands behind the
caption and turns grey italic type into grey type on a grey-green band. The caption carries a
`z-index` so it clears the fade either way.

Cards are pale green with a Food Web Green left edge. `.card--cream` keeps Organic Cream with a tan
edge for anything that should read as a note rather than a panel. No panel has a cream background:
cream is still a shape, never the page.

Organic Cream `--panel` #F4F1EA is used only as bounded rectangles: the figures block on panel 1, the
"On claims" box on panel 4, the directory box on panel 5, the legal block on panel 6. No panel has a
cream background. The pale green `--panel-green` carries the climate callout on panel 2 the same way.

## Type

Montserrat 700 for headlines, eyebrows and the wordmark; Montserrat 600 for subheads; Source Sans 3
for body; **EB Garamond for every piece of small considered text**, as `site.css` asks: the ledes, all
photo captions, all source lines, both pull quotes, and every placeholder note. Font files are the
repository's own subsetted `.woff2` files in `fonts/`; nothing is fetched from a CDN.

## Photographs used, and why

| Panel | File | Why |
| :-- | :-- | :-- |
| 1, Cover | `img/hand-soil-roots-fungi.jpg` | The only file in the library that actually shows what the cover line claims: an aggregate with roots and white fungal strands visible in a hand. 2000 x 2000, plenty at 300 DPI. Chosen over `2-hands-clasped-holding-plant-roots.jpg`, where the soil is a dark mass with no structure legible. |
| 2, Story | `img/Dr Elaine Ingham with Microscope.jpg` | The portrait the copy deck names for this content. 3516 x 4677, the best resolution in the repository. Cropped to keep the microscope in frame, because the caption refers to it. Not paired with a workshop photo: panel 2 already carries the callout and the QR, and a second image pushed the QR off the panel. |
| 3, Teaching | `img/uploads/Loida Teaching 3.JPG` | A mentor teaching outdoors on working land, which is what the panel is about. 1600 x 1066, enough for the 3.75in width used. `ctpfw-student-*-compost` are closer crops of hands and read as compost, not as teaching. |
| 4, Research | `img/Test tubes with sample_.jpg` | Samples with a microscope behind them: lab and field in one frame. 3083 x 2235. Paired with `img/uploads/testate-amoeba-40x.jpg` as a small inset, because that is literally the microscope count the panel says every recommendation starts with. `Elaine and nematode extraction.png` is only 940 x 788, too small to print at any useful size. |
| 5, Practice | `img/erc-rancho-cacachilas-agro.jpg` | Cultivated rows on real land under real sky. 1500 x 1000. Used for the panel's atmosphere only, and the caption says so. **This is not the South Africa tomato farm** named in the copy; see below. |
| 6, Community | `img/uploads/MAR Group Photo 2.jpg` | About thirty people around a finished compost pile, which is what a community panel needs. 1600 x 1200. |

**The logo is provisional.** `img/sfwlogo-240.png` is a 240 x 208 stand-in; `OPEN-ITEMS.md`
Decision 16 records that the real vector mark has never reached the repository. It is set at 0.46in
wide on panel 1, which is about as large as 240px can go at 300 DPI without softening. The type-set
wordmark beside it carries the name, exactly as the live site does. **Replace with the real artwork
before print.** Everything else in the piece is at or above 300 DPI at the size used.

---

## Open items carried forward, not resolved

Every one of these prints as a visible italic note on the panel it belongs to. The site's own `.todo`
class was deliberately not reused: it is `display:none` until `?notes=1` is set, and in a flattened
print PNG that would render as nothing at all. These are set in the `.awaiting` tone instead, always
visible, a straight sentence about what is needed and who supplies it.

1. **Dr. Ingham's publication count (panel 2).** Three different figures are live in this repository
   at once. `about-elaine.html` says 89 publications, 53 of them journal articles. `docs/copy-deck-v2.md`
   section 14 says 82 verified links, and separately lists 77 journal papers, 6 book chapters, 10
   reports and 43 other. `OPEN-ITEMS.md` already flags the contradiction as waiting on Linnea and Evan.
   The brief told me to print "77 peer-reviewed journal papers"; the live page is newer than the copy
   deck and disagrees with both, so **no number is printed**. The panel says so instead. Linnea and Evan.
2. **Dr. Ingham's birth year (panel 2).** Printed as "1952 to 2026" with the standing note that the
   year is unconfirmed against the obituary, same as `about-elaine.html`.
3. **The South Africa tomato case (panel 5).** The brief's draft gave "Grade 1 produce from 18% to
   50% in a single season". `docs/copy-deck-v2.md` line 449 records this as a placeholder needing the
   grower's name, the year and the source. It is an unattributed percentage under the house rule, so
   **the figures are not printed**. The panel names the case and says what is missing. There is also no
   photograph of that farm in this repository; panel 5 uses a different farm and its caption says so. Evan.
4. **The partner list (panel 5).** Only Isha Outreach is named, because it is the only partner named
   anywhere in the built site (`index.html` partner strip, `calendar.html`). The draft's RySS / APCNF
   line is dropped: `docs/copy-deck-v2.md` line 430 records that collaboration as proposed and unsigned,
   and its "close to two million farmers" is an unattributed figure. Kiss the Ground is dropped too:
   `docs/2026-08-interview-evan-buckman.md` describes them as close contacts, not a partner. No partner
   logos exist in the repository. Evan.
5. **Ecoregion hubs (panel 5).** Described as in planning, because `docs/copy-deck-v2.md` carries
   the hub pilots as a placeholder. No hub is named. Evan.
6. **The practitioner directory address (panel 5).** The draft gave `soilfoodweb.com/practitioners`.
   That address appears nowhere in this repository; the copy deck puts the page at `/community/directory`,
   and `OPEN-ITEMS.md` separately records that the production hostname itself is still a guess. No URL
   is printed. Linnea and Evan.
7. **The research roadmap (panel 4).** Published replications, open data releases and a microscopy
   methodology paper appear in no Foundation document in this repository. Named on the panel as
   unconfirmed rather than printed as a commitment. Evan.
8. **Every photo caption.** Place, people and date are unconfirmed for all six photographs, which is
   the standing `OPEN-ITEMS.md` entry covering fourteen pages of the site. Each caption says so.
9. **Consent for the group photograph on panel 6.** `OPEN-ITEMS.md` records that nobody has confirmed
   everyone in `MAR Group Photo 2.jpg` agreed to be published. That is a live question on the website;
   **in print it is worse, because a printed run cannot be taken down.** The caption flags it. Someone
   should clear this specifically before the job is placed.
10. **Prices (panel 3).** Deliberately not printed, and the panel says why. Foundation Courses at
    $4,999 and the Complete Practicum at $3,999 are verified in the copy deck, but the refund rule
    (Decision 2) and payment plans (Decision 3) are open, and a printed price outlives the price. The
    panel points at `school.soilfoodweb.com` instead. Evan.
11. **The grower path (Decision 1)** is not mentioned. Panel 3 had no room for it once the three
    program blocks and the QR were in. It belongs on a later pass if the decision lands.

## Copy I cut from the brief's draft, and why

- **"A teaspoon of healthy soil holds more microorganisms than there are people on Earth."** Cut from
  panel 1. It is a real and widely repeated figure, but it appears nowhere in this repository and has no
  named source, and the house rule is no statistic without one. The cover now uses the homepage lede's
  own wording instead.
- **"Soil is the largest terrestrial carbon sink on Earth."** Cut from the panel 2 climate callout. It
  is a superlative claim with no source in the repository. Replaced verbatim with mechanism six from
  `science.html`, which says the same thing in checkable terms and is already fact-checked.
- **"around eighty peer-reviewed papers"** and its correction to "77 peer-reviewed journal papers".
  Neither is printed; see open item 1.
- **"When she started, the idea that microbes mattered to plant health was considered fringe."** Cut.
  Replaced with the verified lede from `about-elaine.html`.
- **"a community-led organization"** softened to "through the Foundation and the school inside it",
  which is the copy deck's own formulation. No governance document in the repository uses "community-led".
- **"lower input costs, healthier plants, and soil that holds carbon and water the way it's supposed
  to"** on the cover, rewritten to the homepage's own claim language, which is sourced.
- **"The ground beneath our farms is alive"** corrected to **"The ground beneath our farms and forests
  is alive"**, which is the H1 on `index.html` and in the copy deck.
- **"a two-week, in-person intensive ... run several times a year"** softened to "held periodically",
  the copy deck's own word. The durations on record disagree: the copy deck says two weeks, the Wild Ken
  Hill workshop in `community.html` ran ten days, and the India workshop runs twelve. Worth settling, but
  no duration is printed, so nothing is wrong on the panel.
- **Panel 5's film list** was added, not in the brief's draft. Eleven named practitioners with named
  places are published on `practice.html`, and a panel about real growers reads better with real growers
  in it than with three flagged placeholders and nothing else.

## House rules checked

No em dashes anywhere (grepped, zero). No "certified" (grepped, zero). No acronyms in public text:
Foundation Courses, Advanced Programs, Complete Practicum, Soil Microscopy, all spelled out. No
percentages printed at all. No acreage claims. Sentence case headings. American spelling. Every figure
that is printed carries a source line: the three cover figures, the "more than 100 countries" on panel
4, and the eleven films on panel 5. Every dated item shows its date. The ratified legal block is on
panel 6, verbatim from `docs/copy-deck-v2.md` section 1.3. Every course link points at
`school.soilfoodweb.com`; nothing points at the WordPress shop or `/foundation-courses-2/`.

## QR codes

One per panel, never two on a page, on panels 2, 3 and 6. Panels 1, 4 and 5 carry none.

Generated at **error correction M (15%)**, printed at **1.15in square**. Q correction would be
sturdier, but these URLs carry long UTM tails: at Q the community code is 65 modules, which at 1.15in
is 0.45mm a module, under the practical minimum for print. At M the codes are 49, 53 and 57 modules,
which is 0.51 to 0.60mm a module. That is workable but not generous. **Ask the printer to scan a proof
off the press, not off a laser print.** If any of them is marginal, the fix is short redirect addresses
rather than a bigger code: the UTM tail is most of the payload.

The scholarship code points at `soilfoodweb.com/scholarship-opportunities`, which is the current
WordPress page, as given in the brief. The new site has `learn-scholarships.html`. **Re-point this
before print if the new site is live by then**, or the code will need a redirect on day one.

## Also worth a person's eye

- Panel 2's photograph is cropped fairly tight on Dr. Ingham to keep the microscope in frame. A wider
  crop would be kinder to the portrait but loses the instrument the caption names. Worth a look.
- Panel 5's photograph is a 3 to 1 horizon band rather than a full block, because the panel carries
  three placeholder notes and they had to fit. When the tomato case and the partner list land, those
  notes come out and the photograph can grow.
- There is no donate call to action anywhere in the piece. Panel 6 says "donate" as one of four open
  roles, but there is no amount, no code and no link, because `donate.html` still has the impact lines
  for its preset amounts waiting on program costs. Worth deciding whether a print piece should carry one.
- Panel 1 is the only panel carrying the wordmark. On a folded piece the cover is the outward face, so
  that is correct, but confirm it against how the piece will actually be stacked and displayed.

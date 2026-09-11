# Importing linnea-sfw/sfw-visual-assets

What came across, how, and what did not translate cleanly.
Written 10 September 2026.

## What the source is

A TanStack Start app (React 19, Vite 8, TanStack Router file-based routing,
Tailwind 4, shadcn/ui, Bun), connected to Lovable. Fourteen routes, one
2,096-line stylesheet, 43 photographs, and eight modules of procedurally
generated SVG specimens.

## How it was converted

Not by hand. The app was installed and run (`npm install`, `vite dev`), every
route was loaded in a real browser, and the rendered DOM was captured. That
gives an exact conversion rather than an approximate re-typing, including the
thousands of SVG paths the catalogue modules generate at runtime.

The captured markup was then stripped of dev-server bookkeeping
(`data-tsd-source`, React suspense comments), had its asset paths and internal
links rewritten, and was wrapped in this project's own document head.

| Source route | Imported file |
| --- | --- |
| `/` | `lovable/index.html` |
| `/about` | `lovable/about.html` |
| `/brand` | `lovable/brand.html` |
| `/community` | `lovable/community.html` |
| `/donate` | `lovable/donate.html` |
| `/elaine-ingham` | `lovable/elaine-ingham.html` |
| `/learn` | `lovable/learn.html` |
| `/library` | `lovable/library.html` |
| `/now` | `lovable/now.html` |
| `/playground` | `lovable/playground.html` |
| `/projects` | `lovable/projects.html` |
| `/projects/rancho-cacachilas` | `lovable/projects-rancho-cacachilas.html` |
| `/science` | `lovable/science.html` |
| `/workshops` | `lovable/workshops.html` |

`lovable/index-of-mockups.html` lists all fourteen. Every one carries a banner
saying what it is, and `noindex, nofollow`.

Fidelity check against the running original at 1440px: `/` renders 8,962px tall
in the source and 9,049px imported; `/library` 68,536px against 68,490px. The
difference is this project's base type rules showing through where the imported
stylesheet has no rule of its own.

## Assets

All 43 photographs are in `img/`, filenames unchanged as asked, including the
seven with spaces and capitals.

## Does not translate cleanly

**1. There is no `/public/video/` in the repository.** No `sfw-amoeba-loop-hero.mp4`,
no square or 4:5 cut, no stills, no `sfw-amoeba-brand-board.png`. Everything was
supplied separately instead.

*Resolved 11 September 2026.* The amoeba kit arrived as a zip and the rest is
now committed: `img/sfw-amoeba-still-square.jpg`,
`img/sfw-amoeba-still-wide.jpg` and `img/sfw-amoeba-brand-board.png`. The three
loops in the kit are byte-identical to the ones already in `video/`, so nothing
was re-encoded. The stand-in poster frames pulled from the video at frame 90
have been deleted; the real stills are the posters now.

**2. Design tokens could not go in `:root`, against the house rule.** Both
projects use the same token names for different values: `--moss` is `#59a66c`
there and `#22371f` here, `--olive` `#156826` against `#5f6a3c`, `--rule` a
solid `#d2d5c7` against an alpha. In `:root` the import would have restyled the
live site. They are scoped to `.lv` instead. Two house rules were in conflict
and the design-system-is-done rule won.

**3. Nine class names collide** and would have restyled live components:
`.btn`, `.card`, `.eyebrow`, `.lede`, `.plate`, `.plate__f`, `.plate__n`,
`.plate__t`, `.plate__note`, `.stat`, `.wrap`. Every imported rule is prefixed
with `.lv`, which both isolates them and wins on specificity inside the
imported pages. Verified: the live pages still compute `--moss: #22371F`.

**4. Interaction is gone, because none of the JavaScript came across.** The
header's Menu drawer was React state and is captured closed and inert. The
footer's copyright year was `new Date().getFullYear()` and is now frozen at the
capture date. Router `<Link>` became plain `<a>`.

**5. Tailwind and shadcn/ui were not imported, and are not needed.** Checked
rather than assumed: not one utility class appears in any of the fourteen
rendered pages. The 46 Radix components in `src/components/ui/` are used only
by the app's 404 and error boundaries, which have no equivalent here.

**6. Four typefaces are missing on `/brand`.** It asks for Newsreader,
Bricolage Grotesque, Space Grotesk and DM Sans, which the source loaded from
Google Fonts. This project self-hosts and carries only Montserrat, Source Sans
3 and EB Garamond, so those four fall back (to Montserrat, Georgia and
system-ui, which the source declared). `/brand` is a typographic argument, so it
is the one page materially weakened by this. Fixing it means either self-hosting
four more families or accepting a third-party request on that page. Left as a
decision, not taken.

Source Serif 4 is also absent and falls back to Georgia. That one affects
several pages but only in the standfirsts, and Georgia holds up.

**7. The SVG generators did not come across, only their output.** The eight
catalogue modules (`microscopy`, `frames`, `furniture`, `invented`, `kit`,
`pagepieces`, `siteshapes`, `surfaces`) build their specimens procedurally at
runtime. What is in `lovable/library.html` and `lovable/playground.html` is the
SVG they produced on the day, frozen. The specimens cannot be re-seeded, recoloured
or re-parameterised without going back to the source project.

**8. `/library` scrolls sideways.** It does so in the source too, at 1440px:
2,119px wide there against 2,174px imported. Reproduced faithfully rather than
fixed, since fixing it would be a change to the source design.

**9. The copy is placeholder, so the pages are quarantined.** Every one carries
invented text: `REPLACE_WITH_CAPTION`, "Placeholder standfirst", "Placeholder
text throughout. Visual mockup." The live pages for the same subjects already
exist at the top level of this repository with copy-deck copy and are further
along. Overwriting them with these would have destroyed real work and broken
the copy-comes-from-the-copy-deck rule, so the import sits in `lovable/` as
reference instead. Take layout ideas from it; do not take words.

**10. Filenames with spaces survived as asked** and appear both raw and
percent-encoded in the source markup. Both resolve. Worth normalising before
any of this goes to production.

## Removing it again

`rm -rf lovable/` and delete the block at the end of `css/site.css` marked
`IMPORTED: the Lovable visual system`. Nothing on the live site references
either.

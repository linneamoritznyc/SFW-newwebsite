# The cut-out specimens

Where the generated assets go, what they are called, and what the site is
allowed to say about them. Written 11 September 2026.

## What these are

Twelve images generated from the Pinterest mood board: soil monoliths,
strata, lichen branches, turkey tail, morel, soil pigment chips, a Blossfeldt
plate, mycelium on black, a risograph, tissue-paper strata, a microscopy
field and a sheet of engraved plates.

**They are illustrations.** Every one carries the caption "Illustration", not
because four of them do but because all of them are generated and the
distinction is not one a reader can make by looking. The Foundation's own
brightfield microscopy stays the only thing on the site presented as real,
and is the only thing captioned as an observation.

Two of the twelve are therefore **not going on the site at all**:

- **the microscopy field.** The Foundation has real microscopy, running on
  three pages. A generated one beside it invites the reader to take both as
  evidence, and one of them is not.
- **the sheet of engraved plates.** It reads as scans of historical
  scientific literature. The site cites real papers on the research page. A
  generated document that looks like a source is the one thing a science
  nonprofit cannot put on a page.

The **mycelium on black** is held back for a different reason: drawn hyphae
and root lines were on the "leave all of this out" list, and a wood engraving
of a branching network is exactly that, however beautiful. Worth revisiting
deliberately rather than by accident.

## How to prepare them

Put the supplied files in `img/illustration/`, then:

    python3 tools/cutout.py

Each one is flooded in from the four borders, feathered by a pixel, trimmed
to the subject and written to `img/cut/` at 1400 and 700 on the long edge as
a PNG with an alpha channel. The flood only ever removes background connected
to the edge of the frame, so a pale patch inside a specimen survives: a morel
keeps its cream stem.

If what arrives is the single contact sheet rather than twelve files:

    python3 tools/cutout.py --grid 3x4 img/illustration/sheet.png

Two of them should keep their background, because the background is the
picture: the Blossfeldt plate is a photogravure on grey paper, and the
tissue-paper strata are torn paper with the edge showing.

    python3 tools/cutout.py --keep-bg img/illustration/blossfeldt.png

`img/cut/` is exempt from `tools/images.py`, which writes JPEGs, because a
JPEG has no alpha channel.

## Where each one goes

| Asset | Page | Slot |
| --- | --- | --- |
| Soil monolith | index | beside the opening, standing in white space, tall |
| Floating strata | science | mechanism 3, building soil structure |
| Specimen branches | community | the opening, small, three across |
| Turkey tail | science | mechanism 4, the fungal one |
| Morel | learn | beside the path selector |
| Soil pigment chips | research | beside the database, as a column |
| Blossfeldt seedling | science | mechanism 5, the seedling, keeps its ground |
| Risograph hands | donate | beside the volunteer form |
| Tissue-paper strata | about | beside the story, keeps its torn edge |

Placement is one line each once the files exist: `specimen("img/cut/NAME.png",
"a description of what is in the picture")`, with `specimen--tall`,
`--wide` or `--small` where the shape asks for it. `.drawer` puts three in a
row. Both are in `css/site.css` section 19.

## Still needed from the Foundation

Every one of these captions is `REPLACE_WITH_CAPTION` until the Foundation
writes them. "Illustration" is the label, not the caption.

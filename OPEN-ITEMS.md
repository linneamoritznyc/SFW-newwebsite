# Open items

Everything the site still shows as a visible placeholder, with the person who supplies it.

Last updated 11 September 2026 (Community rebuild and the Wild Ken Hill story added the same day). Placeholders render as dashed `.todo` blocks; add `?notes=1` to any page URL to reveal every one of them at once.

A placeholder leaves this list only when the real thing is in the repository. "Confirmed in a document" is not the same as "on the page".

---

## Waiting on Evan

| What | Where | Note |
| :-- | :-- | :-- |
| **Decision 1, grower path** | learn.html | Growers who want their own land fixed and do not want the Consultant title. What do they buy now? |
| **Decision 2, refund rule** | learn.html, every program row | Six versions exist. One sentence, printed on every row. |
| **Decision 3, payment plans** | learn.html | Keep or drop. If kept, 6 × $250 against $1,250 upfront needs a stated reason, and the Field Trial plan is cheaper than upfront, which is an error to fix on Thinkific first. |
| **Decision 4, the 40% off bundle** | omitted from the site | Real offer or leftover? Where does it link, and until when? |
| **Decision 5, Liquid Amendments prerequisites** | learn.html | Thinkific says Microscopy and Compost first; the reopening post says the order is free. |
| **Decision 6, Lab Technician re-testing** | learn.html | Enforced every 12 months or not. |
| **Decision 7, "unlimited mentorship"** | learn.html | Confirm mentor capacity supports it for 42 months, or state an allocation. |
| **Decision 8, contracting entity** | terms.html, privacy.html | Does a student contract with the Foundation or with Soil Foodweb School LLC? Legal review. |
| **Decision 9, public documents** | about-governance.html | IRS determination letter, financial statements, conflict-of-interest / whistleblower / document-retention policies, and the split showing where donations go. The Form 990 and annual report lines now read "will be posted here"; confirm the first filing date. |
| **Decision 10, the rest of the board** | about-team.html | Four Executive Committee members are named. Still needed: officer titles (chair, secretary, treasurer), Jenna Noel's own title, any members beyond the Executive Committee, and board portraits. |
| **Decision 13, Soil Sponge Workshop** | calendar.html | Next cohort dates, or take registration down. |
| **Decision 14, newsletter tool** | footer, every page | Which service receives the footer email field. Needed for the form action; the form currently posts nowhere. |
| **Decision 15, directory counts** | learn.html, directory.html | Confirm roughly 100 consultants and 250 lab technicians in 45 countries. These print on every program row once confirmed. |
| **Decision 16, logo artwork** | every page | The mark was shown in chat but the file never reached the repository, and a hand-traced copy of a brand mark is not the brand mark. **The slot is built and waiting:** put the artwork at `img/logo.svg` (SVG preferred; a transparent PNG at 3x works) and set `LOGO = "img/logo.svg"` at the top of `tools/build.py`. Header, overlay menu and footer all pick it up, sized and positioned, and the type-set wordmark becomes the accessible name. |
| Partner names and logo files | index.html, partner strip | Isha Outreach is named. Every other partner still to come. |
| Dr. Adam Cobb's biography and portrait | about-team.html | Named on the public staff list, no bio anywhere. |
| The 32 imported biographies | about-team.html | Carried over word for word from the old site. Between them: "certified consultant", "Certified Lab-Tech", acreage claims, unattributed superlatives, and the "SFW" acronym. They are people's own words, so they need rewriting with their subjects, not without them. |
| Dr. Ingham's bio figures | about-team.html | "Soil Foodweb Inc. 26 years ago" is undated. "Seventy-six papers" does not match the 82 verified links on the publications list. |
| Dr. Ingham's birth year | about-team.html | The page shows 1952 to 2026. Confirm against the obituary. |
| Events feed | calendar.html | Webinars come from webinar.soilfoodweb.com, future workshops from the interest form. Still open: the feed format, and which system is the source of truth for dates. |
| Contact form routing | practice.html, work with us | The form posts to info@soilfoodweb.com. Confirm the routing and who owns the replies. |
| Webinar series dates | learn-webinars.html | Two sessions are named (Vandana Shiva with Evan Buckman; Dr. Carla Portugal and Dr. Adam Cobb). Dates, times and one-line descriptions still needed, from webinar.soilfoodweb.com. |
| The three short guides | learn-webinars.html | "Reading your soil, first compost, choosing a microscope" are listed as free resources but do not exist as pages. Who writes them, and where do they live? |
| Renald Flores's film | projects/market-garden-sweden.html | The individual Vimeo id and privacy hash. The playlist id 537966540 alone will not embed one video. |
| The Sweden case study body | projects/market-garden-sweden.html | The site, what was done, what was measured, and the year. Four sections are still waiting. |
| Scholarship review cadence | learn-scholarships.html | Step two says applications are read in batches. How often is a round read, and what is weighed? |
| Social account addresses | footer, every page | The staging footer carries X, Facebook, Google and Instagram icons. No addresses were supplied, so no icons print rather than four links to nowhere. |
| Full Consultant Case Studies and Farmer Case Studies playlists | practice.html | Five more films are listed on the page notes. The complete playlists need Vimeo account access. |

## Waiting on Evan and Stephanie

| What | Where | Note |
| :-- | :-- | :-- |
| A restoration-segment case study | practice.html | Three agricultural and practitioner films are in. The restoration case is missing, and the section claims all three segments. |
| The written detail behind each case study | practice.html | Where each grower started, what they practiced, what was measured. The films carry the story; the page carries no numbers. |

## Waiting on the Foundation

| What | Where | Note |
| :-- | :-- | :-- |
| Photo captions | 14 pages, every `.shot` and `.ledger` | Place, people, date. The Image and Video Log sheet in the redesign folder is the lookup table once it is filled. Nothing here is invented: a caption naming a real place and real people is a claim. |
| Staff portraits | about-team.html | Four exist on the Thinkific CDN, listed below. Everyone else still needs one. Until then the cards show initials. |
| Scholarship recipient stories | learn-scholarships.html | Two or three: photo, name, country, one paragraph. None were ever published on the old site, so the honest "the program is growing" framing stays until they arrive. |
| Community map data | community.html | Opt-in member locations at city or region level only, never exact addresses. |
| Impact lines for the donation amounts | donate.html | Pair with the preset amounts once program costs are confirmed. |

### Staff portraits that exist but are not in this repository

These four are on the Thinkific CDN. They could not be downloaded from the build environment, which has no outbound access to that host. Someone with normal internet access needs to save them into `img/team/` and run `python3 tools/images.py`.

| Person | Address |
| :-- | :-- |
| Evan Buckman | `https://import.cdn.thinkific.com/1181504/custom_site_themes/id/WaILrIdyQHO4W7K2RHmL_Screenshot%202026-07-28%20at%208.11.14%E2%80%AFAM.png` |
| Loida Vasquez | `https://import.cdn.thinkific.com/1181504/custom_site_themes/id/PEkwppp1RKa5FaDMIH7Q_loida%20with%20pig.jpg` |
| Gerald Ramírez | `https://import.cdn.thinkific.com/1181504/custom_site_themes/id/egL2u8ypSYaGHrSgXMOJ_Gerald-R.jpg` |
| Kavi Reddy | `https://import.cdn.thinkific.com/1181504/custom_site_themes/id/ij2JVOWvSLamVlGQxugm_Screenshot%202026-07-28%20at%208.12.43%E2%80%AFAM.png` |

## Waiting on Linnea, or Linnea and Evan

| What | Where | Note |
| :-- | :-- | :-- |
| Photosynthate wording | science.html, nutrient cycling | The sentence read "30 to 40% of the sugars" with no citation. That figure is Dr. Ingham's teaching number. The page now says "a large share of the carbon it fixes", cited to Kuzyakov and Domanski (2000), which reports lower shares for cereals than for pasture grasses. **Wording to approve.** |
| Publications count | about-elaine.html, and the Publications page in Phase 3 | Copy deck 14 says "82 verified links" and then lists groups of 77, 6, 10 and 43, which total 136. Which number is right? |
| Privacy policy rebuild | privacy.html | Entity changed to the Foundation (Decision 8), address changed from PO Box 287 Corvallis to the Portland office, children's age unified (the old text says 14 in one place and 13 in another), cookie tables kept. Processors to name: Google Analytics, Thinkific, the newsletter tool (Decision 14), the payment processor. Legal review. |
| Terms rebuild | terms.html | One entity (Decision 8), one refund rule (Decision 2), enrollment terms moved here so buyers can find them. |
| Oregon disclosure | about-governance.html | Oregon DOJ Charitable Activities registration number. |
| Dr. Ingham's Oregon State start year | about.html timeline | The page runs 1985 to 2002 because the entry also covers the Georgia postdoc; copy deck 3.2 dates the OSU post 1986 to 2002. Confirm against the CV. |

---

## Waiting on Linnea, for Community and the Wild Ken Hill story

| What | Where | Note |
| :-- | :-- | :-- |
| **The Wild Ken Hill photographs and clips** | `news/wild-ken-hill-2026.html` | Six photographs and four clips, at the filenames listed in `public/assets/community/README.md`. The clips are masked into circles, so the subject has to be centred and the corners are cut away. Every clip needs a poster with the same base name. The 39 files in the SFW Drive are still HEIC and MOV and need converting first. `python3 tools/imagecheck.py` lists what is still missing. |
| **The five community log photographs** | `community.html` | `living-legacy-webinar`, `soil-health-week-karachi-university`, `soil-health-week-pakistan`, `costa-rica-liquid-amendments`, `costa-rica-microscopes`. The mockup hot-linked these from soilfoodweb.com/wp-content/uploads; they are referenced from `public/assets/community/img/` so the new site does not depend on the old one staying up. Copy the originals across. |
| **Alt text and captions on the story** | `news/wild-ken-hill-2026.html` | Written from the story rather than from the footage, because the footage was not available when the page was built. Read every alt attribute against the picture it now describes once the files land. Captions are marked caption-needed and print nothing until written. |

## Decisions on the Community rebuild

Two places where the approved mockup and the copy in `docs/wild-ken-hill-2026-blog-post.md`
run against a rule in `CLAUDE.md`. Both were built the mockup's way, since the
mockup is the approved design and is the later document, and are listed here so
they can be settled rather than left to drift.

**"certified" is settled.** Linnea said do not write it, 11 September 2026, and
the three uses in the community log are gone: "Certified consultant Nick
Padwick" is now "Consultant Nick Padwick", "107 people became certified
lab-techs" is "107 people earned the lab-tech title", and "we also certified our
50th consultant" is "Our 50th consultant finished the program". One use is left
on the site, in `about-team.html`, inside the 32 imported biographies. Those are
people's own words and are already on this list to be rewritten with their
subjects.

| What | Where | The conflict |
| :-- | :-- | :-- |
| **The course link on the story** | `news/wild-ken-hill-2026.html` | The approved copy points "See every program and price" at `soilfoodweb.com/sfw-courses-overview/`. The rule is that programs link to `learn.html` and to school.soilfoodweb.com, never to the old WordPress site, so it points at `learn.html`. Confirm, or name the page it should be. |
| **Cream as a box, not a band** | `community.html`, "Coming up", "Community by region" and "Work with one of us" | The mockup gives the sidebar boxes and the directory band a full cream background. `site.css` says Organic Cream is a shape, never the page, so the sidebar boxes are cream boxes and the directory band is a cream box inside a white band rather than a cream stripe across the window. Same colour, one step short of the mockup. |

## Two smaller notes on the Community rebuild

- **An empty slot is invisible to a visitor.** Both pages went live before the
  photographs and clips arrived, so a file that is not there yet takes its slot
  with it: the figure is removed and the list around it goes too, and the page
  reads as finished rather than as a building site. The one exception is the
  feature block at the top of Community, where the photograph's half stays as a
  cream field beside the green panel. Add `?notes=1` to either URL and every
  empty slot comes back as a dashed box carrying the description of what belongs
  in it, which is how every other placeholder on this site is read. Drop the real
  files into `public/assets/community/` and they appear; nothing else changes.
- **The Google Drive gallery is gone.** The mockup listed 39 Drive links under the Wild Ken Hill post, still in HEIC and MOV. Those files belong on the story page, converted and hosted here, so the post links to the story instead and the conversion note is a placeholder rather than public text.
- **The map.** The mockup replaces the community map with the "Community by region" list, and the overlay menu on every page still links to `community.html#community-map`. That anchor now lands on the regions list, which carries the note saying the interactive map is still to come. If the map is not coming back, the menu label should change from "Community map" to something the list actually answers to.

---

## Settled since the last pass

| What | Answer | Source |
| :-- | :-- | :-- |
| **Decision 11, Kavi Reddy's title** | Growth, Partnerships, and Permaculture | Public staff page |
| **Decision 12, India workshop dates** | 19 to 30 October 2026. Accelerator Workshop India 2026, Save Soil Farm near the Isha Yoga Center, Coimbatore, Tamil Nadu, in collaboration with Isha Outreach. | The live enrollment page, school.soilfoodweb.com/courses/india-workshop-2026 |
| **Decision 17, the two India events** | One event, not two. The copy deck's "Asia-Pacific Workshop, October 2027" was the same workshop with the wrong year. | Same |
| Homepage testimonial | Dr. David Johnson, New Mexico State University. Trimmed before the IPCC clause, which is a global outcome claim under the claims rule. | Old homepage, retained at Evan's request |
| Who We Are copy | Final as written. No team draft exists in the redesign folder. | Board review copy deck, section 1.3 |
| Dr. Ingham's master's subject | M.S., Microbiology, Texas A&M University | SFW's own About page. The old-site bio saying "Marine Biology" was wrong. |
| Login platform split | By purchase date: after 15 March 2026 on school.soilfoodweb.com, before that on soilfoodweb.com, with accounts migrating in stages. | The live login page |

---

## Flagged on the old site, for Evan

Not bugs in this build, but they will matter at cutover.

- The old privacy policy still names **Soil Foodweb School LLC** and **PO Box 287, Corvallis, OR 97330**. The new site uses the Foundation and the Portland registered office. The old policy needs retiring at the same moment the new one goes live, or the two will contradict each other.
- The old navigation misspells **"Field Trail"**. It is Field Trial. Nothing in this repository carries the misspelling.
- The Foundation launch post says **"approximately 130 countries"**. Everything here says 100+, sourced to enrollment records confirmed August 2026. Two public numbers for the same thing is worse than one conservative one, so the launch post should be corrected rather than the site raised.
- **new.soilfoodweb.com cannot be read from this build environment.** The egress proxy refuses that host, so the staging site, source of truth number one, has only ever been reconciled from screenshots and from the brief. `/how-it-works/` and `/find-a-professional/` in particular have not been compared line by line against `science.html` and `directory.html`. Paste their copy, or run the comparison somewhere with normal internet access.
- **The six science animations are unverified.** They are embedded from Vimeo by id (372925873, 372474782, 372476056, 372479571, 372480255, 372478833). If any is unlisted rather than public it needs its `h` privacy hash appended, or it will show "video not available". Open `/science` in a real browser and check all six.
- **The production hostname is a guess.** `tools/build.py` sets `SITE = "https://soilfoodweb.org"` for the `og:url` and `og:image` tags. Confirm the real hostname at cutover; a wrong one means every shared link unfurls without its picture.
- The external links in `docs/link-map.md` have never been fetched. This build environment has no outbound access to soilfoodweb.com, school.soilfoodweb.com, vimeo.com or doi.org. They need one pass from a machine with normal internet access before launch.

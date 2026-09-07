# Lovable prompt, Soil Food Web Foundation

Attach: the logo, the reference board, the four collage references, and the image and video spreadsheet.

---

Build the website for the **Soil Food Web Foundation**, a 501(c)(3) nonprofit that teaches soil biology, the science of the living organisms in soil and how restoring them restores land. It carries forward the work of Dr. Elaine Ingham, a soil microbiologist who spent forty years on this and died in February 2026.

You are the design lead. I am not specifying a grid, a type scale, or hex values. Decide those and commit.

**The visual design is the point of this build.** Structure and copy are given to you below so that your attention goes where it matters. If you spend your effort anywhere, spend it on making this beautiful.

## The core visual idea

The site should feel **alive**. Not animated, alive. As though something is growing on it and through it.

The mechanism for this is **real photographic texture, cut into organic shapes, placed against a clean ground.**

Look at the four collage references. Real moss, real bark, real lichen, real soil, real fungal caps, photographed closely and then cut out along a biomorphic silhouette and set on white. The edge is hard. There is no shadow, no glow, no blending. The shape is irregular and living, the placement is calm and considered. That contrast, wild material and quiet arrangement, is the whole design.

Build this into the page:

- **Cut-out texture forms as compositional elements.** A moss form entering from a page edge. A bark silhouette running down a margin. A fungal cluster anchoring a corner. They sit behind and beside content, they are never contained in a rectangle, and they bleed off the edge rather than floating in the middle.
- **Textures accumulate as you scroll.** The top of a long page is sparse and clean. Further down, more organic forms enter from the margins, larger and more overlapping, as though the page is being colonised. This is the one structural gesture that makes the site feel alive, and it should be done with CSS positioning of static images, not with scroll-triggered animation.
- **Section transitions are organic edges, not straight rules.** Where one band meets another, let a moss or soil form carry across the boundary.
- **Every texture is a real photograph of a real thing.** Mycelium, soil aggregates, moss, lichen, bark, root systems, compost, bacterial colonies, microscopy plates. Never illustrated, never AI-generated, never abstract vector shapes pretending to be organic.

The site is a clean, quiet, well-typeset document that living material is slowly growing over.

## Palette and treatment

Muted olive, sage, moss green, bone, warm off-white, soil brown, ink black. Tonal rather than contrasting. The ground is a warm near-white so the cut-out textures read as objects placed on paper.

Photographic treatment: close, frontal, sharp. Specimens photographed as evidence. Where images are treated at all, use duotone or a light halftone, and only on a few.

Typography carries the discipline that the imagery does not. Flush-left, ragged-right. A tight modular scale with real hierarchy. Hairline rules. Generous margins. An old-style or transitional serif is appropriate for headings, paired with one clean sans for text. Two typefaces maximum.

## Three audiences, one navigation

Every page must work for three people who want completely different things:

- **A farmer or grower.** Wants to know whether this works on land like theirs, what it costs, and who near them can help. Serve them with named case studies, visible prices, and the practitioner directory.
- **A prospective student.** Wants to know what they would learn, in what order, over how long, for how much. Serve them with a clear programme sequence and honest total cost.
- **A grant-giver or institutional partner.** Wants evidence the organisation is real, governed, active and accountable. Serve them with governance, financials, dated activity, published research and sourced claims.

Design for this by giving the homepage three distinct entry paths, and by never making any of the three read another one's page to find their answer. A farmer should not have to read a mission statement. A funder should not have to read course marketing.

## Structure

Six sections. Navigation is a full-screen overlay opened from a button top right. The viewport floods to deep green, sections stack left as an accordion with a one-line descriptor each, and a dated "Happening now" column sits right. A cut-out moss form should grow across one corner of the overlay.

1. **About us**, mission and story, team and board, governance and financials, Dr. Elaine Ingham, contact
2. **Learn**, all programmes with prices, in-person workshops, free webinars, scholarships, student login
3. **Science**, how the soil food web works, publications, Dr. Elaine's research
4. **Projects**, case studies, field trials, ecoregion hubs
5. **Community**, find a professional, community map, join, volunteer
6. **Now**, a dated index of everything currently happening

Persistent in the header: What's happening, Student login, Donate.

## The content problem

Dozens of case-study videos across six buried pages, several playlists, eighty-two publications, a practitioner directory, blog posts, webinar recordings. All of it currently four clicks deep.

Solve it with information design:

- Index pages are dense and complete with visible filter chips, not twelve items and pagination
- Video is a format, not a category. Case-study video lives on Projects, explainer animation on Science, testimonials on Learn. Do not build a Videos section.
- A playlist is one card showing its count, opening to a filtered index
- Everything carries a visible date

## Copy

Use this text. It is written. Do not rewrite it into marketing language.

### Homepage

Hero heading: **The ground beneath our farms is alive.**

Hero body: Beneath every field and forest there is a living web of bacteria, fungi, protozoa and nematodes that feeds plants, holds water and builds soil. We teach people to see it, restore it, and prove what happens when they do.

Three statistics, each with its source printed beneath: 100+ countries where students and practitioners are working, enrolment records 2026. 10,000+ people enrolled in our programmes, enrolment records 2026. 40 years of soil biology research behind the method, Dr. Elaine Ingham 1981 to 2026.

Section heading: **A nonprofit, and a school inside it.** Body: The Soil Food Web Foundation carries forward the work of Dr. Elaine Ingham, who spent four decades showing that soil is not dirt but a living system. The Soil Food Web School is one of four things we do. It is how the science reaches people. It is not the whole organisation.

Four pillars. Teaching: courses, workshops and free webinars, from a first curiosity through to professional practice. Research: replicating key experiments, opening trial data, and advancing microscopy methods. Practice: working with growers to trial and document the method on real land, in their own ecoregion. Community: a network of students, practitioners, volunteers and donors that outlasts any one of us.

Section heading: **What it looks like on real land.** Body: Every number we publish is attached to a named person, a named place and a year. Where we do not have that yet, we say so instead of rounding up.

Section heading: **Start where you are.** Body: Most people begin with the Foundation Courses. Where you go next depends on whether you want to grow better, or to do this for other people.

Section heading: **What's happening now.** Body: Courses opening, workshops running, new writing, new video. Everything here carries a date, so you can see for yourself whether this place is alive.

### Science page

Heading: **How the soil food web works.** Intro: Six mechanisms. Each one is a claim we can defend, with the research behind it linked rather than summarised.

The web itself: bacteria, fungi, protozoa, nematodes and micro-arthropods, eating each other in a structured set of relationships. The structure is the point, not the individual organisms.

Nutrient cycling: plants send a substantial share of their photosynthetic output into the root zone as exudates, feeding microbes that in turn release nutrients in plant-available form.

Building structure: microbial glues and fungal hyphae bind particles into aggregates. Aggregated soil holds air and water where compacted soil holds neither.

Suppressing weeds: fungal-dominated soils shift nitrogen chemistry in ways that favour perennials and disadvantage many early-succession weeds.

Protecting plants: below ground, oxygen-rich structure favours beneficial organisms over anaerobic pathogens. Above ground, beneficial microbes applied to leaves and stems occupy the niches pathogens would use.

Storing carbon: biology moves carbon into stable soil fractions, and reduces the fuel and manufactured inputs a system needs in the first place.

Closing note: We publish figures only where a specific site, grower and year can be named. Where a result is repeatedly observed but not yet formally measured, we say that rather than attaching a percentage to it.

### Learn page

Heading: **Learn to work with the biology in your soil.** Intro: Whether you grow in raised beds or advise farms at scale, there is a path. Below is every programme we offer and what each one costs.

Closing note: **What the whole path costs.** To become a Soil Food Web Consultant you take the Foundation Courses and then all four Advanced Programmes. Both figures are shown above rather than staged, so nobody discovers the second half after committing to the first. If cost is the obstacle, the scholarship application is open.

### Governance page

Heading: **Governance and financials.** Intro: How the Foundation is constituted, who oversees it, and where the money goes.

Body: Soil Food Web Foundation is a 501(c)(3) nonprofit organisation incorporated in Oregon, EIN 39-4439236, registered at 5441 S Macadam Avenue, Suite N, Portland, Oregon 97239. The Soil Food Web School is a programme of the Foundation, not a separate organisation.

Public documents listed: Form 990, IRS determination letter, annual report, financial statements.

### Case study pages

Each carries four headings: The site. What was done. What was measured. What we cannot claim.

Under the last one: This is one site with one practitioner. It shows what the method can do under these conditions. It is not evidence of an average result.

### Projects

Named case studies, real: Todd Harrington at Governors Island, New York, restoring 172 acres of public park. Shane Plath in South Africa, an organic banana farm at 5,000 acres. Miles Sorel across Ecuador, India, Peru and the USA, grapes, turmeric and other crops. A South African tomato grower whose Grade 1 produce rose from 18% to 50% in one year.

### Directory

Everyone listed earned their title through our programmes. Consultants have completed all four Advanced Programmes. Lab technicians have completed Soil Microscopy.

## Rules on content, not negotiable

- Every number gets a source printed with it. No orphan percentages anywhere. This organisation was penalised by a grant reviewer for unsourced claims.
- Case studies name a person, a place and a year.
- Prices visible on programme pages, full pathway cost stated up front.
- Every page states the 501(c)(3) status and that the School is a programme of the Foundation.
- Never use the phrase "nature's operating system."
- No urgency language, countdowns, or "only X spots left."

## What not to do

Banned, not discouraged. Each is a tell that the site was generated rather than designed.

**Colour and surface**

Gradients of any kind, linear, radial or mesh. Glows, neon, bloom, anything lit from behind. Glassmorphism, frosted panels, backdrop blur. Blurred coloured blobs or aurora shapes. Drop shadows at the same value on everything, especially soft grey shadows under every card. Warm cream with a terracotta accent, the single most common generated palette in circulation. Near-black standing in for black. Dark mode with one acid accent.

**Layout**

Hero carousels, sliders, rotating headlines. Parallax. Background video, and autoplay of any kind. Centred hero with headline, subhead and two buttons stacked mid-screen. Content chopped into identically sized rounded cards. The same border radius on every element. Bento grids. Sticky elements other than the header. Infinite scroll. Floating chat bubbles. Newsletter modals on load or scroll.

**Typography**

Em dashes, anywhere in the copy. Use a comma, a colon, a full stop, or restructure the sentence. Tracked-out all-caps eyebrow labels above every heading. Accenting one word in a headline in italic, bold or a different colour. Meta strings joined with middle dots. A monospace face used to look technical. More than two typefaces. Text over a busy photograph without solid ground behind it. Measures over about 75 characters. Justified body text. An arrow appended to every link.

**Motion**

Fade-and-slide-up entrances on every section. Hover transitions on every card. Counting-up numbers. Typewriter effects. Cursor followers, magnetic buttons, custom cursors. Scroll-hijacking or snap-scrolling. Lottie, animation libraries, WebGL. Anything that moves without the person having acted, other than one considered moment on the whole site.

**Imagery**

Stock photography, including smiling people at laptops and hands cupping seedlings that are not our hands. Illustrated or vector "organic" shapes standing in for real texture. AI-generated botanical or scientific imagery. Abstract concept illustration, connected dots, floating shapes, isometric scenes. Icons standing in for content, a leaf icon above every value proposition. Textures used as full-width background washes rather than as cut-out objects.

**Content and tone**

Emoji anywhere. Numbered markers on content that is not a sequence. Testimonial carousels. Trust-badge logo rows with nothing behind them. Fake statistics or a number without a source beside it. Marketing superlatives: revolutionary, cutting-edge, game-changing, world-class, unlock, empower, seamless, elevate, transform your, journey. Sentences that say what something is not before saying what it is. Headlines that are a question the page then answers.

**Structure**

A Videos or Resources section that becomes a dumping ground. Pagination where filters would serve better. Anything more than two clicks from the homepage. A page that does not state the 501(c)(3) status. Dropdowns that break on the page they link to. Content without a visible date.

## Technical

Static, semantic HTML and CSS, minimal JavaScript. This will be handed to a WordPress developer, so keep the markup clean. No framework, no animation library.

WCAG 2.1 AA. Real focus states. Keyboard-operable navigation. Respect prefers-reduced-motion. Cut-out texture images are decorative and take empty alt attributes so screen readers skip them.

Fast, because this is being reviewed for a Google advertising grant. Self-host fonts, lazy-load below the fold, compress the texture images hard since there will be many of them.

## Images

Use the attached spreadsheet, those assets are owned and cleared. Public-domain scientific plates from the Biodiversity Heritage Library and the USDA Soil Biology Primer are acceptable and preferred over anything invented. Where a real image does not exist, use a labelled placeholder describing what belongs there.

## The test

If a decision is not covered above, ask: does this make the page feel more like a living thing that has been carefully catalogued, or more like a product being sold? Build the first one.

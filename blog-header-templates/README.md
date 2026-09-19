# Blog header templates

One layout for every Soil Food Web Foundation blog post. Only four things
change per post: the background photo, the title, the category label and the
author.

Every header is 1200 x 630, which is the size a blog header wants and also
the size Facebook, LinkedIn and X want for a shared link, so one file does
both jobs.

Starting point was Stephanie's header on the ciliates post: a pale
microscopy photo with a faded box holding the title, the category set large
in black, and AUTHOR: WES SANDER in a black bar. Variation 1 is that idea
cleaned up and put on the new design system. The other three are
alternatives to choose between.

## The four variations

| File | What it is | Good for |
| --- | --- | --- |
| `faded-box.html` | Full photo, cream box sitting over it on the left, green rule along the top of the box, logo inside the box. | Posts where the photograph is the point and you want it to fill the frame. Closest to what we have now. |
| `side-panel.html` | Deep green panel across the left third with the title, photo in the right two thirds. | Long titles, and photos that are busy everywhere. The panel takes ten lines without the photo getting in the way. |
| `bottom-band.html` | Full photo with a Food Web Green band across the bottom holding the title. | Announcements and short titles. The photograph stays almost whole. |
| `microscope-circle.html` | Deep grey ground with the photo cropped into a large circle, like a field of view, title beside it. | Anything about what was seen on a slide. It looks like the thing it is about. |

Previews are in `previews/`, four variations by four examples.

## Making a new header

1. Copy the variation you want, or just edit it in place.
2. Open the file and change the block at the top marked EDIT HERE. It is
   five lines. Nothing below that block needs touching.

   - `title` the post title, exactly as it runs on the post.
   - `category` one of the labels the blog already uses: **Blog, Events,
     Features, Foundation Update, Microscopy, School Updates, Science &
     Education**. Set it to `""` to leave the label off. A post can carry
     two categories on the site, as the ciliates post carries Microscopy
     and Science & Education, but the header shows one. Pick the one that
     says most.
   - `author` the byline, for example `"Wes Sander"`. The template adds the
     word By. Set it to `""` to leave it off, which is what the Foundation
     Update example does.
   - `image` a path relative to this folder, so a photo in `img/w/` is
     `../img/w/name-of-photo.jpg`.
   - `focus` which part of the photo survives the crop to 1200 x 630.
     `50% 50%` is the middle, `50% 30%` holds the top, `50% 70%` holds the
     bottom. Faces usually want about `50% 35%`.

3. View it. The templates use the site's own font files, and browsers will
   not load those from a `file://` path, so serve the repository instead of
   double clicking the file. From the repository root:

   ```
   python3 -m http.server 8000
   ```

   then open `http://localhost:8000/blog-header-templates/faded-box.html`.
   Without the server the layout is right but the type falls back to Arial.
4. Export the PNG. Either screenshot the header area at 100% zoom, or run
   the script below, which is exact.

### Exporting

```
node blog-header-templates/render.js
```

This writes all sixteen preview files into `previews/`, each exactly
1200 x 630. To export your own posts instead, edit the `EXAMPLES` list at
the top of `render.js`: a slug for the file name, then the same five values.

The templates also take those values as query parameters, so a header can be
generated without editing anything:

```
faded-box.html?title=Your%20title&category=Microscopy&author=Wes%20Sander&image=../img/w/photo.jpg
```

That is how `render.js` produces sixteen images from four files.

## The whole blog as one set

`posts.js` holds all twelve posts from page 1 of the news index, read off it
on 19 Sep 2026: title, date, category, author and a photo. To render the
whole blog in one variation:

```
node blog-header-templates/render-blog.js              # side-panel
node blog-header-templates/render-blog.js faded-box    # or any other one
```

That writes twelve headers into `previews/blog-set-<variation>/` and a
contact sheet into `previews/contact-sheet-<variation>.png`. The contact
sheet is the thing to post in chat: the family only shows up when you see
twelve at once.

### The recommendation: side-panel

Both sets are rendered so they can be compared. Side-panel is the one to
pick, for three reasons that only appear at twelve posts:

1. **The panel is the same rectangle every time.** The blog's titles run
   from 25 characters ("October 2025 – Newsletter") to 146. In faded-box the
   box grows and shrinks to fit, so it is a different shape and sits at a
   different height on every post, which is the opposite of what a family
   does. The panel is 440px wide on all twelve.
2. **The photograph is never covered and never darkened.** Faded-box has to
   put a scrim over the whole photo so the box has something to sit against,
   and then the box lands on top of whatever is in the middle of the frame.
   On the three posts with a portrait in them, that means a dimmed photo
   with a box across the face. Side-panel leaves the photo completely alone.
3. **Legacy Purple is legible.** In faded-box it survives only as a 7px rule
   and a small label, so the distinction is nearly invisible.

The cost is that the photo gets two thirds of the frame instead of all of
it. That is the trade.

### Legacy Purple

`css/site.css` reserves `--legacy` `#6B4C7A` for Dr. Elaine content and
nothing else. Three of the twelve posts are about her: the obituary, the
retirement announcement, and the Living Legacy webinar series. Those take
the purple panel by setting `theme: "legacy"`. Everything else about the
layout is identical, so the set still reads as one family while saying that
those three are a different kind of post. White on Legacy Purple is 7.0:1,
which passes AA.

Set `theme` to `""` for every other post.

## Picking a photo

There is no shortage of usable photography already in the repository. A
shortlist, by what the post is about:

**Microscopy and the lab**
`img/w/sfw-amoeba-still-wide.jpg` (two protozoa mid division, the
Foundation's own footage, pale and calm behind a box),
`img/w/sfw-amoeba-still-square.jpg`, `img/w/fungal-spores-in-suspension.jpg`,
`img/uploads/testate-amoeba-40x.jpg`, `img/w/test-tubes-with-sample.jpg`,
`img/w/soil-sample-close-up-test-tube.jpg` (dark, dramatic),
`img/w/sampling-equipment.jpg`.

**Dr. Elaine**
`img/w/dr-elaine-ingham-with-microscope.jpg`,
`img/uploads/elaine-behind-microscope.jpg`, `img/w/elaine-smile-talking.jpg`,
`img/w/elaine-with-sample-bag.jpg`, `img/w/elaine-and-nematode-extraction.jpg`.
These carry Legacy Purple on the site, so if a header is ever needed for Dr.
Elaine content, that is the colour to swap in, not Food Web Green.

**Students, courses and scholarships**
`img/w/ctpfw-student-moving-compost-1.jpg` (a class at work, used in the
scholarship example), `img/w/ctpfw-student-squeezing-compost-1.jpg`,
`img/uploads/loida-teaching-3.jpg`, `img/w/workshop-group-around-compost-pile.jpg`,
`img/uploads/mar25-group-photo.jpg`, `img/uploads/mar-group-photo-2.jpg`.

**Farms, fields and case studies**
`img/w/erc-rancho-cacachilas-agro.jpg` (crop rows under a big sky, used in
the watermelon example), `img/w/erc-rancho-cacachilas-agro2.jpg`,
`img/w/fungi-in-under-grape-soil.jpg`, `img/w/hvdb-inplanten-002.jpg`,
`img/uploads/the-garden-has-well-tended-vegetable-beds-2025-03-05-05-17-00-utc.jpg`,
`img/w/erc-panchamana-garden.jpg`, `img/w/el-nino-2017-tractor-in-mud-in-vineyard.jpg`.

**Soil, compost and hands**
`img/w/hand-of-compost.jpg` (dark and rich, used in the long title example),
`img/w/hand-soil-roots-fungi.jpg`, `img/w/2-dirty-hands.jpg`,
`img/w/handling-loose-soil.jpg`, `img/w/red-soil-hand.jpg`,
`img/w/gloved-hands-red-bucket-mulch.jpg`, `img/w/fist-of-dry-soil.jpg`.

**Public domain, safe for anything**
`img/pd/` holds seven USDA NRCS Montana photographs with their credits in
`img/pd/CREDITS.json`.

The cutouts in `img/uploads/1.png` through `7.png` are microbes on a flat
light ground, not photographs. They do not work as backgrounds, but they
would work well dropped into the circle in `microscope-circle.html`.

## Where the design comes from

Nothing here invents a colour, a typeface or a mark.

- Colours are the tokens in `css/site.css`: Food Web Green `#156826`,
  moss `#22371F`, scope grey `#3C3841`, Organic Cream `#F4F1EA`, soil
  `#4F3433`, glow `#DBE6A7`. Each template copies only the few it uses,
  with a comment saying so. If a token changes in `css/site.css`, change it
  in these files too.
- Type is Montserrat for the title and category label and Source Sans 3 for
  the byline and the line under the logo, loaded from `fonts/`, the same
  files the site loads. Titles are Montserrat 700, category labels are
  Montserrat 600 uppercase tracked out to 0.18em, which is the `.eyebrow`
  setting from `css/site.css`.
- The logo is `img/sfwlogo-240.png`. It shows as the roundel in
  `faded-box.html`, where it sits on cream. On the three dark variations it
  is set as the wordmark in white instead, which is what `css/site.css`
  already does in the footer and the overlay menu: the roundel is a dark
  mark on a transparent ground and goes muddy on green.

Two things from the current header were left off on purpose. The category is
set small and tracked out rather than large and bold, because that is the
`.eyebrow` the rest of the new site uses. And no web address is printed,
because the Foundation and the School are on different domains and it is not
mine to guess which belongs on a Foundation post. Both are easy to add back.

## Readability

The brief was that the title has to hold up on a light photo and on a dark
one. How each variation does it:

- `side-panel`, `bottom-band` and `microscope-circle` never put the title on
  the photograph at all. It sits on a solid brand colour, so the photo
  cannot reach it. White on Food Web Green is 6.9:1, white on moss is
  12.8:1, white on scope grey is 11.0:1. All pass AA at any size.
- `faded-box` does put the box over the photo, so the box is held at 95.5%
  opacity, effectively solid. The current box is more transparent, which is
  where the readability goes on a pale photo. There is also a gradient over
  the whole photo, heavier on the left, so the box has an edge to sit
  against.
- The examples are deliberately mixed. The ciliates one is a pale grey
  microscopy field, the long title one is a dark compost photograph, and the
  scholarship one is a busy mid tone with people in it.

### Long titles

The blog runs long titles. The real ciliates headline is 147 characters:

> How A Rare Microscope Sighting Helps Deduce The Problem With Unhealthy
> Soil: Ciliates, Cysts, And The Clues Hiding In A Struggling Watermelon Crop

So every template has a height budget for the title and steps the size down
a point at a time until it fits, rather than spilling or being cut off. The
`--long-title` previews are that headline in all four variations, set on a
dark photo. `bottom-band` has the least room and drops furthest, to 28px.

The fit waits for Montserrat to load before it measures. Measuring against
the Arial fallback gives the wrong answer and the title overflows the moment
the real font arrives.

## Open items

- **Every photograph in the blog set is a stand-in from this repository.**
  The real post images have not been downloaded. They need to come across as
  the original, unedited photographs, not as the current header graphics,
  because the template does its own cropping and its own treatment and an
  already edited image would be edited twice.
- Eleven of the twelve posts have no byline here. Only the ciliates post
  shows its author in the header we have seen. They are left blank rather
  than guessed. Someone with access to the posts can fill them in.
- There is no photograph of Eric Feiler in the repository, so the board
  member post is running on a group shot. Foundation to supply a portrait.
- There is no white knockout version of the roundel in the repository, which
  is why the dark variations use the wordmark in white rather than the mark.
  If a white PNG or SVG of the roundel exists, we can use the mark
  everywhere and the set gets more consistent. Foundation to supply.
- The category labels here are the ones the live blog uses. The rebuilt
  `news.html` filters on a different set: Foundation news, Blog, Community
  activity, Worldwide news. Those two lists need reconciling before the blog
  is migrated, and whichever wins is what these templates should list.
- Pick one variation before these go anywhere near a post. The point is that
  every post uses the same layout.

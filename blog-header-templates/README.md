# Blog header templates

One layout for every Soil Food Web Foundation blog post. Only three things
change per post: the background photo, the title, and the category label.

Every header is 1200 x 630, which is the size a blog header wants and also
the size Facebook, LinkedIn and X want for a shared link, so one file does
both jobs.

Starting point: Stephanie's current header on the ciliates post, a photo
with a faded box holding the title. Variation 1 is that idea cleaned up.
The other three are alternatives to choose between.

## The four variations

| File | What it is | Good for |
| --- | --- | --- |
| `faded-box.html` | Full photo, cream box sitting over it on the left, green rule along the top of the box, logo inside the box. | Posts where the photograph is the point and you want it to fill the frame. Closest to what we have now. |
| `side-panel.html` | Deep green panel across the left third with the title, photo in the right two thirds. | Long titles. The panel holds six lines without the photo getting in the way. |
| `bottom-band.html` | Full photo with a Food Web Green band across the bottom holding the title. | Announcements and short titles. The photo stays almost whole. |
| `microscope-circle.html` | Deep grey ground with the photo cropped into a large circle, like a field of view, title beside it. | Anything about what was seen on a slide. It looks like the thing it is about. |

Previews of all four, each with three titles, are in `previews/`.

## Making a new header

1. Copy the variation you want, or just edit it in place.
2. Open the file and change the block at the top marked EDIT HERE. It is
   four lines: `title`, `category`, `image`, `focus`. Nothing below that
   block needs touching.
   - `category` takes one of the labels the news page already uses: Blog,
     Case study, Foundation news, Community activity, Worldwide news. Set
     it to `""` to leave the label off.
   - `image` is a path relative to this folder, so a photo in `img/w/` is
     `../img/w/name-of-photo.jpg`.
   - `focus` decides which part of the photo survives the crop to
     1200 x 630. `50% 50%` is the middle, `50% 30%` holds the top,
     `50% 70%` holds the bottom. Faces usually want about `50% 35%`.
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

This writes all twelve preview files into `previews/`, each exactly
1200 x 630. To export your own posts instead, edit the `EXAMPLES` list at
the top of `render.js`: a slug for the file name, the title, the category,
the image path, and the focus point.

The templates also take the same four values as query parameters, so a
header can be generated without editing anything:

```
faded-box.html?title=Your%20title&category=Blog&image=../img/w/photo.jpg&focus=50%25%2035%25
```

That is how `render.js` produces twelve images from four files.

## Where the design comes from

Nothing here invents a colour, a typeface or a mark.

- Colours are the tokens in `css/site.css`: Food Web Green `#156826`,
  moss `#22371F`, scope grey `#3C3841`, Organic Cream `#F4F1EA`, soil
  `#4F3433`, glow `#DBE6A7`. Each template copies only the few it uses,
  with a comment saying so. If a token changes in `css/site.css`, change it
  in these files too.
- Type is Montserrat for the title and the category label and Source Sans 3
  for the small line under the logo, loaded from `fonts/`, the same files
  the site loads. Titles are Montserrat 700, category labels are
  Montserrat 600 uppercase tracked out to 0.18em, which is the `.eyebrow`
  setting from `css/site.css`.
- The logo is `img/sfwlogo-240.png`. It shows as the roundel in
  `faded-box.html`, where it sits on cream. On the three dark variations it
  is set as the wordmark in white instead, which is what `css/site.css`
  already does in the footer and the overlay menu: the roundel is a dark
  mark on a transparent ground and goes muddy on green.

## Readability

The brief was that the title has to hold up on a light photo and on a dark
one. The way each variation does it:

- `side-panel`, `bottom-band` and `microscope-circle` never put the title on
  the photograph at all. It sits on a solid brand colour, so the photo
  cannot reach it. White on Food Web Green is 6.9:1, white on moss is
  12.8:1, white on scope grey is 11.0:1. All pass AA at any size.
- `faded-box` does put the box over the photo, so the box is held at 95.5%
  opacity, effectively solid. Stephanie's current box is more transparent,
  which is where the readability goes on a pale photo. There is also a
  gradient over the whole photo, heavier on the left, so the box has an
  edge to sit against.
- The preview set is deliberately mixed: the ciliates examples use a very
  pale microscopy field and the scholarship examples use a busy mid tone
  photo, so you can see both ends.

Titles shrink to fit rather than overflowing. Each template has a ceiling
and a floor in its script, for example 46px down to 30px in `faded-box`, so
a long title steps down a point at a time until it fits the space instead of
running out of the box.

## Open items

- The three example photos are stand-ins pulled from the repository. They
  are not the photographs these posts carry. Real post photos to come from
  whoever writes the post.
- There is no white knockout version of the roundel in the repository, which
  is why the dark variations use the wordmark in white rather than the mark.
  If a white PNG or SVG of the roundel exists, we can use the mark
  everywhere and the set gets more consistent. Foundation to supply.
- Pick one variation before these go anywhere near a post. The point is
  that every post uses the same layout.

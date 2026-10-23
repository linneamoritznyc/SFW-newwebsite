# Making headers for a new blog post

Every blog post gets the same five header images, made by `tools/blog-cards/build.py`
and exported by `tools/blog-cards/export_jpgs.py`. Do not redesign anything: the look is approved.

## The design (already built into build.py, do not change it)
- The post's photo fills the frame. A torn cream paper card sits at the BOTTOM (bottom left on desktop).
- On the card: category word (Montserrat Bold), headline (Source Sans 3), optional deck line,
  a black READ POST box (EB Garamond) with a mouse cursor, and www.soilfoodweb.com.

## The five sizes and the file names
One folder per post, named after the post title with no number in front
(e.g. `What exactly is Brownian motion`). Inside, five JPGs named `{slug}--{Size}.jpg`:

| Size | File name ending |
| --- | --- |
| Desktop 1920x720 | `--Desktop-1920x720.jpg` |
| Tablet 1024x768 | `--Tablet-1024x768.jpg` |
| Mobile 750x1000 | `--Mobile-750x1000.jpg` |
| Social Square 1400x1400 | `--Social-Square-1400x1400.jpg` |
| Thumbnail 3:2 1200x800 | `--Thumbnail-3x2-1200x800.jpg` |

Deliver it as ONE zip per post that holds that single folder, e.g. `What exactly is Brownian motion.zip`.

## Hard rules from Linnea
- Never crop or cover a face. Check every size by eye: the paper card must not cover anyone's face, and no head may be cut by an edge.
- Never use a plain green background, and never blur a photo to fill space.
- Never drop the post's own photo. A second photo may only be added beside it (desktop usually), and only if it clearly belongs to the post (same place, same subject, same event). No random filler photos.
- Do not reuse a photo that is already on another header.
- No AI-looking images.
- Unsplash photos need the credit `Photo: [name] / Unsplash` in small white text, lower right of the picture.
- Look at all five images yourself before sending anything. Send a preview strip of the five sizes along with the zip.
- Do not change any header that is already approved.

## Setup in a fresh container
```
python3 -m pip install --ignore-installed pillow python-pptx pymupdf
mkdir -p ~/.local/share/fonts && cp tools/blog-cards/fonts/*.ttf ~/.local/share/fonts/ && fc-cache -f
```
(LibreOffice `soffice` must be installed. Without the fonts installed, the text renders in the wrong font.)

## Steps
1. Put the photo in `tools/blog-cards/photos/posts2/` with a descriptive name.
2. Add the post to the `POSTS` list in `build.py`, following the entries already there:
   `dict(slug='post-slug', date='YYYY-MM-DD', cat='Category', field='glow', extra=True, head='Post title', deck='', img='tools/blog-cards/photos/posts2/photo.jpg', focus=(.5, .4))`.
   `focus` is where the important part of the photo is (x, y as fractions).
3. If the photo has people, add their face boxes to `HEADS` as (x0, y0, x1, y1) fractions, so the crop keeps faces whole and clear of the card.
   If a size still crops badly, add a hand crop for that size to `CROP` (see the examples there).
4. Build and export:
   ```
   STYLE=brand ONLY=post-slug python3 tools/blog-cards/build.py OUT
   python3 tools/blog-cards/export_jpgs.py OUT EXPORT "post-slug:Post title folder name"
   ```
5. Look at all five JPGs. Fix crops and rebuild until they are right.
6. Zip the folder (`cd EXPORT && zip -r "Post title folder name.zip" "Post title folder name"`), send the zip and a preview,
   copy the folder into `tools/blog-cards/export/SFW blog headers/`, commit and push.

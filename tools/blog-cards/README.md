# Blog cards

One editable PowerPoint per size, one slide per post, made to be dragged into
the Canva "Blogs Updated" folder:

| File | Size |
| --- | --- |
| feature-social | 1400 x 1400 |
| desktop-header | 1920 x 720 |
| tablet-header | 1024 x 768 |
| mobile-header | 750 x 1000 |

The layout is Linnea's PDC card (colour field, cream card, category word,
headline, READ POST with the cursor, web address) with the post's photograph
whole beside or above the card. Every piece is its own layer: the text is live
text, the photo is one image, the colour field and card are shapes. (The cut
"planes" version is still in build.py; Linnea turned it down.)

```
pip install python-pptx pillow
python3 tools/blog-cards/build.py <output folder>            # all four
python3 tools/blog-cards/build.py <output folder> tablet-header-1024x768
./tools/blog-cards/preview.sh <deck.pptx> <sheet.png>        # needs LibreOffice Impress
```

Posts, colours, headline splits and photos are the `POSTS` list at the top
of `build.py`. Fonts in `fonts/` are the site's own (OFL), converted to TTF
for measuring.

## Open items

- Photos: upload each post's original to `photos/` under its slug (see
  `photos/README.md`) and rerun. Until then each card uses a stand-in from `img/`.
- Headlines are the live titles split at their own colon or dash; the deck
  line is the other half. The PDC card keeps Linnea's wording. Category words
  follow the blog's categories, except PDC (Education, Linnea's) and the
  obituary (In Memoriam). Check before publishing.
- Only the ciliates post has a known author, so no card carries a byline.

# Blog cards

One editable PowerPoint per size, one slide per post, made to be dragged into
the Canva "Blogs Updated" folder:

| File | Size |
| --- | --- |
| feature-social | 1400 x 1400 |
| desktop-header | 1920 x 720 |
| desktop-header-clean | 1920 x 720, the photograph whole, no planes |
| tablet-header | 1024 x 768 |
| mobile-header | 750 x 1000 |

The layout is Linnea's PDC card (colour field, cream card, category word,
headline, READ POST with the cursor, web address) with the post's photograph
cut into planes, each a slightly different view of the same picture. Every
piece is its own layer: the text is live text, each photo plane is its own
PNG, the colour field and card are shapes.

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

- Every photograph is a stand-in from `img/`. The posts' own original,
  unedited photographs replace them in `POSTS`, then rerun.
- Headlines are the live titles split at their own colon or dash; the deck
  line is the other half. The PDC card keeps Linnea's wording. Category words
  follow the blog's categories, except PDC (Education, Linnea's) and the
  obituary (In Memoriam). Check before publishing.
- Only the ciliates post has a known author, so no card carries a byline.

# Motion exports as GIF

Every moving thing on the live site, exported as a looping GIF for use off the web
(slides, email, social, print reference). Generated from the source videos in `video/`
and from Playwright captures of the live pages.

## From the site's own video loops

| File | Source | Size | Notes |
|---|---|---|---|
| `amoeba-loop-square.gif` | `video/sfw-amoeba-loop-square` | 360x360, 10s | Home page slideshow, first slide |
| `amoeba-lab.gif` | `video/sfw-amoeba-lab-640` | 400x225, 10s | Home slideshow, learn.html, volunteer.html |
| `amoeba-loop-hero.gif` | `video/sfw-amoeba-loop-hero` | 400x225, 10s | Home slideshow, third slide |
| `amoeba-social-square.gif` | `video/sfw-amoeba-instagram-4x5` | 360x360, 10s | Social clip. The source has a caption card baked into the bottom 270px, cropped off here. Full frame kept. |
| `amoeba-social-4x5.gif` | `video/sfw-amoeba-instagram-4x5` | 320x400, 10s | Same clip kept at 4:5 for social. Side cropped rather than bottom cropped, so no caption. |
| `wkh-clip-1465.gif` | `video/wild-ken-hill/IMG_1465` | 260x461, 8s | Wild Ken Hill workshop footage |
| `wkh-clip-1467.gif` | `video/wild-ken-hill/IMG_1467` | 260x461, 8s | Wild Ken Hill workshop footage |
| `wkh-clip-1471.gif` | `video/wild-ken-hill/IMG_1471` | 260x461, 7s | Wild Ken Hill workshop footage |
| `wkh-reel-excerpt.gif` | `video/wild-ken-hill/wkh-2026-reel-web` | 260x461, 8s | First 8s only. The full reel is 41s, too long for a usable GIF. |

## Captured from the live pages

| File | What it shows | Size |
|---|---|---|
| `btn-primary-hover.gif` | `.btn` rest to hover and back: green to moss, 1px lift, corner radius morph | 462x142 |
| `btn-ghost-hover.gif` | `.btn--ghost` rest to hover and back: outline fills green | 300x142 |
| `btn-donate-hover.gif` | `.btn--donate` rest to hover and back: gold to deeper gold | 264x142 |
| `microbe-hover.gif` | Single microbe cutout, hover scale to 1.1 and back | 504x384 |
| `microbe-float.gif` | Full microbe gallery, one complete 4s `microbeFloat` cycle with the per item stagger | 1104x350 |

## Not exported, and why

These keyframes exist in `css/site.css` but are not used by any page currently in the
site, so there was nothing live to capture: `grow`, `marq`, `sfwdrift`, `sfwfield`,
`pgdrift`, `pgbreathe`, `scoperack`. They appear to be left over from the `_dev/`
mockups. Worth a look on the next cleanup pass.

`fadeUp` is used only by `.role-picker__courses.is-visible`, which no current page
builds, so it was not captured either.

## A note on baked in text

`video/sfw-amoeba-instagram-4x5.mp4` is the only source with text burned into the
picture: a white caption card reading "What lives in one drop?" over the bottom 270px.
The video area above it is a clean 1080x1080. Both GIFs made from it crop that card away.
Every other source in `video/` is clean footage with no text.

## How these were made

ffmpeg with a per clip generated palette, then `gifsicle -O3`. Settings differ by
footage type, and this matters:

- **Live action (the Wild Ken Hill clips): 256 colours, `sierra2_4a` dither,
  `--lossy=30`.** These were first encoded at 64 colours with heavy Bayer dither and
  `--lossy=110`. That was wrong. With so few colours the palette was taken over by the
  sand and concrete, and skin tones shifted from pink to sandy beige while the yellow
  and teal marker tape disappeared. Anything with skin tones or a wide colour range
  needs the full palette. The files are around 4 to 5 MB as a result, which is the
  honest cost of correct colour.
- **Microscopy (the amoeba loops): 64 colours, Bayer dither, `--lossy=110`.** Checked
  against source and fine. That footage is close to monochrome grey and olive, so a
  small palette costs nothing visible.
- **Interface captures: 64 to 128 colours, no dithering**, so the flat brand colours
  stay flat rather than being stippled.

Regenerating means rerunning the same two steps against the sources, there is no
checked in script. If you do regenerate, compare a frame against the source before
trusting the result.

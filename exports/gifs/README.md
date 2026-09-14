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
| `amoeba-instagram-4x5.gif` | `video/sfw-amoeba-instagram-4x5` | 320x400, 10s | Social crop, not used on a page |
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

## How these were made

ffmpeg with a per clip generated palette, then `gifsicle -O3`. The video derived GIFs
use 64 colours and lossy compression to keep them under about 3 MB; the interface
captures use no dithering so the flat brand colours stay flat. Regenerating them means
rerunning the same two steps against the sources, there is no checked in script.

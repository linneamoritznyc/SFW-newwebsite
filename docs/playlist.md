# The video playlist

What was wrong with the old one, what replaces it, and how to fill it.
Written 11 September 2026.

## The five bugs, and where each one is fixed

The old playlist lives on six WordPress pages and carries each video as a
query string: `?vID=537966540&h=a79eb5d201`. The `h` is the private hash,
and an unlisted video does not play without it.

**1. The hash gets lost.** The page copies `h` out of the URL and into the
player. A link written without it hands the player `?h=` and Vimeo refuses.
The "Other Playlists" thumbnails on the Implementing page link to Case
Studies with no `h` at all.
*Fixed by:* the hash lives in `content/videos.json`, written by a machine
from the page that already works. No link carries it, so no link can drop
it.

**2. One link is mangled.** `?vID=372925873%3Fh%3D707aa77aa3` is
`?vID=372925873?h=707aa77aa3` once unescaped: the hash was pasted inside the
id, so the id is not a number.
*Fixed by:* `tools/playlist.py` reads that shape too. It unescapes first,
splits the id at the `?`, and recovers the hash from the tail. The mangled
link is data, and data can be repaired; a hand-typed hash cannot.

**3. The clean URL shows an empty player.** Google indexes the canonical URL,
which has no `vID`, so a visitor from search gets `player.vimeo.com/video/?h=`
and a blank box.
*Fixed by:* there is no empty state. The page always knows its own playlist,
starts at the first video, and shows a poster rather than a player. A URL
with no `?v=` is a valid URL.

**4. The items link to a redirect.** They drop `/resources/`, so every click
goes through a 301 before it loads.
*Fixed by:* nothing to fix. The new site has no `/resources/` prefix, and
clicks do not navigate at all.

**5. Every video is a full page reload.** Each click reloads the whole of
WordPress, the menus, WPBakery, the tag manager, and the privacy policy and
terms text sitting hidden in the markup, and then Vimeo boots a new player
from zero. This is the slowness, and it is also why autoplay into the next
video is impossible: the page that would have started it no longer exists.
*Fixed by:* one player, created once, on the first click. Every video after
that is `player.loadVideo()` on the player already running, and the URL
changes with `history.pushState`. Nothing reloads. `js/site.js` job 11.

Two smaller ones, for whoever edits the source pages: Nick Padwick has an
empty thumbnail, and the Consultant and Farmer case studies share one image.
Both are fixed by putting a real still in the playlist markup, which
`tools/playlist.py` then picks up.

## Vimeo or YouTube

Vimeo, and the question matters less than it looks.

A fresh iframe per video is slow on both: the platform's script is the
weight, several hundred kilobytes of it, and it is paid again every time the
page reloads. One player that stays on the page and swaps videos pays it
once. That architecture is worth more than any difference between the two
platforms.

Nothing third-party loads here until someone presses play. Until then the
stage is a poster and a button, so arriving at the page costs nothing at
all. This is the facade pattern, and it is the single biggest speed
difference between this and either platform's embed dropped into a page.

Vimeo wins the rest on merit: the videos already live there, there are no
ads, and the end screen stays clean. YouTube ends every video with a grid of
recommendations, which is a door out of the site, and for a nonprofit under
Ad Grant review that register matters.

The player is created with `dnt: true`, so Vimeo sets no tracking cookies.

## The Netflix parts

- **Autoplay into the next video.** When one ends, a panel names the next
  one and counts down from eight, with "Play now" and "Cancel". The first
  play needs a click, because browsers block autoplay with sound; every
  video after that starts on its own, with sound, because the player never
  leaves the page.
- **"Are you still watching?"** After three videos in a row with nobody
  touching anything, it stops and asks instead of playing to an empty room.
  A click, a tap, a pause or a scrub resets the count.
- **Clean, linkable URLs.** `?v=market-garden-makeover` rather than
  `?vID=537966540&h=a79eb5d201`. The hash is not in the URL, so a shared
  link cannot leak or lose it. The back button works.
- **The rail** marks what is playing in the page's accent colour and shows
  each video's real duration, from Vimeo.

If Vimeo's script fails to load, the stage falls back to opening the video
on Vimeo directly. The content stays reachable.

## Filling it

`content/videos.json` ships empty. It is written by:

    cd /path/to/SFW-newwebsite
    python3 tools/playlist.py

Nothing to install. Standard library only, so the Python that comes with
macOS runs it as it is: no `pip`, no `requests`, no BeautifulSoup, no virtual
environment. It writes into the `content/` folder beside itself rather than
into whatever folder you are standing in, so
`python3 ~/SFW-newwebsite/tools/playlist.py` works from anywhere, and it
prints the path it is writing to before it starts.

**Run it locally.** Like `crawl.py`, it needs soilfoodweb.com and vimeo.com,
and the cloud sandbox has no route to either.

It reads the six playlist pages, pulls every `vID` and `h` with the title,
the other lines and the thumbnail beside them, and then checks each one:

    https://vimeo.com/api/oembed.json?url=https://vimeo.com/ID/HASH

200 with a title means it will play. Anything else means the hash is wrong
or the video has been made private, and it is printed at the end as a list
of what to fix rather than written into the file. So a broken video is found
before launch instead of by a visitor. `--verify-only` re-checks what is
already there, which is worth running before each deploy.

Thumbnails are downloaded into `img/video/` rather than hotlinked, so the
rail does not wait on Vimeo's CDN.

Until the file has entries, the Practice page shows exactly what it showed
before: the case-study placeholder. The theatre renders nothing rather than
an empty player, which is bug 3 again.

## One conflict to settle when it runs

The copy deck calls **372925873** the How It Works *playlist*.
`content/science.json` calls it mechanism 1's *video*. One of them is wrong,
and the scrape will say which. Nothing has been seeded from either.

## Two things the fixture test caught

Worth recording, because both were the same mistake in different clothes:
deciding something the page already knows.

**The lines beside the title are not labelled.** An item carries a title and
then one or two more lines, and which is the person and which is the place
varies across the six pages. The first version guessed, and rendered "Sweden
· Renald Flores" backwards. Now nothing guesses: the lines are joined in the
order the page wrote them.

**Slugs came from the guess**, so they read `?v=sweden-market-garden-makeover`.
They come from the title alone now, with the video id appended only when two
videos would otherwise claim the same slug.

The test lives in the scratch directory rather than the repository, and drives
the whole script against fixture markup with no network: a good link, a link
with no hash whose hash is recovered from the iframe, the mangled
`vID=372925873%3Fh%3D707aa77aa3`, a lazy-loaded `data:` thumbnail, and a hash
Vimeo refuses.

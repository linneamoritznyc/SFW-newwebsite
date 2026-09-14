# Openly licensed photographs

Drop openly licensed files here. This folder is the store for photographs the
Foundation did not take: public domain and Creative Commons work brought in to
fill a slot until the Foundation's own picture arrives, or kept because the
picture itself is right.

Nothing in here is a Foundation photograph, and nothing in here may be captioned
as one.

## The rule that matters

**A file without a recorded licence does not go in.** Not "it looked public
domain", not "the account is a government account". The licence as stated on the
file's own source page, recorded in `CREDITS.json`, per file. A photograph
published without that is a claim the Foundation cannot back.

The same goes for what a picture says. A caption naming a place, a date or a
person is a statement of fact, so it comes from the source page, never from what
the picture looks like. Where the source gives no place or date, the caption
does not invent one.

## Adding files

1. Save the original at its largest available size, named in lower case with
   hyphens, describing what is in it: `soil-pit-survey-crew-montana-1979.jpg`,
   not `53393769821_a1b2c3.jpg`.
2. Add an entry to `CREDITS.json` with the source URL, title, author and licence
   exactly as the source page gives them. Leave a field empty rather than
   guessing at it.
3. To put one on a page, copy it up into `img/` and run `python3 tools/images.py`.
   That script reads files directly in `img/` and writes the 1600 and 800 pixel
   versions into `img/w/` that the pages actually load. It does not descend into
   this folder, which is deliberate: arriving here is not the same as being
   chosen.

## Where these came from

**USDA Natural Resources Conservation Service, Montana.**
https://www.flickr.com/photos/160831427@N06/

Modern field photography alongside a scanned soil survey archive from the 1970s
to the 1990s: soil profiles, survey crews with augers and spades, hands in soil,
people standing in pits, cover crops and grazing land.

Work by an officer or employee of the United States government, made as part of
their official duties, carries no copyright in the United States. That is the
usual position for this account, and Flickr shows it per photograph as
"United States Government Work".

Check the licence field on each photograph rather than assuming it from the
account. Agency accounts sometimes carry contributed, contractor or partner
photographs that are not federal works and are not free to use.

## Why the folder was empty until now

An earlier build environment could not reach commons.wikimedia.org,
nrcs.usda.gov or archive.org. Every request was refused at the egress proxy with
a 403, and Flickr is refused the same way today. Nothing was fetched, and no
credit line was written for a file nobody had opened. Files reach this folder by
being uploaded by hand.

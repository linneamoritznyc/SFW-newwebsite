# WordPress migration guide

This document maps the static HTML site to its WordPress equivalents so the migration
developer knows exactly where to cut.

---

## Architecture overview

| Static site | WordPress equivalent |
| :-- | :-- |
| `css/site.css` `:root` tokens | `theme.json` design tokens (colors, spacing, typography) |
| `css/site.css` component classes | Theme stylesheet (`style.css`) |
| `js/site.js` | Enqueued theme script (`assets/js/site.js`) |
| `fonts/` directory | `assets/fonts/` in the theme, loaded via `@font-face` in stylesheet |
| `content/*.json` | ACF field groups or WordPress custom fields |
| `vercel.json` rewrites | WordPress permalink settings (already clean URLs) |
| `vercel.json` redirects | Redirection plugin or `.htaccess` rules |
| `vercel.json` security headers | `.htaccess` or server config |

---

## Template parts

Each HTML page uses the same header and footer. These become WordPress template parts.

| HTML section | WP template part | Notes |
| :-- | :-- | :-- |
| `<header class="header">` | `parts/header.html` or `get_template_part('header')` | Includes the logo, nav links, and menu button |
| `<nav id="overlay">` | `parts/overlay-menu.html` | Full-screen overlay menu with accordion sections |
| `<footer class="footer">` | `parts/footer.html` | Newsletter form, legal block, social links |
| SVG icon sprite | Inline in `functions.php` via `wp_body_open` hook | `img/icons.svg` content |

---

## Page-to-template mapping

| HTML file | WordPress template | Content type |
| :-- | :-- | :-- |
| `index.html` | `front-page.php` or Front Page block template | Page |
| `learn.html` | Custom page template `page-learn.php` | Page |
| `science.html` | Custom page template `page-science.php` | Page |
| `about.html` | Page template (default) | Page |
| `about-governance.html` | Page template (child of About) | Page |
| `about-team.html` | Custom page template `page-team.php` | Page, with team member CPT query |
| `about-elaine.html` | Page template (child of About) | Page |
| `practice.html` | Custom page template with case study CPT query | Page |
| `community.html` | Custom page template | Page |
| `calendar.html` | Custom page template with event CPT query | Page |
| `research.html` | Custom page template with publication CPT query | Page |
| `donate.html` | Page template | Page |
| `contact.html` | Page template | Page |
| `volunteer.html` | Custom page template | Page |
| `directory.html` | Custom page template with directory CPT query | Page |
| `news.html` | Archive template (`archive.php`) | Posts |
| `news/wild-ken-hill-2026.html` | Single post (`single.php`) | Post |
| `projects/market-garden-sweden.html` | Single CPT (`single-case_study.php`) | Case study CPT |
| `privacy.html` | Page template | Page |
| `terms.html` | Page template | Page |
| `accessibility.html` | Page template | Page |

---

## Custom post types (CPT)

| CPT | Source in static site | Fields |
| :-- | :-- | :-- |
| `team_member` | Cards in `about-team.html` | Name, title, bio, portrait, order |
| `case_study` | Cards in `practice.html`, pages in `projects/` | Title, body, before/after photos, Vimeo ID, hash, location |
| `publication` | List in `research.html`, data in `content/research.json` | Title, authors, journal, year, DOI, collection |
| `event` | Rows in `calendar.html`, data in `content/calendar.json` | Title, dates, location, link, type (workshop/webinar) |

---

## Block patterns

Reusable HTML sections that become WordPress block patterns.

| Pattern name | Where it appears | Key classes |
| :-- | :-- | :-- |
| Hero band | Top of most pages | `.band`, `.hero` |
| Card grid | Learn, community, about-team | `.cards`, `.card` |
| Testimonial | Index, learn | `.quote` |
| Before/after comparison | Practice page | `[data-compare]` |
| Video facade | Practice, science | `[data-film]` |
| Pathway diagram | Learn page | `[data-pathway]` |
| Filter chips | Research, community, volunteer | `[data-filter-for]`, `.chips` |
| Accordion | Learn, overlay menu | `[data-accordion]` |
| Photo ledger | Multiple pages | `.ledger` |
| Step list | Learn-scholarships, volunteer | `.step` |

---

## CSS token mapping to theme.json

The `:root` tokens in `site.css` map directly to `theme.json` settings:

```
:root {
  --color-earth:       → settings.color.palette[slug: "earth"]
  --color-cream:       → settings.color.palette[slug: "cream"]
  --color-leaf:        → settings.color.palette[slug: "leaf"]
  --space-xs:          → settings.spacing.spacingSizes[slug: "xs"]
  --font-serif:        → settings.typography.fontFamilies[slug: "serif"]
  --font-sans:         → settings.typography.fontFamilies[slug: "sans"]
}
```

---

## Assets

- **Images:** Copy `img/` contents into the WordPress Media Library. Filenames match the
  Foundation's Google Drive — do not rename them.
- **Videos:** The site embeds Vimeo videos via facades, not self-hosted files. The `video/`
  directory holds only the amoeba animation loops used as decorative backgrounds. These go
  into `assets/video/` in the theme.
- **Fonts:** Move `fonts/*.woff2` into `assets/fonts/` in the theme. Register them in
  `theme.json` under `settings.typography.fontFamilies`.

---

## Redirects

`vercel.json` contains 30+ redirects from old WordPress URLs to new paths. These need to
be replicated in the WordPress site, either via the Redirection plugin or in `.htaccess`.
The full list is in `vercel.json` under `"redirects"`.

---

## JavaScript

`js/site.js` is vanilla JS with no dependencies. It can be enqueued as-is in the WordPress
theme. The only external script it loads is the Vimeo Player API (`player.vimeo.com`),
and only on demand when a visitor plays a video.

---

## Content data

The `content/*.json` files hold structured data that the static pages consume. In WordPress
these become:

| JSON file | WordPress equivalent |
| :-- | :-- |
| `content/videos.json` | ACF repeater field on the Practice page, or a video CPT |
| `content/calendar.json` | Event CPT entries |
| `content/research.json` | Publication CPT entries |
| `content/learn.json` | ACF field group on the Learn page |
| `content/global.json` | Theme options (ACF options page) or `theme.json` |

---

## What to keep from this repo during migration

1. All CSS class names and design tokens — the design system is done
2. The JS logic in `site.js` — it works and handles accessibility correctly
3. The `OPEN-ITEMS.md` tracker — outstanding content gaps carry over
4. The image filenames — they match the Google Drive
5. The redirect list in `vercel.json`
6. The `content/*.json` data files for initial content import

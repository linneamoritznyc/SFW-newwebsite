# Soil Food Web Consultant Directory

## Concept note

The Soil Food Web consultant directory is currently a set of pages you scroll through, with long-form bios for consultants and a flat contact list for lab-techs, which means finding the right person depends on reading everything and guessing. Future development would restructure that same information into filterable fields covering role (consultant, lab-tech, or both), crops worked, soil and climate types, languages spoken, certification year, travel radius, remote availability, and whether they are currently taking clients, with multi-select filters that combine across categories, free-text search across names, locations and bios, and shareable URLs so a filtered view can be sent to someone else. Those results would sit alongside a clustered map with markers colour-coded by role, linked so that hovering a listing highlights its pin and clicking a pin opens the profile, and remote-capable practitioners would still surface in searches outside their travel radius, flagged as remote. When a search returns nothing, the interface would name the filter that failed and show the nearest alternatives rather than an empty page, and a short intake form would let a grower describe their situation and receive a shortlist of three suitable practitioners instead of browsing manually. Lab-techs would be surfaced in the same interface rather than on a separate page, since they are the cheaper entry point and there are more than twice as many of them. Nothing is removed. The same practitioners, made findable.

---

# Product Requirements Document

**Product:** Soil Food Web Practitioner Directory v2
**Status:** Draft for discussion
**Owner:** TBD

---

## 1. Problem

A grower with a specific problem cannot currently find the right practitioner without reading every bio on the page and inferring fit. Three consequences follow.

**Growers self-select badly.** Someone with an olive grove in Andalusia has no way to know whether any of the listed practitioners has worked Mediterranean calcareous soils, or speaks Spanish, or is even taking clients. They either contact the geographically nearest name or give up.

**Lab-techs are invisible.** There are roughly 250 certified lab-techs against roughly 100 consultants. Lab-techs are the cheaper entry point for a grower who wants a soil assessment rather than a full advisory engagement. They currently sit on a separate page as a flat contact list, so the larger and more accessible half of the network is the half nobody browses.

**The network's shape is unknown internally.** Nobody can answer "how many practitioners work tropical smallholder systems" or "where do we have coverage gaps" because the data is prose, not fields.

## 2. Goals and non-goals

**Goals**

- A grower can find a suitable practitioner in under 60 seconds without reading bios
- Lab-techs and consultants surface in the same interface, differentiated by role
- The organisation can query its own network structurally
- Practitioner profiles are self-maintained, not admin-maintained
- Works on a phone, outdoors, on a slow connection

**Non-goals for v1**

- Payments, contracts, or escrow
- Reviews or ratings (see section 9 on why this is deliberate)
- Bidding or reverse auctions (erodes the premium positioning of the credential)
- Replacing the existing bio content, which is good and should be preserved inside the richer profile

## 3. Users

| User | Comes with | Needs |
|---|---|---|
| Grower / farmer | A specific problem, a location, a budget range | A shortlist of 3 people who can actually help |
| Certified practitioner | A profile they want to be found through | Control over their listing, and qualified enquiries |
| Foundation staff | Questions about network coverage | Structural view, gap analysis, export |

## 4. Data architecture

### 4.1 Core entity

```
practitioner
  id                    uuid pk
  slug                  text unique          -- URL-safe, stable
  display_name          text
  roles                 role_enum[]          -- consultant | lab_tech | grower
  certified_since       int
  certifications        jsonb                -- [{program: 'CTP', year: 2022}]
  status                enum                 -- active | inactive | pending
  accepting_clients     bool
  services_remotely     bool
  travel_radius_km      int null
  contact_email         text                 -- never exposed raw, see 8.2
  contact_phone         text null
  website_url           text null
  location              geography(Point,4326)
  city                  text
  admin_area            text                 -- state/province/region
  country_code          char(2)              -- ISO 3166-1 alpha-2
  ecoregion_id          int fk               -- derived, see 4.3
  biome_id              int fk               -- derived
  realm_id              int fk               -- derived
  created_at            timestamptz
  updated_at            timestamptz
```

### 4.2 Why controlled vocabularies, not free tags

Free-text tags fragment immediately across a multilingual network. One practitioner writes "vineyard", another "wine grapes", a third "viticultura". Search then fails silently, which is worse than failing loudly.

Every filterable attribute is therefore a foreign key into a controlled vocabulary table, with a stable integer or slug ID that never changes, and a separate translations table holding the human-readable label per locale.

```
vocabulary_term
  id            int pk
  vocabulary    enum        -- crop | soil_type | climate | language
                            -- | practice | land_use
  slug          text unique -- 'vineyard', never translated
  parent_id     int null fk -- enables hierarchy, see below
  sort_order    int

vocabulary_term_i18n
  term_id       int fk
  locale        char(5)     -- 'en', 'es', 'pt-BR', 'tr', 'sv'
  label         text
  synonyms      text[]      -- search-time expansion only
  primary key (term_id, locale)
```

**Hierarchy matters for recall.** Crops are nested: `perennial_fruit > vine_fruit > vineyard`. A search for "perennial fruit" returns vineyard practitioners. A search for "vineyard" does not return everyone who has ever touched a fruit tree. Query expansion goes down the tree, never up.

**Synonyms are search-time only.** They expand a query; they never appear as selectable filter options. This keeps the filter UI clean while making the search forgiving.

### 4.3 Ecoregion tagging

This is the piece that makes the directory meaningfully better than a map with pins on it.

**The dataset.** RESOLVE Ecoregions 2017 (Dinerstein et al.). 846 terrestrial ecoregions, grouped into 14 biomes and 8 biogeographic realms. Distributed as a polygon shapefile, freely available, and already the standard basemap for conservation planning because it draws on natural rather than political boundaries.

**Why it belongs here.** Political geography is a poor proxy for ecological similarity. A practitioner in southern Spain and one in coastal California share a Mediterranean Forests, Woodlands and Scrub biome, similar rainfall seasonality, and similar soil biology challenges. They are 9,000 km apart and in different countries. Conversely, two practitioners 300 km apart in Chile can sit in entirely different ecoregions with nothing transferable between them.

Country filters cannot express this. Ecoregion filters can.

**Implementation.**

1. Load the RESOLVE shapefile into PostGIS as `ecoregion(id, eco_name, biome_id, realm_id, geom)`.
2. Build a GiST index on `geom`.
3. On practitioner create or location update, run a point-in-polygon lookup:

```sql
UPDATE practitioner p
SET ecoregion_id = e.id,
    biome_id     = e.biome_id,
    realm_id     = e.realm_id
FROM ecoregion e
WHERE ST_Contains(e.geom, p.location)
  AND p.id = $1;
```

4. Store the derived IDs denormalised on the practitioner row so filtering does not require a spatial join at query time.
5. Handle the coastal edge case: if `ST_Contains` returns nothing (point falls in water or on a boundary gap), fall back to nearest polygon within 25 km via `ST_DWithin` ordered by `ST_Distance`, and flag the record for review.

**What it unlocks in the product.**

- *"Find practitioners in an ecologically similar place to mine."* A grower enters their location, the system resolves their ecoregion, and surfaces practitioners in the same ecoregion first, then the same biome, then anywhere remote-capable. This is a fundamentally better relevance signal than distance.
- *Coverage analysis for the Foundation.* Which of the 14 biomes have no certified practitioners? That is a recruitment and course-marketing roadmap, generated automatically.
- *Credibility.* "We have practitioners across 40 ecoregions on 6 continents" is a stronger and more precise claim than "six continents", and it is verifiable.

**Caveat to state plainly.** Ecoregion is a biodiversity classification, not a soil classification. Two points in one ecoregion can have very different soils. It is a good coarse similarity signal and should be presented as one, never as a claim about soil equivalence. If soil-level matching is wanted later, the honest addition is the FAO/HWSD soil classification as a separate independent field, not a conflation with ecoregion.

### 4.4 Junction tables

```
practitioner_crop        (practitioner_id, term_id, years_experience int null)
practitioner_soil_type   (practitioner_id, term_id)
practitioner_language    (practitioner_id, term_id, proficiency enum)
practitioner_practice    (practitioner_id, term_id)
```

`proficiency` on language is `native | fluent | working`. A grower filtering for Turkish should be able to distinguish a native speaker from someone with working Turkish, because a technical soil conversation is not small talk.

## 5. Search architecture

### 5.1 The multilingual problem

The network spans at least a dozen working languages. A naive `ILIKE '%vineyard%'` fails for every non-English speaker, and a single Postgres full-text index fails because stemming rules are language-specific: the English stemmer will mangle Turkish, and Turkish agglutination will defeat the English stemmer.

### 5.2 Approach

**Layer 1: structured filters.** Language-independent by construction. Filtering by `crop_id = 47` works identically regardless of the user's locale, because the ID carries the meaning and the translation table carries the label. This handles the majority of real queries and should be the primary interaction.

**Layer 2: free-text search over a per-locale index.**

```sql
ALTER TABLE practitioner ADD COLUMN search_vector_en tsvector;
ALTER TABLE practitioner ADD COLUMN search_vector_es tsvector;
-- one per supported locale

CREATE INDEX idx_search_en ON practitioner USING GIN (search_vector_en);
```

Each vector is built with the matching language configuration and weighted:

```sql
setweight(to_tsvector('english', display_name), 'A') ||
setweight(to_tsvector('english', city || ' ' || admin_area), 'B') ||
setweight(to_tsvector('english', crop_labels_en), 'B') ||
setweight(to_tsvector('english', bio_en), 'C')
```

Weighting means a name match outranks a bio mention, which is what users expect.

**Layer 3: fuzzy fallback.** Enable `pg_trgm` and add a trigram index on `display_name` and `city`. When full-text returns fewer than three results, retry with similarity matching. This catches misspellings and transliteration variance ("Türkiye" / "Turkiye" / "Turkey", "Gothenburg" / "Göteborg").

**Layer 4: query-time synonym expansion.** Before searching, expand the user's term against `vocabulary_term_i18n.synonyms` in their locale and across locales. A Spanish speaker typing "viñedo" hits `term_id 47`, which resolves to practitioners tagged vineyard regardless of what language their profile is written in.

### 5.3 Ranking

Results are ordered by a composite score, computed at query time:

| Signal | Weight | Rationale |
|---|---|---|
| Ecoregion match with grower's location | 0.30 | Strongest ecological relevance signal |
| Crop overlap with stated need | 0.25 | Direct experience |
| Language match | 0.20 | Hard requirement in practice, soft in ranking |
| Accepting clients | 0.15 | Availability |
| Within travel radius, or remote-capable | 0.10 | Logistics |

Certification recency and years of experience are deliberately excluded from ranking. Ranking by seniority entrenches early cohorts and starves new graduates of work, which is bad for the network and bad for course sales.

### 5.4 Facet counts

Every filter option displays its result count, computed against currently applied filters. This prevents dead ends: the user sees "Turkish (3)" before clicking rather than after. Implement with a single `GROUP BY` over the filtered set rather than N separate count queries.

## 6. Interface

### 6.1 Layout

Desktop: filter rail left (280px), results list centre, map right, roughly 3:4:5. Map and list are one selection model, not two views. Hover a card and its pin lifts; click a pin and its card scrolls into view and highlights.

Mobile: map full-bleed with a swipeable bottom sheet at three detents (peek showing result count, half showing scrollable list, full showing list only). This is the primary experience. Assume a grower standing in a field on a mid-range Android in sunlight.

### 6.2 URL as state

Every filter combination serialises to query parameters:

```
/directory?role=consultant&crop=vineyard,olive&lang=es&remote=true
```

Shareable, bookmarkable, back-button correct, and it means Foundation staff can send a pre-filtered link to an enquiring grower. Non-negotiable.

### 6.3 Empty states

An empty result set must name the constraint that failed and offer the nearest relaxation:

> No consultants found who speak Turkish and have vineyard experience within 200 km of Izmir.
>
> **3 consultants** speak Turkish and work remotely.
> **7 consultants** have vineyard experience in the Mediterranean biome.

Never a blank page. The empty state is where a directory either helps or loses the user permanently.

### 6.4 Profile page

Preserves the existing long-form bio, which is the most human and trust-building content the organisation currently has. Structure sits around it, not instead of it:

- Header: name, roles, certifications with year, accepting-clients status
- Structured summary: crops, soils, languages, ecoregion and biome, service area
- The existing bio, unabridged
- Case studies, if any, linked from their existing consultant case study pages
- Contact via form, not exposed email (see 8.2)

### 6.5 Guided intake

A short conditional form for growers who do not want to filter manually. Six to eight questions maximum, one per screen, with a progress indicator and the ability to go back without losing answers.

Questions: location, land size band, primary crop, primary problem (fertility / disease / compaction / transition to organic / other), whether they want on-site or remote, budget band, timeline.

Output: three ranked practitioners with a plain-language explanation of why each was matched. The explanation matters more than the ranking. "Matched because she works Mediterranean calcareous soils and speaks Spanish" is trustworthy in a way that a bare list is not.

## 7. Practitioner-facing side

Profiles must be self-maintained or they rot within a year.

- Magic-link login, no password
- Edit all structured fields and bio
- Toggle accepting-clients in one tap, from mobile, because this is the field most likely to be stale
- Quarterly automated prompt: "Is your profile still accurate?" with one-click confirm
- Records untouched for 18 months are flagged internally, not hidden publicly

## 8. Compliance and privacy

### 8.1 Legal basis

The network includes practitioners in the EU and UK, so GDPR applies regardless of where the organisation is incorporated. Publishing name, location, contact details and professional history is processing personal data.

Requirements:

- Explicit opt-in consent for public listing, recorded with timestamp and version of the terms consented to
- Self-service removal from the public directory without contacting anyone
- A documented retention policy for practitioners who lapse or leave
- Practitioners can be certified without being publicly listed. These are separate decisions and must be separately recorded.

### 8.2 Contact exposure

Do not publish raw email addresses and phone numbers, as the current lab-tech page does. They are scraped within days.

Contact runs through a server-side form that relays to the practitioner's real address. This also produces the first enquiry-volume data the organisation has ever had, which is directly useful for demonstrating the value of certification to prospective students.

### 8.3 Migration note

The public site currently mixes two legal entities: the footer credits Soil Food Web Foundation (501(c)(3)), while the privacy policy on directory pages is issued by Soil Foodweb School LLC. Whichever entity is the data controller for the directory needs to be stated explicitly in the privacy notice, and consent records need to name it correctly. This is a five-minute decision that is expensive to fix retroactively.

## 9. Deliberate omissions

**No ratings or reviews in v1.** With roughly 350 practitioners, review volume per person would be too low to be statistically meaningful, and low-volume review systems reward the loudest client rather than the best practitioner. A single unfair one-star review would materially damage someone's livelihood on this sample size. Revisit above 1,000 practitioners, or replace with structured outcome data from a registry, which is a better signal anyway.

**No bidding.** Reverse auctions push price down and devalue the credential the organisation sells. Matching on fit is the correct mechanic for a premium certification.

## 10. Technical stack

| Layer | Choice | Note |
|---|---|---|
| Frontend | Next.js 14 App Router, TypeScript | Server components for the list, client for the map |
| Styling | Tailwind, brand tokens from the SFW palette | |
| Map | Mapbox GL JS, muted basemap style | Supercluster for marker clustering |
| Database | Postgres 15 with PostGIS, pg_trgm, unaccent | Supabase is sufficient and includes PostGIS |
| Search | Native Postgres full-text | Do not reach for Elasticsearch at this scale |
| Auth | Magic link | Practitioner side only |
| Hosting | Vercel | |

Do not introduce a separate search service. At a few hundred records, Postgres full-text with GIN indexes returns in single-digit milliseconds and removes an entire class of sync bugs.

## 11. Phasing

| Phase | Scope | Duration |
|---|---|---|
| 1 | Schema, vocabularies, ecoregion ingest and tagging, data migration from existing pages | 2 weeks |
| 2 | Public directory: filters, list, map, profile pages, URL state | 3 weeks |
| 3 | Practitioner self-service editing, magic-link auth, contact relay | 2 weeks |
| 4 | Guided intake and matching, match explanations | 2 weeks |
| 5 | Internal coverage dashboard: gaps by biome, by language, by crop | 1 week |

Phase 1 is the phase that determines whether everything after it works. Resist the temptation to start with the map.

## 12. Success measures

- Time from landing on the directory to submitting an enquiry
- Proportion of sessions that reach an enquiry versus bouncing from the list
- Proportion of enquiries that reach a practitioner in a matching ecoregion
- Share of practitioners with a complete structured profile
- Share of lab-tech enquiries as a proportion of total, which tests whether surfacing them worked
- Number of biomes with zero coverage, tracked over time

## 13. Open questions

1. Does the existing Directory (NEW) already implement any of this, and what is its underlying data model? This PRD assumes a rebuild on the existing prose content and should be revised if there is already structure to build on.
2. Who is the data controller, School LLC or the Foundation?
3. Are practitioners currently required to consent to public listing, and is that consent recorded?
4. Should inactive or lapsed practitioners be delisted automatically, and after how long?
5. Is enquiry volume currently measured at all?

---

## Sources

RESOLVE Ecoregions 2017: Dinerstein et al., *An Ecoregion-Based Approach to Protecting Half the Terrestrial Realm*, BioScience 2017. 846 terrestrial ecoregions, 14 biomes, 8 realms. Available via UNEP-WCMC, ArcGIS Hub, and Google Earth Engine.

# Clipping Pipeline — Context Handoff

Paste this at the start of a new chat.

---

## Situation

I'm starting a one-month paid internship (USD 1,000) with the **Soil Food Web Foundation**, beginning Monday. My contact is **Evan Buckman**, Executive Director. He's a fellow Minerva alum; the role came out of an informal interview rather than a formal hiring process, and the scope is deliberately loose — we're using the month to figure out what I take on longer term. He said compensation scales with scope.

I'm a builder, not a soil scientist. My leverage is software, automation and distribution. I can vibe-code most things and have shipped a number of Claude-powered products.

**The clipping tool is my first deliverable** — chosen because it's fast, visible, and replaces a real recurring cost.

---

## The organisation

Soil Food Web Foundation, a 501(c)(3) that launched around October 2025 to inherit the businesses of **Dr. Elaine Ingham**, the soil biologist who effectively defined the field. She died in February 2026 after a long decline with Lewy Body dementia.

Two entities were absorbed: **Soil Food Web School** (online courses, thousands of students across 130+ countries, over half in the US) and **Soil Food Web Inc** (research and consulting, currently mostly dormant).

State of things, per Evan:
- Revenue is course sales; philanthropy became ~25% of revenue this year
- Small management team, competence uneven, some legacy dysfunction being worked through
- The website is slow, plugin-heavy, and has broken links on pages they're actively selling from
- Google Drive filing is, his word, horrendous
- Thousands of hours of long-form video sit unused in the archive
- Explicit strategic goal: become less US-centric and less insular

**They currently pay a few hundred dollars per clipping session to an external person.** That's the cost I said I could remove.

---

## Why the archive matters strategically

Soil Food Web is co-hosting a workshop in **India in October** with the Isha Foundation / Sadhguru's Save Soil, and Evan is writing a research-collaboration proposal to **RySS / APCNF** — the Andhra Pradesh state programme that has moved 1.8 million farmers to natural farming and won the 2026 Food Planet Prize. APCNF cites Elaine as its primary scientific inspiration.

So: short-form content in more languages isn't a nice-to-have, it's directly aligned with the globalisation push and the India partnership. (Telugu is the language of Andhra Pradesh — but that's phase two. See below.)

---

## What I'm building

A clipping pipeline that turns long-form Soil Food Web lectures into short vertical clips.

**Where it lives:** GitHub repo, built in Claude Code. Media never committed — code, config, prompts and glossary only.

**Storage:** Scratch and intermediates go to my Minerva alumni Drive (large quota). Finished clips go somewhere the org can eventually own, so handover doesn't route through my account. Controlled by a single `OUTPUT_ROOT` config value.

**Auth for Drive:** service account with a shared folder, not OAuth on a personal login — so it transfers cleanly.

**Review step:** clips land in a `/pending/` folder rather than publishing directly. I can't verify translated output myself, and this org's reputation is fragile.

### Two possible engines

**A — OpusClip API** (what they already pay for)
- `Authorization: Bearer <API_KEY>`, some endpoints also take `x-opus-org-id`
- Key from the OpusClip dashboard, API/Integration section
- Base URL `api.opus.pro`, docs at developer.opus.pro/document/introduction, use v2
- API access requires Pro (Beta), Max or Business plan — the key must come from the org's billed account
- Limits: 30 req/min per key, 10-hour max video, 30 GB max file, **projects expire after 30 days** so outputs must be pulled down promptly
- Runs on credits; check balance before submitting

**B — Self-hosted**
- `yt-dlp` → `faster-whisper` (large-v3, word timestamps) → Claude for clip selection → `ffmpeg` for cutting
- Only key needed is `ANTHROPIC_API_KEY`
- Costs pennies per hour of video

**Design decision:** both live behind one `clip()` interface so I can swap or compare. The cost comparison *is* the demo.

### Implementation notes already agreed
- Cache the transcript to disk separately from clip selection — transcription is the slow step, selection is what I'll iterate on
- Clip selection returns **structured JSON**: `{start, end, hook, why, confidence}`. Ask for ~20 candidates, filter locally
- Selection prompt tuned to this content, not generic virality: self-contained segments 45–90s, no prior context needed, prioritise counterintuitive claims and moments where a specific mechanism gets explained
- Drive output structured as `/clips/{source-video}/{lang}/` with a manifest JSON — the org's filing chaos is a live complaint, so good structure is free credibility

---

## Phase two (not now)

Translated subtitles, starting with Telugu.

Notes for when I get there:
- Whisper's built-in translate only goes *to* English — use Claude on the transcript instead
- Maintain `glossary/{lang}.yaml` mapping fixed technical terms (soil food web, fungal-to-bacterial ratio, nematode, protozoa) to agreed renderings or transliterations. This file is versioned, correctable by a native speaker, and improves every future clip — arguably the real deliverable
- Cache translations keyed on segment hash so fixing one clip doesn't re-translate the rest
- I don't speak Telugu. Everything ships labelled as unreviewed machine output, and nothing goes public without a native speaker's check. RySS has hundreds of Telugu speakers — "ready for your team to review" is a better position than "done"
- Caveat: RySS leadership are English-fluent civil servants. Telugu serves farmers and master farmers, not the proposal audience. Frame the demo as *proof the pipeline works and here's what it costs per language*, not as a finished deliverable

---

## How I like to work

Direct, fast, forward momentum. Don't over-hedge or re-litigate a decision I've already made. Positive energy, honest input, no repeated caveats.

# Original, on-style, dimensional visuals for the SFW soil exhibit
## Research report, September 2026

Scope: how to get an AI pipeline to produce original visuals that carry a specific graphic-design sensibility (engraving plates, cut-paper collage, Swiss grid, soil strata) without pasting references or falling back to generic filler, and how to make flat source images dimensional. Written against the brief dated September 2026 and the ChatGPT experiment from the same week. Tool facts are current to early September 2026 and sourced at the end; parameter names are the real ones.

---

## 0. Read this first: two findings that change the brief

**Finding one: your hypothesis is confirmed, and the ChatGPT result is the proof.** v0 and Lovable generate code. When they need a picture they embed one or draw CSS shapes, and v0 says so itself when asked directly: it can write code that calls an image model, but it cannot produce an image in the chat. The ROOTED comp came out of ChatGPT because ChatGPT hands image requests to a natively multimodal image model that reads your reference in context and renders the whole page as pixels. That is a different tool class, and it is the class that does the illustration job. The pipeline is therefore: image model makes assets and comps, code tool lays them out. The rest of this report is about how to run the image half deliberately.

**Finding two, and this is the one that should change your approach most: the aesthetic in your appendix is now itself a documented AI default.** Anthropic's own frontend-design skill (the file Claude Code and Claude Design load before building UI) lists the clusters that generated design currently converges on so the model can avoid them. Cluster one is a warm cream background near #F4F1EA with a high-contrast serif display and a terracotta or warm-clay accent. Cluster five is template chrome: tracked-out ALL-CAPS eyebrow labels above headings, numbered 01/02/03 markers on content that is not a sequence, a monospace face for small data labels, and a "→" appended to links. Read your appendix against that list. Bone off-white, Didone display, uppercase letter-spaced mono captions, sections numbered like specimens, "EXPLORE THE PROGRAMS →". SFW's own brand palette even contains Organic Cream at exactly #F4F1EA. The ChatGPT comp landed in that cluster too: cream ground, serif headlines, mono captions, green accent.

This is not a reason to abandon the direction. It is a reason to relocate where the originality lives. The type system in your brief is the part a model produces on its own with no help, so it cannot be what makes the page look human-made. The parts that are not in any default cluster are the engraving line-work, the hand-cut collage edges, the hard-edged strata layout, and above all real archival and microscopy material. Those are where to spend the effort, and the method below is built around that.

---

## 1. Critique of the research questions, and the revised set

**What was wrongly framed.**

Q1 assumed the handoff was the unknown. It is not; it is settled (see Finding one). The real unknown is which image model to use for which asset type, because they differ sharply on flat editorial styles versus photographic ones.

Q2 asked "how do I set strength so it's inspired by rather than traced." That framing treats one dial as the answer. Style strength is one dial; the bigger lever is separating style references from content references, which every current tool now does explicitly (Midjourney sref vs oref, Recraft V4 Styles vs prompt, Nano Banana role-assigned references). Content leakage happens when you feed one image and ask for both.

Q3 was fine but too big. A glossary of two hundred terms does not help you prompt. What helps is a short bank organised by the five or six mechanics you actually use, with a note on which tools respond to which words.

Q4 conflated three different things: cutting a subject out (solved, cheap), making a flat image move with depth (solved, cheap, easy to overdo), and turning a flat illustration into a 3D object (partly solved, expensive to make look good, and the least useful of the three for a museum-flat aesthetic). They need separate answers.

Q5 was aimed at the wrong literature. Most "anti-slop" writing is about UI code defaults (Inter, purple gradients, three cards). The image-model side has its own convergence literature with measurable causes, and the escape techniques differ.

**What was missing.**

The question that most changes the approach: *which parts of my intended look are already AI defaults, and which are not?* Answered above. Second: *what do I do with SFW's real assets?* The org has microscopy footage and there are public-domain plate archives. A science nonprofit's most credible visuals are real; generation should be reserved for connective tissue. Third: *when should the image model produce a whole comp versus a single cut-out asset?* These are different prompts with different outputs.

**Revised question set.**

- R1. Tool map: which class of tool owns which task, and which image model for which asset type (flat line/vector, collage texture, full-page comp, photographic).
- R2. Reference mechanics: how each model separates style from content, with the real parameter names and safe starting values.
- R3. A short vocabulary bank organised by mechanic (line, colour, composition, medium, texture, and one new category: what to prohibit), with notes on which tools respond.
- R4. Cut-out, depth, and 3D as three separate problems, with a verdict on each.
- R5. Why image models converge, what the measurable causes are, and a pre-flight checklist that includes the "am I inside a default cluster" test.
- R6. The method: a repeatable pipeline for one exhibit section, real assets first, plus cost, licensing, and the credibility rules for a science nonprofit.

---

## R1. Tool map and the handoff

**Code tools (v0, Lovable, Bolt, Claude Code).** Layout, typography, motion, interaction, responsive behaviour, and assembling assets you give them. They cannot draw. v0 can write code that calls an image model through Vercel AI Gateway, which is useful if you ever want an app to generate images at runtime, but that is not the same as v0 producing your illustration. When these tools "use" your reference image they place it, because placing is the only operation they have.

**Multimodal image models (GPT Image, Nano Banana, FLUX.2, Recraft V4).** These read references and text in one context and generate pixels. They are what produced the ROOTED comp. They are the right class for full-page comps, for extending a design system to new content, and for single assets on transparent backgrounds. Current lineup:

- OpenAI GPT Image. `gpt-image-1.5` is the default in the API and supports `background: transparent`. `gpt-image-2` (April 2026) is the newer model behind the ChatGPT image tab but does not support transparent output; route cut-out asset jobs to 1.5. The edit endpoint takes up to 16 input images and a 32,000-character prompt, with `input_fidelity: high|low` controlling how closely it honours the inputs.
- Google Nano Banana Pro (`gemini-3-pro-image`) and Nano Banana 2 (Gemini 3.1 Flash Image). Up to 14 reference images per request, with documented fidelity for up to 6 object references and 5 characters. Outputs carry a SynthID watermark. Best current text rendering alongside GPT Image.
- Black Forest Labs FLUX.2 (Nov 2025; pro, max, flex, and open-weight dev). Up to 8 references via API, 10 in the playground. Supports hex colour codes in the prompt and structured JSON prompts. Carries C2PA provenance metadata.
- Recraft V4 and V4.1 (Feb and May 2026), plus the dedicated V4 Styles line (Aug 2026). The only mainstream model that outputs native, editable SVG. Built around graphic-design primitives rather than photographs. For your flat engraving, vector, and typographic work this is the first tool to reach for, not Midjourney.

**Diffusion-era image tools (Midjourney, Ideogram, Stable Diffusion with ControlNet and IP-Adapter).** Midjourney is now on V8.2 with `--sref` and `--sw` still the style controls; `--oref` (object/identity) only works on V7 and `--cref` only on V6. Midjourney remains the strongest for painterly and photographic mood and the weakest of this group for flat editorial layouts with legible type. Ideogram 3.0 has a Design mode and up to three style-reference images and is good for posters and type-led compositions. The open-source ComfyUI stack gives you the most control (ControlNet for structure, IP-Adapter for style, denoise strength for how much of the source survives) at the cost of manual tuning per job.

**Asset utilities.** Background removal: BiRefNet v2 (open source, best edge quality), Bria RMBG 2.0 (licensed training data, relevant if provenance matters to the org), remove.bg, Photoroom, Photoshop. Depth estimation: the Depth Anything family. Image-to-3D: Meshy 7, Tripo 3.1, Hunyuan 3D 3.0 Pro, Rodin Gen-2, Trellis 2.

**Where the handoff sits.** Image model produces (a) a full-page comp as a raster, used as the reference v0 rebuilds from, and (b) individual assets as transparent PNGs or SVGs. Utilities clean and cut. Code tool assembles. Nothing in the code tool should ever be asked to invent a picture.

---

## R2. Style-reference mechanics per model

The general principle, stated in the InstantStyle paper and observed in every tool: a reference image encodes style and content together, and the higher you push its influence the more content leaks in with the style. Two ways out. Lower the strength, which is what every "weight" parameter does. Or separate the channels, which is what the newer tools do by design. Prefer separation; tune strength second.

**Midjourney.**
`--sref <url or code>` carries look only (colour, medium, texture, lighting), never objects. `--sw` runs 0 to 1000, default 100; Midjourney notes that on V7 it moves more with style codes than with image references. Around 40 the reference is a hint; around 400 it starts to dominate palette and composition. `--oref <url> --ow` (V7 only) puts a specific object or character into a new scene; `--ow` defaults to 1000, and 25 to 100 gives minimal influence, 200 to 400 a balance. Image prompts (URLs at the front of the prompt) bias composition and content and are the thing to avoid when you want originality. Keep the text prompt sparse when using sref so style words do not fight the reference. Safe start for "inspired by": `--sref [plate] --sw 150 --style raw --v 8.2`, no image prompt, then adjust.

**Recraft V4 Styles.**
Upload 1 to 10 reference images to `/v1/styles` and receive a `style_id`, or attach `style_reference_urls` directly to the generation call and the server creates a private style and returns its id. `style_match` takes `precise` or `flexible`; precise holds rendering technique, colour, texture and composition, flexible holds the impression and lets the prompt lead. Sending both `style_id` and references in one request is rejected. Recraft also takes brand colours as RGB values in `controls.colors`, and V4 Vector outputs real SVG paths you can open in Illustrator. Safe start: three engraving plates as references, `style_match: flexible`, prompt the new subject only, and add your five hex colours as controls. This is the closest thing on the market to "absorb the sensibility, draw something new."

**Ideogram 3.0.**
Style Reference accepts up to 3 images and is saved as a reusable style. Style Codes (8 characters) reproduce a look found through generation. Use the Design mode for anything with type or a poster structure. No numeric weight; control comes from how many references and how specific the prompt is.

**GPT Image (gpt-image-1.5 / gpt-image-2).**
No style parameter. Control is entirely in the prompt and the input images on the edit endpoint. `input_fidelity: high` makes it honour the inputs closely, which is what you want for "keep this specimen but re-render it as engraving" and what you do not want for "make something new in this spirit." For the latter, use `low`, describe the mechanics rather than the image, and put the reference last in the input list. Use `background: transparent` with `output_format: png` for cut-out assets on 1.5. This is the model that extrapolated a design system across five sections in your ROOTED test.

**Nano Banana Pro.**
Up to 14 references, but the documented advice is to start with 2 to 4, put the ones that must survive in the first six slots, and assign each image one role in the prompt ("image 1 sets the line style, image 2 sets the palette, do not reproduce their subjects"). When references conflict the model averages them, which is exactly the generic-filler failure. One role per image is the fix.

**FLUX.2.**
Multi-reference by URL array, up to 8 via API. The style/content separation is prompt-driven, but FLUX.2's structured JSON prompting lets you put style, palette (hex codes) and subject in separate keys, which in practice behaves like separate channels. Best of the group for photographic realism that does not look synthetic; less relevant for flat plates.

**ComfyUI (Flux or SDXL with ControlNet and IP-Adapter).**
Three independent strengths. ControlNet strength (canny, depth, HED) controls structure; keep it around 0.7 or above when you want the composition held. IP-Adapter weight controls style; practitioners keep it low because high values degrade image quality and leak content. Denoise strength on img2img controls how much of the source pixel survives; 1.0 remakes everything, 0.2 to 0.3 keeps the composition, and the fal default is 0.85. The Flux IP-Adapter is widely reported to be weak for style transfer, so on Flux the reliable recipe is ControlNet for structure plus img2img for tone, with IP-Adapter as a light touch. This is the only stack where you can feed a public-domain Haeckel plate as a structure map and generate a new organism inside its composition, which is a legitimately interesting move for a specimen-grid section.

**Which tools are good at flat, editorial, engraving, vector and typographic looks.** Recraft first, Ideogram second, GPT Image and Nano Banana for comps with type, Midjourney last. Your instinct was right. Midjourney's default aesthetic is painterly and photographic; even with sref it tends to add atmosphere and gradients you then have to prohibit.

---

## R3. The vocabulary bank

Terms below are standard printmaking, typography and layout language (Müller-Brockmann's Grid Systems in Graphic Design, Lupton's Thinking with Type, Bringhurst's Elements of Typographic Style, and ordinary printmaking references). The value is not the words themselves but that image models respond to named, physical processes far better than to adjectives. "Engraving" moves a model; "archival" does not. Each entry has the visual effect it produces and, where it matters, which tools respond.

**Line and mark.**
- engraving, copperplate engraving: parallel and cross-hatched lines that swell and taper; tonal modelling by line density alone. All models respond; Recraft and GPT Image best.
- etching: looser, scratchier line than engraving; slight ink bleed.
- stipple engraving: tone built from dots; softer than hatching.
- woodcut, linocut: bold cut marks, solid blacks, white carved lines; chunky rather than fine.
- wood engraving: fine white line out of black, the Thomas Bewick look; closest to your "white filaments on black" reference.
- hairline, single-weight contour, no fills: pure outline, the specimen-diagram look.
- hatching, cross-hatching, contour hatching: the vocabulary for how shading is made; say which one.
- scratchboard: white line scraped out of black ground; a modern route to the same effect as wood engraving.

**Colour.**
- limited palette, two-colour, three-colour: caps the count; models otherwise add hues.
- flat fills, no gradients, no shading: removes tonal modelling.
- spot colour: one colour used as an accent on an otherwise mono image.
- duotone: image built from two inks; give the two hexes.
- risograph, screenprint misregistration: slightly offset colour layers, grain, flat ink; strong "printed" signal.
- ink on paper, ink density: keeps darks matte rather than glossy.
- chromatic restraint: works on GPT Image and Nano Banana; less on diffusion models, which want a process word.

**Composition.**
- specimen plate, catalogue plate, taxonomic plate: many subjects in a grid with figure numbers; the Haeckel structure.
- asymmetric grid, off-centre subject, generous margin, ragged right: Swiss composition language.
- figure-ground reversal: subject and background swap roles; use for the black-ground sections.
- negative space as an active element: tells the model not to fill the frame.
- hierarchy by scale, one dominant element: stops the model from making everything equal.
- horizontal bands, hard edges, stratified: your strata device.
- exploded view, cutaway, cross-section: technical-illustration structure that reads as scientific.

**Medium.**
- letterpress, debossed impression: type pressed into paper, slight ink squash.
- screen print on uncoated stock: flat, matte, slightly rough edge.
- cut-paper collage, hand-cut edge, torn edge, layered paper: physical layers with visible edges; say "visible shadow under each paper layer" if you want depth, or "no shadow" if you want flat.
- botanical illustration, natural-history illustration, scientific illustration: precise, labelled, neutral; steers away from fantasy.
- field guide plate, handbook illustration: smaller, tidier, less ornate than a Haeckel plate.
- microscopy, brightfield, darkfield, phase contrast: real imaging vocabulary; use only when you mean real microscopy, see credibility.

**Texture and surface.**
- matte, uncoated paper, paper grain, laid paper, foxing: the aged-book surface.
- halftone, halftone dot screen: photograph converted to dots; a strong period signal.
- ink bleed, plate tone, slight misregistration: the imperfections that read as printed rather than rendered.
- photocopy grain, xerox: harsher than risograph.

**Type (only if the image model is rendering type at all).**
- name the classification, not the font: high-contrast transitional serif, Didone, grotesque, monospaced typewriter, slab. Models respond to classification words.
- tracked-out small caps, ranged left, hanging figures: sets the detail.
- Recraft, Ideogram, GPT Image and Nano Banana render type reliably; Midjourney does not, so keep type out of Midjourney prompts and add it in code.

**Prohibitions (a category your brief already uses, and it works).**
Diffusion models respond to negatives inconsistently, so phrase prohibitions as positives where possible ("flat cream ground" rather than "no gradient"). Multimodal models (GPT Image, Nano Banana) follow explicit "do not" lists well. Your standing list: no gradients, no glow, no lens flare, no bokeh, no particles, no glassmorphism, no soft drop shadows, no photographic shading, no emoji. Add for image work: no watermark, no text (when you want to set type yourself), no frame or border, no vignette.

---

## R4. Cut-out, depth, and 3D as three problems

**(a) Cutting a subject out of a flat image. Solved.**
For photographs and modern illustrations, BiRefNet v2 is the current open-source edge-quality leader; run it locally through `rembg -m birefnet-general` or hosted on fal with `operating_resolution` at 2048 and the Matting variant when an edge matters. Bria RMBG 2.0 is the choice if the org cares that the model was trained on licensed data. remove.bg and Photoshop are fine for one-offs. For engraving plates two things change. The subject is often the same colour as its own line-work background, so segmentation models built for photos can fail; the reliable route is a luminance threshold in Photoshop or with Pillow (which you already use), keeping only the ink and making the paper transparent. And for scans of old plates, the cut should follow the ink, not an imagined silhouette; a plate cut out as pure ink on transparency is a far more flexible asset than a rectangle of paper. For generated assets skip the problem entirely: ask gpt-image-1.5 or Recraft for the asset on a transparent background in the first place.

**(b) Making a flat image dimensional on the web. Solved, and the useful one for you.**
Two routes. Layered cut-outs: separate the subject from the ground, place them on different planes, move them at different rates on scroll or pointer. This is how the ROOTED comp reads as dimensional even though it is flat: the hands, the soil block and the sapling are cut out and sit over the contour lines. Vanikya's layer-splitter and similar tools now split an image into depth planes and inpaint the holes behind each layer, so you get complete planes rather than cut-outs with gaps. Depth-map displacement: run Depth Anything V2 (or V3, or Photoshop's Depth Blur neural filter) to get a greyscale depth map, then displace pixels per-depth in a WebGL shader or a pixi.js DisplacementFilter. The Sygnal knowledge-base article on 2.5D parallax is the best single practical reference and its rule is worth keeping: the depth map is everything, and blurry object edges in the map produce the "melting hologram" look. For a museum-flat aesthetic, layered cut-outs with hard edges and small displacement are correct; per-pixel depth on a photograph tends toward the exact glossy motion the brief prohibits. Keep the movement to a few pixels and tie it to scroll, not to a hover loop.

**(c) Turning a flat illustration into a 3D object. Partly solved, and mostly not what you want.**
Single-image-to-3D is real: Meshy 7, Tripo 3.1, Hunyuan 3D 3.0 Pro, Rodin Gen-2 and open-source Trellis 2 all take one image and return a textured mesh in a minute or two. Independent comparisons agree on the limits: the model has to invent everything the image does not show, textures need significant cleanup before production, and fine hollow detail gets filled in. Feeding these an engraving works poorly because the models expect a photographed or shaded object and an engraving has no tonal cues. Where it does work: a cut-out of a real object (a mushroom, a clod of soil, a microscope) generates a passable turnable model, and Nano Banana Pro or GPT Image can render a flat drawing as a "paper model" or "papercraft object with visible layers" as a 2D image, which is dimensional in the sense you described without any mesh at all. That second move is the one to try first, because it produces exactly the cut-out-turned-object look and costs one generation.

Verdict: (a) and (b) are your tools. (c) is a demo, not a method, unless you specifically want a rotating object.

---

## R5. Why image models converge, and the pre-flight checklist

**The causes are measurable.** Hany Farid's explanation is that most models filter both training data and outputs through an aesthetic scorer, which is why the output shares a certain ethereal, polished quality. A 2025 study of default images in Midjourney v6 found that semantically unrelated prompts still produce the same default images with minor variation. The LatentAesthetic work profiled 26 text-to-image models and found each has a stable, distinctive aesthetic signature that a classifier can identify from a single image, and that most model families have converged toward each other over time, with Ideogram pulling away from Midjourney as one of the exceptions. On top of the model side there is a human side: people prompt with the same cultural references (the Kapwing prompt analysis is the usual citation) and internalise what they see, so brands converge on each other. On the code side, the frontend-design literature makes the same point differently: the model samples the statistical centre of its training data unless it is handed decisions, and no adjective in the prompt fixes that, only decisions do.

**What the escape techniques actually are.**
- Give the model a decision, not a mood. Name a process (wood engraving), a palette (five hexes), a composition (specimen grid, twelve figures, numbered), a surface (uncoated paper). "Archival" and "editorial" are moods; the model will answer with its default version of them.
- Separate style references from content references and assign each a role.
- Use real material as the anchor. Public-domain plates, SFW's microscopy, photographs of actual soil. Generation fills gaps around real things; it should not be the thing.
- Prohibit the model's favourite moves, phrased as positives for diffusion models.
- Pick one direction and hold it in a DESIGN.md that the code tool reads on every prompt. This is now the de facto standard, and Anthropic's frontend-design skill is the canonical reference for the code half.
- Then run the test the skill itself runs: work through the same brief as if it were any similar project and see whether you would arrive at the same place. If yes, that part is a default, not a choice.

**Pre-flight checklist, to run before every generation batch.**
1. Which cluster am I in? Check against: cream ground with high-contrast serif and warm accent; near-black with acid green or vermilion; broadsheet hairlines and zero radius; SaaS cards; ALL-CAPS eyebrows, 01/02/03 numbering, mono data labels, arrows on links. If the mechanic I am about to generate lives entirely inside one of these, it will not read as designed no matter how good the prompt is.
2. What is the one memorable element on this page, and is it made of something real or something generated?
3. Have I named a physical process, a palette in hex, a composition structure and a surface? If any of the four is an adjective, replace it.
4. Are style and content in separate inputs with one role each?
5. Is type being rendered by the image model when it should be set in code?
6. Is the prohibition list attached, phrased for the model in use?
7. Would a designer looking at the output see a decision I made, or a default the model made? Name the decision. If I cannot, regenerate with a different one.

---

## R6. The method

**Repeatable pipeline for one exhibit section (example: 01 The Living Layer, mycelium).**

1. Gather real material first. Pull two or three plates from the Biodiversity Heritage Library (150,000+ high-resolution public-domain illustrations, including fungi and microscopy plates) and one frame of SFW's own microscopy. Note the source of each.
2. Cut the plates as ink. Threshold in Photoshop or Pillow so the ink is opaque and the paper is transparent. Save as PNG. Cut the microscopy frame with BiRefNet if a specimen needs isolating.
3. Create the style once. Recraft V4 Styles: upload three plates to `/v1/styles`, keep the `style_id`. This is your engraving voice for the whole project.
4. Generate the missing pieces, never the specimens. Prompt Recraft with `style_id`, `style_match: flexible`, and a subject the archive does not have (for example a mycelial network as a wood engraving, white line on black, a single fruiting body at the top edge, generous empty space, no text, no frame). Use V4 Vector when you want SVG. Add the five palette colours as controls.
5. For a section comp, hand the cut-out assets plus one plate as a style reference to gpt-image-1.5 or Nano Banana Pro, with one role per image ("image 1 is the specimen, place it as a cut-out; image 2 sets the line style only; do not reproduce its subject") and a description of the composition in structural terms (bands, off-centre, margins). Ask for the comp at the aspect ratio of the section. Iterate by describing the change, not by resending the whole brief.
6. Depth pass, only where it earns its place. Split the comp's hero into two or three layers (subject, mid, ground) and export as transparent PNGs. Keep the specimen sharp-edged.
7. Hand to v0. Put the comp in as the visual reference, the cut-out assets in the project, a DESIGN.md with palette, type roles, layout rules and motion budget (one page-load reveal, scroll-linked parallax on the hero layers, nothing else), and ask for a faithful rebuild. Start a fresh chat per section so you are not re-sending context.
8. Run the checklist before showing Evan.

**Cost.** Recraft V4 Styles is about $0.035 per 1K image on fal plus $0.005 to create a style; V4 Vector and Pro cost more. FLUX.2 pro charges by megapixel (about $0.03 for the first output megapixel). Nano Banana Pro runs roughly $0.14 to $0.24 per image through hosted APIs. GPT Image is billed by token and edit requests with references cost more than generations. Midjourney is subscription only. BiRefNet, rembg and Depth Anything are free to run. Meshy and Tripo are credit-based with limited free tiers; Trellis 2 and Hunyuan3D are free if self-hosted on a GPU. For a mockup phase you are talking tens of dollars, not hundreds; the expensive input is your time tuning references, which is why steps 3 and 4 fix the style once.

**Licensing.** BHL and Internet Archive plates flagged public domain are free to use, cut, and remix; Haeckel's Kunstformen der Natur (1899 to 1904) is public domain and available as high-resolution scans through BHL, Internet Archive and rawpixel. Recraft's free plan makes images public, owned by Recraft, and not licensed for commercial use; paid plans include ownership and commercial rights. Midjourney requires a paid plan for commercial use. Nano Banana output carries an invisible SynthID watermark and FLUX.2 output carries C2PA provenance metadata; both are fine for a nonprofit site and both mean the provenance is checkable, which is a feature here. Whatever is generated, keep a manifest of source references and prompts, the same way the clipping pipeline keeps a manifest, so the org can answer "where did this image come from" later.

**Credibility for a science nonprofit.** Three findings set the rule. Springer Nature, Elsevier and Taylor & Francis ban AI-generated images in publications except where AI is the method and the process is reproducible; that is the standard SFW's scientific partners live under. A 2025 study in Science Communication (Eom, Middleton, Luo, Li and Brossard) tested AI-generated science posts with and without disclaimers and found audience familiarity with the technology shaped credibility judgements; and a 2026 study in Communications Sustainability found that support for climate action dropped when highly realistic imagery was suspected to be AI-generated. Nan Li's 2026 piece argues the wider point: the visual cues scientists rely on for credibility are losing their grip because anyone can fake them.

So the rule for SFW: never present a generated image as a real organism, real soil, or real microscopy. Real specimens come from SFW's own microscopes and from public-domain plates, credited as such. Generation is used for what is obviously illustration: the connective mycelium drawing, the strata diagram, the collage texture, the paper object. Label illustrations as illustrations in the caption ("Illustration" or "Engraving after Haeckel, 1904"), and label microscopy with the method and magnification the way a lab would. This is also a design asset: a caption that says "brightfield, 400x, SFW lab, 2026" is more on-style than any generated specimen, and it is the one thing no default cluster contains.

---

## Sources

Midjourney Style Reference documentation (docs.midjourney.com); Prompt Architects, Midjourney sref explained (2026); imigo.ai, Omni Reference in V7 (Feb 2026); QWE Academy, style reference guide (Apr 2026).
Recraft V4 docs and V4 Styles API reference (recraft.ai/docs); Recraft V4.1 release post (May 2026); fal.ai Recraft V4 Styles endpoint and pricing; Replicate Recraft V4 blog (Feb 2026); The Rundown, Recraft V4/V4.1 licensing summary (Aug 2026).
Ideogram 3.0 model page and Style Reference docs (docs.ideogram.ai).
OpenAI Images API reference, generate and edit endpoints (developers.openai.com); fal.ai GPT Image 1.5 prompt guide (Dec 2025); WaveSpeed GPT Image 2 API guide (May 2026).
Google DeepMind Nano Banana Pro page; Google Cloud, Ultimate prompting guide for Nano Banana (Mar 2026); ai.google.dev image generation docs; aifreeapi, Nano Banana Pro reference images (Mar 2026).
Black Forest Labs, FLUX.2 announcement (Nov 2025); FLUX.2 pro pricing via bfl.ai.
InstantStyle: Free Lunch towards Style-Preserving in Text-to-Image Generation (arXiv 2404.02733); Civitai, Flux IP-Adapter review with ControlNet and img2img (2026); fal.ai FLUX general image-to-image parameters.
v0 chat on image generation (v0.dev); Vercel AI Gateway image generation docs (2026).
fal.ai, 10 best image background removers (Jul 2026); Dupple, best AI background removers (Jun 2026); aifreeforever, rembg and BiRefNet notes (Jul 2026).
Sygnal KB, Image 2.5D parallax effects; Vanikya image layer splitter; RunDiffusion, AI 3D model generators compared (Jul 2026); Scenario, comparing generative 3D models (Apr 2026); ideate.xyz, Trellis vs Tripo vs Meshy vs Rodin vs Hunyuan (2025); Meshy comparison pages (2026).
Anthropic frontend-design skill (anthropics/skills, 2026); Vibe Code Kit, AI slop design (Jun 2026); Guayoyo Tech, design skills for AI agents (May 2026); AIDesigner, Claude Code frontend design (May 2026).
An Exploration of Default Images in Text-to-Image Generation (arXiv 2505.09166); LatentAesthetic, Characterizing the Aesthetic Defaults of Generative Image Models (louvresae.github.io); UC Berkeley I School, Hany Farid on why AI art looks the way it does (Aug 2024); Kompozy, the AI design aesthetic (Jun 2026).
Biodiversity Heritage Library via Colossal, Hyperallergic and Smithsonian Magazine; Internet Archive, Kunstformen der Natur; rawpixel public-domain Haeckel plates.
Thesify, AI policies in academic publishing (Oct 2025); Kennesaw State Office of Research, AI disclosure requirements (Jul 2025); Eom et al., Familiarity Matters, Science Communication (2025, doi 10.1177/10755470251380116); Communications Sustainability, realistic AI-generated climate disaster images (May 2026); Nan Li via Social Science Space (Jul 2026).
Müller-Brockmann, Grid Systems in Graphic Design; Lupton, Thinking with Type; Bringhurst, The Elements of Typographic Style.

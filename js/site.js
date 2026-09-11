/* Soil Food Web Foundation — site.js
   Vanilla JS, no dependencies. Three jobs:
   1. Overlay menu: open, close, focus trap, Escape, body scroll lock.
   2. Accordion inside the overlay: one section open at a time.
   3. Root line: one hairline path drawn by scroll position (reversible).
   Everything degrades: without JS the header links still work, the overlay
   markup is hidden, and reduced-motion users get static states. */

(function () {
  "use strict";

  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- 1. Overlay ---------- */
  var overlay = document.getElementById("overlay");
  var openBtn = document.querySelector("[data-menu-open]");
  var closeBtn = overlay && overlay.querySelector("[data-menu-close]");
  var lastFocus = null;

  function focusables(root) {
    return Array.prototype.slice.call(
      root.querySelectorAll('a[href], button:not([disabled]), input:not([disabled]), [tabindex]:not([tabindex="-1"])')
    ).filter(function (el) { return el.offsetParent !== null; });
  }

  function openMenu() {
    if (!overlay) return;
    lastFocus = document.activeElement;
    overlay.setAttribute("data-open", "true");
    overlay.removeAttribute("aria-hidden");
    openBtn.setAttribute("aria-expanded", "true");
    document.body.classList.add("is-locked");
    window.setTimeout(function () { closeBtn.focus(); }, reduceMotion ? 0 : 60);
  }

  function closeMenu() {
    if (!overlay) return;
    overlay.setAttribute("data-open", "false");
    overlay.setAttribute("aria-hidden", "true");
    openBtn.setAttribute("aria-expanded", "false");
    document.body.classList.remove("is-locked");
    if (lastFocus) lastFocus.focus();
  }

  if (overlay && openBtn && closeBtn) {
    overlay.setAttribute("aria-hidden", "true");
    openBtn.addEventListener("click", openMenu);
    closeBtn.addEventListener("click", closeMenu);

    // Close on any link click inside the overlay.
    overlay.addEventListener("click", function (e) {
      var a = e.target.closest("a[href]");
      if (a) closeMenu();
    });

    document.addEventListener("keydown", function (e) {
      if (overlay.getAttribute("data-open") !== "true") return;
      if (e.key === "Escape") { e.preventDefault(); closeMenu(); return; }
      if (e.key === "Tab") {
        var items = focusables(overlay);
        if (!items.length) return;
        var first = items[0], last = items[items.length - 1];
        if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
        else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
      }
    });
  }

  /* ---------- 2. Accordion ---------- */
  var accordions = document.querySelectorAll("[data-accordion]");
  Array.prototype.forEach.call(accordions, function (acc) {
    var items = acc.querySelectorAll("[data-acc-item]");
    Array.prototype.forEach.call(items, function (item) {
      var btn = item.querySelector("[data-acc-btn]");
      var panel = item.querySelector("[data-acc-panel]");
      if (!btn || !panel) return;
      btn.setAttribute("aria-expanded", item.getAttribute("data-open") === "true" ? "true" : "false");
      btn.addEventListener("click", function () {
        var isOpen = item.getAttribute("data-open") === "true";
        Array.prototype.forEach.call(items, function (other) {
          other.setAttribute("data-open", "false");
          var ob = other.querySelector("[data-acc-btn]");
          if (ob) ob.setAttribute("aria-expanded", "false");
        });
        if (!isOpen) { item.setAttribute("data-open", "true"); btn.setAttribute("aria-expanded", "true"); }
      });
    });
  });

  /* ---------- 3. Root line drawn by scroll ---------- */
  // Markup: <svg class="root-line" data-root-line><path pathLength="1" d="..."/></svg>
  // inside a position:relative container. The path draws from 0 to 1 as the
  // container scrolls through the viewport, and un-draws on the way back up.
  var lines = document.querySelectorAll("[data-root-line]");
  if (lines.length && !reduceMotion) {
    var ticking = false;
    function update() {
      var vh = window.innerHeight;
      Array.prototype.forEach.call(lines, function (svg) {
        var box = svg.parentElement.getBoundingClientRect();
        var total = box.height + vh * 0.5;
        var passed = vh * 0.85 - box.top;
        var t = Math.max(0, Math.min(1, passed / total));
        svg.style.setProperty("--draw", t.toFixed(3));
      });
      ticking = false;
    }
    window.addEventListener("scroll", function () {
      if (!ticking) { window.requestAnimationFrame(update); ticking = true; }
    }, { passive: true });
    window.addEventListener("resize", update);
    update();
  }

  /* ---------- 4. Filter chips (index pages) ---------- */
  // <ul class="chips" data-filter-for="#list"> with <button class="chip" data-filter="all|kind">
  // Items in the list carry data-kind. "all" shows everything. No pagination anywhere.
  // More than one group may point at the same list: an item shows only when
  // every group agrees. A group tests data-kind unless data-filter-attr names
  // another attribute, so Publications filters by collection and by decade.
  // Children carrying none of those attributes (the column header row) are
  // chrome: never hidden, never counted.
  var byList = [];
  Array.prototype.forEach.call(document.querySelectorAll("[data-filter-for]"), function (group) {
    var sel = group.getAttribute("data-filter-for");
    var found = null;
    byList.forEach(function (b) { if (b.sel === sel) found = b; });
    if (!found) {
      var list = document.querySelector(sel);
      if (!list) return;
      found = { sel: sel, list: list, groups: [] };
      byList.push(found);
    }
    found.groups.push(group);
  });

  byList.forEach(function (b) {
    var attrs = b.groups.map(function (g) { return g.getAttribute("data-filter-attr") || "data-kind"; });
    var items = Array.prototype.filter.call(b.list.children, function (item) {
      for (var i = 0; i < attrs.length; i++) { if (item.hasAttribute(attrs[i])) return true; }
      return false;
    });

    function apply() {
      var shown = 0;
      items.forEach(function (item) {
        var show = true;
        b.groups.forEach(function (group, i) {
          if (!show) return;
          var on = group.querySelector('[data-filter][aria-pressed="true"]');
          var key = on ? on.getAttribute("data-filter") : "all";
          if (key !== "all" && item.getAttribute(attrs[i]) !== key) show = false;
        });
        item.hidden = !show;
        if (show) shown++;
      });
      b.groups.forEach(function (group) {
        var status = group.querySelector("[data-filter-status]");
        if (status) status.textContent = shown + " shown";
      });
    }

    b.groups.forEach(function (group) {
      var chips = group.querySelectorAll("[data-filter]");
      Array.prototype.forEach.call(chips, function (chip) {
        chip.addEventListener("click", function () {
          Array.prototype.forEach.call(chips, function (c) {
            c.setAttribute("aria-pressed", c === chip ? "true" : "false");
          });
          apply();
        });
      });
    });

    apply();
  });
})();

/* ---------- 5. Pathway diagram (Learn) ---------- */
// <div data-pathway> with <button data-pathway-btn aria-controls="id"> and a
// panel by that id. One panel open at a time; hover opens too, tap toggles.
(function () {
  var roots = document.querySelectorAll("[data-pathway]");
  Array.prototype.forEach.call(roots, function (root) {
    var btns = root.querySelectorAll("[data-pathway-btn]");
    function closeAll() {
      Array.prototype.forEach.call(btns, function (b) {
        b.setAttribute("aria-expanded", "false");
        var p = document.getElementById(b.getAttribute("aria-controls"));
        if (p) p.hidden = true;
      });
    }
    Array.prototype.forEach.call(btns, function (b) {
      var panel = document.getElementById(b.getAttribute("aria-controls"));
      if (!panel) return;
      function open() { closeAll(); b.setAttribute("aria-expanded", "true"); panel.hidden = false; }
      b.addEventListener("click", function () {
        var isOpen = b.getAttribute("aria-expanded") === "true";
        closeAll();
        if (!isOpen) { b.setAttribute("aria-expanded", "true"); panel.hidden = false; }
      });
      b.addEventListener("mouseenter", open);
      b.addEventListener("focus", open);
    });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape") closeAll(); });
  });
})();

/* ---------- 6. Calendar today marker ---------- */
// The site is static, so "today" cannot be baked into the HTML or it goes stale.
// <div data-cal data-cal-start="YYYY-MM-DD" data-cal-end="YYYY-MM-DD"> with a
// [data-cal-today] span inside .cal__grid. Hidden when today is out of range.
(function () {
  var cals = document.querySelectorAll("[data-cal]");
  Array.prototype.forEach.call(cals, function (cal) {
    var marker = cal.querySelector("[data-cal-today]");
    if (!marker) return;
    var start = new Date(cal.getAttribute("data-cal-start") + "T00:00:00");
    var end = new Date(cal.getAttribute("data-cal-end") + "T00:00:00");
    var now = new Date(); now.setHours(0, 0, 0, 0);
    if (isNaN(start) || isNaN(end) || now < start || now > end) return;
    var span = (end - start) + 86400000;
    marker.style.left = ((now - start) / span * 100).toFixed(3) + "%";
    marker.hidden = false;
    var sr = document.createElement("span");
    sr.className = "visually-hidden";
    sr.textContent = "Today, " + now.toDateString() + ".";
    marker.appendChild(sr);
  });
})();

/* ---------- 7. Production notes ---------- */
// .todo blocks are hidden from visitors by CSS. ?notes=1 on any URL sets
// data-notes on <html>, which reveals every placeholder and prints the
// instruction held on each empty image slot's data-empty attribute.
(function () {
  try {
    var p = new URLSearchParams(window.location.search).get("notes");
    if (p === "1" || p === "true") document.documentElement.setAttribute("data-notes", "");
  } catch (e) { /* no URLSearchParams: notes stay hidden, which is the safe default */ }
})();

/* ---------- 8. Microscopy loops ---------- */
// Every <video data-loop> on the site is the Foundation's own brightfield
// footage. Three rules, in this order:
//   1. Nothing downloads until it is near the viewport. The markup carries
//      data-src rather than src, so a page with a clip below the fold costs
//      nothing until the reader goes there.
//   2. A clip plays only while it is on screen. Off screen it pauses, so a
//      long page never has more than one or two decoding at once.
//   3. Reduced motion means reduced motion. The clip loads and shows its
//      first frame, and never runs.
(function () {
  var vids = document.querySelectorAll("video[data-loop]");
  if (!vids.length) return;
  var still = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  function load(v) {
    if (v.dataset.loaded) return;
    v.dataset.loaded = "1";
    (v.dataset.src || "").split(",").forEach(function (src) {
      src = src.trim();
      if (!src) return;
      var s = document.createElement("source");
      s.src = src;
      s.type = src.slice(-5) === ".webm" ? "video/webm" : "video/mp4";
      v.appendChild(s);
    });
    // data-start seeds the playhead, so several clips of the same reel on one
    // page are several moments rather than several copies of one.
    if (v.dataset.start) {
      v.addEventListener("loadedmetadata", function () {
        try { v.currentTime = parseFloat(v.dataset.start) || 0; } catch (e) { /* not seekable */ }
      }, { once: true });
    }
    v.load();
  }

  if (!("IntersectionObserver" in window)) {
    // No observer: load everything and let the browser decide. Correctness
    // over thrift on browsers this old.
    Array.prototype.forEach.call(vids, function (v) { load(v); if (!still) v.play().catch(function () {}); });
    return;
  }

  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (en) {
      var v = en.target;
      if (!en.isIntersecting) { v.pause(); return; }
      load(v);
      if (!still && !v.hasAttribute("data-scrub")) v.play().catch(function () {});
    });
  }, { rootMargin: "200px 0px" });

  Array.prototype.forEach.call(vids, function (v) { io.observe(v); });
})();

/* ---------- 9. The rack ---------- */
// <div class="rack"> holding a <video data-loop data-scrub>. Scroll position
// through the block drives the playhead and the focus together: sharp as the
// block passes the middle of the window, soft at either end. The organism
// moves when the reader moves. Study 14 from /motion.
//
// Reduced motion turns it into an ordinary still frame, because the whole
// point of it is motion tied to scrolling.
(function () {
  var racks = document.querySelectorAll(".rack video[data-scrub]");
  if (!racks.length) return;
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

  var ticking = false;
  function update() {
    ticking = false;
    Array.prototype.forEach.call(racks, function (v) {
      var box = v.closest(".rack");
      var r = box.getBoundingClientRect();
      if (r.bottom < -200 || r.top > window.innerHeight + 200) return;
      var p = (window.innerHeight - r.top) / (window.innerHeight + r.height);
      p = p < 0 ? 0 : p > 1 ? 1 : p;
      var d = v.duration;
      if (d && isFinite(d)) { try { v.currentTime = p * d * 0.999; } catch (e) { /* not seekable yet */ } }
      // sharp across the middle half of the pass, soft only at the extremes
      var focus = Math.max(0, (Math.abs(p - 0.5) * 2 - 0.45) / 0.55);
      v.style.filter = "brightness(.8) contrast(6.5) saturate(.42) blur(" + (focus * focus * 3.2).toFixed(2) + "px)";
      var m = box.querySelector(".rack__meter i");
      if (m) m.style.width = (p * 100).toFixed(1) + "%";
    });
  }
  function onScroll() { if (!ticking) { ticking = true; requestAnimationFrame(update); } }
  window.addEventListener("scroll", onScroll, { passive: true });
  window.addEventListener("resize", onScroll);
  Array.prototype.forEach.call(racks, function (v) {
    v.addEventListener("loadedmetadata", update, { once: true });
  });
  update();
})();

/* ---------- 10. The reveal ---------- */
// Photographs and plates rise a little and fade as they arrive, once.
//
// The stylesheet hides nothing. This hides only what is ALREADY BELOW THE
// FOLD, so a page with no JavaScript shows everything, and so does a
// screenshot, a thumbnail and a print. Anything on screen at load is left
// exactly as it is, which is why there is no flash.
//
// Reduced motion skips the whole thing rather than shortening it.
(function () {
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  if (!("IntersectionObserver" in window)) return;

  var SEL = ".shot, .slides > li, .ledger > li, .doors > li, .cards > .card," +
            " .step, .banner, .filmstrip, .scope, .plate";
  var els = document.querySelectorAll(SEL);
  if (!els.length) return;

  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (en) {
      if (!en.isIntersecting) return;
      en.target.classList.add("rise-in");
      en.target.classList.remove("rise");
      io.unobserve(en.target);            // once, then never again
    });
  }, { rootMargin: "0px 0px -8% 0px" });

  Array.prototype.forEach.call(els, function (el) {
    // only pre-hide what the reader cannot see yet
    if (el.getBoundingClientRect().top > window.innerHeight) {
      el.classList.add("rise");
      io.observe(el);
    }
  });
})();

/* ---------- 11. The theatre ---------- */
// One player that stays on the page.
//
// The old playlist reloaded the whole of WordPress for every video and then
// booted a new Vimeo player from zero, which is why it felt slow and why
// autoplay into the next video was impossible. Here the player is created
// once, on the first click, and every video after that is a loadVideo() call
// on the player that is already running. The URL changes with pushState, so
// links and the back button still work, and nothing reloads.
//
// Nothing third-party loads until someone presses play. Until then the stage
// is a poster and a button, so the page costs nothing to arrive at. This is
// the facade pattern, and it is the single biggest speed difference between
// this and either a Vimeo or a YouTube embed dropped straight into a page:
// the platform's script is the weight, not the platform.
//
// The private hash travels in the data, never in the URL. Unlisted videos
// need it to play, and every way the old page had of losing it, dropping it
// from a link, pasting it inside the id, arriving with no query string at
// all, is a way of breaking the player. content/videos.json holds it and
// tools/playlist.py checks it against Vimeo before it is committed.
//
// If the platform script does not load, the stage becomes a plain link to
// the video. The content stays reachable.
(function () {
  "use strict";

  var root = document.querySelector("[data-theatre]");
  if (!root) return;
  var holder = root.querySelector("[data-theatre-data]");
  var list = [];
  try { list = JSON.parse(holder.textContent); } catch (err) { return; }
  if (!list.length) return;

  var frame  = root.querySelector("[data-frame]");
  var poster = root.querySelector("[data-poster]");
  var nowT   = root.querySelector("[data-now-title]");
  var nowS   = root.querySelector("[data-now-sub]");
  var live   = root.querySelector("[data-live]");
  var next   = root.querySelector("[data-next]");
  var nextT  = root.querySelector("[data-next-title]");
  var nextN  = root.querySelector("[data-next-count]");
  var check  = root.querySelector("[data-check]");
  var buttons = Array.prototype.slice.call(root.querySelectorAll("[data-i]"));

  var COUNTDOWN = 8;        // seconds before the next video starts
  var STREAK_LIMIT = 3;     // videos in a row unattended before we ask
  var player = null, loading = null, timer = null, i = 0, streak = 0;

  function slugIndex(slug) {
    for (var n = 0; n < list.length; n++) { if (list[n].slug === slug) return n; }
    return -1;
  }

  /* -- the platform script, fetched once and only on demand -- */
  function api() {
    if (window.Vimeo && window.Vimeo.Player) return Promise.resolve();
    if (loading) return loading;
    loading = new Promise(function (resolve, reject) {
      var s = document.createElement("script");
      s.src = "https://player.vimeo.com/api/player.js";
      s.async = true;
      s.onload = resolve;
      s.onerror = function () { loading = null; reject(new Error("player.js")); };
      document.head.appendChild(s);
    });
    return loading;
  }

  // If Vimeo's control script will not load, the video still plays here, in
  // an ordinary iframe that needs no script at all. What is lost is the
  // autoplay chain and the still-watching check, not the video. Nothing ever
  // sends the visitor off to vimeo.com.
  function fallback() {
    var v = list[i];
    player = null;
    root.setAttribute("data-fallback", "true");
    frame.hidden = false;
    frame.innerHTML = "";
    var f = document.createElement("iframe");
    f.src = "https://player.vimeo.com/video/" + encodeURIComponent(v.id) +
            "?h=" + encodeURIComponent(v.hash) +
            "&autoplay=1&dnt=1&title=0&byline=0&portrait=0";
    f.title = v.title;
    f.allow = "autoplay; fullscreen; picture-in-picture";
    f.setAttribute("allowfullscreen", "");
    f.setAttribute("frameborder", "0");
    frame.appendChild(f);
    if (poster) poster.hidden = true;
    if (live) live.textContent = "Now playing: " + v.title;
  }

  function boot() {
    var v = list[i];
    return api().then(function () {
      frame.hidden = false;
      player = new window.Vimeo.Player(frame, {
        id: Number(v.id),
        h: v.hash,              // the private hash, from the data file
        autoplay: true,         // allowed: we are inside the click that asked
        dnt: true,              // no Vimeo tracking cookies
        title: false, byline: false, portrait: false,
        responsive: true
      });
      // The poster's job is over the moment the player exists. Waiting for
      // the play event would leave the poster sitting on top of a video that
      // has already started when autoplay is allowed, and on top of Vimeo's
      // own play button when it is not.
      if (poster) poster.hidden = true;
      player.on("ended", ended);
      // A pause or a scrub is a person, so the unattended count starts over.
      player.on("pause", awake);
      player.on("seeked", awake);
    })["catch"](fallback);
  }

  /* -- selecting, with or without playing -- */
  function select(n, opts) {
    opts = opts || {};
    i = ((n % list.length) + list.length) % list.length;
    var v = list[i];

    buttons.forEach(function (b, n2) {
      var on = n2 === i;
      b.setAttribute("aria-current", on ? "true" : "false");
      b.parentNode.setAttribute("data-active", on ? "true" : "false");
    });
    if (nowT) nowT.textContent = v.title;
    if (nowS) nowS.textContent = v.subtitle || "";
    if (poster) {
      var im = poster.querySelector("img");
      if (im && v.thumb) im.src = v.thumb;
    }
    if (!opts.silent) {
      history.pushState({ v: v.slug }, "", "?v=" + encodeURIComponent(v.slug));
    }

    if (!opts.play) return;
    if (live) live.textContent = "Now playing: " + v.title;
    if (player) {
      player.loadVideo({ id: Number(v.id), h: v.hash })
        .then(function () { return player.play(); })["catch"](fallback);
      if (poster) poster.hidden = true;
    } else {
      boot();
    }
  }

  /* -- what happens when one finishes -- */
  function ended() {
    if (i + 1 >= list.length) { stop(); if (poster) poster.hidden = false; return; }
    streak += 1;
    if (streak >= STREAK_LIMIT) { ask(); return; }
    countdown();
  }

  function countdown() {
    var left = COUNTDOWN;
    nextT.textContent = list[i + 1].title;
    nextN.textContent = left;
    next.hidden = false;
    var go = next.querySelector("[data-next-go]");
    if (go) go.focus();
    clearInterval(timer);
    timer = setInterval(function () {
      left -= 1;
      nextN.textContent = left;
      if (left <= 0) { stop(); select(i + 1, { play: true }); }
    }, 1000);
  }

  // Three in a row with nobody touching anything: stop and ask, the way a
  // streaming service does, rather than playing to an empty room.
  function ask() {
    stop();
    check.hidden = false;
    var go = check.querySelector("[data-check-go]");
    if (go) go.focus();
  }

  function stop() {
    clearInterval(timer);
    timer = null;
    if (next) next.hidden = true;
    if (check) check.hidden = true;
  }

  function awake() { streak = 0; }

  /* -- wiring -- */
  buttons.forEach(function (b, n) {
    b.addEventListener("click", function () { awake(); stop(); select(n, { play: true }); });
  });
  if (poster) poster.addEventListener("click", function () { awake(); select(i, { play: true }); });

  root.addEventListener("click", function (ev) {
    var t = ev.target.closest ? ev.target.closest("[data-next-go],[data-next-cancel],[data-check-go]") : null;
    if (!t) return;
    if (t.hasAttribute("data-next-cancel")) { stop(); return; }
    awake();
    stop();
    select(i + 1, { play: true });
  });

  document.addEventListener("keydown", function (ev) {
    if (ev.key === "Escape" && timer) stop();
  });
  document.addEventListener("pointerdown", awake, { passive: true });

  window.addEventListener("popstate", function () {
    var want = slugIndex(new URLSearchParams(location.search).get("v") || "");
    if (want < 0 || want === i) return;
    stop();
    select(want, { silent: true, play: !!player });
  });

  // Arriving with ?v=slug selects that video and shows its poster. It does
  // not start playing: browsers block autoplay with sound before a click,
  // and a muted autostart is worse than a poster.
  var start = slugIndex(new URLSearchParams(location.search).get("v") || "");
  select(start < 0 ? 0 : start, { silent: true });
})();

/* ---------- 12. Films from the field ----------
   Every case-study still is a facade. Nothing is fetched from Vimeo until a
   visitor presses play; then the button is swapped for the player, in place,
   and focus moves into it so a keyboard user lands where the video is. The
   privacy hash rides on the button, because these videos are unlisted and
   the player refuses them without it. */
(function () {
  var strip = document.querySelectorAll("[data-film]");
  if (!strip.length) return;
  Array.prototype.forEach.call(strip, function (btn) {
    btn.addEventListener("click", function () {
      var frame = document.createElement("iframe");
      frame.src = btn.getAttribute("data-film") + "&autoplay=1";
      frame.title = btn.getAttribute("aria-label") || "Video";
      frame.allow = "autoplay; fullscreen; picture-in-picture";
      frame.setAttribute("allowfullscreen", "");
      btn.parentNode.replaceChild(frame, btn);
      frame.focus();
    });
  });
})();

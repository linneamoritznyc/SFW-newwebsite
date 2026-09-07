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
  var chipGroups = document.querySelectorAll("[data-filter-for]");
  Array.prototype.forEach.call(chipGroups, function (group) {
    var list = document.querySelector(group.getAttribute("data-filter-for"));
    if (!list) return;
    var chips = group.querySelectorAll("[data-filter]");
    var status = group.querySelector("[data-filter-status]");
    Array.prototype.forEach.call(chips, function (chip) {
      chip.addEventListener("click", function () {
        var key = chip.getAttribute("data-filter");
        Array.prototype.forEach.call(chips, function (c) { c.setAttribute("aria-pressed", c === chip ? "true" : "false"); });
        var shown = 0;
        Array.prototype.forEach.call(list.children, function (item) {
          var show = key === "all" || item.getAttribute("data-kind") === key;
          item.hidden = !show;
          if (show) shown++;
        });
        if (status) status.textContent = shown + " shown";
      });
    });
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

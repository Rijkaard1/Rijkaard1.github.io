const toggle = document.querySelector(".menu-toggle");
const sidebar = document.querySelector(".sidebar");

if (toggle && sidebar) {
  toggle.addEventListener("click", () => sidebar.classList.toggle("open"));
  document.addEventListener("click", (e) => {
    if (!sidebar.contains(e.target) && !toggle.contains(e.target)) {
      sidebar.classList.remove("open");
    }
  });
}

/* ---------- Page transition: fade + slide up ---------- */
const OUT_MS = 200;
const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
const main = document.querySelector("main");

// Back/forward cache: make sure the page is visible when returning to it.
window.addEventListener("pageshow", (e) => {
  if (e.persisted && main) main.classList.remove("leaving");
});

document.addEventListener("click", (e) => {
  const a = e.target.closest("a");
  if (!a || !main || reduceMotion) return;
  if (e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
  if (a.target === "_blank" || a.hasAttribute("download")) return;
  const url = new URL(a.href, location.href);
  if (url.origin !== location.origin || url.pathname === location.pathname) return;

  e.preventDefault();
  main.classList.add("leaving");
  setTimeout(() => (location.href = a.href), OUT_MS);
});

/* ---------- Screenshot lightbox ---------- */
const lightbox = document.querySelector(".lightbox");
if (lightbox && typeof lightbox.showModal === "function") {
  const big = lightbox.querySelector("img");
  document.querySelectorAll(".shot").forEach((btn) => {
    btn.addEventListener("click", () => {
      const img = btn.querySelector("img");
      big.src = img.src;
      big.alt = img.alt;
      lightbox.showModal();
    });
  });
  lightbox.querySelector(".lightbox-close").addEventListener("click", () => lightbox.close());
  lightbox.addEventListener("click", (e) => { if (e.target === lightbox) lightbox.close(); });
}

/* ---------- Project version badge (reads version.json, so one file controls the label) ---------- */
document.querySelectorAll("[data-version-src]").forEach(async (box) => {
  try {
    const res = await fetch(box.dataset.versionSrc, { cache: "no-cache" });
    if (!res.ok) return;
    const v = await res.json();
    const num = box.querySelector(".v-num");
    const date = box.querySelector(".v-date");
    if (num && v.version) num.textContent = "v" + v.version;
    if (date && v.updated) date.textContent = v.updated;
  } catch (_) { /* keep the fallback text already in the page */ }
});

/* ---------- Email button: the address is put together here so it is not written plainly in the page ---------- */
const emailBtn = document.getElementById("email-btn");
if (emailBtn) {
  const addr = emailBtn.dataset.u + "@" + emailBtn.dataset.d;
  emailBtn.href = "mailto:" + addr;
  emailBtn.textContent = addr;
}

/* ---------- Course search and filters (Real Analysis page) ---------- */
(function () {
  const grid = document.getElementById("course-grid");
  const search = document.getElementById("course-search");
  if (!grid || !search) return;
  const cards = [...grid.querySelectorAll(".course-card")];
  const chips = [...document.querySelectorAll(".chip")];
  const onlySol = document.getElementById("only-solutions");
  const count = document.getElementById("course-count");
  const empty = document.getElementById("no-results");
  const reset = document.getElementById("reset-filters");
  const text = cards.map((c) => c.textContent.toLowerCase().replace(/\s+/g, " "));
  let band = "all";

  function apply() {
    const words = search.value.toLowerCase().trim().split(/\s+/).filter(Boolean);
    let shown = 0;
    cards.forEach((c, i) => {
      const ok =
        (band === "all" || c.dataset.band === band) &&
        (!onlySol.checked || c.dataset.solutions === "yes") &&
        words.every((w) => text[i].includes(w));
      c.hidden = !ok;
      if (ok) shown++;
    });
    count.textContent = "Showing " + shown + " of " + cards.length + " courses";
    empty.hidden = shown !== 0;
  }
  chips.forEach((chip) =>
    chip.addEventListener("click", () => {
      band = chip.dataset.band;
      chips.forEach((c) => {
        const on = c === chip;
        c.classList.toggle("active", on);
        c.setAttribute("aria-pressed", on ? "true" : "false");
      });
      apply();
    })
  );
  search.addEventListener("input", apply);
  search.addEventListener("keydown", (e) => { if (e.key === "Escape") { search.value = ""; apply(); } });
  onlySol.addEventListener("change", apply);
  reset.addEventListener("click", () => {
    search.value = "";
    onlySol.checked = false;
    chips[0].click();
  });
  apply();
})();

/* ---------- Dark / light theme switch ---------- */
(function () {
  const btn = document.getElementById("theme-toggle");
  if (!btn) return;
  const root = document.documentElement;
  const meta = document.querySelector('meta[name="theme-color"]');
  function paint() {
    const light = root.getAttribute("data-theme") === "light";
    btn.querySelector(".ti").innerHTML = light ? "&#9790;" : "&#9728;";
    btn.querySelector(".tl").textContent = light ? "Dark theme" : "Light theme";
    btn.setAttribute("aria-label", light ? "Switch to dark theme" : "Switch to light theme");
    if (meta) meta.setAttribute("content", light ? "#f3f6fc" : "#05070d");
  }
  btn.addEventListener("click", () => {
    const next = root.getAttribute("data-theme") === "light" ? "dark" : "light";
    root.setAttribute("data-theme", next);
    try { localStorage.setItem("theme", next); } catch (e) { /* not saved */ }
    paint();
  });
  paint();
})();

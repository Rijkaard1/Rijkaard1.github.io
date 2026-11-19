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

/* ---------- Neon wipe page transition (~0.25s) ---------- */
const WIPE_MS = 250;
const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
const wipe = document.createElement("div");
wipe.className = "wipe";
document.body.appendChild(wipe);

function wipeOut() {
  // New page: the bar starts covering the screen, then slides away to the right.
  wipe.className = "wipe wipe-out";
  setTimeout(() => (wipe.className = "wipe"), WIPE_MS);
}

try {
  if (!reduceMotion && sessionStorage.getItem("wipe") === "1") wipeOut();
  sessionStorage.removeItem("wipe");
} catch (e) { /* storage unavailable: skip the entry wipe */ }

// Back/forward cache: make sure the bar is hidden when returning to a page.
window.addEventListener("pageshow", (e) => {
  if (e.persisted) wipe.className = "wipe";
});

document.addEventListener("click", (e) => {
  const a = e.target.closest("a");
  if (!a || reduceMotion) return;
  if (e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
  if (a.target === "_blank" || a.hasAttribute("download")) return;
  const url = new URL(a.href, location.href);
  if (url.origin !== location.origin || url.pathname === location.pathname) return;

  e.preventDefault();
  try { sessionStorage.setItem("wipe", "1"); } catch (err) { /* ignore */ }
  wipe.className = "wipe wipe-in";
  setTimeout(() => (location.href = a.href), WIPE_MS);
});

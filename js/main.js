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

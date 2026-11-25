/* Rijkaard the footballer bot: walks along the bottom of the screen, dribbling a ball, and talks. */
(function () {
  const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const page = location.pathname.split("/").pop() || "index.html";

  /* ---------- Dialogue: edit these lines freely. href = where a click leads. ---------- */
  const LINES = [
    { text: "Hello, I am Rijkaard. Welcome to my website!", href: "about.html" },
    { text: "Anything you want to know further about me? Click me!", href: "about.html" },
    { text: "Want to see what I've built? Click me to check my projects.", href: "projects.html" },
    { text: "Curious about my skills? Programming, cybersecurity and AI. Click me!", href: "skills.html" },
    { text: "I love maths too. Click me for my mathematics notes.", href: "mathematics.html" },
    { text: "Want to get in touch? Click me and say hi!", href: "contact.html" },
  ].filter((l) => l.href !== page);

  /* ---------- Styles ---------- */
  const css = `
  .rk-bot{position:fixed;left:0;bottom:6px;z-index:40;pointer-events:none;width:0;height:0}
  .rk-body{position:absolute;left:0;bottom:0;width:84px;height:140px;padding:0;border:0;background:none;cursor:pointer;pointer-events:auto;transform-origin:50% 100%;-webkit-tap-highlight-color:transparent}
  .rk-body svg{width:100%;height:100%;overflow:visible;display:block}
  .rk-body:focus-visible{outline:2px solid #93c5fd;outline-offset:4px;border-radius:8px}
  .rk-flip{transform:scaleX(-1)}
  .rk-bubble{position:absolute;bottom:150px;left:0;width:max-content;max-width:230px;padding:10px 14px;border-radius:14px;
    background:#e6ecf8;color:#05070d;font:500 .85rem/1.4 Inter,system-ui,sans-serif;box-shadow:0 0 14px rgba(59,130,246,.35);
    border:1px solid #3b82f6;opacity:0;transform:translateY(6px) scale(.96);transition:opacity .25s,transform .25s;
    pointer-events:none;cursor:pointer}
  .rk-bubble.show{opacity:1;transform:none;pointer-events:auto}
  .rk-bubble::after{content:"";position:absolute;bottom:-7px;left:var(--tail,30px);width:12px;height:12px;background:#e6ecf8;
    border-right:1px solid #3b82f6;border-bottom:1px solid #3b82f6;transform:rotate(45deg)}
  .rk-leg{transform-box:view-box}
  .rk-bot.walking .rk-legA{animation:rk-legA .7s ease-in-out infinite;transform-origin:60px 168px}
  .rk-bot.walking .rk-legB{animation:rk-legB .7s ease-in-out infinite;transform-origin:82px 168px}
  .rk-bot.walking .rk-armA{animation:rk-legB .7s ease-in-out infinite;transform-origin:54px 104px}
  .rk-bot.walking .rk-armB{animation:rk-legA .7s ease-in-out infinite;transform-origin:88px 104px}
  .rk-bot.walking .rk-bob{animation:rk-bob .35s ease-in-out infinite}
  .rk-bot.walking .rk-ball{animation:rk-ball .7s ease-in-out infinite}
  .rk-bot.walking .rk-ballspin{animation:rk-spin .7s linear infinite;transform-origin:126px 210px}
  @keyframes rk-legA{0%,100%{transform:rotate(-24deg)}50%{transform:rotate(24deg)}}
  @keyframes rk-legB{0%,100%{transform:rotate(24deg)}50%{transform:rotate(-24deg)}}
  @keyframes rk-bob{0%,100%{transform:translateY(0)}50%{transform:translateY(-3px)}}
  @keyframes rk-ball{0%,100%{transform:translateX(-4px)}50%{transform:translateX(10px)}}
  @keyframes rk-spin{to{transform:rotate(360deg)}}
  @media (max-width:820px){.rk-body{width:66px;height:110px}.rk-bubble{bottom:120px;max-width:190px;font-size:.8rem}}
  `;
  const style = document.createElement("style");
  style.textContent = css;
  document.head.appendChild(style);

  /* ---------- Markup (design B: big-head mascot) ---------- */
  const SVG = `
  <svg viewBox="20 8 130 250" aria-hidden="true">
    <ellipse cx="78" cy="224" rx="52" ry="5" fill="#000" opacity="0.28"/>
    <g class="rk-bob">
      <g class="rk-leg rk-legA"><path d="M60 168 L52 206" stroke="#5A3825" stroke-width="11" stroke-linecap="round" fill="none"/><path d="M54 192 L52 206" stroke="#fff" stroke-width="12" stroke-linecap="round" fill="none"/><ellipse cx="50" cy="212" rx="11" ry="5" fill="#D62828"/></g>
      <g class="rk-leg rk-legB"><path d="M82 168 L100 202" stroke="#5A3825" stroke-width="11" stroke-linecap="round" fill="none"/><path d="M96 190 L100 202" stroke="#fff" stroke-width="12" stroke-linecap="round" fill="none"/><ellipse cx="106" cy="207" rx="11" ry="5" fill="#D62828"/></g>
      <g class="rk-leg rk-armA"><path d="M54 104 L40 128" stroke="#5A3825" stroke-width="9" stroke-linecap="round" fill="none"/></g>
      <path d="M42 62 L34 98 M50 58 L42 104 M98 62 L106 98 M90 58 L98 104" stroke="#1B120C" stroke-width="9" stroke-linecap="round" fill="none"/>
      <circle cx="70" cy="66" r="32" fill="#5A3825"/>
      <path d="M38 60 Q40 28 70 28 Q100 28 102 60 Q70 46 38 60Z" fill="#1B120C"/>
      <circle cx="70" cy="22" r="13" fill="#1B120C"/><path d="M62 16 L78 28 M62 28 L78 16" stroke="#3A2A1E" stroke-width="2"/>
      <circle cx="58" cy="70" r="5.5" fill="#fff"/><circle cx="82" cy="70" r="5.5" fill="#fff"/><circle cx="59.5" cy="70" r="2.8" fill="#1B120C"/><circle cx="83.5" cy="70" r="2.8" fill="#1B120C"/>
      <path d="M58 82 Q70 94 82 82Z" fill="#fff" stroke="#2A1608" stroke-width="1.5" stroke-linejoin="round"/>
      <path d="M54 98 L86 98 L90 142 L50 142Z" fill="#D62828"/>
      <path d="M54 98 L44 112 L52 116 L56 108Z M86 98 L96 112 L88 116 L84 108Z" fill="#fff" stroke="#9A9A9A" stroke-width="0.6"/>
      <path d="M50 142 L90 142 L94 168 L46 168Z" fill="#fff" stroke="#9A9A9A" stroke-width="0.8"/>
      <path d="M50 142 L55 142 L51 168 L46 168Z" fill="#D62828"/>
      <g class="rk-leg rk-armB"><path d="M88 104 L102 120" stroke="#5A3825" stroke-width="9" stroke-linecap="round" fill="none"/></g>
    </g>
    <g class="rk-ball"><g class="rk-ballspin"><circle cx="126" cy="210" r="14" fill="#fff" stroke="#2C2C2A" stroke-width="1.2"/><path d="M126 203 L132 208 L130 215 L122 215 L120 208Z" fill="#2C2C2A"/></g></g>
  </svg>`;

  const root = document.createElement("div");
  root.className = "rk-bot";
  root.innerHTML = `<div class="rk-bubble" role="status" aria-live="polite"></div>
    <button class="rk-body" type="button" aria-label="Rijkaard the football bot. Click to learn more about me.">${SVG}</button>`;
  document.body.appendChild(root);
  const bubble = root.querySelector(".rk-bubble");
  const body = root.querySelector(".rk-body");

  /* ---------- Walking ---------- */
  const SPEED = 55; // px per second
  let x = 0, dir = 1, last = 0, paused = false, talking = false, current = LINES[0];
  const bounds = () => {
    const left = window.innerWidth > 820 ? 270 + 10 : 6;
    return { min: left, max: Math.max(left + 20, window.innerWidth - 90) };
  };
  function place() {
    root.style.transform = `translateX(${x}px)`;
    body.classList.toggle("rk-flip", dir < 0);
    // keep the bubble on screen: its tail points at the bot's head
    const w = bubble.offsetWidth || 200;
    const bw = body.offsetWidth;
    const want = bw / 2 - w / 2;
    const minL = -x + 6, maxL = window.innerWidth - x - w - 6;
    const l = Math.min(Math.max(want, minL), maxL);
    bubble.style.left = l + "px";
    bubble.style.setProperty("--tail", Math.min(Math.max(bw / 2 - l - 6, 14), w - 26) + "px");
  }
  function setWalking(on) { root.classList.toggle("walking", on && !reduce); }
  function tick(t) {
    if (!last) last = t;
    const dt = Math.min((t - last) / 1000, 0.05);
    last = t;
    if (!paused && !reduce) {
      const b = bounds();
      x += dir * SPEED * dt;
      if (x >= b.max) { x = b.max; dir = -1; }
      if (x <= b.min) { x = b.min; dir = 1; }
      place();
    }
    requestAnimationFrame(tick);
  }
  const b0 = bounds();
  x = reduce ? window.innerWidth - 100 : b0.min;
  place();
  setWalking(true);
  requestAnimationFrame(tick);
  window.addEventListener("resize", () => {
    const b = bounds();
    x = Math.min(Math.max(x, b.min), b.max);
    place();
  });

  // Stop for a moment when the user hovers or focuses, so he is easy to click.
  const hold = (on) => { paused = on; setWalking(!on); };
  body.addEventListener("pointerenter", () => hold(true));
  body.addEventListener("pointerleave", () => hold(false));
  body.addEventListener("focus", () => hold(true));
  body.addEventListener("blur", () => hold(false));

  /* ---------- Talking ---------- */
  let idx = 0, timer;
  function say(line) {
    current = line;
    bubble.textContent = line.text;
    bubble.classList.add("show");
    place();
    talking = true;
    clearTimeout(timer);
    timer = setTimeout(hush, 6500);
  }
  function hush() {
    bubble.classList.remove("show");
    talking = false;
    clearTimeout(timer);
    timer = setTimeout(next, 4500);
  }
  function next() {
    if (!LINES.length) return;
    say(LINES[idx % LINES.length]);
    idx++;
  }
  setTimeout(next, 1200);

  /* ---------- Click: go where the current line points ---------- */
  function go() {
    const href = (talking ? current : LINES[0]).href;
    window.location.href = href;
  }
  body.addEventListener("click", go);
  bubble.addEventListener("click", go);
})();

// Renders the ecosystem graph with a mermaid theme that follows the
// colour scheme, and re-renders it when the scheme changes.
(function () {
  var el = document.getElementById("ecosystem-graph");
  if (!el || !window.mermaid) return;
  var source = el.textContent;
  var dark = window.matchMedia("(prefers-color-scheme: dark)");

  function render() {
    var isDark = dark.matches;
    mermaid.initialize({
      startOnLoad: false,
      securityLevel: "loose",   // needed for the `click ... href` links
      theme: "base",
      themeVariables: isDark ? {
        darkMode: true,
        background: "#282f2f",
        primaryColor: "#282f2f",
        primaryBorderColor: "#4b5657",
        primaryTextColor: "#e6e9ea",
        lineColor: "#7f8c8d",
        fontFamily: "Lato, Helvetica Neue, Arial, sans-serif"
      } : {
        background: "#f5f7fa",
        primaryColor: "#f5f7fa",
        primaryBorderColor: "#b8c3cf",
        primaryTextColor: "#222222",
        lineColor: "#8a96a3",
        fontFamily: "Lato, Helvetica Neue, Arial, sans-serif"
      },
      flowchart: { curve: "basis", nodeSpacing: 28, rankSpacing: 48, padding: 10 }
    });
    el.removeAttribute("data-processed");
    el.textContent = source;
    return mermaid.run({ nodes: [el] });
  }

  render();
  if (dark.addEventListener) dark.addEventListener("change", render);
})();

// Copies a publication's BibTeX entry and briefly shows a check mark.
document.addEventListener("click", function (ev) {
  var btn = ev.target.closest(".copy-btn");
  if (!btn || !navigator.clipboard) return;
  var pre = btn.parentNode.querySelector("pre");
  navigator.clipboard.writeText(pre.textContent).then(function () {
    btn.dataset.state = "copied";
    btn.setAttribute("aria-label", "BibTeX copied");
    clearTimeout(btn._reset);
    btn._reset = setTimeout(function () {
      delete btn.dataset.state;
      btn.setAttribute("aria-label", "Copy BibTeX");
    }, 1600);
  });
});

// Draws the title banner's curtain wall (facade coordinates; style.css warps
// it): tall glazing bands between thin spandrels, mullions at an uneven
// wide/narrow rhythm, each joint a dark groove with a light bevel. Then fits
// the banner's 1701x925 design stage to the banner's width.
(function () {
  var svg = document.getElementById("facade-grid");
  if (!svg) return;
  var W = 4400, H = 5200, out = [];
  var seed = 7;
  function rnd() { seed = (seed * 16807) % 2147483647; return seed / 2147483647; }
  function line(x1, y1, x2, y2, stroke, width) {
    out.push('<line x1="' + x1 + '" y1="' + y1 + '" x2="' + x2 + '" y2="' + y2 +
             '" stroke="' + stroke + '" stroke-width="' + width + '"/>');
  }
  function groove(x1, y1, x2, y2) {
    line(x1 + 2.8, y1 + 2.8, x2 + 2.8, y2 + 2.8, "#4b86ab", 2.6);
    line(x1, y1, x2, y2, "#1d4869", 4.6);
  }
  var cols = [], x = 0;
  while (x < W) { cols.push(x); x += (cols.length % 2 ? 50 : 62) + rnd() * 4; }
  for (var y = 0; y < H; ) {
    var tall = 118 + rnd() * 8, thin = 22;
    cols.forEach(function (cx, i) {   // the odd slightly lighter panel
      if (rnd() < 0.05) out.push('<rect x="' + cx + '" y="' + y + '" width="' + ((cols[i + 1] || W) - cx) +
                                 '" height="' + tall + '" fill="#38709a"/>');
    });
    cols.forEach(function (cx) { groove(cx, y, cx, y + tall); });
    groove(0, y + tall, W, y + tall);
    cols.forEach(function (cx, i) { if (i % 2) groove(cx + 18, y + tall, cx + 18, y + tall + thin); });
    groove(0, y + tall + thin, W, y + tall + thin);
    y += tall + thin;
  }
  svg.innerHTML = out.join("");

  var banner = svg.closest(".facade-banner");
  function fit() { banner.style.setProperty("--k", banner.clientWidth / 1701); }
  if (window.ResizeObserver) new ResizeObserver(fit).observe(banner);
  fit();
})();

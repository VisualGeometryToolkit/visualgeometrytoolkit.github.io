// The stack's landing-page script, shared by every toolkit's site: the ecosystem graph, the BibTeX copy buttons and
// the helpers a title banner's own script uses (window.stackSite). A site loads mermaid, this file, then its own
// main.js, which holds only what is its own (its banner's drawing). Another toolkit's site takes this file from this
// repository at a pinned commit and never keeps a copy.

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

// Helpers for a site's own banner script.
window.stackSite = {
  // A seeded generator of numbers in (0, 1) (the Lehmer generator of multiplier 16807): a drawing with random
  // variation is the same on every load.
  random: function (seed) {
    return function () { seed = (seed * 16807) % 2147483647; return seed / 2147483647; };
  },
  // Fits a banner's design stage, `width` px wide, to the banner: sets --k, the scale its stylesheet applies, now and
  // whenever the banner is resized.
  fitStage: function (banner, width) {
    function fit() { banner.style.setProperty("--k", banner.clientWidth / width); }
    if (window.ResizeObserver) new ResizeObserver(fit).observe(banner);
    fit();
  }
};

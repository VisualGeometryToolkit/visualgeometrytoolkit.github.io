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

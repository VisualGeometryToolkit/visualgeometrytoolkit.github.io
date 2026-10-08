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
      flowchart: { curve: "basis", nodeSpacing: 36, rankSpacing: 56 }
    });
    el.removeAttribute("data-processed");
    el.textContent = source;
    return mermaid.run({ nodes: [el] });
  }

  render();
  if (dark.addEventListener) dark.addEventListener("change", render);
})();

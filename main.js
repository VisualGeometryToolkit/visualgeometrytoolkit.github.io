// Draws the title banner's curtain wall (facade coordinates; style.css warps
// it): tall glazing bands between thin spandrels, mullions at an uneven
// wide/narrow rhythm, each joint a dark groove with a light bevel. Then fits
// the banner's 1701x925 design stage to the banner's width. The graph, the BibTeX buttons and the helpers used here
// (stackSite) are the stack's shared script, shared/site.js, loaded first.
(function () {
  var svg = document.getElementById("facade-grid");
  if (!svg) return;
  var W = 4400, H = 5200, out = [];
  var rnd = stackSite.random(7);
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

  stackSite.fitStage(svg.closest(".facade-banner"), 1701);
})();

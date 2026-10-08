# visualgeometrytoolkit.github.io

The landing page of the [Visual Geometry Toolkit](https://visualgeometrytoolkit.github.io):
Julia packages for multi-view geometry from Marine Data Science, Kiel University.

Plain static HTML, CSS and JavaScript with no build step; GitHub Pages serves
`main` as is. The ecosystem graph is rendered in the browser by a pinned
[mermaid](https://mermaid.js.org) release, and the package icons in `icons/`
are self-contained SVGs that switch between light and dark colours with
`prefers-color-scheme`.

To preview locally: `python -m http.server` in this directory, then open
<http://localhost:8000>.

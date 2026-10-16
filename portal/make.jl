# VisualGeometryToolkit documentation portal (visualgeometrytoolkit.github.io).
#
# Aggregates the per-package Documenter sites into one site with a shared
# navigation bar and cross-package search (MultiDocumenter). The six workspace
# packages are read from ONE shallow clone of the monorepo's gh-pages branch
# (gh-pages/<Package>/…); the three separate repositories are cloned by
# MultiDocumenter from their own gh-pages.
#
#   julia --project=portal portal/make.jl                     # clone gh-pages, build portal/out/
#   PORTAL_LOCAL=<dir> julia --project=portal portal/make.jl  # <dir>/<Package>/ holds local builds
#   PORTAL_NO_EXTERNAL=1 …                                    # skip the three external repositories
#   PORTAL_OUT=<dir> …                                        # output directory (default portal/out)
#
# CI (.github/workflows/portal.yml) then copies the hand-written landing page
# (index.html, style.css, main.js, icons/) over the output's root redirect.
#
# Portal paths are the package names without ".jl", so they never collide with
# GitHub project pages (<org>.github.io/<Repo>.jl/).

using MultiDocumenter

const MONOREPO = "https://github.com/VisualGeometryToolkit/VisualGeometryToolkit.jl.git"
const WORKSPACE = ["VisualGeometryCore", "VisualGeometryIo", "VisualGeometryFeatures",
    "RobustVisualGeometry", "VisualGeometryEval", "PoseLib"]
# The separate projects have their own project pages (<project>.github.io)
# and their docs live THERE only: the portal links to them instead of hosting
# a second copy that can go stale. Their old portal URLs (/<Project>/...) are
# redirect pages to the same path on the project site, so shared links keep
# working. The workspace packages have no page of their own: the portal is
# their home (their docs' canonical URLs point here).
const EXTERNAL = ["RansacScoringDoneRight", "LocalOptimizationDoneRight", "BlobBoards"]
site_repo(p) = (o = lowercase(p); "https://github.com/$o/$o.github.io.git")
site_url(p) = "https://$(lowercase(p)).github.io/"

pages = get(ENV, "PORTAL_LOCAL", "")
if isempty(pages)
    pages = mktempdir()
    run(`git clone --depth 1 --branch gh-pages $MONOREPO $pages`)
end

docs = MultiDocumenter.DropdownComponent[]
for p in WORKSPACE
    isdir(joinpath(pages, p)) || (@warn "no docs for $p under $pages"; continue)
    push!(docs, MultiDocumenter.MultiDocRef(; upstream = joinpath(pages, p), path = p, name = p))
end
foreach(p -> push!(docs, MultiDocumenter.Link(p, site_url(p))), EXTERNAL)

outpath = get(ENV, "PORTAL_OUT", joinpath(@__DIR__, "out"))

# /<Project>/<path> → <project site>/<path>, one redirect page per HTML page the
# project site has (read from its repository), so old portal links land on the
# same page of the project site.
function write_redirects(outpath, p)
    src = mktempdir()
    success(pipeline(`git clone -q --depth 1 --branch main $(site_repo(p)) $src`; stderr = devnull)) ||
        (@warn "no site for $p: no redirects"; return)
    n = 0
    for (dir, _, files) in walkdir(src), f in files
        (endswith(f, ".html") && !occursin("/.git", dir)) || continue
        rel = relpath(joinpath(dir, f), src)
        target = site_url(p) * replace(rel, r"(^|/)index\.html$" => s"\1")
        out = joinpath(outpath, p, rel)
        mkpath(dirname(out))
        write(out, """<!DOCTYPE html><html><head><meta charset="utf-8"><title>Moved: $p</title>
            <link rel="canonical" href="$target"><meta http-equiv="refresh" content="0; url=$target">
            </head><body><p>The $p documentation is at <a href="$target">$target</a>.</p></body></html>
            """)
        n += 1
    end
    @info "$p: $n redirect pages to $(site_url(p))"
end
MultiDocumenter.make(
    outpath, docs;
    search_engine = MultiDocumenter.SearchConfig(index_versions = ["stable", "dev"], engine = MultiDocumenter.FlexSearch),
    rootpath = "/",
    canonical_domain = "https://visualgeometrytoolkit.github.io/",
    sitemap = true,
)

get(ENV, "PORTAL_NO_EXTERNAL", "") == "1" || foreach(p -> write_redirects(outpath, p), EXTERNAL)

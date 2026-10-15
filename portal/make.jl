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
const EXTERNAL = ["RansacScoringDoneRight", "LocalOptimizationDoneRight", "BlobBoards"]

pages = get(ENV, "PORTAL_LOCAL", "")
if isempty(pages)
    pages = mktempdir()
    run(`git clone --depth 1 --branch gh-pages $MONOREPO $pages`)
end

docs = MultiDocumenter.MultiDocRef[]
for p in WORKSPACE
    isdir(joinpath(pages, p)) || (@warn "no docs for $p under $pages"; continue)
    push!(docs, MultiDocumenter.MultiDocRef(; upstream = joinpath(pages, p), path = p, name = p))
end
clonedir = mktempdir()
# A separate repository joins once it is public and has a gh-pages branch.
has_pages(url) = success(pipeline(`git ls-remote --exit-code --heads $url gh-pages`; stdout = devnull, stderr = devnull))
if get(ENV, "PORTAL_NO_EXTERNAL", "") != "1"
    for p in EXTERNAL
        has_pages("https://github.com/VisualGeometryToolkit/$p.jl.git") ||
            (@warn "no gh-pages for $p yet"; continue)
        push!(docs, MultiDocumenter.MultiDocRef(;
            upstream = joinpath(clonedir, p), path = p, name = p,
            giturl = "https://github.com/VisualGeometryToolkit/$p.jl.git"))
    end
end

outpath = get(ENV, "PORTAL_OUT", joinpath(@__DIR__, "out"))
MultiDocumenter.make(
    outpath, docs;
    search_engine = MultiDocumenter.SearchConfig(index_versions = ["stable", "dev"], engine = MultiDocumenter.FlexSearch),
    rootpath = "/",
    canonical_domain = "https://visualgeometrytoolkit.github.io/",
    sitemap = true,
)

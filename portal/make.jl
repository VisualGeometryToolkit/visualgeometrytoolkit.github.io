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
# The separate projects publish their docs to their organization pages
# (<project>.github.io, the `main` branch of <org>/<org>.github.io); the portal
# mirrors those, and keeps their canonical URLs pointing at the project pages.
const EXTERNAL = ["RansacScoringDoneRight", "LocalOptimizationDoneRight", "BlobBoards"]
site_repo(p) = (o = lowercase(p); "https://github.com/$o/$o.github.io.git")

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
# A project joins once its organization page has a Documenter build on `main`.
has_site(url) = success(pipeline(`git ls-remote --exit-code --heads $url main`; stdout = devnull, stderr = devnull))
if get(ENV, "PORTAL_NO_EXTERNAL", "") != "1"
    for p in EXTERNAL
        has_site(site_repo(p)) || (@warn "no site for $p yet"; continue)
        push!(docs, MultiDocumenter.MultiDocRef(;
            upstream = joinpath(clonedir, p), path = p, name = p,
            giturl = site_repo(p), branch = "main", fix_canonical_url = false))
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

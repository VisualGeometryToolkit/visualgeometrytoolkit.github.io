# stack_portal.jl — the stack's documentation portal, shared by every toolkit's site: the per-package Documenter sites
# of one workspace aggregated into one site with a shared navigation bar and cross-package search (MultiDocumenter).
#
#   pages = portal_pages(repo)                      # <Package>/ builds: PORTAL_LOCAL, or `repo`'s gh-pages branch
#   docs = portal_docs(pages, packages, links)      # the navigation bar: the packages' docs, then links
#   make_portal(portal_out(default), docs; canonical_domain)
#
# A site's portal/make.jl includes this file, names its repository, packages and links, and adds what only it does
# (redirect pages). Another toolkit's site includes it from this repository at a pinned commit, in the environment of
# this folder's Project.toml, and never keeps a copy.
using MultiDocumenter

# The directory that holds the `<Package>/` Documenter builds: PORTAL_LOCAL when set (local builds), else a shallow
# clone of the gh-pages branch of `repo`. A repository without that branch (before its first docs deploy) is an
# error when `required`, else a warning and an empty directory.
function portal_pages(repo; required = true)
    pages = get(ENV, "PORTAL_LOCAL", "")
    isempty(pages) || return pages
    pages = mktempdir()
    if required
        run(`git clone --depth 1 --branch gh-pages $repo $pages`)
    else
        success(pipeline(`git clone -q --depth 1 --branch gh-pages $repo $pages`; stderr = devnull)) ||
            @warn "no gh-pages branch at $repo: the portal holds no package docs"
    end
    return pages
end

# The output directory: PORTAL_OUT, or `default`.
portal_out(default) = get(ENV, "PORTAL_OUT", default)

# The navigation bar: each of `packages` that has docs under `pages`, at the portal path /<Package>/, then each
# `name => url` of `links` (a project documented on its own site: a link, never a second copy).
function portal_docs(pages, packages, links = ())
    docs = MultiDocumenter.DropdownComponent[]
    for p in packages
        isdir(joinpath(pages, p)) || (@warn "no docs for $p under $pages"; continue)
        push!(docs, MultiDocumenter.MultiDocRef(; upstream = joinpath(pages, p), path = p, name = p))
    end
    foreach(((name, url),) -> push!(docs, MultiDocumenter.Link(name, url)), links)
    return docs
end

# The portal at `outpath`, served from the root of `canonical_domain`; with no package docs at all, an empty
# directory (the landing page alone).
function make_portal(outpath, docs; canonical_domain)
    any(d -> d isa MultiDocumenter.MultiDocRef, docs) || return mkpath(outpath)
    MultiDocumenter.make(
        outpath, docs;
        search_engine = MultiDocumenter.SearchConfig(index_versions = ["stable", "dev"], engine = MultiDocumenter.FlexSearch),
        rootpath = "/",
        canonical_domain,
        sitemap = true,
    )
    return outpath
end

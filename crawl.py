#!/usr/bin/env python3
"""
Crawl soilfoodweb.com (WordPress) and school.soilfoodweb.com (Thinkific)
into docs/crawl/<host>/<slug>.md plus docs/crawl/inventory.csv.

Run in Claude Code LOCAL mode (cloud mode has no egress to these hosts):
    pip install requests beautifulsoup4 trafilatura
    python3 crawl.py

Output per page: title, meta description, canonical, last-modified (if WP
exposes it), every internal and outbound link, every image src, and the
main text as markdown. The inventory CSV is the base for the 301 map.
"""
import csv, os, re, sys, time, urllib.parse as up
import requests
from bs4 import BeautifulSoup
import trafilatura

OUT = "docs/crawl"
UA = {"User-Agent": "SFWF-rebuild-crawler/1.0 (linnea@soilfoodweb.com)"}
HOSTS = {"soilfoodweb.com", "www.soilfoodweb.com", "school.soilfoodweb.com"}

# Thinkific has no sitemap worth trusting; seed every known page.
SEEDS = [
    "https://soilfoodweb.com/",
    "https://school.soilfoodweb.com/collections",
    "https://school.soilfoodweb.com/courses/intro-foundation-course",
    "https://school.soilfoodweb.com/bundles/soilfoodweb-foundation-courses",
    "https://school.soilfoodweb.com/courses/life-in-the-soils-seminar-2-day",
    "https://school.soilfoodweb.com/courses/permaculture-design-certification",
    "https://school.soilfoodweb.com/bundles/introduction-to-ecosystem-restoration",
    "https://school.soilfoodweb.com/bundles/complete-practicum",
    "https://school.soilfoodweb.com/bundles/advanced-soil-microscopy",
    "https://school.soilfoodweb.com/bundles/advanced-biocomplete-compost-production",
    "https://school.soilfoodweb.com/bundles/advanced-biological-liquid-amendments",
    "https://school.soilfoodweb.com/bundles/advanced-field-trial",
    "https://school.soilfoodweb.com/courses/india-workshop-2026",
    "https://school.soilfoodweb.com/pages/workshop-interest",
    "https://school.soilfoodweb.com/products/communities/SFW-public-community",
    # Legacy subdomains: crawl one level so the 301 map covers them.
    "https://promo.soilfoodweb.com/",
    "https://pt.soilfoodweb.com/",
    "https://partners.soilfoodweb.com/",
    "https://webinar.soilfoodweb.com/",
]

def sitemap_urls(root):
    """WordPress exposes /wp-sitemap.xml (core) or /sitemap_index.xml (Yoast)."""
    found = []
    for path in ("/wp-sitemap.xml", "/sitemap_index.xml", "/sitemap.xml"):
        try:
            r = requests.get(root + path, headers=UA, timeout=20)
        except requests.RequestException:
            continue
        if r.status_code != 200 or "<" not in r.text:
            continue
        locs = re.findall(r"<loc>(.*?)</loc>", r.text)
        for loc in locs:
            if loc.endswith(".xml"):
                try:
                    r2 = requests.get(loc, headers=UA, timeout=20)
                    found += re.findall(r"<loc>(.*?)</loc>", r2.text)
                except requests.RequestException:
                    pass
            else:
                found.append(loc)
        if found:
            break
    return found

def slug(url):
    p = up.urlparse(url)
    s = (p.path.strip("/") or "index").replace("/", "__")
    if p.query:
        s += "__" + re.sub(r"[^a-z0-9]+", "-", p.query.lower())
    return s[:120]

def crawl(url, seen, rows, depth=0, max_depth=2):
    if url in seen or depth > max_depth:
        return
    seen.add(url)
    try:
        r = requests.get(url, headers=UA, timeout=30, allow_redirects=True)
    except requests.RequestException as e:
        rows.append([url, "ERROR", "", "", "", str(e)])
        return
    final = r.url
    host = up.urlparse(final).netloc
    soup = BeautifulSoup(r.text, "html.parser")
    title = (soup.title.string or "").strip() if soup.title else ""
    desc = soup.find("meta", attrs={"name": "description"})
    desc = desc["content"].strip() if desc and desc.get("content") else ""
    canon = soup.find("link", rel="canonical")
    canon = canon["href"] if canon else ""
    mod = soup.find("meta", property="article:modified_time")
    mod = mod["content"] if mod else ""
    text = trafilatura.extract(r.text, output_format="markdown", include_links=True,
                               include_images=True, url=final) or ""
    links = sorted({up.urljoin(final, a["href"]) for a in soup.find_all("a", href=True)})
    imgs = sorted({up.urljoin(final, i.get("src") or i.get("data-src") or "")
                   for i in soup.find_all("img") if (i.get("src") or i.get("data-src"))})
    d = os.path.join(OUT, host)
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, slug(final) + ".md"), "w") as f:
        f.write(f"# {title}\n\n- url: {final}\n- requested: {url}\n- status: {r.status_code}\n"
                f"- canonical: {canon}\n- modified: {mod}\n- description: {desc}\n\n")
        f.write("## Text\n\n" + text + "\n\n## Links\n\n" + "\n".join(f"- {l}" for l in links))
        f.write("\n\n## Images\n\n" + "\n".join(f"- {i}" for i in imgs) + "\n")
    rows.append([url, r.status_code, final, title, mod, desc])
    print(f"{r.status_code} {final}")
    time.sleep(0.6)
    for l in links:
        h = up.urlparse(l).netloc
        if h in HOSTS and not re.search(r"\.(jpg|jpeg|png|gif|pdf|mp4|zip|css|js)$", l, re.I):
            l = l.split("#")[0]
            if "/cart" in l or "/checkout" in l or "/wp-admin" in l or "?add-to-cart" in l:
                continue
            crawl(l, seen, rows, depth + 1, max_depth)

def main():
    os.makedirs(OUT, exist_ok=True)
    seen, rows = set(), []
    urls = SEEDS + sitemap_urls("https://soilfoodweb.com")
    print(f"{len(urls)} seed urls")
    for u in urls:
        crawl(u, seen, rows)
    with open(os.path.join(OUT, "inventory.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["requested_url", "status", "final_url", "title", "last_modified", "description"])
        w.writerows(rows)
    print(f"\n{len(rows)} pages -> {OUT}/inventory.csv")

if __name__ == "__main__":
    main()

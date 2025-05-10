import argparse
import requests
from urllib.parse import quote, urlparse, parse_qs

API_SERVER      = "https://apibay.org"
PRECOMPILED_URL = f"{API_SERVER}/precompiled"
SEARCH_API      = f"{API_SERVER}/q.php"

TRACKERS = [
    "udp://tracker.opentrackr.org:1337",
    "udp://open.stealth.si:80/announce",
    "udp://tracker.torrent.eu.org:451/announce",
    "udp://tracker.bittor.pw:1337/announce",
    "udp://public.popcorn-tracker.org:6969/announce",
    "udp://tracker.dler.org:6969/announce",
    "udp://exodus.desync.com:6969",
    "udp://open.demonii.com:1337/announce",
]

def fetch_search(query: str, cat: str = "0"):
    params = {"q": query}
    if cat and cat != "0":
        params["cat"] = cat
    r = requests.get(SEARCH_API, params=params)
    r.raise_for_status()
    return r.json()

def fetch_top100(kind: str):
    # kind might be 'recent' or 'video', 'audio', etc.
    url = f"{PRECOMPILED_URL}/data_top100_{kind}.json"
    r = requests.get(url)
    r.raise_for_status()
    return r.json()

def make_magnet(info_hash: str, name: str) -> str:
    m = f"magnet:?xt=urn:btih:{info_hash}&dn={quote(name)}"
    for tr in TRACKERS:
        m += f"&tr={quote(tr)}"
    return m

def human_size(b: int) -> str:
    MiB, GiB = 1024**2, 1024**3
    return f"{b/GiB:.2f} GiB" if b>=GiB else f"{b/MiB:.2f} MiB"

def print_results(items):
    header = f"{'Name':60} {'Size':>8} {'SE':>4} {'LE':>4} Magnet"
    print(header)
    print("-"*len(header))
    for t in items:
        name = t['name']
        short = name if len(name)<=60 else name[:57]+"..."
        size = human_size(int(t['size']))
        se = t.get('seeders',0)
        le = t.get('leechers',0)
        mg = make_magnet(t['info_hash'], t['name'])
        print(f"{short:60} {size:>8} {se:>4} {le:>4} {mg}")

def parse_tpb_url(url: str):
    """Extract q= and cat= parameters from a TPB-style URL."""
    parsed = urlparse(url)
    qs = parse_qs(parsed.query)
    q = qs.get("q", [""])[0]
    cat = qs.get("cat", ["0"])[0]
    return q, cat

def main():
    parser = argparse.ArgumentParser(description="TPB scraper by URL")
    parser.add_argument(
        "--url",
        help="Full TPB search URL, e.g. https://thepiratebay.org/search.php?q=fire+force&cat=200",
        required=True,
    )
    args = parser.parse_args()

    q, cat = parse_tpb_url(args.url)
    if not q:
        parser.error("URL must include a ?q= parameter")

    # top100:<kind>?
    if q.startswith("top100:"):
        # e.g. "top100:recent" or "top100:video"
        parts = q.split(":", 2)
        kind = parts[1]
        data = fetch_top100(kind)
    else:
        data = fetch_search(q, cat)
    if not data:
        print("⚠️  No results found.")
        return

    print_results(data)

if __name__ == "__main__":
    main()

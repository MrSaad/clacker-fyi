"""
Fetch the top 100 posts from r/customkeyboards plus their top-level comments
and write everything we'll need for parts extraction to raw_posts.json.

Stdlib only. No Reddit API key required — public JSON endpoints.
"""

import html
import json
import time
import urllib.request
import urllib.error

USER_AGENT = "keyboard-part-picker/0.1 by saad"
LISTING_URL = "https://www.reddit.com/r/customkeyboards/top.json?t=all&limit=100"
COMMENTS_URL = "https://www.reddit.com/comments/{id}.json?limit=50&depth=2&sort=top"
OUTPUT_PATH = "raw_posts.json"
SLEEP_BETWEEN = 1.2  # seconds between comment requests
MAX_RETRIES = 3


def fetch_json(url):
    """GET a Reddit JSON endpoint with retries on 429/5xx."""
    for attempt in range(MAX_RETRIES):
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504) and attempt < MAX_RETRIES - 1:
                wait = 2 ** attempt * 5
                print(f"  HTTP {e.code} on {url} — sleeping {wait}s and retrying")
                time.sleep(wait)
                continue
            raise


def extract_image_urls(post):
    """Return a list of image URLs for an image-bearing post, or [] if none."""
    urls = []

    # Single image post
    if post.get("post_hint") == "image" and post.get("url"):
        urls.append(post["url"])

    # Reddit gallery
    if post.get("is_gallery") and post.get("media_metadata"):
        for item in post["media_metadata"].values():
            if item.get("status") != "valid":
                continue
            src = item.get("s", {})
            u = src.get("u") or src.get("gif")
            if u:
                urls.append(html.unescape(u))

    # Direct image URL fallback
    url = post.get("url", "")
    if not urls and url:
        lower = url.lower().split("?")[0]
        if lower.endswith((".jpg", ".jpeg", ".png", ".webp", ".gif")):
            urls.append(url)
        elif "i.redd.it" in url or "i.imgur.com" in url:
            urls.append(url)

    # Dedupe, preserve order
    seen = set()
    out = []
    for u in urls:
        if u not in seen:
            seen.add(u)
            out.append(u)
    return out


def extract_top_comments(comments_payload, op_author):
    """
    Pull top-level comments from a /comments/{id}.json response.
    Mark whether each is by the OP. Skip stickied AutoModerator-style entries.
    """
    out = []
    if len(comments_payload) < 2:
        return out
    listing = comments_payload[1].get("data", {}).get("children", [])
    for child in listing:
        if child.get("kind") != "t1":
            continue
        c = child.get("data", {})
        body = c.get("body") or ""
        author = c.get("author") or ""
        if not body or author == "AutoModerator":
            continue
        out.append({
            "author": author,
            "body": body,
            "score": c.get("score", 0),
            "is_op": author == op_author,
        })
    return out


def main():
    print(f"Fetching top 100 posts: {LISTING_URL}")
    listing = fetch_json(LISTING_URL)
    children = listing.get("data", {}).get("children", [])
    print(f"  got {len(children)} posts")

    image_posts = []
    for child in children:
        if child.get("kind") != "t3":
            continue
        post = child.get("data", {})
        image_urls = extract_image_urls(post)
        if not image_urls:
            continue
        image_posts.append((post, image_urls))

    print(f"  {len(image_posts)} of those are image posts")

    results = []
    for i, (post, image_urls) in enumerate(image_posts, 1):
        post_id = post["id"]
        title = (post.get("title") or "")[:80]
        print(f"[{i}/{len(image_posts)}] {post_id}  {title}")

        comments_url = COMMENTS_URL.format(id=post_id)
        try:
            comments_payload = fetch_json(comments_url)
            top_comments = extract_top_comments(
                comments_payload, post.get("author", "")
            )
        except Exception as e:
            print(f"  comment fetch failed: {e}")
            top_comments = []

        results.append({
            "id": post_id,
            "title": post.get("title", ""),
            "author": post.get("author", ""),
            "permalink": "https://reddit.com" + post.get("permalink", ""),
            "url": post.get("url", ""),
            "created_utc": post.get("created_utc"),
            "score": post.get("score", 0),
            "num_comments": post.get("num_comments", 0),
            "selftext": post.get("selftext", "") or "",
            "link_flair_text": post.get("link_flair_text"),
            "image_urls": image_urls,
            "top_comments": top_comments,
        })

        time.sleep(SLEEP_BETWEEN)

    with open(OUTPUT_PATH, "w") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"\nWrote {len(results)} posts to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()

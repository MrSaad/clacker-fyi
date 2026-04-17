"""
Reduce raw_posts.json into a compact evidence file:
title + permalink + OP comments + any comment that mentions a parts keyword.
This is the input I (Claude) read to do parts extraction.
"""
import json
import re

PART_KEYWORDS = re.compile(
    r"\b(switch|switches|keycap|keycaps|case|plate|pcb|stab|stabili[sz]er|"
    r"layout|gmk|sa |dsa|kat|mt3|kam|cherry|gateron|kailh|holy panda|tealio|"
    r"zealio|alpaca|tangerine|boba|olivia|mode|tofu|keycult|rama|bauer|"
    r"durock|c3|tx |krytox|205g0|tribosys|3204|lubed|lube|filmed|film|"
    r"foam|tape mod|force break|holee|hhkb|brass|aluminum|polycarbonate|"
    r"\bpc\b|pom|fr4|carbon fiber|cf plate|hotswap|soldered|tkl|65%|60%|75%|40%|"
    r"endgame|build|budget|drop|massdrop|novelkeys|cannonkeys|kbdfans|"
    r"taro|botanical|umbra|alter|laser|red samurai|jamon|nautilus|sushi|"
    r"think|exent|geon|space|iron|salvun|satisfaction|owlab|mode eighty|"
    r"vega|sirius|gemini|cyberboard)\b",
    re.IGNORECASE,
)

data = json.load(open("raw_posts.json"))
out_lines = []

for i, p in enumerate(data):
    # title + meta
    out_lines.append(f"=== POST {i} | id={p['id']} | score={p['score']} ===")
    out_lines.append(f"TITLE: {p['title']}")
    out_lines.append(f"FLAIR: {p.get('link_flair_text')}")
    out_lines.append(f"PERMALINK: {p['permalink']}")
    out_lines.append(f"AUTHOR: {p['author']}")
    out_lines.append(f"IMAGES: {len(p['image_urls'])}")
    if p["selftext"]:
        out_lines.append(f"SELFTEXT: {p['selftext']}")

    # OP comments first (always include)
    op_comments = [c for c in p["top_comments"] if c["is_op"]]
    other_comments = [c for c in p["top_comments"] if not c["is_op"]]

    for c in op_comments:
        out_lines.append(f"--- OP COMMENT (score {c['score']}) ---")
        out_lines.append(c["body"])

    # Other comments only if they mention parts keywords AND have OP-relevant content
    # (e.g., someone asks "what switches?" and OP doesn't reply, sometimes other people answer)
    for c in other_comments:
        if PART_KEYWORDS.search(c["body"]) and len(c["body"]) > 20:
            out_lines.append(f"--- OTHER COMMENT by {c['author']} (score {c['score']}) ---")
            out_lines.append(c["body"][:800])

    out_lines.append("")

with open("evidence.txt", "w") as f:
    f.write("\n".join(out_lines))

print(f"wrote evidence.txt ({sum(len(l) for l in out_lines)} chars)")

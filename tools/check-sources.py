#!/usr/bin/env python3
"""Source-quality gate for front-matter `sources` URLs.

Tiers:
  A  official first party  – *.gov.cn, *.npc.gov.cn, flk.npc.gov.cn  (required for
     every policy / legal / fee / deadline claim)
  B  institutional official – hospital, CDC, Red Cross, university, state media
     official sites; acceptable for operational detail, NOT as the sole source
     of a policy rule
  C  blocklisted            – media reposts, content farms, encyclopedias,
     self-media, commercial legal portals; never acceptable

Usage: python3 tools/check-sources.py [--all] [--strict] [path ...]
  --all     also scan URLs that appear in the body
  --strict  treat every B-tier URL as an error (use for Part 3/6-12 policy batches)

Exit 1 when any error is found (C-tier, or B-tier under --strict).
"""
import argparse
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

OFFICIAL_SUFFIXES = (".gov.cn", ".npc.gov.cn")
OFFICIAL_EXACT = {"gov.cn", "npc.gov.cn", "flk.npc.gov.cn"}
# Non-policy links that are legitimately first party.
ALLOW_EXACT = {"creativecommons.org", "github.com", "www.github.com"}

BLOCKLIST_SUFFIXES = (
    "baidu.com", "sohu.com", "163.com", "sina.com.cn", "sina.cn",
    "qq.com", "weixin.qq.com", "zhihu.com", "douban.com", "xiaohongshu.com",
    "toutiao.com", "ifeng.com", "thepaper.cn", "jiemian.com", "36kr.com",
    "baijiahao.baidu.com", "wenku.baidu.com", "docin.com", "doc88.com",
    "book118.com", "lawtime.cn", "findlaw.cn", "66law.cn", "yalaw.org",
    "pkulaw.com", "chinalawinfo.com", "chinacourt.org", "weibo.com",
)

URL_RE = re.compile(r"https?://[^\s\)\]\"'<>，。；]+")


def host_of(url):
    m = re.match(r"https?://([^/]+)", url)
    return (m.group(1) if m else "").lower().split(":")[0]


def tier(host):
    if not host:
        return "C"
    if host in ALLOW_EXACT:
        return "A"
    if host in OFFICIAL_EXACT or any(
        host == s.lstrip(".") or host.endswith(s) for s in OFFICIAL_SUFFIXES
    ):
        return "A"
    if any(host == b or host.endswith("." + b) for b in BLOCKLIST_SUFFIXES):
        return "C"
    return "B"


def front_matter(text):
    m = re.match(r"^---\n(.*?)\n---\n", text, flags=re.S)
    return m.group(1) if m else ""


def scan(path, include_body):
    text = open(path, encoding="utf-8").read()
    fm = front_matter(text)
    scope = text if include_body else fm
    urls, seen = [], set()
    for u in URL_RE.findall(scope):
        u = u.rstrip("。，,；;)")
        if u not in seen:
            seen.add(u)
            urls.append(u)
    out = []
    for u in urls:
        h = host_of(u)
        t = tier(h)
        if t != "A":
            out.append((u, h, t))
    return urls, out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("paths", nargs="*")
    args = ap.parse_args()

    files = list(args.paths)
    if not files:
        for root, _d, names in os.walk(os.path.join(ROOT, "content", "cn")):
            for n in sorted(names):
                if n.endswith(".md") and n not in ("OUTLINE.md", "README.md"):
                    files.append(os.path.join(root, n))

    total_urls = 0
    b_count = c_count = 0
    for f in files:
        urls, off = scan(f, args.all)
        total_urls += len(urls)
        b = [x for x in off if x[2] == "B"]
        c = [x for x in off if x[2] == "C"]
        b_count += len(b)
        c_count += len(c)
        if c or (args.strict and b):
            print(f"✗ {os.path.relpath(f, ROOT)}")
        	# errors and warnings are printed with distinct markers
        for u, h, t in off:
            if t == "C" or (args.strict and t == "B"):
                print(f"    – 错误[{t}] {h}  {u}")
            else:
                print(f"    – 提示[{t}] {h}  {u}")

    errors = c_count + (b_count if args.strict else 0)
    print(
        f"\n{'✅' if errors == 0 else '❌'} {len(files)} 个文件，{total_urls} 条来源链接，"
        f"A 级 {total_urls - b_count - c_count}，B 级 {b_count}，C 级 {c_count}"
        + ("（strict：B 级计入错误）" if args.strict else "")
    )
    return 0 if errors == 0 else 1


if __name__ == "__main__":
    sys.exit(main())

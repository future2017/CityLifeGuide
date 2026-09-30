#!/usr/bin/env python3
"""条目结构校验：front-matter 完整性与来源清单规范性。

用法：
    python3 tools/check-entries.py content/cn

硬性校验（任一失败退出码非 0，可作提交前 gate）：
  1. 文件必须以 `---` 开头并以 `---` 闭合 front-matter
  2. front-matter 可被 YAML 解析
  3. 含必需字段：title / part / section / sources
  4. section 值必须加引号（否则 4.10 会被 YAML 解析成浮点数 4.1）

软性提示（只列出、不影响退出码）：
  5. 来源条目既无自带链接、下一行也不是 URL —— 项目规则允许「找不到官网原文就留名不留链」，
     但这类条目应当在提交说明里报出，因此单列以便人工过目。

为什么要有这个脚本：以上不变量都是历次批量改 front-matter 时真实出过的事故——脚本化
改写时丢掉开头的 `---`、把下一条来源行覆盖成 URL、URL 粘上 markdown 标记造成假 404。
机器改完必须跑一遍，不能只看 diff。
"""
import glob
import os
import re
import sys

import yaml

REQUIRED = ["title", "part", "section", "sources"]
# 热线条目按设计不带 URL：它们本身就是电话号码。
HOTLINE = re.compile(r"^\s*[-—]?\s*(\D{0,12})?(123\d\d|12345)")
PHONE_ENTRY = re.compile(r"123\d\d|热线")


def check_file(path):
    hard, warn = [], []
    text = open(path, encoding="utf-8").read()

    if not text.startswith("---"):
        return ["缺少开头的 `---` 分隔符（front-matter 起点丢失）"], warn
    if len(text.split("---")) < 3:
        return ["front-matter 未闭合（缺少结束的 `---`）"], warn
    fm_raw = text.split("---")[1]

    m = re.search(r"^section:\s*(\S+)\s*$", fm_raw, re.M)
    if m and not re.match(r"^[\"']", m.group(1)):
        hard.append(f"section 未加引号：{m.group(1)}（应写成 \"{m.group(1)}\"）")

    try:
        data = yaml.safe_load(fm_raw)
    except Exception as exc:
        return hard + [f"front-matter 无法解析：{str(exc)[:90]}"], warn
    if not isinstance(data, dict):
        return hard + ["front-matter 不是映射结构"], warn
    for key in REQUIRED:
        if not data.get(key):
            hard.append(f"缺少必需字段：{key}")

    srcs = data.get("sources") or []
    if not srcs:
        hard.append("sources 为空")
    for idx, item in enumerate(srcs, 1):
        if isinstance(item, str) and not re.search(r"https?://", item):
            if PHONE_ENTRY.search(item):
                continue  # 热线条目，按设计无链接
            warn.append(f"sources 第 {idx} 条无链接（如属「查无官网原文」请保持并在提交说明中报出）：{item[:60]}")

    return hard, warn


def main():
    root = sys.argv[1] if len(sys.argv) > 1 else "content/cn"
    files = sorted(glob.glob(os.path.join(root, "0*", "*.md")))
    if not files:
        print(f"未在 {root} 下找到条目文件")
        return 1

    total_hard = total_warn = 0
    for path in files:
        hard, warn = check_file(path)
        rel = os.path.relpath(path, root)
        if hard:
            total_hard += len(hard)
            print(f"✗ {rel}")
            for e in hard:
                print(f"    · {e}")
        if warn:
            total_warn += len(warn)
            print(f"· {rel}")
            for e in warn:
                print(f"    – {e}")

    print()
    if total_hard:
        print(f"❌ {len(files)} 个文件中发现 {total_hard} 个硬性问题、{total_warn} 条软性提示")
        return 1
    print(f"✅ {len(files)} 个文件，front-matter 结构与来源清单硬性校验全部通过"
          f"（另 {total_warn} 条软性提示，未强改）")
    return 0


if __name__ == "__main__":
    sys.exit(main())

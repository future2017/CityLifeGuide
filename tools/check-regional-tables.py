#!/usr/bin/env python3
"""检查《城市生活指南》各条目「各地差异」表的可用性。

这一节是**证据库**（见 content/cn/OUTLINE.md 第二节）：格式不必是结构化数据，但必须
满足几条硬性要求，否则来源会悄悄丢失、地区也会认不出来。

硬性（不通过 → 退出码 1，可直接当提交前的 gate）：
  1. 表头三列：事项 | 各地做法 | 来源（第三列不能是「说明」「性质」「查哪里」）
  2. 每行都有来源（第三列非空）

软性（只报告，不影响退出码）：
  3. 做法单元格里，每个分号段落最好以「地区名：」开头（全角冒号），国家层面用「全国：」
     —— 实测多数做法单元格是散文，硬性化需要重写全部差异表，故 v1 不作硬性要求

用法：
    python3 tools/check-regional-tables.py [content_dir]
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

SECTION_RE = re.compile(r"^##\s.*各地差异.*$", re.M)
NEXT_H2_RE = re.compile(r"^##\s", re.M)
ROW_RE = re.compile(r"^\|(.+)\|\s*$", re.M)
SOURCE_OK_HINTS = ("来源", "source")
BAD_SOURCE_HEADERS = ("说明", "性质", "查哪里", "备注")
LABEL_RE = re.compile(r"^\s*(?:\*\*)?(?P<name>[^：*|]{1,18})(?:\*\*)?\s*[：:]", re.S)

GENERIC_LABELS = {
    "全国", "多数地区", "多数省份", "多数城市", "大部分地区", "部分地区", "少数地区",
    "其他地区", "其他城市", "上述地区", "其余地区", "各地", "京津沪", "北上广深",
    "国家", "省级", "本省", "本市",
}
PLACE_SUFFIX = re.compile(r"(省|市|自治区|特别行政区|区|县|盟|州|旗|地区)$")


def is_plausible_region(name: str) -> bool:
    name = name.strip().strip("*").strip()
    if not name or len(name) > 18:
        return False
    if name in GENERIC_LABELS or PLACE_SUFFIX.search(name):
        return True
    return 2 <= len(name) <= 4 and re.fullmatch(r"[\u4e00-\u9fff]+", name) is not None


def table_rows(section: str) -> list[list[str]]:
    rows = []
    for m in ROW_RE.finditer(section):
        cells = [c.strip() for c in m.group(1).split("|")]
        if len(cells) >= 2 and not all(set(c) <= set("-: ") for c in cells):
            rows.append(cells)
    return rows


def check_file(path: Path) -> tuple[list[str], list[str]]:
    text = path.read_text(encoding="utf-8")
    # 去掉围栏代码块：OUTLINE.md 的条文模板里也有「## 各地差异」字样，会误判
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    m = SECTION_RE.search(text)
    if not m:
        return [], []
    start = m.end()
    nxt = NEXT_H2_RE.search(text, start)
    section = text[start : nxt.start() if nxt else len(text)]

    hard: list[str] = []
    soft: list[str] = []
    rows = table_rows(section)
    if not rows:
        return ["「各地差异」一节没有表格"], []

    header = rows[0]
    if len(header) == 2:
        hard.append(
            "表头只有 2 列（缺来源列）——改为三列，国家层面事项用 `全国：`；"
            "若确实无地方样本，须在表前一句话说明这是差异点清单"
        )
    elif len(header) != 3:
        hard.append(f"表头应为 3 列，实际 {len(header)} 列：{' | '.join(header)}")
    elif not any(h in header[2] for h in SOURCE_OK_HINTS) or any(
        b in header[2] for b in BAD_SOURCE_HEADERS
    ):
        hard.append(f"第三列表头是「{header[2]}」，应为来源")

    for i, cells in enumerate(rows[1:], start=2):
        topic = re.sub(r"\*\*", "", cells[0])[:20]
        practice = cells[1] if len(cells) > 1 else ""
        source = cells[2] if len(cells) > 2 else ""
        if len(cells) == 3 and not source.strip():
            hard.append(f"第 {i} 行（{topic}）的来源为空")
        segments = [s for s in re.split(r"[；;]", practice) if s.strip()]
        if not segments:
            hard.append(f"第 {i} 行（{topic}）的做法单元格是空的")
            continue
        unnamed = [s for s in segments if not (
            (mm := LABEL_RE.match(s)) and is_plausible_region(mm.group("name"))
        )]
        if unnamed:
            soft.append(
                f"第 {i} 行（{topic}）有 {len(unnamed)} 个段落没写「地区名：」，"
                f"例：「{unnamed[0].strip()[:36]}」"
            )
    return hard, soft


def main() -> int:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("content/cn")
    files = sorted(root.rglob("*.md"))
    hard_all: list[str] = []
    soft_all: list[str] = []
    for f in files:
        h, s = check_file(f)
        hard_all += [f"{f}: {p}" for p in h]
        soft_all += [f"{f}: {p}" for p in s]

    if soft_all:
        print(f"ℹ️  软性建议 {len(soft_all)} 处（不影响退出码）：\n")
        for p in soft_all:
            print("   ·", p)
        print()

    if hard_all:
        print(f"❌ 硬性问题 {len(hard_all)} 处：\n")
        for p in hard_all:
            print("  -", p)
        return 1

    print(f"✅ {len(files)} 个文件，「各地差异」表的硬性要求全部通过")
    return 0


if __name__ == "__main__":
    sys.exit(main())

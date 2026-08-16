#!/usr/bin/env python3
"""校验仓库不得跟踪人工私有素材。"""

from __future__ import annotations

import subprocess
import sys


PRIVATE_ASSET_PREFIX = (
    "docs/background/02_crimson_troupe/04_collectibles/assets/collectibles/"
)


def private_asset_violations(paths: list[str]) -> list[str]:
    """返回被 Git 跟踪的私有 PNG 路径。"""

    return sorted(
        path
        for path in paths
        if path.startswith(PRIVATE_ASSET_PREFIX) and path.lower().endswith(".png")
    )


def tracked_paths() -> list[str]:
    result = subprocess.run(
        ["git", "ls-files", "-z"],
        check=True,
        capture_output=True,
    )
    return [path.decode("utf-8") for path in result.stdout.split(b"\0") if path]


def main() -> int:
    violations = private_asset_violations(tracked_paths())
    if not violations:
        print("通过：仓库未跟踪私有 PNG 素材。")
        return 0

    print("失败：以下私有 PNG 素材被 Git 跟踪：", file=sys.stderr)
    for path in violations:
        print(f"  - {path}", file=sys.stderr)
    print("请保留文件名和来源索引，但不要强制提交原图。", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

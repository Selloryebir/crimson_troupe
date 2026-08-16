#!/usr/bin/env python3
"""校验 Conventional Commits 1.0.0 提交消息。"""

from __future__ import annotations

import argparse
import pathlib
import re
import subprocess
import sys


HEADER_PATTERN = re.compile(
    r"^(?P<type>[^\s():!]+)(?:\((?P<scope>[^\s()]+)\))?(?P<breaking>!)?: (?P<description>\S.*)$"
)
BREAKING_PREFIX_PATTERN = re.compile(r"^breaking(?: |-)?change(?::|$)", re.IGNORECASE)
BREAKING_FOOTER_PATTERN = re.compile(r"^(?:BREAKING CHANGE|BREAKING-CHANGE): \S.*$")
FOOTER_PATTERN = re.compile(r"^(?:[^\s:]+|BREAKING CHANGE)(?:: | #)\S.*$")
GITHUB_MERGE_HEADER_PATTERN = re.compile(r"^Merge pull request #\d+ from \S+$")


def validate_message(message: str) -> list[str]:
    """返回提交消息中的规范错误；空列表表示通过。"""

    lines = message.replace("\r\n", "\n").replace("\r", "\n").splitlines()
    errors: list[str] = []

    if not lines or not lines[0].strip():
        return ["提交消息首行不能为空。"]

    if not HEADER_PATTERN.fullmatch(lines[0]):
        errors.append(
            "首行必须符合 <type>[optional scope][optional !]: <description>，且冒号后有一个空格。"
        )

    if len(lines) > 1 and lines[1].strip():
        errors.append("正文或脚注必须与首行之间空一行。")

    for index, line in enumerate(lines[2:], start=2):
        if not BREAKING_PREFIX_PATTERN.match(line):
            continue
        if not BREAKING_FOOTER_PATTERN.fullmatch(line):
            errors.append(
                f"第 {index + 1} 行的破坏性变更脚注必须使用大写 "
                "BREAKING CHANGE: <说明> 或 BREAKING-CHANGE: <说明>。"
            )
            continue

        paragraph_start = index
        while paragraph_start > 2 and lines[paragraph_start - 1].strip():
            paragraph_start -= 1
        if not FOOTER_PATTERN.fullmatch(lines[paragraph_start]):
            errors.append(f"第 {index + 1} 行的脚注必须与正文之间空一行。")

    return errors


def validate_git_commit_message(message: str, parent_count: int) -> list[str]:
    """校验 Git commit；标准 GitHub 双父合并提交改为校验正文中的 PR 标题。"""

    lines = message.replace("\r\n", "\n").replace("\r", "\n").splitlines()
    if (
        parent_count != 2
        or not lines
        or not GITHUB_MERGE_HEADER_PATTERN.fullmatch(lines[0])
    ):
        return validate_message(message)

    if len(lines) < 3 or lines[1].strip():
        return ["GitHub 合并提交必须在自动生成首行与 PR 标题之间保留一个空行。"]

    pr_message = "\n".join(lines[2:])
    if not pr_message.strip():
        return ["GitHub 合并提交正文必须以符合 Conventional Commits 的 PR 标题开头。"]

    return [
        f"GitHub 合并提交中的 PR 标题或正文：{error}"
        for error in validate_message(pr_message)
    ]


def commit_details(commit: str) -> tuple[int, str]:
    result = subprocess.run(
        ["git", "show", "-s", "--format=%P%n%B", commit],
        check=True,
        capture_output=True,
        text=True,
    )
    parent_line, message = result.stdout.split("\n", maxsplit=1)
    return len(parent_line.split()), message


def commits_in_range(revision_range: str) -> list[str]:
    result = subprocess.run(
        ["git", "rev-list", "--reverse", revision_range],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.splitlines()


def validate_named_message(name: str, message: str, parent_count: int = 1) -> bool:
    errors = validate_git_commit_message(message, parent_count)
    if not errors:
        print(f"通过：{name}")
        return True

    print(f"失败：{name}", file=sys.stderr)
    for error in errors:
        print(f"  - {error}", file=sys.stderr)
    print("  规范：https://www.conventionalcommits.org/en/v1.0.0/", file=sys.stderr)
    return False


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--file", type=pathlib.Path, help="提交消息文件，用于 commit-msg hook")
    source.add_argument("--commit", action="append", help="待校验的 commit SHA；可重复传入")
    source.add_argument("--range", dest="revision_range", help="待校验的 Git revision range")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.file is not None:
        ok = validate_named_message(str(args.file), args.file.read_text(encoding="utf-8"))
        return 0 if ok else 1

    commits = args.commit or commits_in_range(args.revision_range)
    ok = True
    for commit in commits:
        parent_count, message = commit_details(commit)
        ok = validate_named_message(commit, message, parent_count) and ok
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""校验仓库文档的编码、结构、引用和声明式契约。"""

from __future__ import annotations

import csv
import io
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Iterable, Optional
from urllib.parse import unquote, urlsplit

try:
    import yaml
    from jsonschema import Draft202012Validator
    from jsonschema.exceptions import SchemaError
except ImportError as error:  # pragma: no cover - 只在依赖未安装时触发
    missing = getattr(error, "name", "开发依赖")
    print(
        f"缺少 {missing}；请先运行 python3 -m pip install -r requirements-dev.txt。",
        file=sys.stderr,
    )
    raise SystemExit(2) from error


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
TEXT_SUFFIXES = {".csv", ".json", ".md", ".py", ".sh", ".txt", ".yaml", ".yml"}
TEXT_FILENAMES = {
    ".editorconfig",
    ".gitattributes",
    ".gitignore",
    "AGENTS.md",
    "CONTRIBUTING.md",
    "LICENSE",
    "README.md",
    "SECURITY.md",
    "THIRD_PARTY_NOTICES.md",
}
MARKDOWN_LINK_PATTERN = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
MARKDOWN_REFERENCE_PATTERN = re.compile(r"(?m)^\s*\[[^\]]+\]:\s*(\S+)")
HTML_LINK_PATTERN = re.compile(r"(?:href|src)=[\"']([^\"']+)[\"']", re.IGNORECASE)
FENCED_CODE_PATTERN = re.compile(r"```.*?```", re.DOTALL)


class UniqueKeyLoader(yaml.SafeLoader):
    """拒绝 YAML 中会被普通解析器静默覆盖的重复键。"""


def _construct_unique_mapping(
    loader: UniqueKeyLoader, node: yaml.MappingNode, deep: bool = False
) -> dict[Any, Any]:
    mapping: dict[Any, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in mapping:
            raise yaml.constructor.ConstructorError(
                "while constructing a mapping",
                node.start_mark,
                f"found duplicate key: {key}",
                key_node.start_mark,
            )
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    _construct_unique_mapping,
)


def repository_paths(root: Path) -> list[str]:
    """列出 Git 已跟踪的仓库文件。"""

    result = subprocess.run(
        [
            "git",
            "-C",
            str(root),
            "ls-files",
            "-z",
        ],
        check=True,
        capture_output=True,
    )
    return sorted(
        path.decode("utf-8")
        for path in result.stdout.split(b"\0")
        if path
    )


def _is_text_path(path: Path) -> bool:
    return path.suffix.lower() in TEXT_SUFFIXES or path.name in TEXT_FILENAMES


def _read_text(path: Path, relative_path: str, errors: list[str]) -> Optional[str]:
    data = path.read_bytes()
    try:
        text = data.decode("utf-8-sig" if path.suffix.lower() == ".csv" else "utf-8")
    except UnicodeDecodeError as error:
        errors.append(f"{relative_path}: 不是有效的 UTF-8（{error}）")
        return None

    if not data.endswith(b"\n"):
        errors.append(f"{relative_path}: 文件末尾缺少换行")
    if b"\r" in data:
        errors.append(f"{relative_path}: 包含 CR 或 CRLF，应统一为 LF")
    if path.suffix.lower() == ".csv" and not data.startswith(b"\xef\xbb\xbf"):
        errors.append(f"{relative_path}: CSV 必须使用 UTF-8 BOM")
    if path.suffix.lower() != ".csv" and data.startswith(b"\xef\xbb\xbf"):
        errors.append(f"{relative_path}: 仅 CSV 使用 UTF-8 BOM")
    return text


def _validate_csv(text: str, relative_path: str, errors: list[str]) -> None:
    try:
        rows = list(csv.reader(io.StringIO(text, newline="")))
    except csv.Error as error:
        errors.append(f"{relative_path}: CSV 无法解析（{error}）")
        return

    if not rows:
        errors.append(f"{relative_path}: CSV 不能为空")
        return
    if not rows[0] or any(not column.strip() for column in rows[0]):
        errors.append(f"{relative_path}: CSV 表头包含空列名")
        return
    if len(set(rows[0])) != len(rows[0]):
        errors.append(f"{relative_path}: CSV 表头包含重复列名")

    width = len(rows[0])
    for line_number, row in enumerate(rows[1:], start=2):
        if len(row) != width:
            errors.append(
                f"{relative_path}:{line_number}: 列数为 {len(row)}，应为 {width}"
            )


def _markdown_targets(text: str) -> Iterable[str]:
    content = FENCED_CODE_PATTERN.sub("", text)
    yield from MARKDOWN_LINK_PATTERN.findall(content)
    yield from MARKDOWN_REFERENCE_PATTERN.findall(content)
    yield from HTML_LINK_PATTERN.findall(content)


def _local_link_path(target: str) -> Optional[str]:
    target = target.strip()
    if target.startswith("<") and ">" in target:
        target = target[1 : target.index(">")]
    else:
        target = target.split(maxsplit=1)[0]

    parsed = urlsplit(target)
    if parsed.scheme or parsed.netloc or not parsed.path:
        return None
    path = unquote(parsed.path)
    if path.startswith("/"):
        return None
    return path


def _validate_markdown_links(
    root: Path,
    path: Path,
    text: str,
    relative_path: str,
    errors: list[str],
) -> None:
    for target in _markdown_targets(text):
        local_path = _local_link_path(target)
        if local_path is None:
            continue
        resolved = (path.parent / local_path).resolve()
        try:
            resolved.relative_to(root.resolve())
        except ValueError:
            errors.append(f"{relative_path}: 本地链接越出仓库范围：{target}")
            continue
        if not resolved.exists():
            errors.append(f"{relative_path}: 本地链接目标不存在：{target}")


def _format_schema_path(parts: Iterable[Any]) -> str:
    rendered = "".join(
        f"[{part}]" if isinstance(part, int) else f".{part}" for part in parts
    )
    return rendered.removeprefix(".") or "<root>"


def _validate_schema(
    instance: Any,
    schema: Any,
    relative_path: str,
    errors: list[str],
    prefix: str = "",
) -> None:
    validator = Draft202012Validator(schema)
    for error in sorted(
        validator.iter_errors(instance),
        key=lambda item: tuple(str(part) for part in item.path),
    ):
        location = _format_schema_path(error.absolute_path)
        if prefix:
            location = f"{prefix}.{location}" if location != "<root>" else prefix
        errors.append(f"{relative_path}:{location}: {error.message}")


def _walk_declared_inputs(value: Any) -> Iterable[str]:
    if isinstance(value, dict):
        for key, child in value.items():
            if key == "信息输入" and isinstance(child, list):
                yield from (item for item in child if isinstance(item, str))
            yield from _walk_declared_inputs(child)
    elif isinstance(value, list):
        for child in value:
            yield from _walk_declared_inputs(child)


def _validate_contracts(
    root: Path,
    structured: dict[str, Any],
    errors: list[str],
) -> None:
    module_schema_path = "docs/blueprint/02_contracts/module.schema.json"
    journey_schema_path = "docs/blueprint/02_contracts/journey.schema.json"
    registry_path = "docs/blueprint/03_journeys/journey_registry.yaml"
    module_prefix = "docs/blueprint/04_modules/"

    for schema_path in (module_schema_path, journey_schema_path):
        schema = structured.get(schema_path)
        if schema is not None:
            try:
                Draft202012Validator.check_schema(schema)
            except SchemaError as error:
                errors.append(f"{schema_path}: JSON Schema 无效（{error}）")

    module_schema = structured.get(module_schema_path)
    modules: dict[str, tuple[str, Any]] = {}
    for relative_path, value in structured.items():
        if not relative_path.startswith(module_prefix) or not relative_path.endswith(".yaml"):
            continue
        if module_schema is not None:
            _validate_schema(value, module_schema, relative_path, errors)
        if isinstance(value, dict) and isinstance(value.get("id"), str):
            module_id = value["id"]
            if module_id in modules:
                errors.append(f"{relative_path}: 模块 id 重复：{module_id}")
            modules[module_id] = (relative_path, value)

    for module_id, (relative_path, value) in modules.items():
        dependencies = value.get("依赖模块", []) if isinstance(value, dict) else []
        if not isinstance(dependencies, list):
            continue
        for dependency in dependencies:
            if dependency != "core" and dependency not in modules:
                errors.append(
                    f"{relative_path}: 模块 {module_id} 引用了不存在的依赖模块 {dependency}"
                )

    registry = structured.get(registry_path)
    journey_schema = structured.get(journey_schema_path)
    if isinstance(registry, dict):
        journeys = registry.get("旅程")
        if not isinstance(journeys, list):
            errors.append(f"{registry_path}: 旅程必须是列表")
        elif journey_schema is not None:
            for index, journey in enumerate(journeys):
                _validate_schema(
                    journey,
                    journey_schema,
                    registry_path,
                    errors,
                    prefix=f"旅程[{index}]",
                )

    for relative_path, value in structured.items():
        if not relative_path.startswith("docs/"):
            continue
        for declared_path in _walk_declared_inputs(value):
            if not declared_path.startswith("docs/"):
                errors.append(f"{relative_path}: 信息输入必须位于 docs/：{declared_path}")
            elif not (root / declared_path).is_file():
                errors.append(f"{relative_path}: 信息输入不存在：{declared_path}")


def validate_repository(
    root: Path, paths: Optional[Iterable[str]] = None
) -> list[str]:
    """返回仓库文档校验错误；空列表表示通过。"""

    selected_paths = list(paths) if paths is not None else repository_paths(root)
    errors: list[str] = []
    structured: dict[str, Any] = {}

    for relative_path in selected_paths:
        path = root / relative_path
        if not path.is_file() or not _is_text_path(path):
            continue
        text = _read_text(path, relative_path, errors)
        if text is None:
            continue

        suffix = path.suffix.lower()
        if suffix == ".csv":
            _validate_csv(text, relative_path, errors)
        elif suffix == ".json":
            try:
                structured[relative_path] = json.loads(text)
            except json.JSONDecodeError as error:
                errors.append(f"{relative_path}:{error.lineno}: JSON 无法解析（{error.msg}）")
        elif suffix in {".yaml", ".yml"}:
            try:
                structured[relative_path] = yaml.load(text, Loader=UniqueKeyLoader)
            except yaml.YAMLError as error:
                errors.append(f"{relative_path}: YAML 无法解析（{error}）")
        elif suffix == ".md":
            _validate_markdown_links(root, path, text, relative_path, errors)

    _validate_contracts(root, structured, errors)
    return sorted(set(errors))


def main() -> int:
    paths = [
        path
        for path in repository_paths(REPOSITORY_ROOT)
        if (REPOSITORY_ROOT / path).is_file()
    ]
    errors = validate_repository(REPOSITORY_ROOT, paths)
    if not errors:
        print(f"通过：已校验 {len(paths)} 个仓库文件的文档规范。")
        return 0

    print("失败：文档规范校验发现以下问题：", file=sys.stderr)
    for error in errors:
        print(f"  - {error}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

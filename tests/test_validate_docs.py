import tempfile
import unittest
from pathlib import Path

from scripts.validate_docs import validate_repository


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


class ValidateDocsTest(unittest.TestCase):
    def test_current_repository_conforms(self) -> None:
        self.assertEqual(validate_repository(REPOSITORY_ROOT), [])

    def test_accepts_valid_csv_and_markdown_link(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "data.csv").write_bytes("编号,名称\n1,条目\n".encode("utf-8-sig"))
            (root / "target.md").write_text("# 目标\n", encoding="utf-8")
            (root / "index.md").write_text(
                "# 索引\n\n[目标](target.md)\n", encoding="utf-8"
            )

            errors = validate_repository(
                root, ["data.csv", "index.md", "target.md"]
            )

            self.assertEqual(errors, [])

    def test_rejects_csv_without_bom_and_inconsistent_width(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "data.csv").write_text(
                "编号,名称\n1,条目,多余值\n", encoding="utf-8"
            )

            errors = validate_repository(root, ["data.csv"])

            self.assertTrue(any("UTF-8 BOM" in error for error in errors))
            self.assertTrue(any("列数为 3，应为 2" in error for error in errors))

    def test_rejects_duplicate_yaml_key_and_invalid_json(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "duplicate.yaml").write_text(
                "id: first\nid: second\n", encoding="utf-8"
            )
            (root / "invalid.json").write_text("{]\n", encoding="utf-8")

            errors = validate_repository(root, ["duplicate.yaml", "invalid.json"])

            self.assertTrue(any("duplicate key: id" in error for error in errors))
            self.assertTrue(any("JSON 无法解析" in error for error in errors))

    def test_rejects_missing_and_out_of_repository_links(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "index.md").write_text(
                "# 索引\n\n[缺失](missing.md)\n[越界](../outside.md)\n",
                encoding="utf-8",
            )

            errors = validate_repository(root, ["index.md"])

            self.assertTrue(any("目标不存在" in error for error in errors))
            self.assertTrue(any("越出仓库范围" in error for error in errors))

if __name__ == "__main__":
    unittest.main()

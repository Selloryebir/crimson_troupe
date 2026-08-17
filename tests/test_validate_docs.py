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
            (root / "target.md").write_bytes("# 目标\n".encode("utf-8"))
            (root / "index.md").write_bytes(
                "# 索引\n\n[目标](target.md)\n".encode("utf-8")
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

    def test_rejects_collectible_images_and_embeds(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            catalog = (
                root
                / "docs/background/02_crimson_troupe/04_collectibles"
            )
            catalog.mkdir(parents=True)
            (catalog / "index.md").write_bytes(
                "# 藏品\n\n![第三方原图](collectible.png)\n".encode("utf-8")
            )
            (catalog / "collectible.png").write_bytes(b"not-an-image\n")

            errors = validate_repository(
                root,
                [
                    "docs/background/02_crimson_troupe/04_collectibles/index.md",
                    "docs/background/02_crimson_troupe/04_collectibles/collectible.png",
                ],
            )

            self.assertTrue(any("不得嵌入图片" in error for error in errors))
            self.assertTrue(any("不得跟踪图片文件" in error for error in errors))

    def test_rejects_invalid_blueprint_references(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            contracts = root / "docs/blueprint/02_contracts"
            journeys = root / "docs/blueprint/03_journeys"
            contracts.mkdir(parents=True)
            journeys.mkdir(parents=True)
            (contracts / "journey.schema.json").write_bytes(
                (
                    REPOSITORY_ROOT
                    / "docs/blueprint/02_contracts/journey.schema.json"
                ).read_bytes()
            )
            (journeys / "journey_registry.yaml").write_bytes(
                (
                    "版本: 1.0.0\n"
                    "旅程:\n"
                    "  - &journey\n"
                    "    id: JRN-001\n"
                    "    名称: 测试旅程\n"
                    "    用户目标: 测试引用校验\n"
                    "    入口: [首页]\n"
                    "    路由: [/]\n"
                    "    模块: [missing_module]\n"
                    "    主流程: [开始, 完成]\n"
                    "    恢复: [返回首页]\n"
                    "    开发批次: M0\n"
                    "    人工审核: 待审\n"
                    "  - *journey\n"
                ).encode("utf-8")
            )
            (root / "docs/blueprint/07_功能目录.csv").write_bytes(
                (
                    "所属模块,名称,优先级,主旅程,辅助旅程,开发批次,人工审核\n"
                    "missing_feature_module,错误功能,P0,JRN-999,JRN-001,M0,待审\n"
                ).encode("utf-8-sig")
            )

            errors = validate_repository(
                root,
                [
                    "docs/blueprint/02_contracts/journey.schema.json",
                    "docs/blueprint/03_journeys/journey_registry.yaml",
                    "docs/blueprint/07_功能目录.csv",
                ],
            )

            self.assertTrue(any("旅程 id 重复：JRN-001" in error for error in errors))
            self.assertTrue(
                any("不存在的模块 missing_module" in error for error in errors)
            )
            self.assertTrue(
                any(
                    "不存在的模块 missing_feature_module" in error
                    for error in errors
                )
            )
            self.assertTrue(
                any("不存在的旅程 JRN-999" in error for error in errors)
            )

if __name__ == "__main__":
    unittest.main()

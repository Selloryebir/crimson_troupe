import unittest

from scripts.validate_commit_message import validate_message


class ValidateCommitMessageTest(unittest.TestCase):
    def assert_valid(self, message: str) -> None:
        self.assertEqual(validate_message(message), [])

    def assert_invalid(self, message: str) -> None:
        self.assertTrue(validate_message(message))

    def test_accepts_required_header(self) -> None:
        self.assert_valid("docs: 补充提交规范")
        self.assert_valid("feat(schedule): 增加演出日期筛选")
        self.assert_valid("FIX: 修复筛选状态")

    def test_accepts_breaking_change_forms(self) -> None:
        self.assert_valid("feat(api)!: 移除旧版场次字段")
        self.assert_valid(
            "feat: 调整场次结构\n\nBREAKING CHANGE: 读取方必须改用 performances 字段"
        )
        self.assert_valid(
            "feat: 调整场次结构\n\nBREAKING-CHANGE: 读取方必须改用 performances 字段"
        )

    def test_accepts_body_and_footers(self) -> None:
        self.assert_valid(
            "fix(parser): 修复空格解析\n\n补充多段上下文。\n\nRefs: #123\nReviewed-by: Example"
        )

    def test_accepts_merge_commit_message(self) -> None:
        self.assert_valid(
            "Merge pull request #2 from Selloryebir/dev\n\nchore(repo): 发布文档库与仓库治理基线"
        )

    def test_rejects_invalid_header(self) -> None:
        self.assert_invalid("更新文档")
        self.assert_invalid("feat:缺少空格")
        self.assert_invalid("feat(): scope 不能为空")
        self.assert_invalid("fix(parser):")

    def test_requires_blank_line_before_body(self) -> None:
        self.assert_invalid("docs: 更新说明\n正文前没有空行")

    def test_requires_uppercase_breaking_footer(self) -> None:
        self.assert_invalid("feat: 调整接口\n\nbreaking change: 接口不兼容")
        self.assert_invalid("feat: 调整接口\n\nBREAKING CHANGE:缺少空格")
        self.assert_invalid("feat: 调整接口\n\nBREAKING CHANGE: ")
        self.assert_invalid(
            "feat: 调整接口\n\n正文。\nBREAKING CHANGE: 脚注前缺少空行"
        )


if __name__ == "__main__":
    unittest.main()

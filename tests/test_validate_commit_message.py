import unittest

from scripts.validate_commit_message import validate_git_commit_message, validate_message


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

    def test_accepts_standard_github_merge_with_conventional_pr_title(self) -> None:
        message = (
            "Merge pull request #2 from Selloryebir/dev\n\n"
            "chore(repo): 发布文档库与仓库治理基线"
        )
        self.assertEqual(validate_git_commit_message(message, parent_count=2), [])

    def test_rejects_github_merge_with_invalid_pr_title(self) -> None:
        message = "Merge pull request #2 from Selloryebir/dev\n\n发布治理基线"
        self.assertTrue(validate_git_commit_message(message, parent_count=2))

    def test_rejects_github_merge_without_pr_title(self) -> None:
        message = "Merge pull request #2 from Selloryebir/dev"
        self.assertTrue(validate_git_commit_message(message, parent_count=2))

    def test_does_not_exempt_non_merge_or_nonstandard_merge_headers(self) -> None:
        github_message = (
            "Merge pull request #2 from Selloryebir/dev\n\n"
            "chore(repo): 发布文档库与仓库治理基线"
        )
        branch_message = "Merge branch 'dev'\n\nchore(repo): 发布治理基线"
        self.assertTrue(validate_git_commit_message(github_message, parent_count=1))
        self.assertTrue(validate_git_commit_message(branch_message, parent_count=2))


if __name__ == "__main__":
    unittest.main()

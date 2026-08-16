# 贡献指南

## 基本流程

1. 修改前阅读 `docs/README.md` 与 `docs/01_文档组织规范.md`，确认信息层级和唯一维护位置。
2. 保留事实、来源、审查状态和多语种缺失标记，不以编辑推测覆盖原记录。
3. 首次运行校验前执行 `python3 -m pip install -r requirements-dev.txt` 安装固定的开发依赖。
4. 提交前运行文档校验和单元测试，并确认没有未经授权的第三方原图进入暂存区。
5. 提交信息遵循下述 Conventional Commits 规范。

## 第三方素材边界

- 仓库不维护第三方原图、私有图片文件名、相对路径或本地挂载点。
- agents、自动化脚本和网站构建不得访问仓库外的人工私有备份，也不得从中复制、恢复或发布内容。
- 贡献只可维护公开来源网址、文字说明、原创资产和已经取得必要授权的素材。
- 第三方原图不得包含在 issue、pull request、构建产物、测试夹具或发布包中。

## Commit 规范

本仓库的所有新提交必须遵循 [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/)。人员、自动化工具和 agents 使用同一规则。

提交消息结构如下：

```text
<type>[optional scope][optional !]: <description>

[optional body]

[optional footer(s)]
```

必须遵守以下要求：

1. `type` 必填；增加功能使用 `feat`，修复缺陷使用 `fix`。
2. `scope` 可选，用括号标明受影响部分，例如 `docs`、`blueprint` 或 `i18n`。
3. 冒号后必须有一个空格和非空的简短说明。
4. 正文可选；如有正文，必须与首行之间空一行。
5. 脚注可选，格式遵循 Git trailer：`Token: value` 或 `Token #value`；Token 中的空格使用 `-`。
6. 破坏性变更必须在 type/scope 后添加 `!`，或在脚注中使用大写 `BREAKING CHANGE: <说明>`；`BREAKING-CHANGE:` 与其同义。
7. 除 `feat`、`fix` 外，可以使用符合变更性质的其他类型，例如 `docs`、`refactor`、`test`、`build`、`ci`、`chore`、`style`、`perf` 和 `revert`。
8. 不得使用 `git commit --no-verify` 绕过仓库校验。
9. GitHub 通过 “Create a merge commit” 自动生成的标准双父合并提交，可以保留 `Merge pull request #<编号> from <来源>` 首行；其正文第一行必须是符合本节规范的 PR 标题。此规则不豁免普通提交、非标准合并消息或不合规的 PR 标题。

推荐使用英文 type 和 scope，description、正文与脚注说明使用简体中文。

以下每一行都是一个独立提交的有效首行：

```text
docs: 补充提交规范
feat(schedule): 增加演出日期筛选
fix(i18n): 修正日文回退标签
feat(api)!: 移除旧版场次字段
```

也可以通过脚注明确破坏性变更：

```text
feat(api): 调整场次字段

BREAKING CHANGE: 场次读取方必须改用 performances 字段
```

无效示例：

```text
更新文档
feat:缺少冒号后的空格
feat(): scope 不能为空
fix(parser):
```

## 启用本地校验

首次克隆后执行：

```bash
./scripts/install-git-hooks.sh
```

该命令将当前仓库的 `core.hooksPath` 设置为 `.githooks`。此后 `git commit` 会调用版本化的 `commit-msg` hook；GitHub Actions 还会检查 pull request 和分支 push 中的新提交，因此本地 hook 未安装时仍会产生远端失败检查。

仓库管理员应将 GitHub 状态检查 `Commit convention / validate-commits` 设为受保护分支的必需检查，从而阻止不合规提交被合并。分支保护属于 GitHub 仓库设置，不能仅通过仓库文件自动启用。

可手动运行完整校验：

```bash
python3 scripts/validate_docs.py
python3 -m unittest discover -s tests -p 'test_*.py'
```

现有历史提交不会被追溯改写，规范从本规则加入后的新提交开始执行。

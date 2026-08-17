# 猩红剧团网页

本仓库用于整理《明日方舟》猩红剧团相关背景事实、创作内容、网站蓝图与项目规划，并为后续网页实现提供唯一、可审查的信息基础。

本项目是非官方同人项目，与《明日方舟》及其权利方不存在隶属、授权或背书关系。当前处于资料与蓝图阶段，优先完善信息库、蓝图与功能元素方案；关键决策统一裁定前不初始化具体网页技术栈，也没有可部署的网站应用。

## 仓库结构

| 路径 | 职责 |
|---|---|
| `docs/background/` | 世界观事实、官方或可回溯专名、事实边界与公开来源索引 |
| `docs/content/` | 基于事实的创作应用、工作译和内容本地化 |
| `docs/blueprint/` | 网站架构、功能、模块、旅程、契约和技术设计 |
| `docs/planning/` | 来源登记、审核事项、覆盖缺口和推进计划 |
| `scripts/`、`tests/` | 仓库规范校验脚本及其测试 |

完整入口和阅读顺序见 [`docs/README.md`](docs/README.md)，组织、命名、格式与唯一来源规则见 [`docs/01_文档组织规范.md`](docs/01_文档组织规范.md)。

## 本地校验

仓库开发与 CI 统一使用 Python 3.14。首次克隆后启用版本化 Git hook：

```bash
./scripts/install-git-hooks.sh
```

安装固定的开发依赖并运行完整校验：

```bash
python3 -m pip install -r requirements-dev.txt
python3 scripts/validate_docs.py
python3 -m unittest discover -s tests -p 'test_*.py'
```

所有新提交必须遵循 Conventional Commits 1.0.0。具体规则、分支协作要求和第三方素材边界见 [`CONTRIBUTING.md`](CONTRIBUTING.md)。

## 第三方素材

仓库不存放或分发第三方原图，也不维护私有图片文件名、相对路径或本地挂载点。背景事实通过公开来源网址和文字说明回溯；未来网站只使用项目原创或已取得必要授权的视觉资产。

## 安全问题

安全漏洞不得通过公开 issue 披露，请按照 [`SECURITY.md`](SECURITY.md) 使用 GitHub Private Vulnerability Reporting。文档事实纠错、来源或翻译问题和功能建议使用对应的 issue 表单。

## 权利声明

本仓库不是开源项目。Selloryebir (Yihao Zhuang) 对其原创贡献保留所有权利；未授予复制、修改、分发或再许可权限。第三方名称、事实来源、商标和素材不属于本项目的授权范围。详见 [`LICENSE`](LICENSE) 与 [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md)。

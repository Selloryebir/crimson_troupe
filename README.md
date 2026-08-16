# 猩红剧团网页

本仓库用于整理《明日方舟》猩红剧团相关背景事实、创作内容、网站蓝图与项目规划，并为后续网页实现提供唯一、可审查的信息基础。

本项目是非官方同人项目，与《明日方舟》及其权利方不存在隶属、授权或背书关系。当前处于资料与蓝图阶段，尚未初始化具体网页技术栈，也没有可部署的网站应用。

## 仓库结构

| 路径 | 职责 |
|---|---|
| `docs/background/` | 世界观事实、官方或可回溯专名、事实边界与私有图像索引 |
| `docs/content/` | 基于事实的创作应用、工作译和内容本地化 |
| `docs/blueprint/` | 网站架构、功能、模块、旅程、契约和技术设计 |
| `docs/planning/` | 来源登记、审核事项、覆盖缺口和推进计划 |
| `scripts/`、`tests/` | 仓库规范校验脚本及其测试 |

完整入口和阅读顺序见 [`docs/README.md`](docs/README.md)，组织、命名、格式与唯一来源规则见 [`docs/01_文档组织规范.md`](docs/01_文档组织规范.md)。

## 本地校验

仓库校验脚本需要 Python 3.9 或更高版本。首次克隆后启用版本化 Git hook：

```bash
./scripts/install-git-hooks.sh
```

运行现有测试：

```bash
python3 -m unittest tests/test_validate_commit_message.py
```

所有新提交必须遵循 Conventional Commits 1.0.0。具体规则、分支协作要求和私有素材边界见 [`CONTRIBUTING.md`](CONTRIBUTING.md)。

## 私有素材

第三方原图不随仓库分发。人工维护的私有素材根目录位于仓库同级的 `../assets/`；仓库内 `docs/background/02_crimson_troupe/04_collectibles/assets/collectibles/` 只作为人工本地挂载位置并被 Git 忽略。

agents、自动化脚本和网站构建不得访问、复制、恢复或发布 `../assets/` 中的内容。仓库只保存文件名、相对路径、来源和文字描述。

## 权利声明

本仓库不是开源项目。Selloryebir (Yihao Zhuang) 对其原创贡献保留所有权利；未授予复制、修改、分发或再许可权限。第三方名称、事实来源、商标和素材不属于本项目的授权范围。详见 [`LICENSE`](LICENSE) 与 [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md)。

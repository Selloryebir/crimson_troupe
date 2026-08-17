# 可插拔体验模块

每个 YAML 只声明本模块的挂载点、路由、依赖、信息输入、状态、产物、降级和验收；核心壳不是插件。

各模块 YAML 中以 `/` 开头的路由均是地域配置前缀后的路径模板。例如 `/archive` 实际挂载为 `/:profile/archive`；只有站点根路径 `/` 用于跳转到 `/yan/`。

| 模块 | 责任 | 依赖 | 主要旅程 |
| --- | --- | --- | --- |
| troupe_information | 组织、人物、部门 | — | JRN-004、JRN-401 |
| repertoire_archive | 日历、剧目、历史演出 | — | JRN-002、003、201、203 |
| purchase_flow | 单场次分区、双币价格、购票结果、导演与最小本地状态 | repertoire_archive | JRN-101～103、105 |
| ticket_game | 购票失败后的黄牛平台支线 | purchase_flow | JRN-104 |
| souvenir_ticket | SVG/PNG 观演凭据与七段组合印章 | purchase_flow | JRN-106 |
| archive | 藏品、探索、版本 | — | JRN-202、203、206 |
| hallucination_layer | 幻觉组合与恢复 | archive | JRN-204 |
| red_velvet_studio | 红丝绒片场 | archive | JRN-205、602 |
| timeline_archive | 剧团/世界时间线 | troupe_information | JRN-203 |
| i18n | 地域展示配置、文本资源、货币与证据 | — | JRN-301～303 |
| join_us | 虚构试镜与舞台名 | troupe_information | JRN-401、402 |
| campaigns | 巡演季、片场周、档案夜与幕间游戏 | repertoire_archive、archive | JRN-601～603 |
| narrative_layer | 双生相、改稿、结局与全站可撤销叙事覆盖 | — | JRN-007、206、501 |
| historical_site | M3 旧酒神历史网站、日期路由、表里隔离与返回 | — | JRN-207 |

批次边界固定为：M0 建立核心壳与 repertoire/troupe 参考模块；M1 安装 purchase_flow、souvenir_ticket、i18n 和 archive 等基础插件；M2 再安装 ticket_game 等互动插件。M1 内部的具体先后顺序仍由问卷 E01 决定。M0 以炎国配置验证 i18n 接入面；首个多语言版本交付炎国、东国、维多利亚和哥伦比亚，后续六个计划配置按阶段人工启用。购票体验的唯一详细规则见 `01_购票体验契约.md`，具体任务、路由和恢复路径见 `../03_journeys/journey_registry.yaml`。

`内容准备依据` 只保存人工与 agent 生成、审阅模块内容时应核对的 `docs/background` 路径，不进入前端构建、模块运行或搜索。`信息输入` 才是构建期依赖，必须直接指向现存的 `docs/content` 或 `docs/blueprint` 文件。实际页面记录由构建入口选择的内容集提供；需要回溯事实时由内容记录保存来源路径和自然定位字段。两类路径都由结构契约校验，不得混用。模块加载失败只降级自身，不能破坏导航、正常演出详情、闭幕和无 JavaScript 基线。

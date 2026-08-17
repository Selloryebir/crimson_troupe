# 可插拔体验模块

每个 YAML 只声明本模块的挂载点、路由、依赖、信息输入、状态、产物、降级和验收；核心壳不是插件。

| 模块 | 责任 | 依赖 | 主要旅程 |
| --- | --- | --- | --- |
| troupe_information | 组织、人物、部门 | — | JRN-004、JRN-401 |
| repertoire_archive | 日历、剧目、历史演出 | — | JRN-002、003、201、203 |
| ticket_basket | 状态、席位、票篮、变更 | repertoire_archive | JRN-101、102、105 |
| ticket_game | 三幕审票与支线种子 | ticket_basket | JRN-103、104 |
| souvenir_ticket | 纪念票与打印 | ticket_basket | JRN-106 |
| archive | 藏品、探索、版本 | — | JRN-202、203、206 |
| hallucination_layer | 幻觉组合与恢复 | archive | JRN-204 |
| red_velvet_studio | 红丝绒片场 | archive | JRN-205、602 |
| timeline_archive | 剧团/世界时间线 | troupe_information | JRN-203 |
| i18n | 交付语言、泰拉语域、证据 | — | JRN-301～303 |
| join_us | 虚构试镜与舞台名 | troupe_information | JRN-401、402 |
| campaigns | 巡演季、片场周、档案夜与幕间游戏 | repertoire_archive、archive | JRN-601～603 |
| narrative_layer | 双生相、改稿、结局与全站可撤销叙事覆盖 | — | JRN-007、206、501 |

推荐按 M0 核心壳 → repertoire/troupe → ticket_basket → souvenir/archive/i18n → 深层模块安装。具体任务、路由和恢复路径见 `../03_journeys/journey_registry.yaml`。

所有 `信息输入` 必须直接指向现存的 `docs/` 文件；需要行级关联时使用目标文件中明确的自然定位字段。模块加载失败只降级自身，不能破坏导航、正常演出详情、闭幕和无 JavaScript 基线。

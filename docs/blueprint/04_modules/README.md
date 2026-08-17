# 可插拔体验模块

每个 YAML 只声明本模块的挂载点、路由、依赖、信息输入、状态、产物、降级和验收；核心壳不是插件。

各模块 YAML 中以 `/` 开头的路由均是地域配置前缀后的路径模板；只有站点根路径 `/` 用于跳转到 `/yan/`。历史网站的 `/archive/site/:terraDate/*` 是网页快照命名空间，不代表通用档案馆模块。

| 模块 | 责任 | 依赖 | 主要旅程 |
| --- | --- | --- | --- |
| troupe_information | 组织、人物、部门、剧务历史与静态“加入我们” | — | JRN-004、203、401 |
| repertoire_archive | 日历、剧目、历史演出 | — | JRN-002、003、201、203 |
| purchase_flow | 单场次分区、双币价格、购票结果、导演与最小本地状态 | repertoire_archive | JRN-101～103、105 |
| ticket_game | 购票失败后的黄牛平台支线 | purchase_flow | JRN-104 |
| souvenir_ticket | SVG/PNG 观演凭据与七段组合印章 | purchase_flow | JRN-106 |
| i18n | 地域展示配置、文本资源、货币与证据 | — | JRN-301～303 |
| narrative_layer | M3 历史网站使用的无状态异常呈现原语 | — | JRN-207 |
| historical_site | M3 旧酒神历史网站、日期路由、表里隔离与返回 | narrative_layer | JRN-207 |

批次边界固定为：M0 建立核心壳、repertoire/troupe 参考模块、炎国配置接入面和静态“加入我们”；M1 依次交付首批地域配置、purchase_flow、souvenir_ticket、演出回顾、新闻和剧务历史；M2 首先安装 ticket_game 并完成黄牛支线与七结局导演；M3 再安装 historical_site 与其无状态异常呈现层。项目不建设通用档案馆、持续活动系统或声音模块。首个多语言版本交付炎国、东国、维多利亚和哥伦比亚，后续六个计划配置按阶段人工启用。购票体验的唯一详细规则见 `01_购票体验契约.md`，具体任务、路由和恢复路径见 `../03_journeys/journey_registry.yaml`。

`内容准备依据` 只保存人工与 agent 生成、审阅模块内容时应核对的 `docs/background` 路径，不进入前端构建、模块运行或搜索。`信息输入` 才是构建期依赖，必须直接指向现存的 `docs/content` 或 `docs/blueprint` 文件。实际页面记录由构建入口选择的内容集提供；需要回溯事实时由内容记录保存来源路径和自然定位字段。两类路径都由结构契约校验，不得混用。模块加载失败只降级自身，不能破坏导航、正常演出详情、已安装模块的恢复操作和无 JavaScript 基线。

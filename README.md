# Agent Scope

![Agent Scope — Do the work. Keep it proportionate.](site/banner.svg)

**让 Agent 把工作做完。真实问题一个不漏，修法保持分寸。**

[网站](https://rikfish163-rgb.github.io/agent-scope/) · [完整提示词](RULES.md) · [安装与兼容](hosts.md) · [案例库](cases/README.md) · [English](README_EN.md)

Agent Scope 是一份跨平台的 Agent 工作约定，以及用来校准判断的公开案例库。它把范围控制、工程习惯、有效验证与交付写作放在一起：对真实问题负责，让复杂度有实际用途，并持续推进任务。

范围原则改编自 [HERO — Anti-OverDefense](https://github.com/wanshuiyin/HERO-Anti-OverDefense)，保留“约束修法，不限制发现”的边界与 MIT 许可说明。工程专题包括生成代码、实时 UI、组件故事、主题语义、接口兼容和持久化执行，均按项目条件适用。

## 开始使用

在目标项目目录运行（Git + Python 3.9+，无需额外依赖）：

```bash
git clone https://github.com/rikfish163-rgb/agent-scope.git "$HOME/.local/share/agent-scope"
python3 "$HOME/.local/share/agent-scope/install.py" --agent codex --project .
```

将 `codex` 换成 `claude`、`cursor`、`copilot`、`gemini` 或 `opencode`。安装器保留已有项目内容，重复运行更新同一个区块。`--profile core` 安装核心九条短版，`--remove` 只卸载本工具区块。

Windows PowerShell：

```powershell
git clone https://github.com/rikfish163-rgb/agent-scope.git "$env:LOCALAPPDATA\agent-scope"
py -3 "$env:LOCALAPPDATA\agent-scope\install.py" --agent codex --project .
```

[全局安装、自定义入口、Gemini 原生扩展与更新方式 →](hosts.md)

## 规则里有什么

- **发现与修法分开。** 文档、公开接口和真实数据可达的问题，即使少见也要报告；不要求先做出复现。
- **复杂度需要理由。** 摘要须替代明显更贵的操作并改变下一步；不为不存在的场景搭建包装、迁移和兼容结构。
- **判断推动行动。** 不用评分表替代判断，不为已经定论的东西重复审阅；合理方案自主选择，非阻塞细节记录后继续。
- **必要工作仍须完成。** 用户、项目和更高优先级要求的安全、迁移、校验和审阅继续执行。
- **交付只呈现最终结果。** 强结果优先、数字如实保留、限制集中说明；不写生成过程和纠偏痕迹。

| 文件 | 用途 |
| --- | --- |
| [RULES.md](RULES.md) | 完整版，保留通用工程专题与适用条件 |
| [rules/core.md](rules/core.md) | 九条核心原则与正反校准例子 |
| [install.py](install.py) / [platforms.json](platforms.json) | 六种原生文件入口与自定义 Markdown 入口 |
| [cases/catalog.json](cases/catalog.json) | 网站案例的唯一数据源 |
| [.github/ISSUE_TEMPLATE](.github/ISSUE_TEMPLATE) | Bad case / Positive case 提交表单 |
| [site](site) / [docs](docs) | 静态页面源码 / GitHub Pages 产物 |

## 两种案例都欢迎

[提交 Bad case](https://github.com/rikfish163-rgb/agent-scope/issues/new?template=bad-case.yml)：无收益校验、假设性边界、过度搭建、机械审阅或停滞。

[提交 Positive case](https://github.com/rikfish163-rgb/agent-scope/issues/new?template=positive-case.yml)：有依据的推进、确有用途的摘要、必要的安全与兼容工作、文档示例暴露的真实错误。

案例要说清任务、行为、证据和合适的下一步。当前八条种子记录是规则示例，标为 `illustrative`；经证据审阅的实测记录标为 `observed`。不虚构节省比例，也不把所有新增检查判成坏例子。[贡献指南 →](CONTRIBUTING.md)

## 本地开发

```bash
python3 -m unittest discover -s tests
node --check site/app.js
python3 scripts/build_site.py
python3 -m http.server 8000 --directory docs
```

浏览 `http://localhost:8000`。页面无需前端构建依赖；正文、案例和平台信息由 Python 标准库构建脚本写入静态页面。GitHub Pages 从 `main` 分支的 `docs/` 发布。

## 已知限制

提示词是工作约定，不保证每次执行。平台加载范围、长度限制、上下文压缩和更具体的规则会影响效果。文件适配有自动化测试；不声称已经验证所有客户端或证明模型效果。完整说明见 [兼容文档](hosts.md#已知限制)。

## 许可与来源

[MIT](LICENSE)。范围规则与校准例子改编自 HERO；版权和来源见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。本项目独立维护，与各 Agent 产品厂商无隶属关系。

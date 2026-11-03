# 🔌 安装与平台兼容

产品显示名称为 **NoOverkill**。Skill、Plugin、marketplace 和受管理文件的标识统一为 `agent-scope`，安装及调用命令使用这个标识。

## 选择入口

| 形式 | 适合什么时候 | 实际加载内容 |
| --- | --- | --- |
| 📜 规则文件 | 希望项目持续采用这份约定 | 完整提示词，或 `--profile core` 九条短版 |
| 🧩 Skill | 希望按任务调用，或让 Agent 按描述选择 | 核心原则；需要时读取随包附带的完整工程约定 |
| 📦 Plugin | 希望由 Codex / Claude Code 管理安装与更新 | 同一个 Skill，由原生插件目录分发 |

通常选一种即可。Plugin 分发 Skill，不会自动把全文写进 `AGENTS.md`。完整正文见 [RULES.md](RULES.md)，核心版见 [rules/core.md](rules/core.md)。

## 📦 原生 Plugin

仓库自带 [Codex marketplace](.agents/plugins/marketplace.json)、[Claude Code marketplace](.claude-plugin/marketplace.json) 和 [插件包](plugins/agent-scope)。两种宿主指向同一插件目录。

### Codex

在系统终端运行，可位于任意目录。需要支持 `codex plugin` 的 Codex CLI，以及 Git：

```bash
codex plugin marketplace add rikfish163-rgb/nooverkill
codex plugin add agent-scope@agent-scope
```

第一条注册这个 GitHub 仓库作为 marketplace；第二条安装其中的 `agent-scope` 插件。`@` 左边是插件名，右边是 marketplace 名，二者在这里相同。安装后新建会话，在插件或技能选择器中选择 **NoOverkill**，并说明要处理的任务。

更新 marketplace 和插件缓存后，新建会话：

```bash
codex plugin marketplace upgrade agent-scope
```

卸载插件；若也不再使用这个来源，再删除 marketplace：

```bash
codex plugin remove agent-scope@agent-scope
codex plugin marketplace remove agent-scope
```

[Codex 插件格式与管理命令](https://developers.openai.com/plugins/build/plugins)。

### Claude Code

在系统终端运行，可位于任意目录。需要支持 Plugin 的 Claude Code 和 Git：

```bash
claude plugin marketplace add rikfish163-rgb/nooverkill
claude plugin install agent-scope@agent-scope --scope user
```

`--scope user` 为当前用户安装，跨项目可用。安装后重新进入 Claude Code，在**对话输入框**中调用：

```text
/agent-scope:agent-scope 用这份约定继续当前任务。
```

这是插件技能的完整命令名；独立 Skill 对应 `/agent-scope`。若要把插件启用配置共享到某个项目，在该项目根目录运行安装命令并改用 `--scope project`。

更新后重启会话：

```bash
claude plugin marketplace update agent-scope
claude plugin update agent-scope@agent-scope --scope user
```

卸载个人安装及 marketplace：

```bash
claude plugin uninstall agent-scope@agent-scope --scope user
claude plugin marketplace remove agent-scope
```

项目安装的更新与卸载须在对应项目中执行，并使用 `--scope project`。[Claude Code marketplace](https://code.claude.com/docs/en/plugin-marketplaces) · [插件技能命名](https://code.claude.com/docs/en/plugins)。

## 📥 下载文件安装器

规则文件和独立 Skill 使用仓库内的 `install.py`，需要 Git 和 Python 3.9+，无额外 Python 依赖。此步骤只下载工具，**不会给目标项目安装任何规则**。在系统终端的任意目录运行一次。

macOS / Linux（Bash / Zsh）：

```bash
git clone https://github.com/rikfish163-rgb/nooverkill.git "$HOME/.local/share/agent-scope"
```

Windows PowerShell：

```powershell
git clone https://github.com/rikfish163-rgb/nooverkill.git "$env:LOCALAPPDATA\agent-scope"
```

已下载过就使用后面的更新命令，不必再次 clone。下面的 `/absolute/path/to/project` 或 `C:\path\to\project` 都要换成你实际要工作的项目路径；不是这个工具仓库的路径。

## 📜 安装规则文件

仍在任意目录执行。以 Codex 为例，命令会给指定项目的 `AGENTS.md` 添加受管理区块；已有项目约定保留：

```bash
python3 "$HOME/.local/share/agent-scope/install.py" --agent codex --kind rules --project "/absolute/path/to/project"
```

Windows PowerShell：

```powershell
py -3 "$env:LOCALAPPDATA\agent-scope\install.py" --agent codex --kind rules --project "C:\path\to\project"
```

将 `codex` 换成下表的平台 ID。默认安装完整正文；加 `--profile core` 只安装核心九条。已经进入目标项目目录时，可以用 `--project .`。

| ID | 项目规则文件（相对目标项目） | 个人规则文件 | 官方说明 |
| --- | --- | --- | --- |
| `codex` | `AGENTS.md` | `~/.codex/AGENTS.md`，尊重 `CODEX_HOME` | [AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md) |
| `claude` | `CLAUDE.md` | `~/.claude/CLAUDE.md` | [Memory](https://code.claude.com/docs/en/memory) |
| `cursor` | `.cursor/rules/agent-scope.mdc` | 本安装器使用项目入口 | [Rules](https://cursor.com/docs/rules) |
| `copilot` | `.github/copilot-instructions.md` | 本安装器使用项目入口 | [Custom instructions](https://docs.github.com/en/copilot/concepts/prompting-and-context/custom-instructions) |
| `gemini` | `GEMINI.md` | `~/.gemini/GEMINI.md` | [Context files](https://geminicli.com/docs/cli/gemini-md/) |
| `opencode` | `AGENTS.md` | `~/.config/opencode/AGENTS.md` | [Rules](https://opencode.ai/docs/rules/) |

Codex 与 OpenCode 共用项目 `AGENTS.md`，安装一次即可。Cursor 文件带有 `alwaysApply: true`。

个人范围用 `--global` 替代 `--project ...`；它会影响该用户后续在各项目中的会话。自定义规则文件用 `--target`：

```bash
python3 "$HOME/.local/share/agent-scope/install.py" --agent claude --kind rules --global
python3 "$HOME/.local/share/agent-scope/install.py" --agent generic --kind rules --target "/absolute/path/to/instructions.md" --profile core
```

`generic` 由使用者指定真实加载入口。Cursor 的自定义规则目标必须以 `.mdc` 结尾。安装后新建会话，或使用宿主的规则刷新功能。

## 🧩 安装独立 Skill

安装完整的 `agent-scope/` 文件夹，包含 `SKILL.md`、完整工程参考、显示信息和许可。**只复制 `SKILL.md` 会丢失参考内容。**

macOS / Linux，在任意目录执行：

```bash
python3 "$HOME/.local/share/agent-scope/install.py" --agent codex --kind skill --project "/absolute/path/to/project"
```

Windows PowerShell：

```powershell
py -3 "$env:LOCALAPPDATA\agent-scope\install.py" --agent codex --kind skill --project "C:\path\to\project"
```

将 `codex` 换成下面的平台 ID。`--global` 代替 `--project ...` 可为当前用户跨项目安装。Skill 已含核心原则和完整参考，不使用 `--profile`。

| ID | 项目 Skill 目录（相对目标项目） | 个人 Skill 目录 | 官方说明 |
| --- | --- | --- | --- |
| `codex` | `.agents/skills/agent-scope` | `~/.agents/skills/agent-scope` | [Skills](https://learn.chatgpt.com/docs/build-skills) |
| `claude` | `.claude/skills/agent-scope` | `~/.claude/skills/agent-scope` | [Skills](https://code.claude.com/docs/en/skills) |
| `cursor` | `.cursor/skills/agent-scope` | `~/.cursor/skills/agent-scope` | [Skills](https://cursor.com/docs/skills) |
| `copilot` | `.github/skills/agent-scope` | `~/.copilot/skills/agent-scope` | [Agent skills](https://docs.github.com/en/copilot/concepts/customizations/agent-skills) |
| `gemini` | `.gemini/skills/agent-scope` | `~/.gemini/skills/agent-scope` | [Agent skills](https://geminicli.com/docs/cli/skills/) |
| `opencode` | `.opencode/skills/agent-scope` | `~/.config/opencode/skills/agent-scope` | [Agent skills](https://opencode.ai/docs/skills/) |

新建会话后，在 Codex 输入 `$agent-scope`，在 Claude Code 输入 `/agent-scope`，并附上任务。其他宿主使用技能选择器，或明确说“使用 agent-scope 技能继续这个任务”。宿主也可依据技能描述自动选择它。

自定义支持 Agent Skills 的宿主可以指定完整目录，目录名须为 `agent-scope`：

```bash
python3 "$HOME/.local/share/agent-scope/install.py" --agent generic --kind skill --target "/absolute/path/to/skills/agent-scope"
```

## 🔄 文件安装的更新与卸载

先更新下载的工具仓库，再**重跑原安装命令**，保持相同的 `--agent`、`--kind` 和目标路径。规则安装还须保留原 `--profile` 选择。

macOS / Linux：

```bash
git -C "$HOME/.local/share/agent-scope" pull --ff-only
```

Windows PowerShell：

```powershell
git -C "$env:LOCALAPPDATA\agent-scope" pull --ff-only
```

卸载是在原安装命令末尾加 `--remove`。例如移除目标项目中的 Codex Skill：

```bash
python3 "$HOME/.local/share/agent-scope/install.py" --agent codex --kind skill --project "/absolute/path/to/project" --remove
```

```powershell
py -3 "$env:LOCALAPPDATA\agent-scope\install.py" --agent codex --kind skill --project "C:\path\to\project" --remove
```

卸载规则时把 `--kind skill` 改为 `--kind rules`；个人安装用 `--global` 替代项目参数。规则更新和卸载只触及 `<!-- agent-scope:start -->` 与 `<!-- agent-scope:end -->` 之间的区块。Skill 更新和卸载只处理包内文件，保留额外添加的文件。不要在受管理区块或包内文件中保存自定义约定，更新会替换它们。

给安装命令加 `--dry-run` 只显示目标位置，不写入文件。`--project`、`--global`、`--target` 三者只能选一个。

## ♊ Gemini 原生上下文扩展

若使用 Gemini 的扩展管理器，可直接加载完整规则：

```bash
gemini extensions install https://github.com/rikfish163-rgb/nooverkill
```

这个入口加载的是 `RULES.md` 上下文，与按需调用的 Skill 不同。[Gemini 扩展管理](https://geminicli.com/docs/extensions/)。

## 已知限制

- 提示词是工作约定，不能保证每次遵循。更具体的项目要求、上下文压缩、规则长度和禁用设置会影响效果。
- Plugin 包支持 Codex 与 Claude Code 的原生管理器；这是本仓库提供的 marketplace，未宣称上架宿主官方目录。其他平台使用规则文件或独立 Skill。
- 本地验证使用 Codex CLI 0.166.0 的 marketplace 发现、Claude Code 2.1.316 的包与 marketplace 验证器，以及 Skill 格式验证。自动化测试覆盖文件安装、包内容与站点数据；不代表所有客户端和模型的端到端效果测试。
- 个人 Skill 安装到本机，云端 Agent 是否同步取决于宿主与账号配置。Copilot 各客户端能力有区别；Cursor 本地个人技能不会自动提供给所有远程运行环境。
- 完整正文约 15 KiB；Codex 默认指令合并预算为 32 KiB，还会计入其他文件。容量不足可安装核心规则，或使用按需读取参考的 Skill。
- Codex 同目录 `AGENTS.override.md` 优先，安装器会提示改用 `--target`；Gemini 自定义 `context.fileName` 也可能改变规则入口。Claude Code 可用 `/memory` 查看规则来源，Gemini 可用 `/memory show` 查看、`/memory reload` 刷新。
- 文件安装支持 UTF-8 的 LF/CRLF，不转换其他编码。损坏的区块标记须先修复；同名且不属于本仓库的 Skill 或 Cursor 规则需要换位置或手动合并。

官方入口核对日期：2026-11-03。

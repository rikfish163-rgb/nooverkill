# 安装与平台兼容

完整正文在 [RULES.md](RULES.md)，核心短版在 [rules/core.md](rules/core.md)。默认安装完整版；短版保留九条原则和校准例子，省略工程专题。案例目录不写入 Agent 上下文。

## 项目安装

需要 Git 和 Python 3.9+。在目标项目目录运行；工具仓库放在个人工具目录，不混入目标项目。

macOS / Linux：

```bash
git clone https://github.com/rikfish163-rgb/agent-scope.git "$HOME/.local/share/agent-scope"
python3 "$HOME/.local/share/agent-scope/install.py" --agent codex --project .
```

Windows PowerShell：

```powershell
git clone https://github.com/rikfish163-rgb/agent-scope.git "$env:LOCALAPPDATA\agent-scope"
py -3 "$env:LOCALAPPDATA\agent-scope\install.py" --agent codex --project .
```

将 `codex` 换成表中的平台 ID。也可以把 `--project .` 换成其他项目目录。不要在工具仓库内部运行 `--project .`，除非你就是要给工具仓库安装规则。

## 平台入口

| ID | 平台 | 项目入口 | 全局入口 | 官方依据 |
| --- | --- | --- | --- | --- |
| `codex` | Codex | `AGENTS.md` | `~/.codex/AGENTS.md`，尊重 `CODEX_HOME` | [AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md) |
| `claude` | Claude Code | `CLAUDE.md` | `~/.claude/CLAUDE.md` | [Memory](https://code.claude.com/docs/en/memory) |
| `cursor` | Cursor | `.cursor/rules/agent-scope.mdc`，含 `alwaysApply: true` | 使用项目入口或手动指定文件 | [Rules](https://cursor.com/docs/rules) |
| `copilot` | GitHub Copilot | `.github/copilot-instructions.md` | 各客户端配置不同，使用项目入口 | [Custom instructions](https://docs.github.com/en/copilot/concepts/prompting-and-context/custom-instructions) |
| `gemini` | Gemini CLI | `GEMINI.md` | `~/.gemini/GEMINI.md` | [Context files](https://geminicli.com/docs/cli/gemini-md/) |
| `opencode` | OpenCode | `AGENTS.md` | `~/.config/opencode/AGENTS.md` | [Rules](https://opencode.ai/docs/rules/) |

Codex 与 OpenCode 的项目入口相同，只安装一次即可；第二次运行更新同一规则区块。Cursor 使用专用 `.mdc` 文件和原生元数据，不写旧式 `.cursorrules`。

## 全局、短版与自定义位置

支持全局文件的平台可明确指定 `--global`：

```bash
python3 /path/to/agent-scope/install.py --agent claude --global
python3 /path/to/agent-scope/install.py --agent codex --project . --profile core
python3 /path/to/agent-scope/install.py --agent generic --target /path/to/host-instructions.md
```

`generic` 是纯 Markdown 写入方式；真实加载入口由使用者指定，不代表自动验证了新宿主。自定义配置目录也可以使用 `--target`。Cursor 的自定义项目规则目标须以 `.mdc` 结尾。

先看写入位置，再决定是否安装：

```bash
python3 /path/to/agent-scope/install.py --agent codex --project . --dry-run
```

安装器只维护 `<!-- agent-scope:start -->` 与 `<!-- agent-scope:end -->` 之间的区块。已有项目文字保留；再次安装替换区块，内容相同则不写文件。它不创建后台任务，不改变模型、权限或网络设置。

## 更新和卸载

更新工具仓库后，重新运行原安装命令：

```bash
git -C "$HOME/.local/share/agent-scope" pull --ff-only
python3 "$HOME/.local/share/agent-scope/install.py" --agent codex --project .
```

Windows 对应使用 `$env:LOCALAPPDATA\agent-scope` 与 `py -3`。更新只触及本项目的标记区块。

```bash
python3 /path/to/agent-scope/install.py --agent codex --project . --remove
```

卸载保留区块外的内容；仅剩本工具内容的文件会移除。全局安装的卸载同样使用 `--global`。

## Gemini 原生扩展

仓库包含 `gemini-extension.json`，直接以 `RULES.md` 为上下文源，没有额外 MCP 服务或常驻进程：

```bash
gemini extensions install https://github.com/rikfish163-rgb/agent-scope
```

原生扩展与文件安装选一种，避免重复加载同一正文。扩展管理遵循 [Gemini 官方说明](https://geminicli.com/docs/extensions/managing-extensions/)。

## 加载检查

安装后重新启动 Agent 或使用它提供的上下文刷新方式。检查实际加载内容的目的，是发现文件位置错误、覆盖或禁用；发现后修改入口或配置，不靠重复粘贴解决。

- Codex：同目录的 `AGENTS.override.md` 优先；安装器发现它会给出 `--target` 处理提示。
- Claude Code：使用 `/memory` 查看规则来源；项目设置可排除某些来源。
- Cursor：查看规则是否为 Always Apply。
- Gemini CLI：`/memory show` 查看，`/memory reload` 刷新；自定义 `context.fileName` 会改变发现机制。
- Copilot：按实际 IDE、CLI、代码审阅或聊天入口核对官方支持矩阵。

## 已知限制

文件兼容不等于模型行为保证，也不等于已经在每个客户端完成端到端验证。本仓库测试覆盖安装器的文件操作和静态站点数据；平台加载机制以所列官方文档为依据。

完整正文约 15 KiB。Codex 默认合并预算为 32 KiB，还会计入其他指令文件；其他宿主也可能有长度或加载限制。上下文压缩、禁用规则、更具体的项目要求和冲突指令都可能影响效果。容量不足时选择核心版，或按任务保留适用的工程专题。

安装器支持常见 UTF-8 文件（LF/CRLF），不转换其他编码。手动破坏或复制管理标记后，需要先修复标记；已有同名 Cursor 专用规则且不属于本工具时，改用另一个 `.mdc` 目标或手动合并。

官方入口核对日期：2026-11-03。

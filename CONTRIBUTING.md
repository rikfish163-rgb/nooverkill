# 贡献案例与平台适配

欢迎 bad cases 和 positive cases。判断依据是项目真实需要什么、Agent 实际做了什么，以及这些动作是否推动目标。案例不是对某个模型的排名，也不要求每次审阅都找出问题。

## 提交案例

使用 [Bad case 表单](https://github.com/rikfish163-rgb/agent-scope/issues/new?template=bad-case.yml) 或 [Positive case 表单](https://github.com/rikfish163-rgb/agent-scope/issues/new?template=positive-case.yml)。给出原始任务、平台和版本、关键行为、必要证据、实际影响，以及合适的处理方式。代码或文档已经证明受支持用法可达时，不要求额外复现。

Bad case 可以是无收益摘要、假设性边界扩展、重复审阅、过度搭建、不必要停顿或交付文案问题。Positive case 可以是及时作出的合理判断，也可以是必要的校验、安全措施和兼容工作。不能因为一项工作听起来像“防御”就判它多余。

提交前删去密钥、私有客户资料和无关个人信息。保留足以理解问题的最小上下文。未测量的时间、成本和成功率不写成数据；不要把一次成功归因成已证明的普遍效果。

维护者判断证据和适用边界后，将接受的案例加入 `cases/catalog.json`。不自动把每个 Issue 当成已验证案例。现有八条标为 `illustrative`，来自规则中的校准示例；社区实测用 `observed`，并附公开来源或已脱敏的具体证据。两者在页面上明确区分。

## 提交 PR

规则正文以 `RULES.md` 为准；`rules/core.md` 是九条核心原则的短版，省略工程专题。改规则时同步检查短版是否仍表达同一边界。

平台适配写在 `platforms.json`；新增平台须提供官方规则发现机制的文档链接、文件位置和必要元数据，并给出能验证该适配的安装测试。不要因为另一个平台使用同名文件就声称已经兼容。

修改 `site/`、规则、平台或案例后重新构建静态页面：

```bash
python3 scripts/build_site.py
```

安装器修改应验证已有内容保留、重复安装、更新和卸载；页面修改应验证受影响的交互和布局。

```bash
python3 -m unittest discover -s tests
node --check site/app.js
```

`docs/` 由构建脚本从正文、案例和页面源文件生成，随 PR 一并提交。没有新变更或未解决问题时，不必重复运行已经通过的检查。

## 授权

贡献遵循仓库的 MIT 许可证。仅提交你有权公开和授权的内容。来源于其他项目的实质内容保留适用的版权和许可证说明。

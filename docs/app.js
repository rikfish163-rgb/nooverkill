'use strict';

const data = JSON.parse(document.getElementById('scope-data').textContent);
const byId = (id) => document.getElementById(id);
const repository = 'https://github.com/rikfish163-rgb/nooverkill.git';
let platform = 'codex';
let ruleProfile = 'full';
let caseFilter = 'all';
let toastTimer;

function notify(message) {
  const toast = byId('toast');
  toast.textContent = message;
  toast.hidden = false;
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => { toast.hidden = true; }, 3200);
}

async function copy(text) {
  try {
    await navigator.clipboard.writeText(text);
    notify('已复制');
  } catch {
    notify('浏览器未允许复制，请手动选中并复制文本。');
  }
}

function renderInstall() {
  const host = data.platforms[platform];
  const kindSelect = byId('install-kind');
  const supportsPlugin = platform === 'codex' || platform === 'claude';
  kindSelect.options[2].disabled = !supportsPlugin;
  if (kindSelect.value === 'plugin' && !supportsPlugin) kindSelect.value = 'skill';
  const kind = kindSelect.value;
  const isSkill = kind === 'skill';
  const isPlugin = kind === 'plugin';
  const scope = byId('install-scope');
  const globalPath = isSkill ? host.skill_global : host.global;
  scope.disabled = isPlugin;
  scope.options[1].disabled = !isPlugin && !globalPath;
  if (isPlugin) scope.value = 'global';
  else if (!globalPath) scope.value = 'project';
  const isGlobal = scope.value === 'global';
  byId('install-profile').disabled = kind !== 'rules';
  const profile = byId('install-profile').value;
  const windows = byId('install-os').value === 'windows';
  const location = isPlugin ? 'agent-scope@agent-scope' : isGlobal ? `~/${globalPath}` : isSkill ? host.skill_project : host.project;
  byId('install-target').textContent = location;
  if (isPlugin) {
    byId('platform-source').href = platform === 'codex' ? 'https://developers.openai.com/plugins/build/plugins' : 'https://code.claude.com/docs/en/plugin-marketplaces';
    byId('install-command').textContent = platform === 'codex'
      ? 'codex plugin marketplace add rikfish163-rgb/nooverkill\ncodex plugin add agent-scope@agent-scope'
      : 'claude plugin marketplace add rikfish163-rgb/nooverkill\nclaude plugin install agent-scope@agent-scope --scope user';
    byId('terminal-label').textContent = 'TERMINAL · 任意目录 · 个人插件';
    byId('platform-note').textContent = `第一条注册本仓库 marketplace，第二条安装插件。新建会话后，${platform === 'codex' ? '在插件或技能选择器中选择 NoOverkill。' : '在对话框输入 /agent-scope:agent-scope 并附上任务。'}`;
    byId('install-requirements').textContent = '需要 Git 与支持插件命令的宿主。Plugin 内含 NoOverkill Skill。';
  } else {
    const project = windows ? '"C:\\path\\to\\project"' : '"/absolute/path/to/project"';
    const args = `--agent ${platform} --kind ${kind} ${isGlobal ? '--global' : `--project ${project}`}${kind === 'rules' && profile === 'core' ? ' --profile core' : ''}`;
    const instruction = isGlobal ? '# 个人安装，跨项目可用' : '# 将目标项目路径替换为你实际工作的目录';
    byId('install-command').textContent = windows
      ? `# 下载工具一次；已下载请更新仓库\ngit clone ${repository} "$env:LOCALAPPDATA\\agent-scope"\n${instruction}\npy -3 "$env:LOCALAPPDATA\\agent-scope\\install.py" ${args}`
      : `# 下载工具一次；已下载请更新仓库\ngit clone ${repository} "$HOME/.local/share/agent-scope"\n${instruction}\npython3 "$HOME/.local/share/agent-scope/install.py" ${args}`;
    byId('terminal-label').textContent = 'TERMINAL · 任意目录';
    byId('platform-source').href = isSkill ? host.skill_source : host.source;
    const invocation = platform === 'codex' ? '输入 $agent-scope 并附上任务。' : platform === 'claude' ? '输入 /agent-scope 并附上任务。' : '在技能选择器中选择 NoOverkill，或明确让 Agent 使用 agent-scope 技能。';
    byId('platform-note').textContent = isSkill ? `安装完整技能目录，含核心原则及按需读取的工程参考。新建会话后${invocation}` : host.note;
    byId('install-requirements').textContent = '需要 Git 与 Python 3.9+。工具下载目录与目标项目是两个目录。';
  }
  document.querySelectorAll('[data-platform]').forEach((button) => {
    const selected = button.dataset.platform === platform;
    button.setAttribute('aria-selected', String(selected));
    button.tabIndex = selected ? 0 : -1;
  });
  const panel = document.querySelector('.install-body');
  panel.setAttribute('role', 'tabpanel');
  panel.setAttribute('aria-labelledby', `platform-${platform}`);
}

Object.entries(data.platforms).forEach(([id, host]) => {
  const button = document.createElement('button');
  button.type = 'button';
  button.id = `platform-${id}`;
  button.dataset.platform = id;
  button.setAttribute('role', 'tab');
  button.setAttribute('aria-controls', 'install-content');
  button.textContent = host.name;
  button.addEventListener('click', () => { platform = id; renderInstall(); });
  button.addEventListener('keydown', (event) => {
    const keys = Object.keys(data.platforms);
    const index = keys.indexOf(platform);
    const next = {ArrowRight: (index + 1) % keys.length, ArrowLeft: (index + keys.length - 1) % keys.length, Home: 0, End: keys.length - 1}[event.key];
    if (next === undefined) return;
    event.preventDefault();
    platform = keys[next];
    renderInstall();
    byId(`platform-${platform}`).focus();
  });
  byId('platform-tabs').append(button);
});
document.querySelector('.install-body').id = 'install-content';
['install-kind', 'install-scope', 'install-profile', 'install-os'].forEach((id) => byId(id).addEventListener('change', renderInstall));
byId('copy-install').addEventListener('click', () => copy(byId('install-command').textContent));

function renderRules() {
  const text = data.rules[ruleProfile];
  byId('rule-text').textContent = text;
  byId('rule-text').scrollTop = 0;
  byId('rule-size').textContent = `${(new TextEncoder().encode(text).length / 1024).toFixed(1)} KiB`;
  byId('download-rules').href = ruleProfile === 'full' ? 'RULES.md' : 'CORE.md';
  document.querySelectorAll('[data-profile]').forEach((button) => button.setAttribute('aria-pressed', String(button.dataset.profile === ruleProfile)));
}
document.querySelectorAll('[data-profile]').forEach((button) => button.addEventListener('click', () => { ruleProfile = button.dataset.profile; renderRules(); }));
byId('copy-rules').addEventListener('click', () => copy(data.rules[ruleProfile]));

function element(tag, text, className) {
  const node = document.createElement(tag);
  if (text) node.textContent = text;
  if (className) node.className = className;
  return node;
}

function renderCases() {
  const query = byId('case-search').value.trim().toLocaleLowerCase();
  const cases = data.cases.filter((item) => (caseFilter === 'all' || item.kind === caseFilter) && [item.id, item.title, item.family, item.task, item.behavior, item.reason, item.action].join(' ').toLocaleLowerCase().includes(query));
  byId('case-grid').replaceChildren();
  cases.forEach((item) => {
    const card = element('article', '', 'case-card');
    card.id = `case-${item.id}`;
    const top = element('div', '', 'case-top');
    top.append(element('span', item.kind === 'bad' ? 'BAD CASE' : 'POSITIVE CASE', `case-tag ${item.kind}`), element('span', item.id, 'case-id'));
    card.append(top, element('h3', item.title), element('p', item.reason, 'case-summary'), element('p', item.family, 'case-family'));
    const details = element('details');
    details.append(element('summary', '展开任务、行为与下一步'));
    const definition = element('dl');
    [['任务', item.task], ['实际行为', item.behavior], ['合适的动作', item.action]].forEach(([label, text]) => definition.append(element('dt', label), element('dd', text)));
    const evidence = element('p', item.evidence === 'illustrative' ? '规则示例 · ' : '实际报告 · ', 'evidence');
    const source = element('a', item.source_label);
    source.href = item.source;
    evidence.append(source);
    details.append(definition, evidence);
    card.append(details);
    byId('case-grid').append(card);
  });
  byId('case-empty').hidden = cases.length > 0;
  document.querySelectorAll('[data-filter]').forEach((button) => {
    button.setAttribute('aria-pressed', String(button.dataset.filter === caseFilter));
    button.querySelector('span').textContent = data.cases.filter((item) => button.dataset.filter === 'all' || item.kind === button.dataset.filter).length;
  });
}
document.querySelectorAll('[data-filter]').forEach((button) => button.addEventListener('click', () => { caseFilter = button.dataset.filter; renderCases(); }));
byId('case-search').addEventListener('input', renderCases);

const sections = document.querySelectorAll('.section-anchor');
const observer = new IntersectionObserver((entries) => {
  const current = entries.find((entry) => entry.isIntersecting);
  if (!current) return;
  document.querySelectorAll('.nav-link').forEach((link) => {
    const active = link.hash === `#${current.target.id}`;
    link.classList.toggle('active', active);
    if (active) link.setAttribute('aria-current', 'location');
    else link.removeAttribute('aria-current');
  });
}, {rootMargin: '-10% 0px -65% 0px'});
sections.forEach((section) => observer.observe(section));
document.querySelectorAll('.facts-strip strong')[0].textContent = String(Object.keys(data.platforms).length).padStart(2, '0');
document.querySelectorAll('.facts-strip strong')[2].textContent = String(data.cases.length).padStart(2, '0');
renderInstall();
renderRules();
renderCases();

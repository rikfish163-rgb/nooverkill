'use strict';

const data = JSON.parse(document.getElementById('scope-data').textContent);
const byId = (id) => document.getElementById(id);
const repository = 'https://github.com/rikfish163-rgb/agent-scope.git';
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
  const scope = byId('install-scope');
  scope.options[1].disabled = !host.global;
  if (!host.global) scope.value = 'project';
  const isGlobal = scope.value === 'global';
  const profile = byId('install-profile').value;
  const windows = byId('install-os').value === 'windows';
  const location = isGlobal ? `~/${host.global}` : host.project;
  byId('install-target').textContent = location;
  byId('platform-source').href = host.source;
  byId('platform-note').textContent = host.note;
  byId('terminal-label').textContent = isGlobal ? 'TERMINAL · 个人全局规则' : 'TERMINAL · 在目标项目目录运行';
  const args = `--agent ${platform} ${isGlobal ? '--global' : '--project .'}${profile === 'core' ? ' --profile core' : ''}`;
  byId('install-command').textContent = windows
    ? `git clone ${repository} "$env:LOCALAPPDATA\\agent-scope"\npy -3 "$env:LOCALAPPDATA\\agent-scope\\install.py" ${args}`
    : `git clone ${repository} "$HOME/.local/share/agent-scope"\npython3 "$HOME/.local/share/agent-scope/install.py" ${args}`;
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
['install-scope', 'install-profile', 'install-os'].forEach((id) => byId(id).addEventListener('change', renderInstall));
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

'use strict';

document.querySelectorAll('[data-copy]').forEach((button) => {
  const label = button.textContent;
  button.addEventListener('click', async () => {
    try {
      await navigator.clipboard.writeText(document.getElementById(button.dataset.copy).textContent);
      document.getElementById('copy-status').textContent = 'Copied to clipboard.';
      button.textContent = 'Copied';
      setTimeout(() => { button.textContent = label; }, 2000);
    } catch {
      document.getElementById('copy-status').textContent = 'Clipboard access is unavailable. Select and copy the text.';
    }
  });
});

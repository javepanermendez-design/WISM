export class ShortcutManager {
  constructor(searchModal) { this.searchModal = searchModal; }
  bind() { document.addEventListener('keydown', event => { if ((event.ctrlKey || event.metaKey) && event.key.toLowerCase() === 'k') { event.preventDefault(); if (this.searchModal) bootstrap.Modal.getOrCreateInstance(this.searchModal).show(); } if (event.key.toLowerCase() === 'n' && document.activeElement.tagName !== 'INPUT') { const link = document.querySelector('a[href$="/new"]'); if (link) window.location.href = link.href; } }); }
}

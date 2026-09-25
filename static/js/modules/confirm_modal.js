export class ConfirmModal {
  constructor(selector = '#signOutModal') { this.modal = document.querySelector(selector); }
  bind() { this.modal?.querySelector('.btn-primary')?.addEventListener('click', () => { if (this.modal.id === 'signOutModal') window.location.href = '/logout'; }); }
}

export class ToastManager {
  constructor(region = document.querySelector('#toastRegion')) { this.region = region; }
  show(message, tone = 'success') {
    if (!this.region) return;
    const match = message.match(/^(.*?)::undo=(\S+)$/);
    const text = match ? match[1] : message;
    const toast = document.createElement('div');
    toast.className = `toast app-toast text-bg-${tone} show`;
    toast.innerHTML = `<i class="bi bi-check-circle-fill"></i><span>${text}</span>${match ? '<button class="btn btn-sm btn-light">Undo</button>' : ''}`;
    this.region.appendChild(toast);
    if (match) toast.querySelector('button').addEventListener('click', async () => { await fetch(match[2], { method: 'POST', headers: { 'X-Requested-With': 'fetch' } }); window.location.reload(); });
    setTimeout(() => toast.remove(), match ? 8000 : 4200);
  }
}

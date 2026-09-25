export class UndoManager {
  constructor(toasts) { this.toasts = toasts; }
  offer(message, undo) { this.toasts.show(`${message} <button class="btn btn-sm btn-light ms-2">Undo</button>`); document.querySelector('#toastRegion button')?.addEventListener('click', undo, { once: true }); }
}

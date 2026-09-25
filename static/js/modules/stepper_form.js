export class StepperForm {
  constructor(root = document) { this.root = root; }
  bind() { this.root.querySelectorAll('[data-step-next]').forEach(button => button.addEventListener('click', () => { const current = button.closest('[data-step]'); current?.classList.remove('active'); current?.nextElementSibling?.classList.add('active'); })); }
}

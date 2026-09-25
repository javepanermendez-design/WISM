export class TableSearch {
  constructor(input, rows) { this.input = input; this.rows = rows; }
  bind() { this.input?.addEventListener('input', () => { const query = this.input.value.toLowerCase(); this.rows.forEach(row => { row.hidden = !row.textContent.toLowerCase().includes(query); }); }); }
}

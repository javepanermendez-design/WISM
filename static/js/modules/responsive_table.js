export class ResponsiveTable {
  constructor(table) {
    this.table = table;
    this.mobileMedia = window.matchMedia('(max-width: 767.98px)');
    this.cardList = null;
    this.sortSelect = null;
  }

  bind() {
    if (!this.table) return;
    this.table.setAttribute('data-responsive-table', 'true');
    this.sync();
    window.addEventListener('resize', () => this.sync());
  }

  sync() {
    if (!this.table) return;
    if (this.mobileMedia.matches) {
      this.enableMobileCards();
    } else {
      this.disableMobileCards();
    }
  }

  enableMobileCards() {
    if (this.table.dataset.mobileEnabled === 'true') return;
    const tableWrap = this.table.parentElement;
    if (!tableWrap || !this.table.querySelector('tbody')) return;

    this.table.dataset.mobileEnabled = 'true';
    this.table.style.display = 'none';

    this.cardList = document.createElement('div');
    this.cardList.className = 'responsive-card-list';
    this.cardList.setAttribute('aria-live', 'polite');

    this.sortSelect = document.createElement('label');
    this.sortSelect.className = 'responsive-table-sort';

    const headers = [...this.table.querySelectorAll('thead th')].map(th => th.textContent.trim());
    const sortOptions = headers.slice(0, -1).map((label, index) => `<option value="${index + 1}">${label}</option>`).join('');
    this.sortSelect.innerHTML = `<span>Sort by</span><select aria-label="Sort table by column"><option value="0">Default</option>${sortOptions}</select>`;
    const select = this.sortSelect.querySelector('select');
    select.addEventListener('change', event => this.sortRows(Number(event.target.value)));

    tableWrap.insertBefore(this.sortSelect, this.table);
    tableWrap.insertBefore(this.cardList, this.table.nextSibling);
    this.renderCards();
  }

  disableMobileCards() {
    if (this.table.dataset.mobileEnabled !== 'true') return;
    this.table.dataset.mobileEnabled = 'false';
    this.table.style.display = '';
    this.sortSelect?.remove();
    this.cardList?.remove();
    this.cardList = null;
    this.sortSelect = null;
  }

  sortRows(index) {
    const tbody = this.table.querySelector('tbody');
    if (!tbody) return;

    const rows = [...tbody.querySelectorAll('tr')].filter(row => row.querySelector('td'));
    if (!rows.length) return;

    if (!index) {
      rows.forEach(row => tbody.appendChild(row));
      this.renderCards();
      return;
    }

    const target = index - 1;
    rows.sort((a, b) => {
      const left = (a.cells[target]?.textContent || '').replace(/\s+/g, ' ').trim().toLowerCase();
      const right = (b.cells[target]?.textContent || '').replace(/\s+/g, ' ').trim().toLowerCase();
      const numeric = !Number.isNaN(Number(left)) && !Number.isNaN(Number(right));
      if (numeric) return Number(left) - Number(right);
      return left.localeCompare(right);
    });

    rows.forEach(row => tbody.appendChild(row));
    this.renderCards();
  }

  renderCards() {
    if (!this.cardList) return;
    const tbody = this.table.querySelector('tbody');
    const headerCells = [...this.table.querySelectorAll('thead th')];
    const rows = [...tbody?.querySelectorAll('tr') || []].filter(row => row.querySelector('td'));

    this.cardList.innerHTML = rows.map((row, rowIndex) => {
      const cells = [...row.cells];
      const titleCell = cells[0] || document.createElement('td');
      const actionCell = cells.at(-1) && cells.at(-1).querySelector('.dropdown') ? cells.at(-1) : null;
      const summaryCells = [];
      const extraCells = [];

      cells.forEach((cell, index) => {
        if (index === 0 || (actionCell && cell === actionCell)) return;
        const key = (headerCells[index]?.textContent || `Field ${index + 1}`).replace(/\s+/g, ' ').trim();
        const field = document.createElement('div');
        field.className = 'responsive-field';
        field.innerHTML = `<span class="responsive-label">${key}</span><div class="responsive-value">${cell.innerHTML}</div>`;
        if (index < 4) summaryCells.push(field.outerHTML); else extraCells.push(field.outerHTML);
      });

      const statusBadge = row.querySelector('.status')?.outerHTML || '';
      const titleHtml = titleCell.innerHTML || `<strong>Row ${rowIndex + 1}</strong>`;
      const toggle = extraCells.length ? `<button class="responsive-more-toggle" type="button" aria-expanded="false">Show more</button>` : '';
      const details = extraCells.length ? `<div class="responsive-details">${extraCells.join('')}</div>` : '';

      return `
        <article class="responsive-card-item">
          <div class="responsive-card-header">
            <div class="responsive-card-title">${titleHtml}</div>
            ${statusBadge ? `<div class="responsive-card-status">${statusBadge}</div>` : ''}
          </div>
          <div class="responsive-card-body">
            ${summaryCells.join('')}
            ${details}
          </div>
          ${toggle}
        </article>
      `;
    }).join('') || '<div class="responsive-card-empty">No records to display.</div>';

    this.cardList.querySelectorAll('.responsive-more-toggle').forEach(button => {
      button.addEventListener('click', () => {
        const card = button.closest('.responsive-card-item');
        const details = card?.querySelector('.responsive-details');
        const open = button.getAttribute('aria-expanded') === 'true';
        button.setAttribute('aria-expanded', String(!open));
        button.textContent = open ? 'Show more' : 'Show less';
        details?.classList.toggle('open', !open);
      });
    });
  }
}

const moduleNames = ['toast_manager', 'confirm_modal', 'undo_manager', 'stepper_form', 'table_search', 'responsive_table', 'shortcut_manager'];
Promise.all(moduleNames.map(name => import(`/static/js/modules/${name}.js`))).then(([toast, confirm, undo, stepper, search, responsive, shortcuts]) => {
  const toasts = new toast.ToastManager();
  new confirm.ConfirmModal().bind();
  new undo.UndoManager(toasts);
  new stepper.StepperForm().bind();
  document.querySelectorAll('table').forEach(table => new responsive.ResponsiveTable(table).bind());
  document.querySelectorAll('.filter-bar .input-icon input').forEach(input => new search.TableSearch(input, [...document.querySelectorAll('tbody tr')]).bind());
  new shortcuts.ShortcutManager(document.querySelector('#searchModal')).bind();
  document.querySelectorAll('[data-toast]').forEach(element => element.addEventListener('click', () => toasts.show(element.dataset.toast)));
  document.querySelectorAll('a[href="#"]').forEach(link => link.addEventListener('click', event => { event.preventDefault(); toasts.show(link.dataset.toast || 'This action is not available in the prototype.'); }));
  document.querySelectorAll('[data-toast-message]').forEach(element => toasts.show(element.dataset.toastMessage, element.dataset.toastTone === 'danger' ? 'danger' : 'success'));
  document.querySelector('.row-flash')?.scrollIntoView({ behavior: 'smooth', block: 'center' });
  document.querySelectorAll('.password-toggle').forEach(button => button.addEventListener('click', () => { const input = button.parentElement.querySelector('input'); const visible = input.type === 'text'; input.type = visible ? 'password' : 'text'; button.innerHTML = `<i class="bi bi-eye${visible ? '' : '-slash'}"></i>`; }));
  const password = document.querySelector('#password'); const caps = document.querySelector('#capsWarning'); password?.addEventListener('keyup', event => { if (caps) caps.style.display = event.getModifierState('CapsLock') ? 'block' : 'none'; });
  document.querySelectorAll('[data-count]').forEach(element => { const target = Number(element.dataset.count); let value = 0; const tick = () => { value = Math.min(target, value + Math.max(1, Math.ceil(target / 18))); element.textContent = value; if (value < target) requestAnimationFrame(tick); }; setTimeout(tick, 180); });

  const closeSidebar = () => {
    document.querySelector('.sidebar')?.classList.remove('open');
    document.querySelector('.sidebar-backdrop')?.classList.remove('is-visible');
  };

  document.querySelector('.mobile-menu')?.addEventListener('click', () => {
    const sidebar = document.querySelector('.sidebar');
    const backdrop = document.querySelector('.sidebar-backdrop');
    const open = sidebar?.classList.toggle('open');
    backdrop?.classList.toggle('is-visible', Boolean(open));
  });

  document.querySelector('.sidebar-backdrop')?.addEventListener('click', closeSidebar);
  document.querySelectorAll('.sidebar a').forEach(link => link.addEventListener('click', closeSidebar));

  document.querySelectorAll('.mobile-search-trigger').forEach(button => {
    button.addEventListener('click', () => {
      const shell = button.closest('.mobile-search-shell');
      const isOpen = shell.classList.toggle('open');
      button.setAttribute('aria-expanded', String(isOpen));
      if (isOpen) shell.querySelector('input')?.focus();
    });
  });

  const kpiGrid = document.querySelector('.kpi-grid');
  if (kpiGrid) {
    const cards = [...kpiGrid.querySelectorAll('.kpi-card')];
    const dots = document.createElement('div');
    dots.className = 'kpi-scroll-dots';
    cards.forEach((_, index) => {
      const dot = document.createElement('button');
      dot.type = 'button';
      dot.className = 'kpi-scroll-dot';
      dot.setAttribute('aria-label', `Go to KPI ${index + 1}`);
      dot.addEventListener('click', () => {
        cards[index]?.scrollIntoView({ behavior: 'smooth', inline: 'start', block: 'nearest' });
      });
      dots.appendChild(dot);
    });
    kpiGrid.insertAdjacentElement('afterend', dots);

    const syncKpiDots = () => {
      const maxIndex = Math.max(cards.length - 1, 0);
      const ratio = cards.length <= 1 ? 0 : (kpiGrid.scrollLeft / Math.max(1, kpiGrid.scrollWidth - kpiGrid.clientWidth));
      const currentIndex = Math.min(maxIndex, Math.max(0, Math.round(ratio * maxIndex)));
      [...dots.children].forEach((dot, index) => dot.classList.toggle('active', index === currentIndex));
    };

    syncKpiDots();
    kpiGrid.addEventListener('scroll', syncKpiDots, { passive: true });
    window.addEventListener('resize', syncKpiDots);
  }

  document.addEventListener('click', event => {
    const shell = event.target.closest('.mobile-search-shell');
    if (!shell) {
      document.querySelectorAll('.mobile-search-shell').forEach(item => {
        item.classList.remove('open');
        item.querySelector('.mobile-search-trigger')?.setAttribute('aria-expanded', 'false');
      });
    }
  });

  document.querySelectorAll('.filter-bar').forEach(bar => {
    if (bar.querySelector('.filter-sheet-toggle')) return;
    const toggle = document.createElement('button');
    toggle.type = 'button';
    toggle.className = 'filter-sheet-toggle';
    toggle.innerHTML = '<i class="bi bi-funnel"></i><span>Filters</span>';
    toggle.setAttribute('aria-expanded', 'false');
    toggle.addEventListener('click', () => {
      const open = bar.classList.toggle('is-open');
      toggle.setAttribute('aria-expanded', String(open));
    });
    bar.appendChild(toggle);
  });

  document.querySelectorAll('.zone-block').forEach(zone => {
    zone.addEventListener('click', event => {
      if (window.matchMedia('(max-width: 767.98px)').matches) {
        event.preventDefault();
        const sheet = document.querySelector('#zoneDetailSheet') || document.createElement('div');
        if (!sheet.id) {
          sheet.id = 'zoneDetailSheet';
          sheet.className = 'mobile-sheet';
          document.body.appendChild(sheet);
        }

        const title = zone.getAttribute('title') || zone.dataset.title || 'Zone details';
        const content = zone.dataset.details || zone.querySelector('small')?.textContent || 'Inventory details for this zone.';
        sheet.innerHTML = `
          <div class="mobile-sheet-backdrop"></div>
          <div class="mobile-sheet-panel">
            <div class="mobile-sheet-header">
              <button type="button" class="btn-icon sheet-close" aria-label="Close zone details"><i class="bi bi-x-lg"></i></button>
              <h3>${title}</h3>
            </div>
            <div class="mobile-sheet-body">
              <p>${content}</p>
              <a href="${zone.getAttribute('href') || '#'}" class="btn btn-primary w-100">Open inventory</a>
            </div>
          </div>
        `;
        sheet.classList.add('open');
        sheet.querySelector('.sheet-close')?.addEventListener('click', () => sheet.classList.remove('open'));
        sheet.querySelector('.mobile-sheet-backdrop')?.addEventListener('click', () => sheet.classList.remove('open'));
      }
    });
  });

  document.querySelectorAll('input:not([type]), input[type="text"], input[type="email"], input[type="password"]').forEach(input => {
    const fieldName = (input.name || input.id || '').toLowerCase();
    if (fieldName.includes('date') || fieldName.includes('expiry') || fieldName.includes('arrival') || fieldName.includes('created') || fieldName.includes('received') && fieldName.includes('date')) {
      input.type = 'date';
    } else if (/(qty|quantity|count|reorder|stock|min_stock|max_stock|received|expected|price|cost|amount)/.test(fieldName)) {
      input.type = 'number';
      input.inputMode = 'numeric';
    }
  });

  document.querySelectorAll('form').forEach(form => {
    if (form.dataset.stickyActionsReady || form.closest('.auth-panel') || form.closest('.login-shell') || form.closest('.modal')) return;

    const hasExplicitActionRow = form.querySelector('.form-actions, [class*="justify-content-end"][class*="gap-2"], [class*="form-actions"]');
    if (hasExplicitActionRow) return;

    const primary = form.querySelector('button[type="submit"], input[type="submit"]');
    if (!primary) return;
    const placeholder = document.createElement('div');
    placeholder.className = 'sticky-form-actions';
    const cancel = document.createElement('button');
    cancel.type = 'button';
    cancel.className = 'btn btn-quiet';
    cancel.textContent = 'Cancel';
    cancel.addEventListener('click', () => {
      if (document.referrer) {
        window.history.back();
      } else {
        window.location.href = '/';
      }
    });
    const wrap = document.createElement('div');
    wrap.className = 'sticky-form-primary';
    wrap.appendChild(primary);
    placeholder.append(cancel, wrap);
    form.appendChild(placeholder);
    form.dataset.stickyActionsReady = 'true';
  });

  document.querySelectorAll('.modal form textarea[name="reason"]').forEach(textarea => {
    const form = textarea.closest('form');
    const submit = form?.querySelector('button[type="submit"]');
    const hint = form?.querySelector('.field-hint');
    if (!form || !submit || !hint) return;

    const sync = (showHint = false) => {
      const hasText = textarea.value.trim().length > 0;
      submit.disabled = !hasText;
      submit.setAttribute('aria-disabled', String(!hasText));
      hint.hidden = !(showHint && !hasText);
    };

    textarea.addEventListener('input', () => sync(false));
    submit.addEventListener('click', event => {
      if (!textarea.value.trim()) {
        event.preventDefault();
        sync(true);
        textarea.focus();
      }
    });
    sync(false);
  });

  document.querySelectorAll('form').forEach(form => form.addEventListener('submit', () => { const button = form.querySelector('button[type="submit"]'); if (button && !button.dataset.keepLabel) { button.disabled = true; button.innerHTML = '<span class="spinner-border spinner-border-sm"></span>Saving...'; } }));
});

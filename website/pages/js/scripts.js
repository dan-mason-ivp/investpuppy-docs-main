/* ============================================================
   InvestPuppy — Site JavaScript
   ============================================================ */

document.addEventListener('DOMContentLoaded', function () {

  /* ── Mobile nav toggle ──────────────────────────────────── */
  const toggle = document.querySelector('.navbar__toggle');
  const links  = document.querySelector('.navbar__links');
  if (toggle && links) {
    toggle.addEventListener('click', () => links.classList.toggle('open'));
  }

  /* ── Accordion ──────────────────────────────────────────── */
  document.querySelectorAll('.accordion__header').forEach(header => {
    header.addEventListener('click', () => {
      const item = header.closest('.accordion__item');
      const isOpen = item.classList.contains('open');
      // Close all
      document.querySelectorAll('.accordion__item').forEach(i => i.classList.remove('open'));
      // Open clicked (unless it was already open)
      if (!isOpen) item.classList.add('open');
    });
  });

  /* ── Document tabs ──────────────────────────────────────── */
  document.querySelectorAll('.doc-tab').forEach(tab => {
    tab.addEventListener('click', () => {
      const target = tab.dataset.tab;
      document.querySelectorAll('.doc-tab').forEach(t => t.classList.remove('active'));
      document.querySelectorAll('.doc-panel').forEach(p => p.classList.remove('active'));
      tab.classList.add('active');
      const panel = document.getElementById(target);
      if (panel) panel.classList.add('active');
    });
  });

  /* ── Netlify form success handling ─────────────────────── */
  // Show success message after Netlify processes form
  const params = new URLSearchParams(window.location.search);
  if (params.get('success') === 'true') {
    const success = document.querySelector('.form-success');
    if (success) {
      success.style.display = 'block';
      success.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
  }

});

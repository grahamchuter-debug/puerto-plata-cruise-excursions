/**
 * Loads shared layout partials when not already inlined.
 * data-static="1" means nav/hero/content/footer are server-visible — no fetch.
 */
(function () {
  function basePath() {
    const base = document.body.dataset.base;
    if (base === undefined || base === '') return '';
    return base.endsWith('/') ? base : base + '/';
  }

  async function loadInto(id, url) {
    const el = document.getElementById(id);
    if (!el || !url) return;

    try {
      const res = await fetch(basePath() + url);
      if (!res.ok) throw new Error(res.statusText);
      el.innerHTML = await res.text();
    } catch (err) {
      console.error('Layout load failed:', url, err);
      el.innerHTML =
        '<p class="p-4 text-sm text-red-700 bg-red-50 border border-red-200 rounded-lg">Could not load ' +
        url +
        '. Run the site with a local server, e.g. <code class="text-xs">python3 -m http.server</code>.</p>';
    }
  }

  function setActiveNav() {
    const page = document.body.dataset.page;
    if (!page) return;

    document.querySelectorAll('[data-nav]').forEach(function (link) {
      const isActive = link.dataset.nav === page;
      link.classList.toggle('text-ocean-600', isActive);
      link.classList.toggle('font-semibold', isActive);
      link.classList.toggle('text-gray-600', !isActive);
      if (isActive) link.setAttribute('aria-current', 'page');
    });
  }

  function bindMobileMenu() {
    const toggle = document.getElementById('menu-toggle');
    const menu = document.getElementById('mobile-menu');
    if (!toggle || !menu) return;
    toggle.addEventListener('click', function () {
      const open = menu.classList.toggle('hidden') === false;
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }

  document.addEventListener('DOMContentLoaded', async function () {
    if (document.body.dataset.static === '1') {
      setActiveNav();
      bindMobileMenu();
      return;
    }

    const hero = document.body.dataset.hero;
    const content = document.body.dataset.content;
    const trustStrip = document.body.dataset.trustStrip;

    await Promise.all([
      loadInto('site-nav', 'partials/nav.html'),
      loadInto('site-footer', 'partials/footer.html'),
      loadInto('page-hero', hero),
      loadInto('page-trust-strip', trustStrip),
      loadInto('page-content', content),
    ]);

    setActiveNav();
    bindMobileMenu();
  });
})();

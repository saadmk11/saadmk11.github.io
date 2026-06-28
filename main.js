// ---------------------------------------------------------------------------
// Dark Mode Logic
// ---------------------------------------------------------------------------
const themeToggleBtn = document.getElementById('theme-toggle');
const darkIcon = document.getElementById('theme-toggle-dark-icon');
const lightIcon = document.getElementById('theme-toggle-light-icon');

// The `dark` class is set in <head> before paint to avoid a flash.
// Here we only sync which toggle icon is shown.
function syncThemeIcon() {
    if (document.documentElement.classList.contains('dark')) {
        darkIcon.classList.add('hidden');
        lightIcon.classList.remove('hidden');
    } else {
        lightIcon.classList.add('hidden');
        darkIcon.classList.remove('hidden');
    }
}
syncThemeIcon();

themeToggleBtn.addEventListener('click', function () {
    const isDark = document.documentElement.classList.toggle('dark');
    localStorage.setItem('color-theme', isDark ? 'dark' : 'light');
    syncThemeIcon();
});

// ---------------------------------------------------------------------------
// Fetch and Render Repositories
// ---------------------------------------------------------------------------
function getJSON(url, callbackFunction) {
    const xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function () {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
            try {
                const responseData = JSON.parse(xmlhttp.responseText);
                callbackFunction(responseData);
            } catch (error) {
                console.error('Error parsing JSON:', error);
                return;
            }
        }
    };
    xmlhttp.open('GET', url, true);
    xmlhttp.send();
}

// Map a language to a colored badge (Tailwind classes).
function languageBadge(language) {
    switch (language) {
        case 'Python':
            return 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200';
        case 'JavaScript':
            return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200';
        case 'Rust':
            return 'bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-200';
        case 'TypeScript':
            return 'bg-sky-100 text-sky-800 dark:bg-sky-900 dark:text-sky-200';
        default:
            return 'bg-slate-100 text-slate-700 dark:bg-slate-700 dark:text-slate-200';
    }
}

function renderRepositories(data) {
    const container = document.getElementById('openSourceRepos');
    if (!container) return;
    container.innerHTML = '';

    data.forEach(function (repo) {
        const name = repo.full_name.split('/')[1] || repo.full_name;
        const badge = languageBadge(repo.main_programing_language);

        const child = `
            <div class="group flex h-full flex-col rounded-xl border border-slate-200 bg-slate-50 p-3.5 transition-all hover:border-blue-300 hover:shadow-md dark:border-slate-700 dark:bg-slate-800/40 dark:hover:border-blue-800">
                <div class="mb-1.5 flex items-center justify-between gap-2">
                    <h3 class="min-w-0 text-sm font-bold text-slate-900 dark:text-white">
                        <a href="${repo.url}" target="_blank" rel="noopener noreferrer" class="flex items-center gap-1.5 hover:text-blue-600 dark:hover:text-blue-400">
                            <i class="fas fa-book text-xs text-blue-500"></i>
                            <span class="truncate">${name}</span>
                        </a>
                    </h3>
                    <span class="shrink-0 rounded-full px-2 py-0.5 text-[10px] font-medium ${badge}">
                        ${repo.main_programing_language}
                    </span>
                </div>
                <p class="mb-2.5 line-clamp-2 text-[13px] leading-snug text-slate-600 dark:text-slate-300">
                    ${repo.short_description || ''}
                </p>
                <div class="mt-auto flex items-center gap-3 text-xs text-slate-500 dark:text-slate-400">
                    <span class="flex items-center gap-1"><i class="fas fa-star text-yellow-400"></i> ${repo.stars}</span>
                    <span class="flex items-center gap-1"><i class="fas fa-code-branch text-green-500"></i> ${repo.forks}</span>
                    <span class="flex items-center gap-1"><i class="far fa-eye text-blue-400"></i> ${repo.watchers}</span>
                </div>
            </div>
        `;
        container.insertAdjacentHTML('beforeend', child);
    });
}

// ---------------------------------------------------------------------------
// Scroll-reveal animations (progressive enhancement)
// ---------------------------------------------------------------------------
function initReveal() {
    const revealEls = document.querySelectorAll('.reveal');
    if (!('IntersectionObserver' in window)) {
        revealEls.forEach((el) => el.classList.add('is-visible'));
        return;
    }
    const observer = new IntersectionObserver(
        function (entries, obs) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting) {
                    entry.target.classList.add('is-visible');
                    obs.unobserve(entry.target);
                }
            });
        },
        { rootMargin: '0px 0px -10% 0px', threshold: 0.05 }
    );
    revealEls.forEach((el) => observer.observe(el));
}

// ---------------------------------------------------------------------------
// Navbar scroll-spy (highlights the active section link)
// ---------------------------------------------------------------------------
function initScrollSpy() {
    const navLinks = Array.from(document.querySelectorAll('[data-nav]'));
    if (!navLinks.length || !('IntersectionObserver' in window)) return;

    const sections = navLinks
        .map((link) => document.querySelector(link.getAttribute('href')))
        .filter(Boolean);

    const observer = new IntersectionObserver(
        function (entries) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting) {
                    const id = '#' + entry.target.id;
                    navLinks.forEach((link) =>
                        link.classList.toggle('is-active', link.getAttribute('href') === id)
                    );
                }
            });
        },
        { rootMargin: '-45% 0px -50% 0px', threshold: 0 }
    );
    sections.forEach((section) => observer.observe(section));
}

// ---------------------------------------------------------------------------
// Init
// ---------------------------------------------------------------------------
document.addEventListener('DOMContentLoaded', function () {
    getJSON('repo_data.json', renderRepositories);
    initReveal();
    initScrollSpy();
});

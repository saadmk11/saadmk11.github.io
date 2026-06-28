// Dark mode toggle. The `dark` class is applied in <head> before paint (to avoid
// a flash), so here we only sync the icon and remember the choice.
const themeToggleBtn = document.getElementById("theme-toggle");
const darkIcon = document.getElementById("theme-toggle-dark-icon");
const lightIcon = document.getElementById("theme-toggle-light-icon");

function syncThemeIcon() {
    const isDark = document.documentElement.classList.contains("dark");
    darkIcon.classList.toggle("hidden", isDark);
    lightIcon.classList.toggle("hidden", !isDark);
}

themeToggleBtn.addEventListener("click", () => {
    const isDark = document.documentElement.classList.toggle("dark");
    localStorage.setItem("color-theme", isDark ? "dark" : "light");
    syncThemeIcon();
});

// Highlight the nav link for the section currently in view.
function initScrollSpy() {
    const navLinks = Array.from(document.querySelectorAll("[data-nav]"));
    if (!navLinks.length || !("IntersectionObserver" in window)) return;

    const sections = navLinks
        .map((link) => document.querySelector(link.getAttribute("href")))
        .filter((section) => section !== null);

    const observer = new IntersectionObserver(
        (entries) => {
            entries.forEach((entry) => {
                if (!entry.isIntersecting) return;
                const activeHref = `#${entry.target.id}`;
                navLinks.forEach((link) =>
                    link.classList.toggle("is-active", link.getAttribute("href") === activeHref)
                );
            });
        },
        { rootMargin: "-45% 0px -50% 0px", threshold: 0 }
    );
    sections.forEach((section) => observer.observe(section));
}

syncThemeIcon();
document.addEventListener("DOMContentLoaded", () => {
    initScrollSpy();
});

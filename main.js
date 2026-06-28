// ---------------------------------------------------------------------------
// Dark mode toggle
// The `dark` class is set in <head> before paint (to avoid a flash); here we
// only sync which icon is shown and persist the user's choice.
// ---------------------------------------------------------------------------
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

// ---------------------------------------------------------------------------
// Scroll-reveal animations (progressive enhancement)
// ---------------------------------------------------------------------------
function initReveal() {
    const elements = document.querySelectorAll(".reveal");
    if (!("IntersectionObserver" in window)) {
        elements.forEach((element) => element.classList.add("is-visible"));
        return;
    }
    const observer = new IntersectionObserver(
        (entries, obs) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    entry.target.classList.add("is-visible");
                    obs.unobserve(entry.target);
                }
            });
        },
        { rootMargin: "0px 0px -10% 0px", threshold: 0.05 }
    );
    elements.forEach((element) => observer.observe(element));
}

// ---------------------------------------------------------------------------
// Navbar scroll-spy — highlights the link for the section currently in view
// ---------------------------------------------------------------------------
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

// ---------------------------------------------------------------------------
// Init
// ---------------------------------------------------------------------------
syncThemeIcon();
document.addEventListener("DOMContentLoaded", () => {
    initReveal();
    initScrollSpy();
});

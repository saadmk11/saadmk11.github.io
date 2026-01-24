// Dark Mode Logic
const themeToggleBtn = document.getElementById('theme-toggle');
const darkIcon = document.getElementById('theme-toggle-dark-icon');
const lightIcon = document.getElementById('theme-toggle-light-icon');

// Check for saved user preference, if any, on load
if (localStorage.getItem('color-theme') === 'dark' || (!('color-theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
    document.documentElement.classList.add('dark');
    lightIcon.classList.remove('hidden');
} else {
    document.documentElement.classList.remove('dark');
    darkIcon.classList.remove('hidden');
}

themeToggleBtn.addEventListener('click', function() {
    // If is set in localstorage
    if (localStorage.getItem('color-theme')) {
        if (localStorage.getItem('color-theme') === 'light') {
            document.documentElement.classList.add('dark');
            localStorage.setItem('color-theme', 'dark');
        } else {
            document.documentElement.classList.remove('dark');
            localStorage.setItem('color-theme', 'light');
        }
    } else {
        // if NOT set in localstorage
        if (document.documentElement.classList.contains('dark')) {
            document.documentElement.classList.remove('dark');
            localStorage.setItem('color-theme', 'light');
        } else {
            document.documentElement.classList.add('dark');
            localStorage.setItem('color-theme', 'dark');
        }
    }

    // Toggle icons visibility based on the new state
    if (document.documentElement.classList.contains('dark')) {
        darkIcon.classList.add('hidden');
        lightIcon.classList.remove('hidden');
    } else {
        lightIcon.classList.add('hidden');
        darkIcon.classList.remove('hidden');
    }
});

// Fetch and Render Repositories
function getJSON(url, callbackFunction) {
    const xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function() {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
            try {
                const responseData = JSON.parse(xmlhttp.responseText);
                callbackFunction(responseData);
            } catch(error) {
                console.error("Error parsing JSON:", error);
                return;
            }
        }
    };
    xmlhttp.open("GET", url, true);
    xmlhttp.send();
}

document.addEventListener('DOMContentLoaded', (event) => {
    const container = document.getElementById("openSourceRepos");

    getJSON('repo_data.json', function(data) {
        container.innerHTML = "";

        data.forEach(function (repo) {
            // Determine language color
            let langColor = "text-gray-600 dark:text-gray-400";
            if (repo.main_programing_language === "Python") langColor = "text-blue-500";
            if (repo.main_programing_language === "JavaScript") langColor = "text-yellow-500";

            const child = `
                <div class="p-2 w-full md:w-1/2">
                    <div class="h-full bg-slate-50 dark:bg-slate-700/30 border border-slate-100 dark:border-slate-700 rounded-xl hover:border-blue-200 dark:hover:border-blue-800 hover:shadow-md transition-all p-6 flex flex-col justify-between">
                        <div>
                            <div class="flex items-center justify-between mb-2">
                                <h3 class="text-lg font-bold text-gray-900 dark:text-white truncate">
                                    <a href="${repo.url}" target="_blank" class="hover:text-blue-600 dark:hover:text-blue-400 flex items-center gap-2">
                                        <i class="fas fa-book text-blue-500"></i>
                                        ${repo.full_name.split('/')[1]}
                                    </a>
                                </h3>
                                <span class="text-xs font-medium px-2.5 py-0.5 rounded bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300">
                                    ${repo.main_programing_language}
                                </span>
                            </div>
                            <p class="text-gray-600 dark:text-gray-300 text-sm mb-4 line-clamp-3">
                                ${repo.short_description}
                            </p>
                        </div>
                        <div class="flex items-center space-x-4 text-sm text-gray-500 dark:text-gray-400 mt-auto pt-4 border-t border-gray-100 dark:border-slate-700">
                            <span class="flex items-center gap-1"><i class="fas fa-star text-yellow-400"></i> ${repo.stars}</span>
                            <span class="flex items-center gap-1"><i class="fas fa-code-branch text-green-500"></i> ${repo.forks}</span>
                            <span class="flex items-center gap-1"><i class="far fa-eye text-blue-400"></i> ${repo.watchers}</span>
                        </div>
                    </div>
                </div>
            `;
            container.insertAdjacentHTML('beforeend', child);
        });
    });
});

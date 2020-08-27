function getJSON(url, callbackFunction) {
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function() {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
            try {
                var responseData = JSON.parse(xmlhttp.responseText);
            } catch(error) {
                return;
            }
            callbackFunction(responseData);
        }
    };

    xmlhttp.open("GET", url, true);
    xmlhttp.send();
}


document.addEventListener('DOMContentLoaded', (event) => {
    var container = document.getElementById("openSourceRepos");

    getJSON('repo_data.json', function(data) {
        data.forEach(function (repo) {
            var child = `
                <div class="col-sm-6 pb-2">
                    <div class="card">
                        <div class="card-body">
                            <h6 class="card-title">
                                <i class="fa fa-book text-primary"></i>
                                <a href="${repo.url}" target="_blank">
                                    <b>${repo.full_name}</b>
                                </a>
                            </h6>
                            <p class="card-text">${repo.short_description}</p>
                            <p class="card-text">
                                <span class="pr-4"><i class="fa fa-circle text-primary pr-2" aria-hidden="true"></i> ${repo.main_programing_language}</span>
                                <span class="pr-4"><i class="fas fa-star text-warning pr-2" aria-hidden="true"></i> ${repo.stars}</span>
                                <span class="pr-4"><i class="fas fa-code-branch text-success pr-2" aria-hidden="true"></i> ${repo.forks}</span>
                                <span class="pr-4"><i class="far fa-eye text-dark pr-2" aria-hidden="true"></i> ${repo.watchers}</span>
                            </p>
                        </div>
                    </div>
                </div>
            `;
            container.insertAdjacentHTML('beforeend', child);
        });
    });
});

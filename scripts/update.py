import json

import requests


def get_repositories_data(data):
    new_data = []

    for repo in data:

        repo_name = repo['full_name']

        url = f'https://api.github.com/repos/{repo_name}'
        response = requests.get(url)

        response_data = response.json()

        repo.update({
            "short_description": response_data['description'],
            "stars": response_data['stargazers_count'],
            "forks": response_data['forks_count'],
            "watchers": response_data['watchers_count']
        })
        new_data.append(repo)

    return new_data


def update_json_file():
    with open('repo_data.json', 'r') as json_file:
        data = json.load(json_file)
        updated_data = get_repositories_data(data)

    with open('repo_data.json', 'w') as json_file:
        json_file.write(json.dumps(updated_data, indent=4))


if __name__ == '__main__':
    update_json_file()

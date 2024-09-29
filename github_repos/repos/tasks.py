import celery
import requests

from .core import GithubData, ErrorMessage


@celery.shared_task(time_limit=3)
def get_data_repositories_by_username(username: str) -> GithubData | ErrorMessage:
    url = f"https://api.github.com/users/{username}/repos"
    response = requests.get(url=url)

    if data := response.json():
        return [
            {"name": repo["name"], "stars": repo["stargazers_count"]} for repo in data
        ]

    return {"Error": f"Пользователь с именем {username} - не зарегистрирован на github"}

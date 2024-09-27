# celery tasks module
import asyncio
import importlib
import time
from typing import NewType, Optional
import json
import aiohttp
import celery
import requests
from celery.result import AsyncResult
from django.utils.asyncio import async_unsafe

CELERY_RESULT_BACKEND = importlib.import_module("github_repos.settings").CELERY_RESULT_BACKEND

ErrorMessage = NewType("ErrorMessage", dict[str, str])
GithubData = NewType("GithubData", list[Optional[dict[str, str]]])

app = celery.Celery(
    main="tasks",
    broker="amqp://guest@localhost//",
    backend=CELERY_RESULT_BACKEND,
)


# @app.task(expires=5)
# async def get_repositories_by_username(username: str) -> GithubData | ErrorMessage:
#     url = f"https://api.github.com/users/{username}/repos"
#     response = requests.get(url)
#     if data := response.json():
#         repos = [
#             {"name": repo["name"], "stars": repo["stargazers_count"]}
#             for repo in data
#         ]
#
#         return repos
#     return {"Error": f"Пользователь с именем {username} - не зарегистрирован на github"}

@app.task(expires=5)
async def get_repositories_by_username(username: str) -> GithubData | ErrorMessage:
    pass
    # url = f"https://api.github.com/users/{username}/repos"
    # async with aiohttp.ClientSession() as session:
    #     async with session.get(url=url) as response:
    #         # data = await response.json()
    #         data = {"name": 1, "stargazers_count": 2}
    #         if data:
    #             return [
    #                 {"name": repo["name"], "stars": repo["stargazers_count"]}
    #                 for repo in data
    #             ]
    #
    # return {"Error": f"Пользователь с именем {username} - не зарегистрирован на github"}


@async_unsafe
def get_celery_result_by_task_id(task_id: str) -> Optional[GithubData]:
    pass
#     if task_id:
#         timeout = 10
#         task: AsyncResult = celery.result.AsyncResult(id=task_id)
#         try:
#             result = task.get(timeout=timeout)
#             while result.status != "SUCCESS":
#                 with open("status.txt", "a", encoding="utf-8") as file:
#                     print(result.status, file=file)
#             return result
#         except celery.exceptions.TimeoutError:
#             return {"Error": f"Превышен лимит запроса в размере {timeout} секунд"}
#
#     return None

import time

import aiohttp
import celery
from asgiref.sync import async_to_sync, sync_to_async
from celery.result import AsyncResult

from .core import GithubData, ErrorMessage


async def async_get_data_repositories_by_username(username: str) -> GithubData:
    url = f"https://api.github.com/users/{username}/repos"
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url) as response:
            return await response.json()


@celery.shared_task(time_limit=3)
def get_data_repositories_by_username(username: str) -> GithubData | ErrorMessage:
    data = async_to_sync(async_get_data_repositories_by_username)(username)
    if data:
        return [
            {"name": repo["name"], "stars": repo["stargazers_count"]} for repo in data
        ]

    return {"Error": f"Пользователь с именем {username} - не зарегистрирован на github"}


@sync_to_async
def get_celery_result_by_task_id(task_id: str, timeout: int) -> GithubData | ErrorMessage | None:
    if task_id:
        task: AsyncResult = AsyncResult(id=task_id)
        start = time.perf_counter()
        status = ""

        try:
            while status != "SUCCESS" and time.perf_counter() - start < timeout:
                status = task.status
            return task.result
        except celery.exceptions.TimeoutError:
            return {"Error": f"Превышен лимит запроса в размере {timeout} секунд"}

    return None

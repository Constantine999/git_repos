import asyncio
from typing import Optional

from asgiref.timeout import timeout
from celery.result import AsyncResult
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect
from django.utils.asyncio import async_unsafe

from .tasks import get_repositories_by_username, get_celery_result_by_task_id, GithubData


async def index(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        github_user = request.POST["username"]
        task_id: Optional[str] = get_repositories_by_username.apply_async(args=[github_user]).id
        # request.session["task_id"] = task_id
        await asyncio.to_thread(lambda: setattr(request.session, "task_id", task_id))

        return await asyncio.to_thread(redirect, "result")
    return await asyncio.to_thread(
        render,
        request=request,
        template_name="repos/index.html",
    )


async def result(request: HttpRequest) -> HttpResponse:
    # task_id: str = request.session.get("task_id")
    task_id: str = await asyncio.to_thread(request.session.get, "task_id")
    result: Optional[GithubData] = get_celery_result_by_task_id(task_id=task_id)


    if "Error" not in result:
        return await asyncio.to_thread(
            render,
            request=request,
            template_name="repos/result.html",
            context={"result": result},
        )
    return await asyncio.to_thread(
        HttpResponse,
        content=result["Error"],
    )

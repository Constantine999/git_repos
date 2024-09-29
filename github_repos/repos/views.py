import time

import celery
from asgiref.sync import sync_to_async
from celery.result import AsyncResult
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect

from .core import TIMEOUT
from .tasks import get_data_repositories_by_username


@sync_to_async
def index(request: HttpRequest) -> HttpResponse:
    if request.method == "POST" and request.POST["username"]:
        github_user = request.POST["username"]
        task_id: str = get_data_repositories_by_username.apply_async(args=[github_user]).id
        request.session["task_id"] = task_id
        return redirect("result")

    return render(
        request=request,
        template_name="repos/index.html",
    )


@sync_to_async
def result(request: HttpRequest) -> HttpResponse:
    task_id: str = request.session.get("task_id")

    if task_id:
        task: AsyncResult = AsyncResult(id=task_id)

        try:
            start = time.perf_counter()
            while task.status != "SUCCESS" and time.perf_counter() - start < TIMEOUT:
                continue

            return render(
                request=request,
                template_name="repos/result.html",
                context={"result": task.result},
            )

        except celery.exceptions.TimeoutError:
            return HttpResponse(
                content=f"Превышен лимит запроса в размере {TIMEOUT} секунд")

    return None

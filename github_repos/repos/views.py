from typing import Optional

from asgiref.sync import sync_to_async, async_to_sync
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect

from .tasks import get_data_repositories_by_username, get_celery_result_by_task_id, GithubData


@sync_to_async
def index(request: HttpRequest) -> HttpResponse:
    if request.method == "POST" and request.POST["username"]:
        github_user = request.POST["username"]
        task_id: Optional[str] = get_data_repositories_by_username.apply_async(args=[github_user]).id
        request.session["task_id"] = task_id
        return redirect("result")

    return render(
        request=request,
        template_name="repos/index.html",
    )


@sync_to_async
def result(request: HttpRequest) -> HttpResponse:
    task_id: str = request.session.get("task_id")
    result: Optional[GithubData] = async_to_sync(get_celery_result_by_task_id)(task_id, 6)
    if "Error" not in result:
        return render(
            request=request,
            template_name="repos/result.html",
            context={"result": result},
        )

    return HttpResponse(
        content=result["Error"],
    )

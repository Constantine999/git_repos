"""
ASGI config for github_repos project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
import sys
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "github_repos.settings")

# Получаем путь до папки с текущим файлом
current_dir = os.path.dirname(__file__)
# Получаем путь до папки с проектом MicroservicesRabbitMQ
project_dir = os.path.dirname(os.path.dirname(current_dir))
# Добавляем путь до папки с проектом в sys.path
sys.path.insert(0, project_dir)

application = get_asgi_application()

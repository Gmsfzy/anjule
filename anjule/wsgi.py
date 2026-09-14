"""
WSGI config for anjule project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# 配置Django的settings模块（必须和项目名一致）
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'anjule.settings')

# 核心：定义WSGI应用入口（必须命名为application）
application = get_wsgi_application()
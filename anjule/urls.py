from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from rest_framework.authtoken.views import ObtainAuthToken

urlpatterns = [
    path('admin/', admin.site.urls),
    # 首页
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
    # 用户中心服务
    path('accounts/', include('accounts.urls')),
    # 小区管理服务
    path('community/', include('community.urls')),
    # 物业服务服务
    path('property/', include('property.urls')),
    # 第三方服务集成
    path('third-party/', include('third_party.urls')),
    # API接口
    path('api/accounts/', include('accounts.urls_api')),
    path('api/community/', include('community.urls_api')),
    path('api/property/', include('property.urls_api')),
    path('api/third-party/', include('third_party.urls_api')),
    # 404页面
    path('404/', TemplateView.as_view(template_name='404.html'), name='404'),

    path('api/houses/', include('property.urls')),
]

# 配置Django admin中文显示
admin.site.site_header = '安居乐智慧社区管理平台'
admin.site.site_title = '安居乐管理后台'
admin.site.index_title = '欢迎使用安居乐管理后台'
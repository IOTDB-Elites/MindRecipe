"""master URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from master.logic.heartbeat import service
from master.view import operation, monitor

service()
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/operation/read', operation.handle_read),
    path('api/operation/write', operation.handle_write),
    path('api/admin/monitor', monitor.monitor),
    path('api/user/get_info', operation.get_user_info),
    path('api/user/update_info', operation.update_user_info),
    path('api/user/get_read_list', operation.get_read_list),
    path('api/article/get_list', operation.get_article_list),
    path('api/article/get_popular', operation.get_popular),
    path('api/article/get_article', operation.get_article),
    path('api/article/get_feedback', operation.get_feedback)


]

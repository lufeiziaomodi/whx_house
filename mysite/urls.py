"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


from django.urls import path
from app01.views import login
from app01.views import index
from app01.views import comment

urlpatterns = [
    # path("admin/", admin.site.urls),
    path("login_page/", login.login_page),
    path("user_add/", login.user_add),
    #首页
    path("index_page/", index.index_page),
    path("index/", index.index),
    path("index/change", index.index_change),
    path("indexange", index.index_change),

    #舆情分析
    path("comment/", comment.comment_page),
    path("event1/", comment.event1),
    path("event2/", comment.event2),
    path("event3/", comment.event3),
    path("event4/", comment.event4),
    path("event5/", comment.event5),
    path("ciyun/", comment.ciyun),
    path("update/", comment.update),
    path("snownlp/", comment.snownlp),
    path("cbaemotion/", comment.cbaemotion),

]

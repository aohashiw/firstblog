"""firstblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from blog import views

hander404 = 'blog.views.page_not_found'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name='index'),
    path('list-<int:lid>.html',views.list,name='list'),
    path('show-<int:sid>.html',views.show,name='show'),
    path('tag/<tag>',views.tag,name='tag'),
    path('s/',views.search,name='search'),
    path('about/',views.about,name='about'),
    path('ueditor/',include('DjangoUeditor.urls')),
    path('userprofile/',include('userprofile.urls',namespace='userprofile')),
    path(r'^captcha/',include('captcha.urls')),
    path('success/<int:id>/',views.success,name='success'),
    path('a/',views.article_create,name='article_create'),
    path('article-delete/<int:id>',views.article_delete,name='article_delete'),
    path('password-reset/', include('password_reset.urls')),
    path('mdeditor/',include('mdeditor.urls')),
    path('comment/',include('comment.urls',namespace='comment')),
    path('article-update/<int:id>',views.article_update,name='article_update'),
]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)


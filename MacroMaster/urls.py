"""MacroMaster URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import *
from django.contrib import admin
from django.contrib.auth.views import login, logout
from users.views import signup as user_signup, get_user_home, get_my_recipes, get_my_favorites, add_to_favorites, change_my_recipe, go_to_change_page, delete_recipe,rate_recipe, del_from_favorites
from polls.views import check_recipe_ins
admin.autodiscover()

urlpatterns = [
    url(r'^polls/', include('polls.urls')),
    url(r'^admin/', include(admin.site.urls)),
]


urlpatterns += [
    url(r'^login/$', login, name='user_login'),
    url(r'^logout/$', logout, name='user_logout'), 
    url(r'^signup$', user_signup, name='user_signup'), 
]

urlpatterns += [
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^accounts/user/', include('users.urls')),
]

urlpatterns += [
    url(r'^recipe/detail', check_recipe_ins),
]






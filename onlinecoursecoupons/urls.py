"""onlinecoursecoupons URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path, re_path
from courses import views, api_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('averyverysecureadmin/', admin.site.urls),
    path('', views.home, name='home'),
    path('courses', views.courses, name='courses'),
    path('search/', views.search, name='search'),
    path('category/', views.category, name='category'),
    path('subscribe/', views.subscribe, name='subscribe'),
    re_path('^api/$', api_views.api, name='api'),
    path('info-page/', views.info_page, name='info_page'),
    path('test/', views.test, name='test'),
    path('XVuWnuQVjyS49iY2ks4gRSaYNtHv32Uw4hR5Y4JujhoUooQ5Yn3LYGGt9WXvfMA8', 
        views.show_coupons, name='show_coupons')
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'courses.views.error_404_view'
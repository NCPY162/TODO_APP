"""
URL configuration for todo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.contrib import admin # type: ignore
from django.urls import path, include # type: ignore
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title = "To Do API Documentation",
        default_version ="v1",
        description = "Cet API permet de gérer une liste de tâches",
        terms_of_service = "",
        contact = openapi.Contact(email="ncpy162@gmail.com"),
        license = openapi.License(name="BSD License")
    ),
    public = True,
    permission_classes = (permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tasks/', include('tasks.urls')),
    path('todos/', include('todoList.urls')),
    path('users/', include('users.urls')),
    path('todo-api-doc/', schema_view.with_ui('swagger', cache_timeout=0), name="schema-swagger-ui"),
    path('todo-api-redoc/', schema_view.with_ui('redoc', cache_timeout=0), name="schema-redoc")
]

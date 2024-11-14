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

    path('', include('tokens.urls')),

    path('todo-api-doc/', schema_view.with_ui('swagger', cache_timeout=0), name="api-doc"),
    path('todo-api-redoc/', schema_view.with_ui('redoc', cache_timeout=0), name="api-redoc")   
]

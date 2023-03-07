"""mayor URL Configuration

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
# django
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# rest framework
from rest_framework.permissions import AllowAny

# third party
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from django.conf import settings


schema_view = get_schema_view(
    openapi.Info(
        title="Ajay Bhawani Clothe House - APIs Documentation",
        default_version="v1",
        description="A well documented APIs for Ajay Bhawani clothe store.",
        terms_of_service="",
    ),
    public=True,
    permission_classes=(AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    # API docs
    path("docs/", schema_view.with_ui("redoc"), name="schema-redoc"),
    path("api/auth/", include("userauth.urls")),
    path("api/", include("products.urls")),
]


if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns +=  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

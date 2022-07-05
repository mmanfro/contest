from django.views.i18n import JavaScriptCatalog
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import include, path


from contest import views as v

urlpatterns = i18n_patterns(
    path(
        "jsi18n/",
        JavaScriptCatalog.as_view(),
        name="javascript-catalog",
    ),
    path("admin/", admin.site.urls),
    path("", v.index),
    path("voting/", include("voting.urls", namespace="voting")),
)

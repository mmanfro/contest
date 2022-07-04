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

handler500 = "contest.views.handler500"
handler404 = "contest.views.handler404"
handler403 = "contest.views.handler403"
handler400 = "contest.views.handler400"

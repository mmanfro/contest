from django.urls import path
from voting import views as v

app_name = "voting"
urlpatterns = [
    path("", v.participants, name="participants"),
    path("vote/", v.vote, name="vote"),
]

from django.urls import path
from voting import views as v

app_name = "voting"
urlpatterns = [
    path("", v.participants, name="participants"),
    path("vote/<int:participant_id>", v.vote, name="vote"),
]

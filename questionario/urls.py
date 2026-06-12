from django.urls import path
from . import views

urlpatterns = [
    path("", views.email_gate, name="email_gate"),
    path("questionario/", views.questionario, name="questionario"),
    path("q/<str:token>/", views.questionario_invito, name="questionario_invito"),
    path("grazie/", views.grazie, name="grazie"),
    path("risultati/", views.dashboard, name="dashboard"),
]

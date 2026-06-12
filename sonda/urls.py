from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.shortcuts import redirect
from django.urls import path, include


def admin_login_redirect(request):
    return redirect("/accounts/google/login/?next=/admin/")


urlpatterns = [
    # Rimanda il login admin direttamente a Google OAuth
    path("admin/login/", admin_login_redirect),
    path("admin/logout/", LogoutView.as_view(next_page="/"), name="admin-logout"),
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("", include("questionario.urls")),
]

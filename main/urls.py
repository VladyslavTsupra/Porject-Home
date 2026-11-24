from django.urls import path

from main import views

app_name = "main"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("about/", views.AboutView.as_view(), name="about"),
    # Pages that are not ready yet, so they show a 404 error
    path("delivery/", views.PageNotFoundView.as_view(), name="delivery"),
    path("contacts/", views.PageNotFoundView.as_view(), name="contacts"),
    path("profile-cart/", views.PageNotFoundView.as_view(), name="profile_cart"),
]

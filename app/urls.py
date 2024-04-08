from django.urls import path
from . import views

app_name = "app"
urlpatterns = [
    path("", views.index, name="index"),
    path("<int:pk>/", views.post_detail, name="post_detail"),
    path("new/", views.post_new, name="post_new"),
    path("analyze/", views.analyze_text, name="analyze_text"),
]

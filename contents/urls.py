from django.urls import path
from . import views
from rest_framework import routers

app_name = "contents"
router = routers.SimpleRouter()
router.register('category', views.CategoryViewSet)

urlpatterns = [
    path("posts/", views.PostListView.as_view(), name="posts-list"),
    path("post/create/", views.PostCreateView.as_view(), name="post-create"),
    path("post/<int:post_id>", views.PostDetailView.as_view(), name="post-detail"),
]+ router.urls

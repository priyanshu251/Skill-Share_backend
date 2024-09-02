from django.urls import path
from recommend_post import views

urlpatterns = [path("", views.get_recommended_posts, name="recommend-post")]

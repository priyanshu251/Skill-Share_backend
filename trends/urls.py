from django.urls import path
from trends import views

urlpatterns = [
    path("skill/",views.SkillTrendView.as_view(),name="skill-trends"),
    path("community/",views.CommunityTrendView.as_view(),name="community-trends"),
]

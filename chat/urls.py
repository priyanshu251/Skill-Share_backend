from django.urls import path
from chat import views

urlpatterns = [path("", views.ChatListCreateView.as_view(), name="chat-user-view")]

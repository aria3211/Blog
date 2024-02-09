from django.urls import path
from . import views

app_name = "home"
urlpatterns = [
    path('',views.HomeView.as_view(),name="home"),
    path('post/<int:post_id>/<slug:post_slug>', views.PostView.as_view(), name="detail"),
    path('post/delete/<int:post_id>',views.PostDelete.as_view(),name='post_delete'),
    path('post/update/<int:post_id>', views.PostUpdateView.as_view(), name='post_update'),
    path('post/create/', views.PostCrateView.as_view(), name='post_create'),
    path('about/', views.listmembers.as_view(), name='members'),
    path('reply/<int:post_id>/<int:comment_id>', views.PostReplyView.as_view(), name='reply'),
    path('Like/<int:post_id>', views.LikePostView.as_view(), name='like'),


]
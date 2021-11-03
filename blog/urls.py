from django.urls import path
from blog import views

app_name = 'blog'

urlpatterns = [
    path('',views.PostListView.as_view(),name='post-list'),
    path('post/<int:pk>/',views.PostDetailView.as_view(),name='post-detail'),
    path('post/create/',views.PostCreateView.as_view(),name='create_post'),
    path('post/<int:pk>/edit/',views.PostUpdateView.as_view(),name='edit_post'),
    path('post/<int:pk>/remove/',views.PostDeleteView.as_view(),name='remove_post'),
    path('drafts/',views.DraftListView.as_view(),name='post_draft'),
    path('post/<int:pk>/publish/', views.post_publishing, name='post_publishing'),
    path('post/<int:pk>/comments', views.CommentCreateView.as_view(),name='add_comment_to_post'),
    path('comment/<int:pk>/remove', views.CommentDeleteView.as_view(), name='remove_comment'),
    path('comment/<int:pk>/approve',views.approve_comment_view,name='approve_comment'),
]

from django.conf.urls.static import static
from django.urls import path
from .views import (
    IdeaListView,
    IdeaDetailView, 
    LikeView,
    UnLikeView,
    CommentLikeView,
    CommentUnLikeView,
    IdeaUpdateView,
    IdeaCommentsUpdateView,
    IdeaDeleteView,
    IdeaCommentsDeleteView,
    IdeaCreateView,
    IdeaCommentsCreateView,
    )

app_name = 'idea'

urlpatterns = [
    path('<int:pk>/unlike-comment/', CommentUnLikeView, name='unlike_comment'),
    path('<int:pk>/like-comment/', CommentLikeView, name='like_comment'),
    path('<int:pk>/unlike-idea/', UnLikeView, name='unlike_idea'),
    path('<int:pk>/like-idea/', LikeView, name='like_idea'),
    path('<int:pk_idea>/comment_edit/<int:pk>/', IdeaCommentsUpdateView.as_view(), name='comment_edit'),
    path('<int:pk_idea>/comment-delete/<int:pk>/', IdeaCommentsDeleteView.as_view(), name='comment_delete'),
    path('<int:pk_idea>/new_comment/', IdeaCommentsCreateView.as_view(),name='comment_new'),
    path('new/', IdeaCreateView.as_view(), name='idea_new'),
    path('<int:pk>/edit/', IdeaUpdateView.as_view(), name='idea_edit'),
    path('<int:pk>/', IdeaDetailView.as_view(), name='idea_detail'),
    path('<int:pk>/delete/', IdeaDeleteView.as_view(), name='idea_delete'),
    path('', IdeaListView.as_view(), name='idea_list')
] 

handler404 = 'news.views.error_404'

from django.conf.urls.static import static
from django.urls import path
from .views import (
    NewsListView,
    NewsUpdateView,
    NewsDetailView,
    NewsDeleteView,
    NewsCreateView,
    NewsCommentsCreateView,
    NewsCommentsDeleteView,
    NewsCommentsUpdateView,
    CategoryCreatingView,
    CategoryView,
    LikeView,
    UnLikeView,
    CommentLikeView,
    CommentUnLikeView,
    # google_news,
    )

urlpatterns = [
    # path('update/', google_news, name='update_news'),
    path('<int:pk>/unlike-comment/', CommentUnLikeView, name='unlike_comment'),
    path('<int:pk>/like-comment/', CommentLikeView, name='like_comment'),
    path('<int:pk>/unlike-news/', UnLikeView, name='unlike_news'),
    path('<int:pk>/like-news/', LikeView, name='like_news'),
    path('<int:pk_news>/comment_edit/<int:pk>/', NewsCommentsUpdateView.as_view(), name='comment_edit'),
    path('<int:pk_news>/comment-delete/<int:pk>/', NewsCommentsDeleteView.as_view(), name='comment_delete'),
    path('<int:pk_news>/new_comment/', NewsCommentsCreateView.as_view(),name='comment_new'),
    path('category/', CategoryCreatingView.as_view(), name='category_new'),
    path('category/<slug:slug>/', CategoryView, name='category'),
    path('new/', NewsCreateView.as_view(), name='news_new'),
    path('<int:pk>/edit/', NewsUpdateView.as_view(), name='news_edit'),
    path('<int:pk>/', NewsDetailView.as_view(), name='news_detail'),
    path('<int:pk>/delete', NewsDeleteView.as_view(), name='news_delete'),
    path('', NewsListView.as_view(), name='news_list')
] 

handler404 = 'news.views.error_404'

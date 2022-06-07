from django.urls import path
from news.api import views as api_views

# class case has .as_view()
urlpatterns = [
    path('articles/',api_views.ArticleListCreateAPIView.as_view(),name="article_list"),
    path('articles/<int:pk>',api_views.ArticleDetailAPIView.as_view(),name="article-detail"),
    path('authors/',api_views.JournalistListCreateAPIView.as_view(),name="authors_list"),
]


# function case
# urlpatterns = [
#     path('articles/',api_views.article_list_create_api_view,name="article/list"),
#     path('articles/<int:value_from_url>',api_views.article_detail_api_view,name="article-detail"),
# ]
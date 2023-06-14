from django.urls import path
from .views import *


urlpatterns = [
    path("", PostList.as_view(), name='post_list'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('news/create/', NwCreate.as_view(), name='nw_create'),
    path('articles/create/', ArCreate.as_view(), name='ar_create'),
    path('news/<int:pk>/delete/', NwDelete.as_view(), name='nw_delete'),
    path('articles/<int:pk>/delete/', ArDelete.as_view(), name='ar_delete'),
    path('<int:pk>/edit/', newsUpdate.as_view(), name='news_update'),
]
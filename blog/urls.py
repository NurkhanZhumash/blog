from django.urls import path

from blog import views
from .views import (ListPostView, DetailPostView, PostUpdateView, PostDeleteView, PostCreateView,)

urlpatterns = [
    path('', ListPostView.as_view(), name='list_post'),
    path('<int:pk>', DetailPostView.as_view(), name='post_detail'),
    path('<int:pk>/edit', PostUpdateView.as_view(),name='update_post'),
    path('<int:pk>/delete>', PostDeleteView.as_view(),name='delete_post'),
    path('new/',PostCreateView.as_view(),name='new_post'),
    path('comment/<int:pk>/add', views.comment_create_view,name='new_comment')
]

from django.urls import path

from post.views import PostListApiView, PostCreateView, PostRetrieveUpdateDestroyView, PostCommentListApiView, \
    CommentListCreateApiView, PostLikeListApiView, CommentRetrieveView, CommentLikeListView, \
    PostCommentLikeListView, PostLikeApiView, CommentLikeApiView
# PostLikeCreateView, PostLikeDeleteView, PostCommentCreateApiView
from users.urls import urlpatterns


urlpatterns = [
    path('list/', PostListApiView.as_view()),
    path('create/', PostCreateView.as_view()),
    path('<uuid:pk>/', PostRetrieveUpdateDestroyView.as_view()),
    path('<uuid:pk>/likes/', PostLikeListApiView.as_view()),
    path('<uuid:pk>/comments/', PostCommentListApiView.as_view()),
    # path('<uuid:pk>/comments/create/', PostCommentCreateApiView.as_view()),

    path('comments/', CommentListCreateApiView.as_view()),
    path('comments/<uuid:pk>/', CommentRetrieveView.as_view()),
    path('comments/<uuid:pk>/likes', CommentLikeListView.as_view()),

    path('likes/', PostCommentLikeListView.as_view()),
    # path('likes/create/', PostLikeCreateView.as_view()),
    # path('likes/<uuid:pk>/delete/'), PostLikeDeleteView.as_view(),

    path('<uuid:pk>/create-delete-like/', PostLikeApiView.as_view()),
    path('comments/<uuid:pk>/create-delete-like/', CommentLikeApiView.as_view()),

]
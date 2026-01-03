from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT
from rest_framework.views import APIView

from shared.custom_pagination import CustomPagination
from .models import Post, PostComment, PostLike, CommentLike
from .serializers import PostSerializer, CommentSerializer, PostLikeSerializer, CommentLikeSerializer


# Create your views here.

class PostListApiView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [AllowAny,]
    pagination_class = CustomPagination

    def get_queryset(self):
        return Post.objects.all()

class PostCreateView(generics.CreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, ]

    def perform_create(self, serializer):
        serializer.save(author=self.request.data)

class PostRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, ]

    def put(self, request, *args, **kwargs):
        post = self.get_object()
        serializer = self.serializer_class(post, self.request)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                'success':True,
                'code':status.HTTP_200_OK,
                'message':'Post successfully updated',
                'data':serializer.data
            }
        )
    def delete(self, request, *args, **kwargs):
        post = Post.objects.all()
        post.delete()
        return  Response(
            {
                'success':True,
                'code':status.HTTP_204_NO_CONTENT,
                'message':'Post successfully deleted!'
            }
        )

class PostCommentListApiView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [AllowAny, ]

    def get_queryset(self):
        post_id = self.kwargs['pk']
        queryset = PostComment.objects.filter(post__id = post_id)
        return queryset

# class PostCommentCreateApiView(generics.CreateAPIView):
#     serializer_class = PostSerializer
#     permission_classes = [IsAuthenticated, ]
#
#     def perform_create(self, serializer):
#         post_id = self.kwargs['pk']
#         serializer.save(author = self.request.user, post__id=post_id)

class CommentListCreateApiView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, ]
    queryset = PostComment.objects.all()
    pagination_class = CustomPagination
    def perform_create(self, serializer):
        serializer.save(author = self.request.user)

class CommentRetrieveView(generics.RetrieveAPIView):
    serializer_class = CommentSerializer
    permission_classes = [AllowAny, ]
    queryset = PostComment.objects.all()


class PostLikeListApiView(generics.ListAPIView):
    serializer_class = PostLikeSerializer
    permission_classes = [AllowAny, ]

    def get_queryset(self):
        post_id = self.kwargs['pk']
        return  PostLike.objects.filter(post_id = post_id)


class CommentLikeListView(generics.ListAPIView):
    serializer_class = CommentLikeSerializer
    permission_classes = [AllowAny, ]

    def get_queryset(self):
        comment_id = self.kwargs['pk']
        return CommentLike.objects.filter(comment_id=comment_id)

class PostCommentLikeListView(generics.ListAPIView):
    serializer_class = CommentLikeSerializer
    permission_classes = [AllowAny, ]
    queryset = CommentLike.objects.all()

# class PostLikeCreateView(generics.CreateAPIView):
#     serializer_class = PostLikeSerializer
#     permission_classes = [IsAuthenticatedOrReadOnly, ]
#
#     def perform_create(self, serializer):
#         serializer.save(author = self.request.user)
#
# class PostLikeDeleteView(generics.DestroyAPIView):
#     queryset = PostLike.objects.all()
#     serializer_class = PostLikeSerializer
#     permission_classes = [IsAuthenticated, ]
#
#     def get_queryset(self):
#         post_like_id = self.kwargs['pk']
#         return  PostLike.objects.filter(post_like_id = post_like_id)
#
#     def delete(self, request, *args, **kwargs):
#         post_like = self.get_queryset()
#         post_like.delete()
#         return  Response(
#             {
#                 'success':True,
#                 'code':status.HTTP_204_NO_CONTENT,
#                 'message':'PostLike successfully deleted!'
#             }
#         )

class PostLikeApiView(APIView):

    # def post(self, request, pk):
    #     try:
    #         post_like = PostLike.objects.create(
    #             author=self.request.user,
    #             post_id = pk
    #         )
    #         serializer = PostLikeSerializer(post_like)
    #         data = {
    #             "success": True,
    #             "message": "Post like posted successfully!",
    #             "data":serializer.data
    #         }
    #         return  Response(data, status=HTTP_201_CREATED)
    #     except Exception as e:
    #         data = {
    #             "success":False,
    #             "message": f"{e}",
    #             "data": None
    #         }
    #
    # def delete(self, request, pk):
    #     try:
    #         post_like = PostLike.objects.get(
    #             author=self.request.user,
    #             post_id = pk
    #         )
    #         post_like.delete()
    #         data = {
    #             "success": True,
    #             "message": "Post like deleted successfully!",
    #             "data": None
    #         }
    #         return Response(data, status=HTTP_204_NO_CONTENT)
    #
    #     except Exception as e:
    #         data = {
    #             "success": False,
    #             "message": f"{e}",
    #             "data": None
    #         }
    #         return Response(data, status=HTTP_400_BAD_REQUEST)

    def post(self, pk):
        try:
            post_like = PostLike.objects.get(
                author=self.request.user,
                post_id=pk
            )
            post_like.delete()
            data = {
                "success": True,
                "message": f"Post Like has been deleted successfully",
            }
            return Response(data, status=HTTP_204_NO_CONTENT)
        except PostLike.DoesNotExist:
            post_like = PostLike.objects.create(
                author = self.request.user,
                post_id = pk
            )
            serializer = PostLikeSerializer(post_like)
            data = {
                "success":True,
                "message":"Post Like has been posted successfully!",
                "data":serializer.data
            }
            return Response(data, status=HTTP_201_CREATED)


class CommentLikeApiView(APIView):
    # def comment_like(self, request, pk):
    #     try:
    #         comment_like = CommentLike.objects.create(
    #             author=self.request.user,
    #             comment_id=pk
    #         )
    #         serializer = CommentLikeSerializer(comment_like)
    #         data = {
    #             "success": True,
    #             "message": "Like of comment has been posted successfully!",
    #             "data": serializer.data
    #         }
    #         return Response(data, status=HTTP_201_CREATED)
    #     except Exception as e:
    #         data = {
    #             "success": False,
    #             "message": f"{e}",
    #             "data": None
    #         }
    # def delete(self, request, pk):
    #     try:
    #         comment_like = CommentLike.objects.get(
    #             author=self.request.user,
    #             comment_id=pk
    #         )
    #         comment_like.delete()
    #         data = {
    #             "success": True,
    #             "message": f"Like has been deleted successfully",
    #             "data": None
    #         }
    #         return Response(data, status = HTTP_204_NO_CONTENT)
    #     except Exception as e:
    #         data = {
    #             "success": False,
    #             "message": f"{e}",
    #             "data": None
    #         }
    #         return Response(data, status=HTTP_400_BAD_REQUEST)

    def post(self, pk):
        try:
            comment_like = CommentLike.objects.get(
                author = self.request.user,
                comment_id = pk
            )
            comment_like.delete()
            data = {
                "success": True,
                "message": f"Post Like has been deleted successfully",
            }
            return Response(data, status=HTTP_204_NO_CONTENT)
        except CommentLike.DoesNotExist:
            comment_like = CommentLike.objects.create(
                author = self.request.user,
                comment_id = pk
            )
            serializer = CommentLikeSerializer(comment_like)
            data = {
                "success":True,
                "message":"CommentLike has been successfully posted!",
                "data":serializer.data
            }
            return Response(data, status=HTTP_201_CREATED)
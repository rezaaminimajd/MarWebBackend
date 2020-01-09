from django.shortcuts import render

from rest_framework.generics import GenericAPIView


# Create your views here.


class PostsListAPIView(GenericAPIView):

    def get(self, request):
        pass


class PostAPIView(GenericAPIView):

    def get(self, request, post_id):
        pass

    def post(self, request):
        pass

    def put(self, request, post_id):
        pass

    def delete(self, request, post_id):
        pass


class CommentsListAPIView(GenericAPIView):

    def get(self, request, post_id):
        pass


class CommentAPIView(GenericAPIView):

    def get(self, request, post_id, comment_id):
        pass

    def post(self, request, post_id):
        pass

    def put(self, request, post_id, comment_id):
        pass

    def delete(self, request, post_id, comment_id):
        pass


class LikeAPIView(GenericAPIView):

    def post(self, request, action_id):
        pass

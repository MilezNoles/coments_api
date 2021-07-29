from django.template.defaultfilters import slugify
from rest_framework.viewsets import ModelViewSet

from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer, ThinPostSerializer, CommentInstanceSerializer


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = "slug"

    def get_serializer_class(self):
        if self.action == "list":
            return ThinPostSerializer
        return PostSerializer

    def perform_create(self, serializer):
        serializer.save(slug=slugify(self.request.POST["title"]), )


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return CommentSerializer
        return CommentInstanceSerializer

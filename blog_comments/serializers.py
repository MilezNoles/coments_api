from rest_framework.relations import HyperlinkedIdentityField
from rest_framework.serializers import ModelSerializer, SerializerMethodField

from .models import Post, Comment
from .utils import path_to_children


class PostCommentSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(view_name='comment-detail', read_only=True)

    class Meta:
        model = Comment
        fields = ("id", "url", "post", "name", "body", "reply_to")


class PostSerializer(ModelSerializer):
    replies = SerializerMethodField()

    def get_replies(self, obj):
        node_comment_ids = []
        q_for_node_comments = Comment.objects.filter(post_id=obj.id, reply_to=None)
        for el in q_for_node_comments:
            node_comment_ids.append(el.id)
        recursive_q = path_to_children(tuple(node_comment_ids))
        q_depth_limit3 = [x for x in list(recursive_q) if x.path_len < 4]
        serializer = PostCommentSerializer(q_depth_limit3, many=True, context=self.context)
        return serializer.data

    class Meta:
        model = Post
        fields = ("id", "title", "slug", "body", "publish", "created", "updated", "status", "author", "replies")


class ThinPostSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(view_name="post-detail", lookup_field="slug")

    class Meta:
        model = Post
        fields = ("id", "title", "url")


class CommentSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(view_name="comment-detail")

    class Meta:
        model = Comment
        fields = ("id", "url", "name", "body", "created", "post", "reply_to",)


class CommentInstanceSerializer(ModelSerializer):
    replies = SerializerMethodField()
    url = HyperlinkedIdentityField(view_name="comment-detail")

    def get_replies(self, obj):
        q_for_parent = Comment.objects.get(pk=obj.pk)
        recursive_q = path_to_children(q_for_parent.id)
        q_for_children = [x for x in list(recursive_q) if x.path_len > 1]
        serializer = PostCommentSerializer(q_for_children, many=True, context=self.context)
        return serializer.data

    class Meta:
        model = Comment
        fields = ("id", "url", "name", "email", "body", "created", "post", "reply_to", "replies")

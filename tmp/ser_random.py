from datetime import datetime
from rest_framework import serializers


class Comment(object):
    def __init__(self, email, text, created=None) -> None:
        self.email = email
        self.text = text
        self.created = created or datetime.now()


class CommentSerializer(serializers.Serializer):
    email = serializers.EmailField()
    text = serializers.CharField(max_length=255)
    created = serializers.DateTimeField()


comm = Comment("idcdtokms@gmail.com", "foo bar")

serializer = CommentSerializer(comm)

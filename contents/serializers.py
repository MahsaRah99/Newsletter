from rest_framework import serializers
from .models import Category, Post


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"

    def create(self, validated_data):
        FB_WORDS = ["gun", "drug"]
        user = self.context["request"].user
        if user.is_staff:
            validated_data["status"] = Post.Statuses.PUBLISHED
        else:
            if any(
                word in validated_data["title"] or word in validated_data["body"]
                for word in FB_WORDS
            ):
                validated_data["status"] = Post.Statuses.UNPUBLISHED
            else:
                validated_data["status"] = Post.Statuses.DRAFT
        post = Post.objects.create(**validated_data)
        return post

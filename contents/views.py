from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from .models import Category, Post
from .serializers import CategorySerializer, PostSerializer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from permissions import IsOwnerOrReadOnly


class CategoryViewSet(viewsets.ViewSet):
    """A viewset for handling CRUD operations on Category objects."""

    permission_classes = (IsAuthenticated,)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def create(self, request):
        """Creates a new category."""
        srz_data = self.serializer_class(data=request.data)
        if srz_data.is_valid():
            srz_data.save()
            return Response(srz_data.data, status=status.HTTP_201_CREATED)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def list(self, request):
        """Retrieves a list of all categories."""
        srz_data = self.serializer_class(instance=self.queryset, many=True)
        return Response(data=srz_data.data)

    def partial_update(self, request, category_id):
        """Partially updates the specified category."""
        category = get_object_or_404(self.queryset, pk=category_id)
        srz_data = CategorySerializer(
            instance=category, data=request.POST, partial=True
        )
        if srz_data.is_valid():
            srz_data.save()
            return Response(data=srz_data.data)
        return Response(data=srz_data.errors)

    def destroy(self, request, category_id):
        """Deletes the specified category."""
        category = get_object_or_404(self.queryset, pk=category_id)
        category.delete()
        return Response({"message": "category deleted"})


class PostListView(APIView):
    """Retrieves a list of published posts."""

    def get(self, request):
        posts = Post.objects.filter(status=Post.Statuses.PUBLISHED)
        srz_data = PostSerializer(instance=posts, many=True).data
        return Response(srz_data, status=status.HTTP_200_OK)


class PostCreateView(APIView):
    """Creates a new post with the provided data."""

    permission_classes = (IsAuthenticated,)
    serializer_class = PostSerializer

    def post(self, request):
        srz_data = PostSerializer(data=request.data)
        if srz_data.is_valid():
            srz_data.save()
            return Response(srz_data.data, status=status.HTTP_201_CREATED)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDetailView(APIView):
    """A view for retrieving, updating, and deleting individual posts."""

    permission_classes = (IsOwnerOrReadOnly,)

    def get(self, request, post_id):
        """Retrieves details of the specified post."""
        post = get_object_or_404(Post, id=post_id)
        srz_data = PostSerializer(instance=post)
        return Response(data=srz_data.data, status=status.HTTP_200_OK)

    def put(self, request, answer_id):
        """Updates the specified post with the provided data."""
        post = get_object_or_404(Post, id=answer_id)
        self.check_object_permissions(request, post)
        srz_data = PostSerializer(instance=post, data=request.data, partial=True)
        if srz_data.is_valid():
            srz_data.save()
            return Response(srz_data.data, status=status.HTTP_200_OK)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, answer_id):
        """Marks the specified post as inactive."""
        post = get_object_or_404(Post, id=answer_id)
        self.check_object_permissions(request, post)
        post.is_active = False
        return Response({"message": "post deleted"}, status=status.HTTP_200_OK)

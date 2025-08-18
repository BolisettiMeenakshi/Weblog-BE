from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import Post
from .serializers import PostSerializer
from rest_framework.permissions import AllowAny

# Create your views here.

#from rest_framework.permissions import IsAuthenticatedOrReadOnly

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

#class PostViewSet(viewsets.ModelViewSet):
    #queryset = Post.objects.all()
    #serializer_class = PostSerializer

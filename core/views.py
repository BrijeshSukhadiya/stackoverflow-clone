from django.shortcuts import render
from rest_framework import viewsets, permissions, filters
from .models import Question, Answer
from .serializers import QuestionSerializer, AnswerSerializer
from .pagination import QuestionPagination
from django_filters.rest_framework import DjangoFilterBackend

# Create your views here.

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all().order_by('-created_at')
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = QuestionPagination
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['title', 'tags']
    filterset_fields = ['tags']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


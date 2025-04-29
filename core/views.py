from django.shortcuts import render
from rest_framework import viewsets, permissions, filters
from .models import Question, Answer
from .serializers import QuestionSerializer, AnswerSerializer
from .pagination import QuestionPagination
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import IsAnswerAuthorOrReadOnly, IsQuestionAuthor
from rest_framework.decorators import action

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
    queryset = Answer.objects.all().order_by('-created_at')
    serializer_class = AnswerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAnswerAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated, IsQuestionAuthor])
    def accept(self, request, pk=None):
        answer = self.get_object()

        # Unmark all other answers to this question
        Answer.objects.filter(question=answer.question).update(is_accepted=False)
        answer.is_accepted = True
        answer.save()

        return Response({'status': 'answer accepted'}, status=status.HTTP_200_OK)


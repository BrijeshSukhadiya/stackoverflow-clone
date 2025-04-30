from django.shortcuts import render
from rest_framework import viewsets, permissions, filters, status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action

from .models import Question, Answer, Vote
from .serializers import (
    QuestionSerializer,
    AnswerSerializer,
    UserRegisterSerializer,
    UserProfileSerializer
)
from .pagination import QuestionPagination
from .permissions import IsAnswerAuthorOrReadOnly, IsQuestionAuthor
from django.core.mail import send_mail

User = get_user_model()

# -------------------- Questions --------------------
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

# -------------------- Answers --------------------
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

# -------------------- Voting --------------------
class VoteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        model_type = request.data.get('model')
        obj_id = request.data.get('id')
        vote_value = int(request.data.get('vote'))  # 1 or -1

        if model_type not in ['question', 'answer'] or vote_value not in [-1, 1]:
            return Response({'error': 'Invalid input'}, status=status.HTTP_400_BAD_REQUEST)

        model = Question if model_type == 'question' else Answer

        try:
            content_object = model.objects.get(pk=obj_id)
        except model.DoesNotExist:
            return Response({'error': 'Object not found'}, status=status.HTTP_404_NOT_FOUND)

        content_type = ContentType.objects.get_for_model(model)

        vote, created = Vote.objects.update_or_create(
            user=request.user,
            content_type=content_type,
            object_id=obj_id,
            defaults={'vote': vote_value}
        )

        return Response({'status': 'voted', 'vote': vote_value}, status=status.HTTP_200_OK)

# -------------------- User Registration --------------------
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]

# -------------------- User Profile --------------------
class UserProfileView(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

# Inside AnswerViewSet
@action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated, IsQuestionAuthor])
def accept(self, request, pk=None):
    answer = self.get_object()

    # Unmark all other answers to this question
    Answer.objects.filter(question=answer.question).update(is_accepted=False)
    answer.is_accepted = True
    answer.save()

    # Notify answer author
    if answer.author.email:
        send_mail(
            subject='Your Answer was Accepted!',
            message=f'Hi {answer.author.username},\n\n'
                    f'Your answer to "{answer.question.title}" was accepted by the question author.',
            from_email=None,
            recipient_list=[answer.author.email],
            fail_silently=True
        )

    return Response({'status': 'answer accepted'}, status=status.HTTP_200_OK)

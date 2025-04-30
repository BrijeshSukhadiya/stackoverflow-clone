from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import QuestionViewSet, AnswerViewSet, VoteView, RegisterView, UserProfileView

router = DefaultRouter()
router.register(r'questions', QuestionViewSet)
router.register(r'answers', AnswerViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('vote/', VoteView.as_view(), name='vote'),

    # User Management
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', UserProfileView.as_view(), name='profile'),
]

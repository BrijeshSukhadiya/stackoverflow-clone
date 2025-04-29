from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

# --- User ---
class CustomUser(AbstractUser):
    reputation = models.IntegerField(default=0)

# --- Question ---
class Question(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    body = models.TextField()
    tags = models.CharField(max_length=255)  # Comma-separated
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    @property
    def vote_count(self):
        from django.contrib.contenttypes.models import ContentType
        from .models import Vote
        content_type = ContentType.objects.get_for_model(self)
        return Vote.objects.filter(content_type=content_type, object_id=self.id).aggregate(score=models.Sum('vote'))['score'] or 0

# --- Answer ---
class Answer(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")
    body = models.TextField()
    is_accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Answer by {self.author} on {self.question}'

    @property
    def vote_count(self):
        from django.contrib.contenttypes.models import ContentType
        from .models import Vote
        content_type = ContentType.objects.get_for_model(self)
        return Vote.objects.filter(content_type=content_type, object_id=self.id).aggregate(score=models.Sum('vote'))['score'] or 0

# --- Generic Vote ---
class Vote(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    vote = models.SmallIntegerField(choices=((1, 'Upvote'), (-1, 'Downvote')))

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        unique_together = ('user', 'content_type', 'object_id')  # One vote per user per object

    def __str__(self):
        return f"{self.user} voted {self.vote} on {self.content_object}"

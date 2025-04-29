from rest_framework import serializers
from .models import Question, Answer, Vote, CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'reputation')

class QuestionSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Question
        fields = '__all__'
        read_only_fields = ("author", "created_at",)

class AnswerSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    fields = '__all__'
    read_only_fields = ('author', 'is_accepted', 'created_at')

    class Meta:
        model = Answer
        fields = '__all__'


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = '__all__'
        read_only_fields = ('user',)
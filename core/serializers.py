from rest_framework import serializers
from .models import Question, Answer, Vote, CustomUser

# -------------------- User Serializers --------------------
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'reputation')

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'reputation')

# -------------------- Question Serializer --------------------
class QuestionSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Question
        fields = '__all__'
        read_only_fields = ('author', 'created_at',)

# -------------------- Answer Serializer --------------------
class AnswerSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Answer
        fields = '__all__'
        read_only_fields = ('author', 'is_accepted', 'created_at')

# -------------------- Vote Serializer --------------------
class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = '__all__'
        read_only_fields = ('user',)

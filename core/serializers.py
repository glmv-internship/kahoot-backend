from core.models import User, Quiz, Poll, Game, UserResult, PollOption
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        
class PollOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PollOption
        fields = '__all__'

class PollSerializer(serializers.ModelSerializer):
    options = PollOptionSerializer(many=True)

    class Meta:
        model = Poll
        fields = '__all__'
    def create(self, validated_data):
        options_data = validated_data.pop('options', [])
        poll = Poll.objects.create(**validated_data)
        for option_data in options_data:
            PollOption.objects.create(poll=poll, **option_data)
        return poll

class QuizSerializer(serializers.ModelSerializer):
    polls = PollSerializer(many=True, read_only=True)
    class Meta:
        model = Quiz
        fields = '__all__'
        
class GameSerializer(serializers.ModelSerializer):
    join_code = serializers.CharField(read_only=True)
    class Meta:
        model = Game
        fields = '__all__'
        
    def create(self, validated_data : dict):
        quiz_id = validated_data.pop('quiz_id')
        host_uid = validated_data.pop('host_uid')
        quiz = Quiz.objects.get(pk=quiz_id)
        host = User.objects.get(uid=host_uid)
        join_code = Game.generate_join_code()
        validated_data['join_code'] = join_code
        game = Game.objects.create(quiz=quiz, host=host, **validated_data)
        return game
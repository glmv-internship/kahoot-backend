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
    host_uid = serializers.CharField(write_only=True)
    host = UserSerializer(read_only=True)
    # quiz = QuizSerializer(read_only=True)
    players = UserSerializer(many=True,read_only=True)
    class Meta:
        model = Game
        fields = ['id','host','host_uid','created_time','quiz','join_code','is_active','started_at','players']
        # depth = 1
        read_only_fields = ['join_code','is_active','started_at','created_time']

        
    def create(self, validated_data : dict):

        host_uid=validated_data.pop('host_uid')
        host = User.objects.get(uid=host_uid)
        join_code = Game.generate_join_code()
        validated_data['join_code'] = join_code
        game = Game.objects.create(host=host,**validated_data)
        return game
    def to_representation(self, instance):
        
        data = super().to_representation(instance)
        data['quiz'] = QuizSerializer(Quiz.objects.get(id=instance.quiz.id)).data
        return data
    
class GameDetailSerializer(serializers.ModelSerializer):
    host = UserSerializer(read_only=True)
    players = UserSerializer(many=True,read_only=True)
    quiz = QuizSerializer(read_only=True)
    class Meta:
        model = Game
        fields = ['id','host','quiz','created_time','join_code','is_active','started_at','players']
        read_only_fields = ['created_time']
        
    def create(self, validated_data : dict):

        host_uid=validated_data.pop('host_uid')
        host = User.objects.get(uid=host_uid)
        join_code = Game.generate_join_code()
        validated_data['join_code'] = join_code
        game = Game.objects.create(host=host,**validated_data)
        return game
    def to_representation(self, instance):
        instance.host_uid = instance.host.uid
        return super().to_representation(instance)
    
class UserResultSerializer(serializers.ModelSerializer):   
    # user = UserSerializer(read_only=True)
    # game = GameSerializer(read_only=True)
    class Meta:
        model = UserResult
        fields = '__all__'
        
    def to_representation(self, instance):
        # instance.game = GameSerializer(Game.objects.get(id=instance.game.id)).instance
        # print(instance.game)
        data = super().to_representation(instance)
        print(data)
        data['game'] = GameSerializer(Game.objects.get(id=instance.game.id)).data
        return data
    
    
    
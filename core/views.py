from core.models import User
from rest_framework import generics, views, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from core.serializers import UserSerializer, QuizSerializer, PollSerializer, GameSerializer, GameDetailSerializer, UserResultSerializer
from core.models import Quiz, Poll, Game, UserResult
from django.db.models import Sum
import logging

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'uid'

class UserCreate(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class QuizDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Quiz.objects.select_related('user').prefetch_related('polls').all()  # Optimize with select_related and prefetch_related
    serializer_class = QuizSerializer
    lookup_field = 'id'

class QuizCreate(generics.ListCreateAPIView):
    queryset = Quiz.objects.select_related('user').prefetch_related('polls').all()  # Optimize with select_related and prefetch_related
    serializer_class = QuizSerializer

class AddPollToQuiz(views.APIView):
    def post(self, request, quiz_id):
        try:
            quiz = Quiz.objects.get(pk=quiz_id)
        except Quiz.DoesNotExist:
            return Response({'error': 'Quiz not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = PollSerializer(data=request.data)
        if serializer.is_valid():
            poll = serializer.save(quiz=quiz)
            return Response(PollSerializer(poll).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ShowUserQuizzes(views.APIView):
    def get(self, request, uid):
        try:
            user = User.objects.prefetch_related('quizzes__questions').get(uid=uid)  # Optimize with prefetch_related
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        quizzes = user.quizzes.all()
        return Response(QuizSerializer(quizzes, many=True).data)

class GamesList(generics.ListCreateAPIView):
    queryset = Game.objects.select_related('quiz').prefetch_related('players').all()  # Optimize with select_related and prefetch_related
    serializer_class = GameSerializer

@api_view(['POST'])
def add_player_to_game(request, game_code, user_id):
    try:
        game = Game.objects.prefetch_related('players').get(join_code=game_code)  # Optimize with prefetch_related
        user = User.objects.get(uid=user_id)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    except Game.DoesNotExist:
        return Response({'error': 'Game not found'}, status=status.HTTP_404_NOT_FOUND)

    if user.games.filter(is_active=True).exists():
        return Response({'error': 'User already in game'}, status=status.HTTP_406_NOT_ACCEPTABLE)

    game.players.add(user)
    game.save()

    return Response(GameSerializer(game).data, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def delete_player_from_game(request, game_code, user_id):
    try:
        game = Game.objects.prefetch_related('players').get(join_code=game_code)  # Optimize with prefetch_related
        user = User.objects.get(uid=user_id)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    except Game.DoesNotExist:
        return Response({'error': 'Game not found'}, status=status.HTTP_404_NOT_FOUND)

    if not game.players.contains(user):
        return Response({'error': 'User not in this game'}, status=status.HTTP_406_NOT_ACCEPTABLE)

    game.players.remove(user)
    game.save()

    return Response(GameSerializer(game).data, status=status.HTTP_201_CREATED)

class GameDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Game.objects.select_related('quiz').prefetch_related('players', 'game_results__user').all()  # Optimize with select_related and prefetch_related
    serializer_class = GameDetailSerializer
    lookup_field = 'join_code'

@api_view(['GET'])
def user_stats(request, uid):
    try:
        user = User.objects.prefetch_related('results__game__quiz').get(uid=uid)  # Optimize with prefetch_related
        user_stats_data = {
            'username': user.nickname,
            'uid': user.uid,
            'total_games_played': user.results.count(),
            'total_score': user.results.aggregate(Sum('score'))['score__sum'] or 0,
            'last_5_games': [
                {
                    'game_id': result.game.id,
                    'game_name': result.game.quiz.name,
                    'score': result.score,
                    'total_questions': result.game.quiz.polls.count(),
                    'date_played': result.joined_at.strftime('%b %d, %Y, %I:%M %p'),
                }
                for result in user.results.order_by('-id')[:5]
            ]
        }
        return Response(user_stats_data, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logging.error(e)
        return Response({'error': 'An error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UserResultList(generics.ListCreateAPIView):
    queryset = UserResult.objects.select_related('user', 'game').all()  # Optimize with select_related
    serializer_class = UserResultSerializer

    def post(self, request, uid):
        try:
            user = User.objects.get(uid=uid)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserResultSerializer(data=request.data)
        if serializer.is_valid():
            result = serializer.save(user=user)
            return Response(UserResultSerializer(result).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserResultDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserResult.objects.select_related('user', 'game').all()  # Optimize with select_related
    serializer_class = UserResultSerializer
    lookup_field = 'id'

@api_view(['GET'])
def game_standings(request, game_id):
    try:
        game = Game.objects.prefetch_related('game_results__user').get(id=game_id)  # Optimize with prefetch_related
        results = game.game_results.order_by('-score')
        standings = []
        place = 0
        for result in results:
            place += 1
            data_ = {
                'user': UserSerializer(result.user).data,
                'score': result.score,
                'place': place,
            }
            standings.append(data_)
        return Response(standings, status=status.HTTP_200_OK)
    except Game.DoesNotExist:
        return Response({'error': 'Game not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logging.error(e)
        return Response({'error': 'An error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

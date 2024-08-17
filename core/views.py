from core.models import User
from rest_framework import generics,views,status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from core.serializers import UserSerializer, QuizSerializer, PollSerializer, GameSerializer,GameDetailSerializer, UserResultSerializer
from core.models import Quiz, Poll, Game, UserResult
import logging
class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'uid'
    
class UserCreate(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class QuizDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    lookup_field = 'id'
    
class QuizCreate(generics.ListCreateAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer

class AddPollToQuiz(views.APIView):
    def post(self, request, quiz_id):   
        try:
            quiz = Quiz.objects.get(pk=quiz_id)
        except Quiz.DoesNotExist:
            return Response({'error': 'Quiz not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Use the PollSerializer to validate and save the Poll and its options
        serializer = PollSerializer(data=request.data)
        if serializer.is_valid():
            # Save the Poll instance
            poll = serializer.save(quiz=quiz)
            
            # Optionally, you can also handle saving PollOptions manually if needed
            return Response(PollSerializer(poll).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class ShowUserQuizzes(views.APIView):
    def get(self, request, uid):
        try:
            user = User.objects.get(uid=uid)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        quizzes = user.quizzes.all()
        return Response(QuizSerializer(quizzes, many=True).data)
    
class GamesList(generics.ListCreateAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    
@api_view(['POST'])
def add_player_to_game(request,game_code,user_id):
    try:
        user = User.objects.get(uid=user_id)
    except:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
    try: 
        game = Game.objects.get(join_code=game_code)
    except:
        return Response({'error': 'Game not found'}, status=status.HTTP_404_NOT_FOUND)
    if user.games.filter(is_active=True).exists():
        return Response({'error': 'User already in game'}, status=status.HTTP_406_NOT_ACCEPTABLE)
    game.players.add(user)
    game.save()
    
    return Response(GameSerializer(game).data, status=status.HTTP_201_CREATED)
@api_view(['POST'])
def delete_player_from_game(request,game_code,user_id):
    try:
        user = User.objects.get(uid=user_id)
    except:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
    try: 
        game = Game.objects.get(join_code=game_code)
    except:
        return Response({'error': 'Game not found'}, status=status.HTTP_404_NOT_FOUND)
    if not game.players.contains(user):
        return Response({'error': 'User not in this game'}, status=status.HTTP_406_NOT_ACCEPTABLE)
    game.players.remove(user)
    game.save()
    
    return Response(GameSerializer(game).data, status=status.HTTP_201_CREATED)

class GameDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Game.objects.all()
    serializer_class = GameDetailSerializer
    lookup_field = 'join_code'
@api_view(['GET'])
def user_stats(request,uid):
    try:
        try: 
            user = User.objects.get(uid=uid)
        except:
            return Response({'error':'User not found'}, status=status.HTTP_404_NOT_FOUND)
        games = user.results.count()
        data = dict()
        data['played_games'] = games
        data['last_results'] = []
        results = user.results.order_by('-id')
        for result in results:
            result_ = dict()
            result_['game'] = GameSerializer(result.game).data
            result_['score'] = result.score
            data['last_results'].append(result_)
        print(data)
        return Response(data,status=status.HTTP_200_OK)
    except Exception as e:
        logging.error(e)
class UserResultList(generics.ListCreateAPIView):
    queryset = UserResult.objects.all()
    serializer_class = UserResultSerializer
    def post(self, request, uid):
        try:
            user = User.objects.get(uid=uid)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Use the UserResultSerializer to validate and save the UserResult
        serializer = UserResultSerializer(data=request.data)
        if serializer.is_valid():
            # Save the UserResult instance
            result = serializer.save(user=user)
            return Response(UserResultSerializer(result).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserResultDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserResult.objects.all()
    serializer_class = UserResultSerializer
    lookup_field = 'id'
@api_view(['GET'])
def game_standings(request, game_id):
    try:
        game = Game.objects.get(id=game_id)
        results = game.game_results.order_by('-score')
        standings = []
        place = 0
        for result in results:
            place = place + 1
            data_= dict()
            data_['user'] = UserSerializer(result.user).data
            data_['score'] = result.score
            data_['place'] = place
            standings.append(data_)
        # print(standings)
        return Response(standings,status=status.HTTP_200_OK    )
    except Exception as e:
        return Response(e, status=status.HTTP_400_BAD_REQUEST)
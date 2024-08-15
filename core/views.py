from core.models import User
from rest_framework import generics,views,status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from core.serializers import UserSerializer, QuizSerializer, PollSerializer, GameSerializer
from core.models import Quiz, Poll, Game
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
    

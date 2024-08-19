from django.urls import path
from core.views import UserCreate, UserDetail, AddPollToQuiz, ShowUserQuizzes, QuizCreate,QuizDetail, GamesList, add_player_to_game,delete_player_from_game, GameDetail, user_stats, UserResultDetail, UserResultList, game_standings
urlpatterns = [
    path('users/', UserCreate.as_view(), name='user_create'),
    path('users/<uid>/', UserDetail.as_view(), name='user_detail'),
    path('users/<uid>/quizzes/', ShowUserQuizzes.as_view(),name='user_quizzes'),
    path('quiz/', QuizCreate.as_view(),name='quiz_create' ),
    path('quiz/<int:id>/', QuizDetail.as_view(),name='quiz_detail'),
    path('quiz/<int:quiz_id>/add_poll/', AddPollToQuiz.as_view(),name='quiz_add_poll'),
    path('games/', GamesList.as_view(),name="games"),
    path('game/<game_code>/add/<user_id>/',add_player_to_game, name="add_user_to_game"),
    path('game/<game_code>/delete/<user_id>/',delete_player_from_game,name="delete_user_from_game"),
    path('game/<join_code>/',GameDetail.as_view(),name="Game detail"),
    path('users/<uid>/stats/',user_stats,name='user_stats'),
    path('users/<uid>/results/',UserResultList.as_view(), name="user_detail"),
    path('result/<id>/',UserResultDetail.as_view(),name="change_result"),
    path('standings/<game_id>/', game_standings,name="game_standings")
]

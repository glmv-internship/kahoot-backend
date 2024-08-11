from django.urls import path
from core.views import UserCreate, UserDetail, AddPollToQuiz, ShowUserQuizzes, QuizCreate,QuizDetail
urlpatterns = [
    path('users/', UserCreate.as_view(), name='user_create'),
    path('users/<int:uid>/', UserDetail.as_view(), name='user_detail'),
    path('users/<int:uid>/quizzes/', ShowUserQuizzes.as_view(),name='user_quizzes'),
    path('quiz/', QuizCreate.as_view(),name='quiz_create' ),
    path('quiz/<int:id>/', QuizDetail.as_view(),name='quiz_detail'),
    path('quiz/<int:quiz_id>/add_poll', AddPollToQuiz.as_view(),name='quiz_add_poll')
]

from typing import Any
from core.models import User
class String:
    def __init__(self,uz,en) -> None:
        self.uz = uz
        self.en = en
    def get(self,id ) -> Any:
        user = User.objects.get(uid=id)
        if user.language == 'uz':
            return self.uz
        return self.en
        
        # return super().__getattribute__(__name)
        pass

class Strings:
    
    choose_language = String('Tilni tanlang','Choose language')
    welcome = String('Assalomu alaykum! Botga xush kelibsiz!\nQuyidagilardan birini tanlang👇','Hello! Welcome to the bot!\nChoose one of the following👇')
    join_the_game_button = String("O'yinga qo'shilish🧩",'Join the game🧩')
    create_the_game_button = String("O'yin yaratish🎮",'Create the game🎮')
    create_the_quiz_button = String("Test yaratish📝",'Create the quiz📝')
    # nickname
    change_the_nickname_button = String("Nickname o'zgartirish👤",'Change the nickname👤')
    request_nickname = String("Iltimos, nickname ingizni kiriting👤\nHozirgi nickname: {current_nickname}",'Please enter your nickname👤\nYour current nickname: {current_nickname}')
    nickname_changed = String("Nickname o'zgartirildi✅",'Nickname changed✅')
    nickname_wrong = String("Nickname xato! Iltimos, qaytadan kiriting👤",'Nickname wrong! Please enter again👤')
    
    # quiz
    quiz_name = String("Test nomini kiriting📝",'Enter the name of the quiz📝')
    quiz_description = String("Testning tavsifini kiriting📝",'Enter the description of the quiz📝')
    quiz_question_duration = String("Savollar uchun vaqt🕒",'Duration for questions🕒')
    quiz_number_of_questions = String("Savollar soni📝",'Number of questions📝')
    quiz_send_poll = String("Savolni poll ko'rinishida yuboring📝",'Send the question in poll format📝')
    quiz_success = String("Test muvaffaqiyatli yaratildi✅",'Quiz created successfully✅')
    quiz_send_quiz_error = String('Poll quiz ko\'rinishida yuborilishi kerak!','Poll quiz should be sent!')
    
    cancel = String("Bekor qilish❌",'Cancel❌')
    
    # join
    enter_the_game_code = String("O'yin kodini kiriting📝",'Enter the game code📝')
    
    # more
    more_quiz = String("Boshqa testlar📝",'More quizzes📝')
    
    # create game
    quiz_list = String("Siz yaratgan testlar📝",'Quizzes you created📝')
# strings = Strings()
# print(strings.choose_language.id1)
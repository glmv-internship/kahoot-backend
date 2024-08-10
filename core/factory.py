
import telebot
from core.strings import Strings
from django.conf import settings
import logging
from core.models import User
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
import re
from threading import Thread
from core.quiz_factory import QuizFactory, generate_reply_markup, generate_cancel_markup, generate_cancel_inline_markup, generate_user_quiz_markup
from core.models import Quiz
# logger = telebot.logger
# telebot.logger.setLevel(logging.DEBUG)
bot = telebot.TeleBot(settings.BOT_TOKEN)

def generate_lan_markup():
    choose_language_keyboard = InlineKeyboardMarkup()
    choose_language_keyboard.row_width = 2
    choose_language_keyboard.add(InlineKeyboardButton('Uzbek🇺🇿', callback_data='lan_uz'),InlineKeyboardButton('English🏴󠁧󠁢󠁥󠁮󠁧󠁿', callback_data='lan_en'))
    return choose_language_keyboard
def remove_markup(message):
    try:
        msg2 = bot.send_message(message.chat.id,'...', reply_markup=ReplyKeyboardRemove())
        bot.delete_message(message.chat.id, msg2.message_id)
    except Exception as e:
        logging.error(e)

strings = Strings()
@bot.message_handler(commands=['start'])
def command_start(message):
    try:
        # print("command")
        if message.chat.type != 'private':
            bot.send_message(message.chat.id, "Ooops! I can only work in private chats.")
            return
        if User.objects.filter(uid=message.chat.id).exists():
            
            bot.send_message(message.chat.id, strings.welcome.get(message.chat.id), reply_markup=generate_reply_markup(message.chat.id))
        else:
            
            bot.send_message(message.chat.id, strings.choose_language.en, reply_markup=generate_lan_markup())
        
        
    except Exception as e:
        logging.error(e)


@bot.callback_query_handler(func=lambda call: call.data.startswith('lan_'))
def callback_inline(call):
    try:
        user = User.objects.get_or_create(uid=call.message.chat.id)[0]
        lan = call.data.split('_')[1]
        user.language = lan
        user.nickname = call.message.chat.username if call.message.chat.username else call.message.chat.first_name
        user.save()
        bot.send_message(call.message.chat.id, strings.welcome.get(call.message.chat.id), reply_markup=generate_reply_markup(call.message.chat.id))
    except Exception as e:
        logging.error(e)
        
@bot.message_handler(func=lambda message: message.text == strings.change_the_nickname_button.en or message.text == strings.change_the_nickname_button.uz)
def change_nickname(message):
    try:
        if User.objects.filter(uid=message.chat.id).exists() is False:
            bot.send_message(message.chat.id, strings.choose_language.en, reply_markup=generate_lan_markup())
            return
        curr_nickname = User.objects.get(uid=message.chat.id).nickname
        msg = bot.send_message(message.chat.id, strings.request_nickname.get(message.chat.id).format(current_nickname=curr_nickname), reply_markup=ReplyKeyboardRemove())
        bot.register_next_step_handler(msg, change_nickname_handler)
    except Exception as e:
        logging.error(e)

def change_nickname_handler(message):
    try:
        nickname = message.text
        if " " in nickname:
            bot.send_message(message.chat.id, strings.nickname_wrong.get(message.chat.id), reply_markup=generate_reply_markup(message.chat.id))
            return
        user = User.objects.get(uid=message.chat.id)
        user.nickname = message.text
        user.save()
        bot.send_message(message.chat.id, strings.nickname_changed.get(message.chat.id), reply_markup=generate_reply_markup(message.chat.id))
        
    except Exception as e:
        logging.error(e)


@bot.message_handler(func=lambda message: message.text == strings.create_the_quiz_button.en or message.text == strings.create_the_quiz_button.uz)
def create_quiz(message):
    try:
        if User.objects.filter(uid=message.chat.id).exists() is False:
            bot.send_message(message.chat.id, strings.choose_language.en, reply_markup=generate_lan_markup())
            return
        user = User.objects.get(uid=message.chat.id)
        user.temp_data = "quiz"
        user.save()
        msg = bot.send_message(message.chat.id, strings.quiz_name.get(message.chat.id), reply_markup=generate_cancel_inline_markup(message.chat.id))
        # bot.edit_message_reply_markup(chat_id=message.chat.id, message_id=message.message_id, reply_markup=None)
        remove_markup()
        bot.register_next_step_handler(msg, create_quiz_handler)
    except Exception as e:
        logging.error(e)
def create_quiz_handler(message):
    try:
        user = User.objects.get(uid=message.chat.id)
        quiz = QuizFactory(user, Quiz.objects.create(user=user, name=message.text), bot)
        quiz.set_description()
    except Exception as e:
        logging.error(e)
@bot.callback_query_handler(func=lambda call: call.data == 'cancel')
def cancel(call):
    try:
        message = call.message
        user = User.objects.get(uid=message.chat.id)
        user.temp_data = ""
        user.save()
        bot.send_message(message.chat.id, strings.welcome.get(message.chat.id), reply_markup=generate_reply_markup(message.chat.id))
    except Exception as e:
        logging.error(e)
        
# Join the game 
@bot.message_handler(func=lambda message: message.text == strings.join_the_game_button.en or message.text == strings.join_the_game_button.uz)
def join_the_game(message: telebot.types.Message):
    try:
        if User.objects.filter(uid=message.chat.id).exists() is False:
            bot.send_message(message.chat.id, strings.choose_language.en, reply_markup=generate_lan_markup())
            return
        user = User.objects.get(uid=message.chat.id)
        user.temp_data = "join"
        user.save()
        bot.send_message(message.chat.id, strings.enter_the_game_code.get(message.chat.id), reply_markup=generate_cancel_inline_markup(message.chat.id))
        bot.register_next_step_handler(message, join_the_game_step)
        remove_markup(message)
    except Exception as e:
        logging.error(e)
        
def join_the_game_step(message):
    try:
        bot.send_message(message.chat.id, "This feature is not available yet.")
    except Exception as e:
        logging.error(e)

@bot.message_handler(func=lambda message: message.text == strings.create_the_game_button.en or message.text == strings.create_the_game_button.uz)
def create_the_game(message):
    try:
        if User.objects.filter(uid=message.chat.id).exists() is False:
            bot.send_message(message.chat.id, strings.choose_language.en, reply_markup=generate_lan_markup())
            return
        if User.objects.get(uid=message.chat.id).nickname is None:
            bot.send_message(message.chat.id, strings.request_nickname.get(message.chat.id).format(current_nickname=""), reply_markup=ReplyKeyboardRemove())
            return
        if Quiz.objects.filter(user=User.objects.get(uid=message.chat.id)).exists() is False:
            bot.send_message(message.chat.id, "You have not created any quizzes yet.")
            return
        user = User.objects.get(uid=message.chat.id)
        user.temp_data = "game"
        user.save()
        bot.send_message(message.chat.id, strings.quiz_list.get(message.chat.id), reply_markup=generate_user_quiz_markup(user))
        # bot.send_message(message.chat.id, "This feature is not available yet.")
    except Exception as e:
        logging.error(e)

# Thread(target=bot.infinity_polling).start()
# bot.polling(allowed_updates=['message', 'callback_query'])
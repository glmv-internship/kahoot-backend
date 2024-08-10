from core.models import User, Quiz, Poll, PollOption
from core.strings import Strings
import telebot
from telebot.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import logging
# from core.factory import generate_reply_markup
strings = Strings()
def generate_reply_markup(id : int)->ReplyKeyboardMarkup:
    reply_markup = ReplyKeyboardMarkup(resize_keyboard=True)
    reply_markup.add(KeyboardButton(strings.join_the_game_button.get(id)),KeyboardButton(strings.create_the_game_button.get(id)))
    reply_markup.add(KeyboardButton(strings.create_the_quiz_button.get(id)),KeyboardButton(strings.change_the_nickname_button.get(id)))
    return reply_markup
def generate_cancel_markup(id : int)->ReplyKeyboardMarkup:
    reply_markup = ReplyKeyboardMarkup(resize_keyboard=True)
    reply_markup.add(KeyboardButton(strings.cancel.get(id)))
    return reply_markup
def generate_cancel_inline_markup(id : int):
    reply_markup = InlineKeyboardMarkup()
    
    reply_markup.add(InlineKeyboardButton(strings.cancel.get(id),callback_data='cancel'))
    return reply_markup
def generate_user_quiz_markup(user: User):
    reply_markup = InlineKeyboardMarkup()
    num = 0
    for quiz in Quiz.objects.filter(user=user):
        if num == 10:
            break
        num += 1
        reply_markup.add(InlineKeyboardButton(quiz.name,callback_data=f'quiz_{quiz.id}'))
    if Quiz.objects.filter(user=user).count() > 10:
        reply_markup.add(InlineKeyboardButton(strings.more_quiz.get(user.uid),callback_data='more'))
    return reply_markup
class QuizFactory:
    def __init__(self, user: User, quiz: Quiz, bot: telebot.TeleBot) -> None:
        self.user = user
        self.quiz = quiz
        self.bot = bot
        
    def set_description(self):
        try:
            self.bot.send_message(self.user.uid, strings.quiz_description.get(self.user.uid), reply_markup=generate_cancel_inline_markup(self.user.uid))
            self.bot.register_next_step_handler_by_chat_id(self.user.uid, self.set_duration)
        except Exception as e:
            logging.error(e)
    def set_duration(self, message: Message):
        try:
            self.quiz.description = message.text
            self.quiz.save()
            self.bot.send_message(self.user.uid, strings.quiz_question_duration.get(self.user.uid), reply_markup=generate_cancel_inline_markup(self.user.uid))
            self.bot.register_next_step_handler_by_chat_id(self.user.uid, self.set_number_of_questions)
        except Exception as e:
            logging.error(e)
    def set_number_of_questions(self, message: Message):
        try:
            self.quiz.duration = int(message.text)
            self.quiz.save()
            self.bot.send_message(self.user.uid, strings.quiz_number_of_questions.get(self.user.uid), reply_markup=generate_cancel_inline_markup(self.user.uid))    
            self.bot.register_next_step_handler_by_chat_id(self.user.uid, self.set_questions)
        except Exception as e:
            logging.error(e)
    def set_questions(self, message: Message):
        try:
            self.quiz.number_of_questions = int(message.text)
            self.quiz.save()
            Poll.objects.create(quiz=self.quiz, question=message.text)
            self.bot.send_message(self.user.uid, strings.quiz_send_poll.get(self.user.uid), reply_markup=generate_cancel_inline_markup(self.user.uid))
            self.bot.register_next_step_handler_by_chat_id(self.user.uid, self.get_poll)
        except Exception as e:
            logging.error(e)
    def get_poll(self, message: Message):
        try:
           
            # poll = Poll.objects.get(quiz=self.quiz, question=message.text)
            # PollOption.objects.create(poll=poll, option=message.text)
            if message.poll.type != 'quiz':
                self.bot.send_message(message.chat.id, strings.quiz_send_quiz_error.get(message.chat.id))
                self.bot.register_next_step_handler_by_chat_id(self.user.uid, self.get_poll)
                return
            poll = Poll.objects.get(quiz=self.quiz, question=message.poll.question,tip=message.poll.explanation)
            num = 0
            for option in message.poll.options:
                if num == message.poll.correct_option_id:
                    PollOption.objects.create(poll=poll, text=option.text, is_true=True)
                else:
                    PollOption.objects.create(poll=poll, text=option.text)
                num += 1
            self.bot.register_next_step_handler_by_chat_id(self.user.uid, self.get_poll)
            if self.quiz.polls.count() == self.quiz.number_of_questions:
                self.bot.send_message(self.user.uid, strings.quiz_success.get(self.user.uid), reply_markup=generate_reply_markup(self.user.uid))    
                # self.bot.register_next_step_handler_by_chat_id(self.user.uid, self.set_questions)
                return
        except Exception as e:
            logging.error(e)
        pass
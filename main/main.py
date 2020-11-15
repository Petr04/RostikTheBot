from telebot import TeleBot, types

from lib.rt_search import rt_search
from lib.dict_to_keyboard import dict_to_keyboard

import config


bot = TeleBot(config.bot_token)

class ChatData:
    def __init__(self):
        self.set_defaults()

    def set_defaults(self):
        self.section = None
        self.answers = None
        self.answer_index = None

    @property
    def current_answer(self):
        return self.answers[self.answer_index]

sections_keyboard = {
    'Интернет': 'internet',
    'Мобильная связь': 'mobile',
    'Телевидение': 'hometv',
    'Телефон': 'phone',
    'Видеонаблюдение': 'video',
}

yes_no_keyboard = {
    'Да': 'yes',
    'Нет': 'no',
}

chats_data = {}

def is_new_user(message):
    return message.chat.id not in chats_data

@bot.message_handler(func=is_new_user)
def new_user_message_handler(message):
    chats_data[message.chat.id] = ChatData()
    start_handler(message)

@bot.message_handler(commands=['start'])
def start_handler(message):
    bot.send_message(message.chat.id, 'Здравствуйте')
    main_handler(message)

def cannot_answer(message):
    data = chats_data[message.chat.id]
    bot.send_message(message.chat.id,
        'Я не могу найти ответ на ваш вопрос.'
        ' Придётся перенаправить вас к оператору.'
        ' Вы можете позвонить ему по телефону +7 (800) 100-0-800'
        ' или написать в ВКонтакте: https://vk.com/rostelecom'
    )
    data.set_defaults()
    main_handler(message)

@bot.message_handler(content_types=['text'])
def main_handler(message):
    print(list(chats_data.keys())[0])
    data = chats_data[message.chat.id]
    print(message.text)

    if data.section == None:
        bot.send_message(message.chat.id,
            'Выберите категорию вопроса',
            reply_markup=dict_to_keyboard(sections_keyboard)
        )
    elif data.answers == None:
        bot.send_message(message.chat.id, 'Ищу ответ на вопрос...')
        data.answers = rt_search(message.text, data.section)
        if len(data.answers) == 0:
            cannot_answer(message)
            return

        data.answer_index = 0

        bot.send_message(message.chat.id,
            'Вот статья по этому вопросу\n' + data.current_answer)
        bot.send_message(message.chat.id,
            'Помогло?',
            reply_markup=dict_to_keyboard(yes_no_keyboard)
        )

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    data = chats_data[call.message.chat.id]

    if data.answers == None:
        data.section = call.data
        bot.send_message(call.message.chat.id, 'Какая у вас проблема или вопрос?')
    elif call.data == 'no':
        data.answer_index += 1
        if data.answer_index >= len(data.answers):
            cannot_answer(call.message)
            return

        bot.send_message(call.message.chat.id,
            'Ещё статья по этому вопросу\n' + data.current_answer)
        bot.send_message(call.message.chat.id,
            'Помогло ли на этот раз?',
            reply_markup=dict_to_keyboard(yes_no_keyboard)
        )
    else:
        bot.send_message(call.message.chat.id,
            'Ну и отлично'
        )
        data.set_defaults()
        main_handler(call.message)

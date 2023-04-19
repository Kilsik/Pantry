import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
)


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

CHOICE1, CHOICE2, CHOICE3 = range(3)


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, 
        text="Мы расширяем Ваше пространство хранения вещей")


def build_menu(buttons, n_cols,
               header_buttons=None,
               footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, [header_buttons])
    if footer_buttons:
        menu.append([footer_buttons])
    return menu


def orderbox(update, _):
    button_list = []
    for addr in adresses:
        button_list.append(InlineKeyboardButton(addr,
            callback_data=adresses.index(addr)))

    reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=2))
    update.message.reply_text('Пожалуйста, выберите адрес хранения:',
        reply_markup=reply_markup)
    return CHOICE1
    

def delivery_from_method(update, _):
    query = update.callback_query
    variant = query.data
    query.answer()
    button_list = [
        InlineKeyboardButton('Я сам привезу вещи', callback_data='self'),
        InlineKeyboardButton('Вы вывезите вещи', callback_data='you'),
    ]
    reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=2))
    query.edit_message_text(text=f"Вы выбрали адрес хранения: {variant} \
        \nМы предлагаем бесплатную доставку Ваших вещей из дома на хранение. \
        Хотите воспользоваться?", reply_markup=reply_markup)
    return CHOICE2


def delivery_method(update, _):
    query = update.callback_query
    variant = query.data
    query.answer()
    query.edit_message_text(text="Благодарим за заказ")
    return ConversationHandler.END


adresses = ['Адрес 1', 'Адрес 2', 'Адрес 3']
SELECTED_ADDRESS = list(range(len(adresses)))


if __name__ == '__main__':
    TOKEN = '6265890695:AAEFXFkuGxpElm_qaodxgRGSGg_UYud2vkg'

    updater = Updater(token=TOKEN)

    app = updater.dispatcher

    app.add_handler(CommandHandler('start', start))
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('orderbox', orderbox)],
        states = {
            CHOICE1: [CallbackQueryHandler(delivery_from_method)],
        },
        fallbacks = [CallbackQueryHandler(delivery_method)]
    )
    app.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()
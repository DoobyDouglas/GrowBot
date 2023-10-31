from telegram import Update
from telegram.ext import (
    Updater,
    ConversationHandler,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackContext,
)
from dotenv import load_dotenv
import os
from messages import (
    INVALID_NUM,
    HELLO,
    ENTRY_BOX_WIDTH,
    ENTRY_BOX_DEPTH,
    CALC_LIGHT_RESULT
)
from utilits import WIDTH, DEPTH
from buttons import CALC_LIGHT_BUTTON
from calculations import calculate_light


load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')


def send_message(
        update: Update,
        context: CallbackContext,
        message: str,
        **kwargs,
        ) -> None:
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=message,
        **kwargs,
    )


def wake_up(update: Update, context: CallbackContext) -> None:
    kwargs = {}
    kwargs['reply_markup'] = CALC_LIGHT_BUTTON
    message = HELLO.format(name=update.message.chat.username)
    send_message(update, context, message, **kwargs)


def calculate_box(update: Update, context: CallbackContext) -> int:
    context.user_data['calculate_light'] = {}
    send_message(update, context, ENTRY_BOX_WIDTH)
    return WIDTH


def get_box_width(update: Update, context: CallbackContext) -> int:
    try:
        context.user_data['calculate_light']['box_width'] = float(
            update.message.text
        )
        send_message(update, context, ENTRY_BOX_DEPTH)
        return DEPTH
    except ValueError:
        send_message(update, context, INVALID_NUM)
        return WIDTH


def get_box_depth(update: Update, context: CallbackContext) -> int:
    try:
        context.user_data['calculate_light']['box_depth'] = float(
            update.message.text
        )
        square, led_min, led_max = calculate_light(
            context.user_data['calculate_light']['box_width'],
            context.user_data['calculate_light']['box_depth']
        )
        kwargs = {}
        kwargs['reply_markup'] = CALC_LIGHT_BUTTON
        message = CALC_LIGHT_RESULT.format(
            square=square, LED_min=led_min, LED_max=led_max
        )
        send_message(update, context, message, **kwargs)
        return ConversationHandler.END
    except ValueError:
        send_message(update, context, INVALID_NUM)
        return DEPTH


def main() -> None:
    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('calculate_light', calculate_box)],
        states={
            WIDTH: [MessageHandler(Filters.text, get_box_width)],
            DEPTH: [MessageHandler(Filters.text, get_box_depth)],
        },
        fallbacks=[]
    )
    updater = Updater(token=TELEGRAM_TOKEN)
    updater.dispatcher.add_handler(CommandHandler('start', wake_up))
    updater.dispatcher.add_handler(conversation_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

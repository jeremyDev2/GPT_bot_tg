from settings import config
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)
from services.open_ai_chat import utils, client
import logging


openai_client = client.OpenAIClient()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = utils.load_welcome_text("gpt")
    image = utils.get_images_path("gpt")

    with open(image, "rb") as new_img:
        await update.message.reply_photo(
            photo=new_img,
            caption=text,
            disable_notification=False,
            parse_mode="Markdown"
        )

async def random_fact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = utils.load_welcome_text("random")
    image_path = utils.get_images_path("random")
    prompt = utils.get_prompts("random_prompt")

    keyboard = [
        [InlineKeyboardButton("One more fact", callback_data="random_again")],
        [InlineKeyboardButton("End", callback_data="finish")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    context.user_data['mode'] = 'random'

    try:
        gpt_response = await openai_client.ask("", prompt)
        with open(image_path, 'rb') as photo:
            await update.message.reply_photo(
                photo=photo,
                caption=f"{text}\n\n{gpt_response}",
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )
    except Exception as e:
        logging.error(f"Error in random_fact: {e}")
        await update.message.reply_text("Sorry, error happened.")


async def gpt_interface(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = utils.load_welcome_text("main")
    image_path = utils.get_images_path("main")

    context.user_data['mode'] = 'gpt'

    with open(image_path, 'rb') as photo:
        await update.message.reply_photo(
            photo=photo,
            caption=text,
            parse_mode='Markdown'
        )


async def talk_with_personality(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = utils.load_welcome_text("famous_personality")
    image_path = utils.get_images_path("talk")

    keyboard = [
        [InlineKeyboardButton("Kurt Cobain", callback_data='talk_cobain')],
        [InlineKeyboardButton("Stephen Hawking", callback_data='talk_hawking')],
        [InlineKeyboardButton("Friedrich Nietzsche", callback_data='talk_nietzsche')],
        [InlineKeyboardButton("Freddie Mercury", callback_data='talk_queen')],
        [InlineKeyboardButton("J.R.R. Tolkien", callback_data='talk_tolkien')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    with open(image_path, 'rb') as photo:
        await update.message.reply_photo(
            photo=photo,
            caption=text,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )

async def quiz_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = utils.load_welcome_text("quiz")
    image_path = utils.get_images_path("quiz")

    keyboard = [
        [InlineKeyboardButton("History", callback_data='quiz_history')],
        [InlineKeyboardButton("Science", callback_data='quiz_science')],
        [InlineKeyboardButton("Arts", callback_data='quiz_art')],
        [InlineKeyboardButton("Sport", callback_data='quiz_sport')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    with open(image_path, 'rb') as photo:
        await update.message.reply_photo(
            photo=photo,
            caption=text,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )

async def text_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_mode = context.user_data.get('mode', '')
    user_text = update.message.text

    if user_mode == "gpt":
        prompt = utils.get_prompts("main_prompt")
        try:
            gpt_response = await openai_client.ask(user_text, prompt)
            await update.message.reply_text(gpt_response)
        except Exception as e:
            logging.error(f"Error in gpt mode: {e}")
            await update.message.reply_text("Error happened.")

    elif user_mode not in ("random_prompt", "main_prompt", "quiz_prompt"):
        prompt = utils.get_prompts()
        keyboard = [[InlineKeyboardButton("End", callback_data='finish')]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        try:
            gpt_response = await openai_client.ask(user_text, prompt)
            await update.message.reply_text(gpt_response, reply_markup=reply_markup)
        except Exception as e:
            logging.error(f"Error in talk mode: {e}")
            await update.message.reply_text("Error happened.")

    elif user_mode.startswith('quiz_'):
        topic = user_mode.split('_')[1]
        score = context.user_data.get('score', 0)

        if 'quiz_question' in context.user_data:
            try:
                check_prompt = f"User answered: '{user_text}' on question: '{context.user_data['quiz_question']}'. Say if it is right or not."
                gpt_response = await openai_client.ask(check_prompt, "You are a quiz expert. Check users' answers.")

                is_correct = "yes" in gpt_response.lower() or "right" in gpt_response.lower()
                if is_correct:
                    context.user_data['score'] = score + 1

                current_score = context.user_data.get('score', 0)

                keyboard = [
                    [InlineKeyboardButton("More questions", callback_data=f'quiz_{topic}')],
                    [InlineKeyboardButton("Change topic", callback_data='quiz_change_topic')],
                    [InlineKeyboardButton("End", callback_data='finish')]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)

                response_text = f"{gpt_response}\n\nYour score: {current_score}"
                await update.message.reply_text(response_text, reply_markup=reply_markup)

                del context.user_data['quiz_question']
            except Exception as e:
                logging.error(f"Error in quiz mode: {e}")
                await update.message.reply_text("Sorry, error happened. Try again later.")


async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'random_again':
        prompt = utils.get_prompts("random_prompt")
        try:
            gpt_response = await openai_client.ask("", prompt)

            keyboard = [
                [InlineKeyboardButton("One more fact", callback_data='random_again')],
                [InlineKeyboardButton("End", callback_data='finish')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            await query.edit_message_caption(
                caption=f"{utils.load_welcome_text('random')}\n\n{gpt_response}",
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )
        except Exception as e:
            logging.error(f"Error in random_again: {e}")
            await query.edit_message_caption("Sorry, error happened.")

    elif query.data == 'finish':
        context.user_data.clear()
        await start(update, context)

    elif query.data.startswith('talk_'):
        personality = query.data.split('_')[1]
        context.user_data['mode'] = query.data

        personality_images = {
            'cobain': 'talk_cobain',
            'hawking': 'talk_hawking',
            'nietzsche': 'talk_nietzsche',
            'queen': 'talk_queen',
            'tolkien': 'talk_tolkien'
        }

        image_path = utils.get_images_path(personality_images[personality])

        keyboard = [[InlineKeyboardButton("End", callback_data='finish')]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        with open(image_path, 'rb') as photo:
            await query.message.reply_photo(
                photo=photo,
                caption="You can start conversation! Write your message.",
                reply_markup=reply_markup
            )

    elif query.data.startswith('quiz_'):
        if query.data == 'quiz_change_topic':
            await quiz_game(update, context)
            return

        topic = query.data.split('_')[1]
        context.user_data['mode'] = query.data

        if 'score' not in context.user_data:
            context.user_data['score'] = 0

        topic_prompts = {
            'history': 'Create an interesting history question with 4 answers. Format: Question? A) ... B) ... C) ... D) ...',
            'science': 'Create an interesting science question with 4 answers. Format: Question? A) ... B) ... C) ... D) ...',
            'art': 'Create an interesting art question with 4 answers. Format: Question? A) ... B) ... C) ... D) ...',
            'sport': 'Create an interesting sport question with 4 answers. Format: Question? A) ... B) ... C) ... D) ...'
        }

        try:
            gpt_response = await openai_client.ask(topic_prompts[topic], utils.get_prompts("quiz"))
            context.user_data['quiz_question'] = gpt_response

            await query.edit_message_caption(
                caption=f"{gpt_response}\n\nWrite your answer (A, B, C or D):"
            )
        except Exception as e:
            logging.error(f"Error in quiz: {e}")
            await query.edit_message_caption("Sorry, error happened.")


app = ApplicationBuilder().token(config.TG_BOT_API_KEY).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("random", random_fact))
app.add_handler(CommandHandler("gpt", gpt_interface))
app.add_handler(CommandHandler("talk", talk_with_personality))
app.add_handler(CommandHandler("quiz", quiz_game))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_message_handler))
app.add_handler(CallbackQueryHandler(handle_callback))

app.run_polling()

import asyncio,logging,sys,json
from os import getenv
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, html, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart,Command, StateFilter
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, Message, ReplyKeyboardMarkup, ReplyKeyboardRemove, keyboard_button, message, reply_keyboard_markup
from aiogram.fsm.state import State,StatesGroup
from aiogram.fsm.context import FSMContext

from groq import Groq

load_dotenv()
TOKEN = getenv("BOT_TOKEN")
LLM = Groq(
    api_key= getenv("GROQ_API_KEY")
)

INLINE_DISH_IDEAS_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[
    [
     InlineKeyboardButton(text="🔄",callback_data="pressed reload"),
     InlineKeyboardButton(text="❌",callback_data="pressed X")
     ]
]
)

INLINE_CUSTOM_DISH_IDEAS_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[
    [
     InlineKeyboardButton(text="⬅",callback_data="custom_recipes_back_to_first"),
     InlineKeyboardButton(text="❌",callback_data="custom_recipes_main_menu")
     ]
]
)


REPLY_DISH_IDEAS_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='1️⃣'),
            KeyboardButton(text='2️⃣'),
            KeyboardButton(text='3️⃣'),
            KeyboardButton(text='4️⃣'),
            KeyboardButton(text='5️⃣')
        ],
        [
            KeyboardButton(text='6️⃣'),
            KeyboardButton(text='7️⃣'),
            KeyboardButton(text='8️⃣'),
            KeyboardButton(text='9️⃣'),
            KeyboardButton(text='🔟')
        ]
    ],
    resize_keyboard=True
)


REPLY_CUSTOM_DISH_IDEAS_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='1️⃣'),
            KeyboardButton(text='2️⃣'),
            KeyboardButton(text='3️⃣'),
            KeyboardButton(text='4️⃣'),
            KeyboardButton(text='5️⃣')
        ],
    ],
    resize_keyboard=True
)

IDEAS_INDEX = {
    '1️⃣':0,
    '2️⃣':1,
    '3️⃣':2,
    '4️⃣':3,
    '5️⃣':4,
    '6️⃣':5,
    '7️⃣':6,
    '8️⃣':7,
    '9️⃣':8,
    '🔟':9
}

MAIN_MENU_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[
    [
        KeyboardButton(text='🧠'),
        KeyboardButton(text='📝'),
        KeyboardButton(text='❓')
    ]
],
    resize_keyboard=True
)

FAQ_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='⬅',callback_data="faq_go_back")
        ]
    ]
)


DISH_IDEAS_RECIPE_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='⬅',callback_data="recipe_go_back"),
            InlineKeyboardButton(text='⭐',callback_data="recipe_add_fav")
        ]
    ]
)

INLINE_KEYBOARD_CUSTOM_RECIPE_MESSAGE = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="❌",callback_data="custom_recipe_message_back")
        ]
    ]
)


FAQ = f"""
The {html.bold("Chef-Brain BOT")} can generate random recipes. 🥗🥪🧆🥘👨‍🍳

Click 🧠 emoji to generate a unique recipes
Click ⭐emoji to see your favourite recipes
Click ⚙  to change your preferences

{html.bold("⬅  GO BACK TO MAIN MENU")}
"""

CUSTOM_RECIPE_TEXT = f"""
Please, write below what ingredients you have 🍆🥩🥚🧂
or describe what you want to eat!
The {html.bold("Chef-Brain BOT")} can create recipes based on a description alone!👨‍🍳🍳

❌ - go back to main menu
"""

dp = Dispatcher()

#defining state group
class RecipeFlow(StatesGroup):
    waiting_for_dish_idea = State()
    reading_faq = State()
    watching_recipe = State()
    writing_custom_recipe = State()





#NOTE: api calls, main logic

def completion(prompt,model):
    comp = LLM.chat.completions.create(model=model,
                                       messages=[
                                       {"role":"user","content":prompt}
                                       ],
                                       response_format={"type":"json_object"})
    return comp.choices[0].message.content

def text_prompt(prompt,model):
    comp = LLM.chat.completions.create(model=model,
                                       messages=[
                                       {"role":"user","content":prompt}
                                       ],)
    return comp.choices[0].message.content


def text_prompt_completion(prompt:str,model:str = "openai/gpt-oss-20b") -> str:
    return str(text_prompt(prompt,model))

def json_completion(prompt:str, model:str = "openai/gpt-oss-20b") -> dict:
    content = completion(prompt,model)
    return json.loads(content)

def get_dish_ideas(prev:list):
    dish_dict = json_completion(f"""
        Return a json array of 10 dish ideas,
        in the format {{dish_ideas:[string]}}.
        Do not include {prev}.
    """)
    # print(dish_dict)
    dishes = dish_dict.get("dish_ideas",[])
    return dishes


def format_dish_ideas(dishes:list):
    text = f"{html.bold("Suggested recipes:")}\n"
    for index,dish in enumerate(dishes,start=1):
        text += f"{html.bold(str(index))}. {dish}\n"

    text += f"""
    {html.bold("🔃 - refresh reicipes list")}
    {html.bold("❌ - go back to main menu")}
        """
    return text

def format_custom_dish_ideas(dishes:list):
    text = f"{html.bold("Suggested recipes:")}\n"
    for index,dish in enumerate(dishes,start=1):
        text += f"{html.bold(str(index))}. {dish}\n"

    text += f"""
    {html.bold("⬅ - go back to crafting recipe")}
    {html.bold("❌ - go back to main menu")}
        """
    return text


def generate_recipe(recipe_name:str):
    unformatted_recipe = text_prompt_completion(f"""
    Generate the recipe for {recipe_name},
    Do not include the name of the recipe at the top of the response.
    Do not use Markdown (like # or **), and do not use unsupported HTML tags (like <h2>, <ul>, <li>). 
    To make text bold, use ONLY the <b>text</b> tag. For new lines, use standard \\n characters.
    """)
    return unformatted_recipe


def custom_recipe_valid_check(user_input:str):
    answer_dict = json_completion(f"""
    Check if the following input is a valid list of food ingredients and/or description of the dish.
    Input: '{user_input}'.
    Return a json array in the format {{answer:True/False}}.
    """)
    answer = answer_dict.get("answer",bool)
    return answer

def generate_recipe_custom(description:str):
    dish_dict = json_completion(f"""
    Return a json array of 5 dish ideas using this input : '{description}' as the preferences for the dish.
    All dishes have to contain those ingredients and/or be the type of a dish that is described in input.
    The format {{dish_ideas:[string]}}.
    """)
    dishes = dish_dict.get("dish_ideas",[])
    return dishes


@dp.message(RecipeFlow.writing_custom_recipe)
async def take_custom_recipe_input(message: Message, state: FSMContext):
    user_data = await state.get_data()

    user_input = str(message.text)

    if custom_recipe_valid_check(user_input):
        dishes = generate_recipe_custom(user_input)
        text = format_custom_dish_ideas(dishes)
        await message.answer(text=text,
                             reply_markup=INLINE_CUSTOM_DISH_IDEAS_KEYBOARD)
        await message.answer(text=f"{html.bold("USE NUMBERS FROM 1️⃣TO 5️⃣ TO GENERATE COMPLETE RECIPE")}",
                             reply_markup=REPLY_CUSTOM_DISH_IDEAS_KEYBOARD)
    else:
        custom_recipe_wrong_description = await message.answer(text=f"Your input : '{html.bold(user_input)}' is not a valid description of the dish or ingredients.")
        await state.update_data(custom_recipe_wrong_description = custom_recipe_wrong_description)



#NOTE: inline keyboard logic

@dp.callback_query(F.data == "pressed reload")
async def handle_dishideas_reload(callback: CallbackQuery, state: FSMContext):
    await callback.answer("reloading")

    user_data = await state.get_data()

    dishes = get_dish_ideas(user_data.get("used_recipes_ideas",[]))
    await state.update_data(used_recipes_ideas=dishes)

    text = format_dish_ideas(dishes)

    await callback.message.edit_text(text=text,
                                     reply_markup=INLINE_DISH_IDEAS_KEYBOARD)



@dp.callback_query(F.data == "pressed X")
async def handle_dishideas_close(callback: CallbackQuery, bot: Bot, state: FSMContext):
    await callback.answer()

    user_data = await state.get_data()
    suggest_recipe_reply_message = user_data.get("suggest_recipe_reply_message")

    await bot.delete_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id
    )

    await bot.delete_message(chat_id=callback.message.chat.id,
                             message_id=suggest_recipe_reply_message)

    await state.clear()


    await send_to_main_menu(
        chat_id = callback.message.chat.id,
        full_name = callback.from_user.full_name,
        state = state,
        bot = bot
    )



@dp.callback_query(F.data == "custom_recipe_message_back")
async def handle_custom_recipe_message_back(callback: CallbackQuery, bot: Bot, state: FSMContext):
    await callback.answer()

    # user_data = await state.get_data()
    # suggest_recipe_reply_message = user_data.get("suggest_recipe_reply_message")

    await bot.delete_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id
    )

    # await bot.delete_message(chat_id=callback.message.chat.id,
    #                          message_id=suggest_recipe_reply_message)

    await state.clear()


    await send_to_main_menu(
        chat_id = callback.message.chat.id,
        full_name = callback.from_user.full_name,
        state = state,
        bot = bot
    )


@dp.callback_query(F.data == "faq_go_back")
async def handle_faq_go_back(callback: CallbackQuery, bot: Bot, state: FSMContext):
    await callback.answer()

    await state.clear()

    await bot.delete_message(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id
        )

    await send_to_main_menu(
        chat_id = callback.message.chat.id,
        full_name = callback.from_user.full_name,
        state = state,
        bot = bot
    )


@dp.callback_query(F.data == "recipe_go_back")
async def handle_recipe_go_back(callback: CallbackQuery, state: FSMContext):
    await callback.answer("returning to suggested recipes")

    user_data = await state.get_data()
    await state.set_state(RecipeFlow.waiting_for_dish_idea)
    dishes = user_data.get("used_recipes_ideas",[])
    text = format_dish_ideas(dishes)
    # print(await state.get_state())

    reply_message = await callback.message.answer(text=f"{html.bold("USE NUMBERS FROM 1️⃣TO 🔟 TO GENERATE COMPLETE RECIPE")}",
                             reply_markup=REPLY_DISH_IDEAS_KEYBOARD)
    await state.update_data(suggest_recipe_reply_message = reply_message.message_id)


    await callback.message.edit_text(text=text,
                                     reply_markup=INLINE_DISH_IDEAS_KEYBOARD)



# @dp.callback_query(F.data.in_({"pressed <-","pressed ->"}))
# async def handle_dishideas_scroll(callback: CallbackQuery, state: FSMContext):
#     await callback.answer()
#
#     if callback.data == "pressed <-":
#         await callback.answer("going back")
#     elif callback.data == "pressed ->":
#         await callback.answer("going forward")


#NOTE: bot commands


@dp.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext, bot: Bot) -> None:
    await send_to_main_menu(
        chat_id = message.chat.id,
        full_name = message.from_user.full_name,
        state = state,
        bot = bot
    )

# @dp.message(Command("suggest_recipe"))
# async def show_suggested_recipes(message:Message,state:FSMContext,bot:Bot):
#     # dish_dict = get_dish_ideas()
#     # print(dish_dict)
#     # text = f"{html.bold("Suggested recipes:")}\n"
#     # dishes = dish_dict.get("dish_ideas",[])
#     #
#     # for index,dish in enumerate(dishes,start=1):
#     #     text += f"{index}. {html.bold(dish)}\n"
#
#     user_data = await state.get_data()
#
#     dishes = get_dish_ideas(user_data.get("used_recipes_ideas",[]))
#
#     await state.update_data(used_recipes_ideas=dishes)
#
#     text = f"{html.bold("Suggested recipes:")}\n"
#     for index,dish in enumerate(dishes,start=1):
#             text += f"{index}. {html.bold(dish)}\n"
#
#     await message.answer(text=text, 
#                          reply_markup=INLINE_DISH_IDEAS_KEYBOARD)
#
#     await bot.delete_message(chat_id=message.chat.id,
#                              message_id=message.message_id)





#NOTE: reply keyboards handlers

@dp.message(F.text == "🧠", StateFilter(None))
async def show_suggest_recipe(message: Message, state: FSMContext, bot: Bot):
    user_data = await state.get_data()

    old_menu_id = user_data.get("menu_message_id")

    if old_menu_id:
        try:
            await bot.delete_message(chat_id=message.chat.id,message_id=old_menu_id)
        except Exception:
            pass

    dishes = get_dish_ideas(user_data.get("used_recipes_ideas",[]))

    await state.update_data(used_recipes_ideas=dishes)
    await state.set_state(RecipeFlow.waiting_for_dish_idea)

    text = format_dish_ideas(dishes)

    clear_msg = await message.answer(text='thinking...',reply_markup=ReplyKeyboardRemove())

    inline_message = await message.answer(text=text,
                         reply_markup=INLINE_DISH_IDEAS_KEYBOARD)

    reply_message = await message.answer(text=f"{html.bold("USE NUMBERS FROM 1️⃣TO 🔟 TO GENERATE COMPLETE RECIPE")}",
                         reply_markup=REPLY_DISH_IDEAS_KEYBOARD)

    await state.update_data(suggest_recipe_reply_message = reply_message.message_id)
    await state.update_data(suggest_recipe_inline_message = inline_message)

    await bot.delete_message(chat_id=message.chat.id,
                             message_id=message.message_id)
    await bot.delete_message(chat_id=message.chat.id,
                             message_id=clear_msg.message_id)



@dp.message(F.text == "📝", StateFilter(None))
async def generate_custom_recipe(message: Message, state: FSMContext, bot: Bot):
    user_data = await state.get_data()

    old_menu_id = user_data.get("menu_message_id")

    if old_menu_id:
        try:
            await bot.delete_message(chat_id=message.chat.id,message_id=old_menu_id)
        except Exception:
            pass

    await state.set_state(RecipeFlow.writing_custom_recipe)

    await bot.delete_message(chat_id=message.chat.id,
                             message_id=message.message_id)


    await message.answer(text=CUSTOM_RECIPE_TEXT,
                         reply_markup=INLINE_KEYBOARD_CUSTOM_RECIPE_MESSAGE)



@dp.message(F.text.in_(IDEAS_INDEX.keys()), RecipeFlow.waiting_for_dish_idea)
async def generate_show_suggest_recipe(message: Message, state: FSMContext, bot: Bot):
    user_data = await state.get_data()
    dishes = user_data.get("used_recipes_ideas",[])
    inline_message = user_data.get("suggest_recipe_inline_message",str)

    await state.set_state(RecipeFlow.watching_recipe)

    index = IDEAS_INDEX[str(message.text)]

    unformatted_recipe = generate_recipe(dishes[index]).replace("\\n","\n")
    text = f"{html.bold(dishes[index])}👨‍🍳\n"
    text += unformatted_recipe
    text += """
    ⬅ - go back to dish ideas
    ⭐- add this recipe to favourite
    """

    clear_msg = await message.answer(text='thinking...',reply_markup=ReplyKeyboardRemove())


    await inline_message.edit_text(text=text,
                         parse_mode="HTML",
                         reply_markup=DISH_IDEAS_RECIPE_KEYBOARD)


    await bot.delete_message(chat_id=message.chat.id,
                             message_id=message.message_id)
    await bot.delete_message(chat_id=message.chat.id,
                             message_id=clear_msg.message_id)
    await bot.delete_message(chat_id=message.chat.id,
                             message_id=user_data.get("suggest_recipe_reply_message",int)
                             )



@dp.message(F.text == '❓', StateFilter(None))
async def show_help(message: Message, state: FSMContext, bot: Bot):
    user_data = await state.get_data()

    old_menu_id = user_data.get("menu_message_id")

    if old_menu_id:
        try:
            await bot.delete_message(chat_id=message.chat.id,message_id=old_menu_id)
        except Exception:
            pass

    await state.set_state(RecipeFlow.reading_faq)

    clear_msg = await message.answer(text='thinking...',reply_markup=ReplyKeyboardRemove())

    await message.answer(text=FAQ,
                         reply_markup=FAQ_KEYBOARD)

    await bot.delete_message(chat_id=message.chat.id,
                                 message_id=message.message_id)
    await bot.delete_message(chat_id=message.chat.id,
                                 message_id=clear_msg.message_id)





#NOTE: cornercases

@dp.message(F.text.in_({'🧠','❓'}), RecipeFlow.waiting_for_dish_idea)
async def handle_cornercases1(message: Message):
    await message.answer("You cant use this command here")


@dp.message(F.text.in_({'🧠','❓'}), RecipeFlow.reading_faq)
async def handle_cornercases2(message: Message):
    await message.answer("You cant use this command here")


async def send_to_main_menu(chat_id:int, full_name:str, state: FSMContext, bot: Bot):
    text = f"""
    Hello, {html.bold(full_name)}!
    🧠 - generate recipe ideas
    📝 - craft custom recipe
    ❓ - help
    """
    menu_message = await bot.send_message(text=text,chat_id=chat_id,reply_markup=MAIN_MENU_KEYBOARD)
    await state.update_data(menu_message_id = menu_message.message_id)




async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())




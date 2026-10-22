import asyncio,logging,sys,json,itertools
from os import getenv
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, html, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, StateFilter
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, Message, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.fsm.state import State,StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder,ReplyKeyboardBuilder

from groq import Groq



test_dict = {
    "recipe1":{"recipe_content"},
    "recipe2":{"recipe_content"},
    "recipe3":{"recipe_content"},
    "recipe4":{"recipe_content"},
    "recipe5":{"recipe_content"},
    "recipe6":{"recipe_content"},
    "recipe7":{"recipe_content"},
    "recipe8":{"recipe_content"},
    "recipe9":{"recipe_content"},
    "recipe10":{"recipe_content"},
    "recipe11":{"recipe_content"},
    "recipe12":{"recipe_content"},
    "recipe13":{"recipe_content"},
    "recipe14":{"recipe_content"},
    "recipe15":{"recipe_content"},
    "recipe16":{"recipe_content"},
    "recipe17":{"recipe_content"},
    "recipe18":{"recipe_content"},
    "recipe19":{"recipe_content"},
    "recipe20":{"recipe_content"},
    "recipe21":{"recipe_content"},
}

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

RANDOM_IDEAS_INDEX = {
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


CUSTOM_IDEAS_INDEX = {
    '1️⃣':0,
    '2️⃣':1,
    '3️⃣':2,
    '4️⃣':3,
    '5️⃣':4,
}


MAIN_MENU_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[
    [
        KeyboardButton(text='🧠'),
        KeyboardButton(text='📝'),
        KeyboardButton(text='⭐'),
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

CUSTOM_DISH_IDEAS_RECIPE_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='⬅',callback_data="custom_recipe_go_back"),
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
    waiting_for_custom_dish_idea = State()
    waiting_for_fav_dish_idea = State()





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
    {html.bold("🔃 - refresh recipes list")}
    {html.bold("❌ - go back to main menu")}
        """
    return text

async def format_fav_dishes(state: FSMContext, page=1):
    high = 10*page
    low = high-10
    dishes = list(itertools.islice(test_dict.keys(),low,high))
    await state.update_data(fav_dishes_page_content = dishes)
    # data = await state.get_data()
    # print(data.get("fav_dishes_page_content"))


    text = f"{html.bold("⭐Your favourite recipes:")}\n"
    for index,dish in enumerate(dishes,start=1):
        text += f"{html.bold(str(index))}. {dish}\n"

    if len(test_dict) < 10:
        text += f"""
        {html.bold("❌ - go back to main menu")}
        """

    elif len(test_dict) > 10 and page == 1:
        text += f"""
        {html.bold("➡ - go to the next page")}
        {html.bold("❌ - go back to main menu")}
        """
    elif len(test_dict) < 10*page:
        text += f"""
        {html.bold("⬅ - go to the previous page")}
        {html.bold("❌ - go back to main menu")}
        """
    else:
        text += f"""
        {html.bold("⬅ - go to the previous page")}
        {html.bold("➡ - go to the next page")}
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
    It can contain phrases like 'i want to make', but it has to be a description or ingredients for a dish.
    Input: '{user_input}'.
    Return a json array in the format {{answer:True/False}}.
    """)
    answer = answer_dict.get("answer",bool)
    return answer

def get_custom_dish_ideas(description:str):
    dish_dict = json_completion(f"""
    Return a json array of 5 dish ideas using this input : '{description}' as the preferences for the dish.
    All dishes have to contain those ingredients and/or be the type of a dish that is described in input.
    The format {{dish_ideas:[string]}}.
    """)
    dishes = dish_dict.get("dish_ideas",[])
    return dishes


@dp.message(RecipeFlow.writing_custom_recipe)
async def take_custom_recipe_input(message: Message, state: FSMContext, bot: Bot):
    user_data = await state.get_data()

    first_message = user_data.get("custom_recipe_first_message")

    user_input = str(message.text)

    if custom_recipe_valid_check(user_input):

        dishes = get_custom_dish_ideas(user_input)
        text = format_custom_dish_ideas(dishes)
        inline_message = await message.answer(text=text,
                             reply_markup=INLINE_CUSTOM_DISH_IDEAS_KEYBOARD)
        reply_message = await message.answer(text=f"{html.bold("USE NUMBERS FROM 1️⃣TO 5️⃣ TO GENERATE COMPLETE RECIPE")}",
                             reply_markup=REPLY_CUSTOM_DISH_IDEAS_KEYBOARD)
        await state.set_state(RecipeFlow.waiting_for_custom_dish_idea)

        await bot.delete_message(chat_id=message.chat.id,
                                 message_id=first_message.message_id)
        await state.update_data(custom_recipe_reply_message = reply_message)
        await state.update_data(custom_recipe_inline_message = inline_message)
        await state.update_data(custom_dish_ideas = dishes)

    else:

        custom_recipe_wrong_description = await message.answer(text=f"Your input : '{html.bold(user_input)}' is not a valid description of the dish or ingredients.")
        await state.update_data(custom_recipe_wrong_description = custom_recipe_wrong_description)


async def fav_dish_inline_keyboard(state: FSMContext):
    user_data = await state.get_data()
    page = user_data.get("fav_dish_page",int)

    if page == 1:
        buttons = {
            '➡': "fav_dish_next_page",
            '❌': "fav_dish_main_menu"
        }
    elif len(test_dict) > 10*page:
        buttons = {
            '⬅': "fav_dish_previous_page",
            '➡': "fav_dish_next_page",
            '❌': "fav_dish_main_menu"
        }
    else:
        buttons = {
            '⬅': "fav_dish_previous_page",
            '❌': "fav_dish_main_menu"
        }


    builder = InlineKeyboardBuilder()

    for key,value in buttons.items():
        builder.button(
            text=key,
            callback_data=value
        )

    return builder.as_markup()

async def fav_dish_reply_keyboard(state: FSMContext):
    user_data = await state.get_data()
    dishes = user_data.get("fav_dishes_page_content",list)
    buttons = list(RANDOM_IDEAS_INDEX.keys())

    builder = ReplyKeyboardBuilder()

    for index in range(len(dishes)):
        print(index)
        builder.button(
            text= buttons[index]
        )
    builder.adjust(5)
    return builder.as_markup(resize_keyboard = True)

async def fav_dish_reply_message(state: FSMContext):
    user_data = await state.get_data()
    dishes = user_data.get("fav_dishes_page_content",list)

    numbers = list(RANDOM_IDEAS_INDEX.keys())

    max_number = numbers[len(dishes)-1]
    text = f"USE NUMBERS FROM 1️⃣TO {max_number} TO GENERATE COMPLETE RECIPE"

    return text

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


@dp.callback_query(F.data == "custom_recipe_go_back")
async def handle_custom_recipe_go_back(callback: CallbackQuery, state: FSMContext):
    await callback.answer("returning to suggested recipes")

    user_data = await state.get_data()
    await state.set_state(RecipeFlow.waiting_for_custom_dish_idea)
    dishes = user_data.get("custom_dish_ideas",[])
    print(dishes)
    text = format_custom_dish_ideas(dishes)

    reply_message = await callback.message.answer(text=f"{html.bold("USE NUMBERS FROM 1️⃣TO 5️⃣ TO GENERATE COMPLETE RECIPE")}",
                             reply_markup=REPLY_CUSTOM_DISH_IDEAS_KEYBOARD)
    await state.update_data(custom_recipe_reply_message = reply_message)


    await callback.message.edit_text(text=text,
                                     reply_markup=INLINE_CUSTOM_DISH_IDEAS_KEYBOARD)



@dp.callback_query(F.data == "custom_recipes_back_to_first")
async def handle_custom_recipes_go_back(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await callback.answer("returning to crafting recipe")

    user_data = await state.get_data()
    number_message = user_data.get("custom_recipe_reply_message")
    await state.set_state(RecipeFlow.writing_custom_recipe)

    text = CUSTOM_RECIPE_TEXT

    first_message = await callback.message.edit_text(text=text,
                                                     reply_markup=INLINE_KEYBOARD_CUSTOM_RECIPE_MESSAGE)

    await state.update_data(custom_recipe_first_message = first_message)
    await bot.delete_message(chat_id=number_message.chat.id,
                             message_id=number_message.message_id)

@dp.callback_query(F.data == "custom_recipes_main_menu")
async def handle_custom_recipes_main_menu(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await callback.answer("returning to main menu")
    user_data = await state.get_data()

    number_message = user_data.get("custom_recipe_reply_message")

    await state.clear()

    await bot.delete_message(chat_id=callback.message.chat.id,
                             message_id=callback.message.message_id)
    await bot.delete_message(chat_id=number_message.chat.id,
                             message_id=number_message.message_id)

    await send_to_main_menu(
        chat_id = callback.message.chat.id,
        full_name = callback.from_user.full_name,
        state = state,
        bot = bot
    )


@dp.callback_query(F.data == "recipe_add_fav")
async def handle_add_fav_recipe(callback: CallbackQuery, state: FSMContext):
    await callback.answer("Recipe was added to your favourite recipes list")
    user_data = await state.get_data()

    await state.update_data(fav_recipe_dict = {user_data.get("current_recipe_name"):user_data.get("current_recipe")})
    user_data = await state.get_data()
    print(user_data.get("fav_recipe_dict"))


# @dp.callback_query(F.data.in_({"pressed <-","pressed ->"}))
# async def handle_dishideas_scroll(callback: CallbackQuery, state: FSMContext):
#     await callback.answer()
#
#     if callback.data == "pressed <-":
#         await callback.answer("going back")
#     elif callback.data == "pressed ->":
#         await callback.answer("going forward")



@dp.callback_query(F.data == "fav_dish_next_page")
async def handle_fav_dish_next_page(callback: CallbackQuery, state: FSMContext, bot: Bot):
    user_data = await state.get_data()
    page = user_data.get("fav_dish_page",int)

    callback.answer()
    await state.update_data(fav_dish_page = page+1)
    text = await format_fav_dishes(state,page=page+1)
    inline_message = await callback.message.edit_text(text=text,
                                     reply_markup=await fav_dish_inline_keyboard(state))

    await bot.delete_message(message_id=user_data.get("fav_recipe_reply_message"),
                             chat_id=callback.message.chat.id)

    reply_message = await callback.message.answer(text=f"{html.bold(await fav_dish_reply_message(state))}",
                         reply_markup=await fav_dish_reply_keyboard(state))

    await state.update_data(fav_recipe_reply_message = reply_message.message_id)
    await state.update_data(fav_recipe_inline_message = inline_message)



@dp.callback_query(F.data == "fav_dish_previous_page")
async def handle_fav_dish_previous_page(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    page = user_data.get("fav_dish_page",int)

    callback.answer()
    await state.update_data(fav_dish_page = page-1)
    text = await format_fav_dishes(state,page=page-1)

    await callback.message.edit_text(text=text,
                                     reply_markup=await fav_dish_inline_keyboard(state))






#NOTE: bot commands


@dp.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext, bot: Bot) -> None:
    await send_to_main_menu(
        chat_id = message.chat.id,
        full_name = message.from_user.full_name,
        state = state,
        bot = bot
    )




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


    first_message = await message.answer(text=CUSTOM_RECIPE_TEXT,
                         reply_markup=INLINE_KEYBOARD_CUSTOM_RECIPE_MESSAGE)
    await state.update_data(custom_recipe_first_message=first_message)



@dp.message(F.text.in_(RANDOM_IDEAS_INDEX.keys()), RecipeFlow.waiting_for_dish_idea)
async def generate_show_suggest_recipe(message: Message, state: FSMContext, bot: Bot):
    user_data = await state.get_data()
    dishes = user_data.get("used_recipes_ideas",[])
    inline_message = user_data.get("suggest_recipe_inline_message",str)

    await state.set_state(RecipeFlow.watching_recipe)

    index = RANDOM_IDEAS_INDEX[str(message.text)]

    unformatted_recipe = generate_recipe(dishes[index]).replace("\\n","\n")
    text = f"{html.bold(dishes[index])}👨‍🍳\n"
    text += unformatted_recipe
    text += """
    ⬅ - go back to dish ideas
    ⭐- add this recipe to favourite
    """

    await state.update_data(current_recipe_name = dishes[index],
                            current_recipe = unformatted_recipe)

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



@dp.message(F.text.in_(CUSTOM_IDEAS_INDEX.keys()),RecipeFlow.waiting_for_custom_dish_idea)
async def generate_show_custom_recipe(message: Message, state: FSMContext, bot: Bot):
    user_data = await state.get_data()
    dishes = user_data.get("custom_dish_ideas",[])
    inline_message = user_data.get("custom_recipe_inline_message",str)
    reply_message = user_data.get("custom_recipe_reply_message",str)

    await state.set_state(RecipeFlow.watching_recipe)

    index = CUSTOM_IDEAS_INDEX[str(message.text)]

    unformatted_recipe = generate_recipe(dishes[index]).replace("\\n","\n")
    text = f"{html.bold(dishes[index])}👨‍🍳\n"
    text += unformatted_recipe
    text += """
    ⬅ - go back to dish ideas
    ⭐- add this recipe to favourite
    """
    await state.update_data(current_recipe_name = dishes[index],
                            current_recipe = unformatted_recipe)

    clear_msg = await message.answer(text='thinking...',reply_markup=ReplyKeyboardRemove())


    await inline_message.edit_text(text=text,
                         parse_mode="HTML",
                         reply_markup=CUSTOM_DISH_IDEAS_RECIPE_KEYBOARD)


    await bot.delete_message(chat_id=message.chat.id,
                             message_id=message.message_id)
    await bot.delete_message(chat_id=message.chat.id,
                             message_id=clear_msg.message_id)
    await bot.delete_message(chat_id=message.chat.id,
                             message_id=reply_message.message_id
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


@dp.message(F.text == '⭐', StateFilter(None))
async def show_fav_recipes(message: Message, state: FSMContext, bot: Bot):
    user_data = await state.get_data()

    await state.update_data(fav_dish_page = 1)

    old_menu_id = user_data.get("menu_message_id")

    if old_menu_id:
        try:
            await bot.delete_message(chat_id=message.chat.id,message_id=old_menu_id)
        except Exception:
            pass

    await state.set_state(RecipeFlow.waiting_for_fav_dish_idea)

    text = await format_fav_dishes(state,page=1)

    clear_msg = await message.answer(text='thinking...',reply_markup=ReplyKeyboardRemove())

    inline_message = await message.answer(text=text,
                         reply_markup=await fav_dish_inline_keyboard(state))

    reply_message = await message.answer(text=f"{html.bold(await fav_dish_reply_message(state))}",
                         reply_markup=await fav_dish_reply_keyboard(state))

    await state.update_data(fav_recipe_reply_message = reply_message.message_id)
    await state.update_data(fav_recipe_inline_message = inline_message)

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
    ⭐ - your favourite recipes
    ❓ - help
    """
    menu_message = await bot.send_message(text=text,chat_id=chat_id,reply_markup=MAIN_MENU_KEYBOARD)
    await state.update_data(menu_message_id = menu_message.message_id)
    await state.clear()




async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())




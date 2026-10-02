import asyncio,logging,sys,json
from os import getenv
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, html, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart,Command, StateFilter
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, Message, ReplyKeyboardMarkup, ReplyKeyboardRemove, message
from aiogram.fsm.state import State,StatesGroup
from aiogram.fsm.context import FSMContext

from groq import Groq

load_dotenv()
TOKEN = getenv("BOT_TOKEN")
LLM = Groq(
    api_key= getenv("GROQ_API_KEY")
)

KEYBOARD_DISH_IDEAS = InlineKeyboardMarkup(
    inline_keyboard=[
    [
     InlineKeyboardButton(text="🔄",callback_data="pressed reload"),
     InlineKeyboardButton(text="❌",callback_data="pressed X")
     ]
]
)
MAIN_MENU_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[
    [
        KeyboardButton(text="🧠"),
        KeyboardButton(text="❓")
    ]
],
    resize_keyboard=True
)

dp = Dispatcher()

#defining state group
class RecipeFlow(StatesGroup):
    waiting_for_dish_idea = State()





#NOTE: api calls, main logic

def completion(prompt,model):
    comp = LLM.chat.completions.create(model=model,
                                       messages=[
                                       {"role":"user","content":prompt}
                                       ],
                                       response_format={"type":"json_object"})
    return comp.choices[0].message.content

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



#NOTE: inline keyboard logic

@dp.callback_query(F.data == "pressed reload")
async def handle_dishideas_reload(callback: CallbackQuery, state: FSMContext):
    await callback.answer("reloading")

    user_data = await state.get_data()

    dishes = get_dish_ideas(user_data.get("used_recipes_ideas",[]))
    await state.update_data(used_recipes_ideas=dishes)

    text = f"{html.bold("Suggested recipes:")}\n"
    for index,dish in enumerate(dishes,start=1):
        text += f"{index}. {html.bold(dish)}\n"

    await callback.message.edit_text(text=text,
                                     reply_markup=KEYBOARD_DISH_IDEAS)



@dp.callback_query(F.data == "pressed X")
async def handle_dishideas_close(callback: CallbackQuery, bot: Bot, state: FSMContext):
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
#                          reply_markup=KEYBOARD_DISH_IDEAS)
#
#     await bot.delete_message(chat_id=message.chat.id,
#                              message_id=message.message_id)





#NOTE: reply keboards handlers

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

    text = f"{html.bold("Suggested recipes:")}\n"
    for index,dish in enumerate(dishes,start=1):
            text += f"{index}. {html.bold(dish)}\n"
    
    clear_msg = await message.answer(text='thinking...',reply_markup=ReplyKeyboardRemove())

    await message.answer(text=text, 
                         reply_markup=KEYBOARD_DISH_IDEAS)

    await bot.delete_message(chat_id=message.chat.id,
                             message_id=message.message_id)
    await bot.delete_message(chat_id=message.chat.id,
                             message_id=clear_msg.message_id)






#NOTE: cornercases

@dp.message(F.text.in_({'🧠','❓'}), RecipeFlow.waiting_for_dish_idea)
async def handle_cornercases(message: Message):
    await message.answer("You cant use this command here")


async def send_to_main_menu(chat_id:int, full_name:str, state: FSMContext, bot: Bot):
    text = f"""
    Hello, {html.bold(full_name)}!
    🧠 - generate recipe ideas
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




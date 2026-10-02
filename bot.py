import asyncio,logging,sys,json
from os import getenv
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, html, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart,Command
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message
from aiogram.fsm.state import State,StatesGroup
from aiogram.fsm.context import FSMContext

from groq import Groq

load_dotenv()
TOKEN = getenv("BOT_TOKEN")
LLM = Groq(
    api_key= getenv("GROQ_API_KEY")
)

KEYBOARD_DISH_IDEAS = [
    [
     InlineKeyboardButton(text="🔄",callback_data="pressed reload"),
     InlineKeyboardButton(text="❌",callback_data="pressed X")
     ]
]

keyboard_dish_ideas_markup = InlineKeyboardMarkup(inline_keyboard=KEYBOARD_DISH_IDEAS)

dp = Dispatcher()

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

def get_dish_ideas():
    dish_dict = json_completion(f"""
        Return a json array of 10 dish ideas,
        in the format {{dish_ideas:[string]}}.
    """)
    print(dish_dict)
    text = f"{html.bold("Suggested recipes:")}\n"
    dishes = dish_dict.get("dish_ideas",[])

    for index,dish in enumerate(dishes,start=1):
        text += f"{index}. {html.bold(dish)}\n"

    return text



#NOTE: inline keyboard logic

@dp.callback_query(F.data == "pressed reload")
async def handle_dishideas_reload(callback: CallbackQuery, state: FSMContext):
    await callback.answer("reloading")

    text = get_dish_ideas()
    await callback.message.edit_text(text=text,
                                     reply_markup=keyboard_dish_ideas_markup)



@dp.callback_query(F.data == "pressed X")
async def handle_dishideas_close(callback: CallbackQuery, bot: Bot):
    await callback.answer()

    await bot.delete_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id
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

#defining state group
class RecipeFlow(StatesGroup):
    waiting_for_choice = State()

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")

@dp.message(Command("suggest_recipe"))
async def show_suggested_recipes(message:Message,state:FSMContext,bot:Bot):
    # dish_dict = get_dish_ideas()
    # print(dish_dict)
    # text = f"{html.bold("Suggested recipes:")}\n"
    # dishes = dish_dict.get("dish_ideas",[])
    #
    # for index,dish in enumerate(dishes,start=1):
    #     text += f"{index}. {html.bold(dish)}\n"
    text = get_dish_ideas()
    await message.answer(text=text, 
                         reply_markup=keyboard_dish_ideas_markup)

    await bot.delete_message(chat_id=message.chat.id,
                             message_id=message.message_id)




async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())




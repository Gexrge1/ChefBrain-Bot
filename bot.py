import asyncio,logging,sys,json
from os import getenv
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, html, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart,Command
from aiogram.types import Message
from aiogram.fsm.state import State,StatesGroup
from aiogram.fsm.context import FSMContext

from groq import Groq

load_dotenv()
TOKEN = getenv("BOT_TOKEN")
LLM = Groq(
    api_key= getenv("GROQ_API_KEY")
)


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
    dish_ideas = json_completion(f"""
        Return a json array of 10 dish ideas,
        in the format {{dish_ideas:[string]}}.
    """)
    return dish_ideas

dp = Dispatcher()

#defining state group
class RecipeFlow(StatesGroup):
    waiting_for_choice = State()

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")

@dp.message(Command("suggest_recipe"))
async def show_suggested_recipes(message:Message,state:FSMContext):
    dish_dict = get_dish_ideas()
    print(dish_dict)
    text = f"{html.bold("Suggested recipes:")}\n"
    dishes = dish_dict.get("dish_ideas",[])

    for index,dish in enumerate(dishes,start=1):
        text += f"{index}. {html.bold(dish)}\n"

    await message.answer(text)




async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())




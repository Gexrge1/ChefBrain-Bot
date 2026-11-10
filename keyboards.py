from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup 

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

LANGUAGE_INDEX = {
    '1️⃣':"en",
    '2️⃣':"pl",
    '3️⃣':"ru"
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

LANGUAGE_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='1️⃣'),
            KeyboardButton(text='2️⃣'),
            KeyboardButton(text='3️⃣')
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

FAV_DISH_RECIPE_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='⬅',callback_data="fav_recipe_go_back"),
            InlineKeyboardButton(text='💔',callback_data="recipe_remove_fav")
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

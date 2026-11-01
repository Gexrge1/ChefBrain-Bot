from aiogram import html
from textwrap import dedent


TRANSLATIONS = {
    "en":{
        "faq": dedent(f"""
        The {html.bold("Chef-Brain BOT")} can generate random recipes. 🥗🥪🧆🥘👨‍🍳

        Click 🧠 to generate a unique recipes
        Click ⭐to see your favorite recipes
        Click ⚙  to change your preferences

        {html.bold("⬅  GO BACK TO MAIN MENU")}
        """).strip(),

        "custom_recipe_text": dedent(f"""
        Please, write below what ingredients you have 🍆🥩🥚🧂
        or describe what you want to eat!
        The {html.bold("Chef-Brain BOT")} can create recipes based on a description alone!👨‍🍳🍳

        ❌ - go back to main menu
        """).strip(),

        "fav_recipes_text": "⭐Your favorite recipes:",

        "go_back_main_menu": "❌ - go back to the main menu",
        "go_back_craft": "⬅ - go back to crafting recipe",

        "fav_recipes_next_page": "➡ - go to the next page",
        "fav_recipes_prev_page": "⬅ - go to the previous page",

        "suggested_recipes": "Suggested recipes:",
        "refresh_recipe": "🔃 - refresh recipes list",

        "custom_recipe_numbers": "USE NUMBERS FROM 1️⃣ TO 5️⃣ TO GENERATE COMPLETE RECIPE",
        "random_recipe_numbers": "USE NUMBERS FROM 1️⃣ TO 🔟 TO GENERATE COMPLETE RECIPE",

        "no_fav": "YOU DONT HAVE A FAVORITE RECIPE YET👨‍🍳⭐",
        "one_fav": "PRESS 1️⃣ TO SHOW A COMPLETE RECIPE",

        "callback_reloading": "reloading",
        "callback_returning_to_sugg_recipes": "returning to suggested recipes",
        "callback_returning_to_fav_recipes": "returning to favorite recipes",
        "callback_returning_to_crafting_recipes": "returning to crafting recipe",
        "callback_returning_to_main_menu": "returning to the main menu",
        "callback_recipe_was_added_to_fav": "Recipe was added to your favorite recipes list",
        "callback_recipe_was_removed_from_fav": "Recipe was removed from your favorite recipes list",

        "watching_recipe_buttons_text": dedent("""
            \n\n⬅ - go back to dish ideas
            ⭐ - add this recipe to favorite
        """).strip(),

        "watching_fav_recipe_buttons_text": dedent("""
            \n\n⬅ - go back to favorite dishes
            💔 - remove from favorites
        """).strip(),

        "main_menu_text": dedent(
                    "Hello, {full_name}!\n"
                    "🧠 - generate recipe ideas\n"
                    "📝 - craft custom recipe\n"
                    "⭐ - your favorite recipes\n"
                    "❓ - help"
                ).strip(),

            "fav_recipes_number_text": dedent(
                "USE NUMBERS FROM 1️⃣ TO {max_number} "
                "TO SHOW A COMPLETE RECIPE"
            ).strip(),

            "bad_input_text": dedent(
                "Your input: '{user_input}' is not a valid "
                "description of the dish or ingredients."
            ).strip()
    },

    "ru": {
        "faq": dedent(f"""
            {html.bold("Chef-Brain BOT")} умеет создавать рецепты. 🥗🥪🧆🥘👨‍🍳

            Нажми на 🧠, чтобы сгенерировать уникальные рецепты
            Нажми на ⭐, чтобы посмотреть избранные рецепты
            Нажми на ⚙, чтобы изменить свои предпочтения

            {html.bold("⬅  ВЕРНУТЬСЯ В ГЛАВНОЕ МЕНЮ")}
        """).strip(),

        "custom_recipe_text": dedent(f"""
            Напиши ниже, какие ингредиенты у тебя есть 🍆🥩🥚🧂
            или опиши, что ты хочешь приготовить!
            {html.bold("Chef-Brain BOT")} может создавать рецепты имея только описание блюда!👨‍🍳🍳

            ❌ - вернуться в главное меню
        """).strip(),

        "fav_recipes_text": "⭐Твои избранные рецепты:",

        "go_back_main_menu": "❌ - вернуться в главное меню",
        "go_back_craft": "⬅ - вернуться к созданию рецепта",

        "fav_recipes_next_page": "➡ - перейти на следующую страницу",
        "fav_recipes_prev_page": "⬅ - перейти на предыдущую страницу",

        "suggested_recipes": "Предложенные рецепты:",
        "refresh_recipe": "🔃 - обновить список рецептов",

        "custom_recipe_numbers": "ИСПОЛЬЗУЙ ЦИФРЫ ОТ 1️⃣ ДО 5️⃣, ЧТОБЫ ПОЛУЧИТЬ ПОЛНЫЙ РЕЦЕПТ",
        "random_recipe_numbers": "ИСПОЛЬЗУЙ ЦИФРЫ ОТ 1️⃣ ДО 🔟, ЧТОБЫ ПОЛУЧИТЬ ПОЛНЫЙ РЕЦЕПТ",

        "no_fav": "У ТЕБЯ ПОКА НЕТ ИЗБРАННЫХ РЕЦЕПТОВ👨‍🍳⭐",
        "one_fav": "НАЖМИ 1️⃣, ЧТОБЫ ПОСМОТРЕТЬ ПОЛНЫЙ РЕЦЕПТ",

        "callback_reloading": "обновляется",
        "callback_returning_to_sugg_recipes": "возвращение к предложенным рецептам",
        "callback_returning_to_fav_recipes": "возвращение к избранным рецептам",
        "callback_returning_to_crafting_recipes": "возвращение к созданию рецепта",
        "callback_returning_to_main_menu": "возвращение в главное меню",
        "callback_recipe_was_added_to_fav": "Рецепт добавлен в список избранного",
        "callback_recipe_was_removed_from_fav": "Рецепт удалён из списка избранного",

        "watching_recipe_buttons_text": dedent("""
            \n\n⬅ - вернуться к идеям блюд
            ⭐ - добавить этот рецепт в избранное
        """).strip(),

        "watching_fav_recipe_buttons_text": dedent("""
            \n\n⬅ - вернуться к избранным блюдам
            💔 - удалить из избранного
        """).strip(),

        "main_menu_text": dedent(
                    "Привет, {full_name}!\n"
                    "🧠 - сгенерировать идеи рецептов\n"
                    "📝 - создать собственный рецепт\n"
                    "⭐ - избранные рецепты\n"
                    "❓ - помощь"
                ).strip(),

            "fav_recipes_number_text": dedent(
                "ИСПОЛЬЗУЙ ЦИФРЫ ОТ 1️⃣ ДО {max_number}, "
                "ЧТОБЫ ПОСМОТРЕТЬ ПОЛНЫЙ РЕЦЕПТ"
            ).strip(),

            "bad_input_text": dedent(
                "Твой ввод: '{user_input}' не является корректным "
                "описанием блюда или ингредиентов."
            ).strip()
    },

    "pl": {
        "faq": dedent(f"""
            {html.bold("Chef-Brain BOT")} potrafi generować przepisy. 🥗🥪🧆🥘👨‍🍳

            Kliknij 🧠, aby wygenerować unikalne przepisy
            Kliknij ⭐, aby zobaczyć ulubione przepisy
            Kliknij ⚙, aby zmienić swoje preferencje

            {html.bold("⬅  POWRÓT DO MENU GŁÓWNEGO")}
        """).strip(),

        "custom_recipe_text": dedent(f"""
            Napisz poniżej, jakie składniki masz do dyspozycji 🍆🥩🥚🧂
            lub opisz, na co masz ochotę!
            {html.bold("Chef-Brain BOT")} potrafi tworzyć przepisy nawet na podstawie samego opisu!👨‍🍳🍳

            ❌ - powrót do menu głównego
        """).strip(),

        "fav_recipes_text": "⭐Twoje ulubione przepisy:",

        "go_back_main_menu": "❌ - powrót do menu głównego",
        "go_back_craft": "⬅ - powrót do tworzenia przepisu",

        "fav_recipes_next_page": "➡ - przejdź do następnej strony",
        "fav_recipes_prev_page": "⬅ - przejdź do poprzedniej strony",

        "suggested_recipes": "Proponowane przepisy:",
        "refresh_recipe": "🔃 - odśwież listę przepisów",

        "custom_recipe_numbers": "UŻYJ CYFR OD 1️⃣ DO 5️⃣, ABY WYGENEROWAĆ PEŁNY PRZEPIS",
        "random_recipe_numbers": "UŻYJ CYFR OD 1️⃣ DO 🔟, ABY WYGENEROWAĆ PEŁNY PRZEPIS",

        "no_fav": "NIE MASZ JESZCZE ŻADNYCH ULUBIONYCH PRZEPISÓW👨‍🍳⭐",
        "one_fav": "NACIŚNIJ 1️⃣, ABY ZOBACZYĆ PEŁNY PRZEPIS",

        "callback_reloading": "odświeżanie",
        "callback_returning_to_sugg_recipes": "powrót do proponowanych przepisów",
        "callback_returning_to_fav_recipes": "powrót do ulubionych przepisów",
        "callback_returning_to_crafting_recipes": "powrót do tworzenia przepisu",
        "callback_returning_to_main_menu": "powrót do menu głównego",
        "callback_recipe_was_added_to_fav": "Przepis został dodany do ulubionych",
        "callback_recipe_was_removed_from_fav": "Przepis został usunięty z ulubionych",

        "watching_recipe_buttons_text": dedent("""
            \n\n⬅ - powrót do pomysłów na dania
            ⭐ - dodaj ten przepis do ulubionych
        """).strip(),

        "watching_fav_recipe_buttons_text": dedent("""
            \n\n⬅ - powrót do ulubionych dań
            💔 - usuń z ulubionych
        """).strip(),

        "main_menu_text": dedent(
                    "Cześć, {full_name}!\n"
                    "🧠 - wygeneruj pomysły na przepisy\n"
                    "📝 - stwórz własny przepis\n"
                    "⭐ - ulubione przepisy\n"
                    "❓ - pomoc"
                ).strip(),

            "fav_recipes_number_text": dedent(
                "UŻYJ CYFR OD 1️⃣ DO {max_number}, "
                "ABY ZOBACZYĆ PEŁNY PRZEPIS"
            ).strip(),

            "bad_input_text": dedent(
                "Twój tekst: '{user_input}' nie jest prawidłowym "
                "opisem dania ani składników."
            ).strip()
    }
}

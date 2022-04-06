from vkbottle.bot import Blueprint, Message
import aiosqlite
import random

bp = Blueprint("Start command")
bp.labeler.vbml_ignore_case = True

NAMES = (
    "Люмин", "Итэр", "Ху Тао",
    "Кэ Цин", "Эмбер", "Чжун Ли",
    "Янь Фей", "Ноэлль", "Барбара",
    "Венти", "Эола", "Лиза ( ͡° ͜ʖ ͡°)",
    "Кокоми", "Ци Ци", "Дилюк",
    "Тимми (🏹 ---> 🕊)", "Райдэн",
    "Тарталья", "Тома", "Шэнь Хэ",
    "Яэ Мико", "Хиличурл", "Маг бездны",
    "Фишль", "Гань Юй", "Паймон",
    "Путешественник", "СтасБарецкий228",
    "Ваша жаба", "Дед", "Буба",
    "Кокосовая коза", "чича"
    "Консерва", "мда", "кринж",
    "амогус", "сус", "сырник",
    "0); DROP DATABASE users; --",
    "Null Null", "c6 Ху Тао", "донатер"
)


@bp.on.message(text="!начать")
async def standard_wish(message: Message):
    async with aiosqlite.connect("db.db") as db:
        async with db.execute(
            "SELECT user_id FROM players WHERE user_id=(?)",
            (message.from_id,)
        ) as cursor:
            if await cursor.fetchone():
                await message.answer("Вы уже зашли в Genshin Impact")
            else:
                await db.execute(
                    "INSERT INTO players (user_id, peer_id, nickname) VALUES "
                    "(?, ?, ?)",
                    (message.from_id, message.peer_id, random.choice(NAMES),)
                )
                await db.commit()
                await message.answer(
                    "Вы зашли в Genshin Impact!\n"
                    "Напишите !персонаж, что бы увидеть ваш никнейм "
                    "и количество молитв"
                )

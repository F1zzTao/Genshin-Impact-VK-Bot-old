from vkbottle.bot import Blueprint, Message
from player_exists import HasAccount
import aiosqlite
import random
import time

bp = Blueprint("Mini-games")
bp.labeler.vbml_ignore_case = True


@bp.on.message(HasAccount(), text="!начать поручения")
async def start_daily_quests(message: Message):
    """
    Игрок сможет начать поручение только если:
    Он зарегестрирован;
    did_quest_today == 0;
    doing_quest == 0
    daily_quests_time + 86400 секунд (24 часа) < текущего unix времени
    """
    async with aiosqlite.connect("db.db") as db:
        async with db.execute(
            "SELECT "
            "daily_quests_time, "
            "doing_quest "
            "FROM players WHERE user_id=(?)",
            (message.from_id,),
        ) as cur:
            result = await cur.fetchone()

        daily_quests_time: int = result[0]
        doing_quest: int = result[1]
        if daily_quests_time + 86400 < int(time.time()) and doing_quest == 0:
            await db.execute(
                "UPDATE players SET "
                "daily_quests_time=(?), "
                "doing_quest=1 "
                "WHERE user_id=(?)",
                (int(time.time()), message.from_id,),
            )
            await db.commit()
            await message.answer(
                "Вы начали выполнять поручения. "
                "Возвращайтесь через 20 минут!"
            )
        else:
            await message.answer(
                "Вы уже начали поручения или выполнили их!"
            )


@bp.on.message(HasAccount(), text="!закончить поручения")
async def complete_daily_quests(message: Message):
    """
    Игрок сможет закончить поручение только если:
        Он зарегестрирован;
        doing_quest == 1;
        daily_quests_time + 1200 секунд (20 минут) < текущего unix времени
    """
    async with aiosqlite.connect("db.db") as db:
        async with db.execute(
            "SELECT "
            "daily_quests_time, "
            "doing_quest "
            "FROM players WHERE user_id=(?)",
            (message.from_id,),
        ) as cur:
            result = await cur.fetchone()

        started_time: int = result[0]
        doing_quest: int = result[1]

        # 1200 - 20 минут
        if doing_quest == 1 and started_time + 1200 < int(time.time()):
            standard_wish_reward = random.randint(5, 20)
            event_wish_reward = random.randint(5, 20)
            await db.execute(
                "UPDATE players SET "
                "doing_quest=0, "
                "did_quest_today=1, "
                "standard_wishes=standard_wishes+(?), "
                "event_wishes=event_wishes+(?) "
                "WHERE user_id=(?) ",
                (
                    standard_wish_reward,
                    event_wish_reward,
                    message.from_id,
                ),
            )
            await db.commit()

            await message.answer(
                "Вы выполнили поручения и получили "
                f"{standard_wish_reward} судьбоносных встреч и "
               f"{event_wish_reward} переплетающих судьб"
            )
        else:
            await message.answer(
                "Еще не прошло 20 минут или сегодня вы уже выполнили все "
                "поручения!"
            )
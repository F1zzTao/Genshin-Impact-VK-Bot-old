from vkbottle.bot import Blueprint, Message
from player_exists import exists
from loguru import logger
from variables import STANDARD_VARIANTS, EVENT_VARIANTS
import create_pool

bp = Blueprint("Fates shop")
bp.labeler.vbml_ignore_case = True


@bp.on.chat_message(text=("!магазин", "!shop"))
async def shop(message: Message):
    if not await exists(message):
        return
    return (
        "Добро пожаловать в магазин паймон!\n"
        "Цена молитв - 160 примогемов"
    )


@bp.on.chat_message(text="!купить молитвы <fate_type> <amount:int>")
async def buy_fates(message: Message, fate_type, amount: int):
    pool = create_pool.pool
    if not await exists(message):
        return
    async with pool.acquire() as pool:
        if amount <= 0:
            await message.answer("Ты пьяный?")
            return

        primogems = await pool.fetchrow(
            "SELECT primogems FROM players WHERE user_id=$1 AND peer_id=$2",
            message.from_id, message.peer_id,
        )
        if primogems[0] >= 160 * amount:
            if fate_type in STANDARD_VARIANTS:
                logger.info(
                    f"Начисление пользователю {message.from_id} в беседе "
                    f"{message.peer_id} {amount} стандартных молитв"
                )
                await pool.execute(
                    "UPDATE players SET primogems=primogems-$1, "
                    "standard_wishes=standard_wishes+$2 WHERE user_id=$3 AND "
                    "peer_id=$4",
                    160 * amount, amount, message.from_id, message.peer_id,
                )
                await message.answer(
                    f"Вы купили {amount} стандартных молитв за "
                    f"{amount*160} примогемов!"
                )
            elif fate_type in EVENT_VARIANTS:
                logger.info(
                    f"Начисление пользователю {message.from_id} в беседе "
                    f"{message.peer_id} {amount} ивентовых молитв"
                )
                await pool.execute(
                    "UPDATE players SET primogems=primogems-$1, "
                    "event_wishes=event_wishes+$2 WHERE user_id=$3 AND "
                    "peer_id=$4",
                    160 * amount, amount, message.from_id, message.peer_id,
                )
                await message.answer(
                    f"Вы купили {amount} ивентовых молитв за "
                    f"{amount*160} примогемов!"
                )
            else:
                await message.answer("Неа, таких молитв не существует!")

        else:
            await message.answer(
                f"Вам не хватает примогемов, {amount} молитв стоят "
                f"{amount*160} примогемов!"
            )

import logging
import os
from datetime import timedelta
from pathlib import Path
from aiogram import Bot, Dispatcher, executor, types  # type: ignore
from aiogram.utils.markdown import escape_md  # type: ignore
import asyncio

from stablecoin_rates.model import LendingRate
from stablecoin_rates.reporter.formatter import format_lending_rate_table
from stablecoin_rates.scraper import SCRAPER_METHODS

TOKEN_PATH = Path.cwd() / "telegram_token.txt"
_LOGGER = logging.getLogger(__name__)

STABLECOIN_CHAT_ID = os.environ.get("STABLECOIN_CHAT_ID", "-630417396")
SLEEP_INTERVAL = int(
    os.environ.get("SLEEP_INTERVAL", timedelta(hours=12).total_seconds())
)


async def scrape_all_rates() -> list[LendingRate]:
    results = await asyncio.gather(*(method() for method in SCRAPER_METHODS))
    rates = [r for rates in results for r in rates]

    return rates


def get_bot_token() -> str:
    return TOKEN_PATH.read_text().strip()


async def main() -> None:
    token = get_bot_token()

    bot = Bot(token=token)
    dp = Dispatcher(bot)

    # Print the rates to the console
    rates = await scrape_all_rates()
    formatted_message = format_lending_rate_table(rates)
    print(formatted_message)

    @dp.message_handler(commands=["rates"])
    async def handle_rates(message: types.Message):
        await send_rates_to_chat(bot, message.chat.id)

    @dp.message_handler(commands=["help"])
    async def handle_help(message: types.Message):
        await message.answer("/rates - Show the current lending rates")

    await bot.set_my_commands(
        [
            types.BotCommand("rates", "Show the current lending rates"),
            types.BotCommand("help", "Show the help documentation"),
        ]
    )

    periodic_task = asyncio.create_task(periodic_send_task(bot))

    try:
        await dp.start_polling()
    finally:
        periodic_task.cancel()
        await periodic_task
        await dp.wait_closed()
        await (await bot.get_session()).close()


async def send_rates_to_chat(bot: Bot, chat_id: str) -> None:
    _LOGGER.info(f"Sending stablecoin rates...")
    rates = await scrape_all_rates()
    formatted_message = "```\n" + format_lending_rate_table(rates) + "\n```"
    await bot.send_message(chat_id, formatted_message, parse_mode="MarkdownV2")


async def periodic_send_task(bot: Bot) -> None:
    try:
        while True:
            await send_rates_to_chat(bot, STABLECOIN_CHAT_ID)
            await asyncio.sleep(SLEEP_INTERVAL)
    except asyncio.CancelledError:
        pass


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())

import logging
from pathlib import Path
from aiogram import Bot, Dispatcher, executor, types  # type: ignore
from aiogram.utils.markdown import escape_md  # type: ignore
import asyncio

from stablecoin_rates.model import LendingRate
from stablecoin_rates.reporter.formatter import format_lending_rate_table
from stablecoin_rates.scraper import SCRAPER_METHODS

TOKEN_PATH = Path.cwd() / "telegram_token.txt"
_LOGGER = logging.getLogger(__name__)


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
        rates = await scrape_all_rates()
        formatted_message = "```\n" + format_lending_rate_table(rates) + "\n```"
        await bot.send_message(
            message.chat.id, formatted_message, parse_mode="MarkdownV2"
        )

    @dp.message_handler(commands=["help"])
    async def handle_help(message: types.Message):
        await message.answer("/rates - Show the current lending rates")

    await bot.set_my_commands(
        [
            types.BotCommand("rates", "Show the current lending rates"),
            types.BotCommand("help", "Show the help documentation"),
        ]
    )

    try:
        await dp.start_polling()
    finally:
        await dp.wait_closed()
        await (await bot.get_session()).close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())

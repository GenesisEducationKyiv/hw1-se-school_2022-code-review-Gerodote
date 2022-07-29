import asyncio
import json

import aiofiles

import GetterPriceBinance
import mail_handler

str_disclaimer = "\n\n\nThis message was sent because you was" +\
" subscribed to have current price for this symbol. " +\
    "Price is calculated in way (best_ask_price + best_bid_price) / 2 ."

async def send_emails(mail_client, file_with_emails, subject_text, message_plain_text):
    async with aiofiles.open(file_with_emails, "r") as subscribed_emails:
        list_subscribed_emails = json.loads(await subscribed_emails.read())
        mail_client.send_plain_messages_to_emails(
                list_subscribed_emails=list_subscribed_emails,
                subject_text=subject_text,
                message_plain_text=message_plain_text
        )


async def main():
    binance_websocket = GetterPriceBinance.book_ticker_price_binance(symbol="BTCUAH")
    task_get_price = asyncio.create_task(binance_websocket.get_price("BTCUAH"))
    mail_client = mail_handler.factory_mail_handler(mode='gmail')
    await task_get_price
    price_to_send = task_get_price.result()
    task_send_emails = send_emails(mail_client=mail_client, 
                                   file_with_emails='subscribed_emails.json',
                                   subject_text="Ticker price BTC/UAH",
                                   message_plain_text=str(price_to_send) + str_disclaimer)
    await task_send_emails

if __name__ == "__main__":
    asyncio.run(main())

import asyncio

from fastapi import FastAPI, Form, HTTPException, status

import class_main

API = FastAPI()

main_object = class_main.MainApp()


@API.get("/rate")
async def get_rate():
    rate = main_object.get_rate()
    if rate is None:
        raise HTTPException(
            status_code=400,
            detail="Or try a little bit later, or check connection of server to Binance.",
        )
    else:
        return rate


@API.post("/subscribe")
async def subscribe(email: str = Form()):
    task = asyncio.create_task(main_object.subscribe(email))
    await task
    if task.result()[0] == 409:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=task.result()[1]
        )
    return {"description": task.result()[1]}


str_disclaimer = (
    "\n\n\nThis message was sent because you was"
    + " subscribed to have current price for this symbol. "
    + "Price is calculated in way (best_ask_price + best_bid_price) / 2 ."
)


@API.post("/sendEmails")
async def send_emails():
    rate = await main_object.get_rate()
    await main_object.send_emails(
        subject_text="GSES2 BTC application",
        message_plain_text=str(rate) + str_disclaimer,
    )
    return "Emails maybe sent. Check server's logs to check it's true or not."


@API.on_event("shutdown")
def shut_down():
    main_object.stop_binance_websocket()

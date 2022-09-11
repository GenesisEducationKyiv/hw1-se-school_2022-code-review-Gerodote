from fastapi import FastAPI, Form, HTTPException, status
from pydantic.error_wrappers import ValidationError

from src.email_handling.email_handler import AlreadyExist
from src.class_main import MainApp

API = FastAPI()

main_object = MainApp()


@API.get("/rate")
def get_rate():
    rate = main_object.get_rate()
    if rate is None:
        raise HTTPException(
            status_code=400,
            detail=
            "Or try a little bit later, or check connection of server to Binance.",
        )
    else:
        return rate


@API.post("/subscribe")
async def subscribe(email: str = Form()):
    try:
        task = await main_object.subscribe(email)
    except AlreadyExist as exception_obj:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=exception_obj.__str__())
    except ValidationError as exception_obj:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail=exception_obj.__str__())
    return {"description": "succesfully"}


@API.post("/sendEmails")
async def send_emails():
    await main_object.send_emails()
    return "Emails maybe sent. Check server's logs to check it's true or not."


# @API.on_event("shutdown")
# def shut_down():
#     main_object.stop_binance_websocket()

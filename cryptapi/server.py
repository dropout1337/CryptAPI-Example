from uvicorn import run
from fastapi import FastAPI, Request, HTTPException

from .db import Database
from .logging import logging

app = FastAPI(
    docs_url=None,
    redoc_url=None,
    openapi_url=None
)

database = Database()
whitelisted = ["145.239.119.223", "135.125.112.47"]

class Server():

    def __init__(self, host: str = "0.0.0.0", port: int = 80):
        self.host = host
        self.port = port
        self.app = app

    @app.on_event("startup")
    async def startup():
        logging.info("Started \x1b[38;5;63mfastapi\x1b[0m.\n")

    @app.on_event("shutdown")
    async def shutdown():
        print()
        logging.info("Shutting down \x1b[38;5;63mfastapi\x1b[0m api server.")
        database.close()

    @app.get("/api/callback")
    @app.post("/api/callback")
    async def callback(request: Request, user: str, uuid: str, address_in: str, txid_in: str, confirmations: int, value_coin: str, coin: str, result: str, txid_out: str = None, value_forwarded_coin: str = None):
        if not request.client.host in whitelisted:
            logging.info("\x1b[38;5;63m%s\x1b[0m tried to access the callback endpoint" % (request.client.host))
            return HTTPException(
                status_code=401,
                detail="IP not whtelisted."
            )
        
        if result == "pending":
            logging.info("Received payment of \x1b[38;5;63m%s\x1b[0m %s (\x1b[38;5;63m%s\x1b[0m)" % (value_coin, coin, txid_in))
            database.query("INSERT INTO transactions VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (user, uuid, address_in, txid_in, confirmations, value_coin, coin, ("pending" if result == "pending" else "completed"), txid_out, value_forwarded_coin,))
        else:
            logging.info("Completed payment \x1b[38;5;63m%s\x1b[0m %s (\x1b[38;5;63m%s\x1b[0m)" % (value_forwarded_coin, coin, txid_out))
            database.query("UPDATE transactions SET status=?, txid_out=?, value_forwarded_coin=? WHERE user=?", (("pending" if result == "pending" else "completed"), txid_out, value_forwarded_coin, user,))
        
        return {
            "error": False,
            "message": "Successfully received transaction."
        }

    def run(self):
        run(
            app=app,
            port=self.port,
            host=self.host,
            log_level="error"
        )
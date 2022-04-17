# CryptAPI Example
- CryptAPI.IO is an easy to use crypto api for fast and simple transactions.
- This example uses the fastapi libary for the callback server.

# Example
```py
import uuid
from cryptapi import API
from cryptapi import Server
from cryptapi import Database

api = API(
    coin="ltc",
    callback="https://..../api/callback",
    priority="default"
)
server = Server()
database = Database()

@server.app.get("/new")
async def new():
    user = str(uuid.uuid4())

    reply = api.create_address(
        "LaC9dPyA9McnVm4an4Ws4isJZfp7bYwFX1",
        user=user
    )

    return {
        "status": "success",
        "address": reply["address_in"],
        "user": user
    }

@server.app.get("/check")
async def check(user: str):
    reply = database.query("SELECT * FROM transactions WHERE user=?", (user,)).fetchall()
    if reply == []:
        return {
            "status": "failed",
            "message": "Invalid user."
        }

    else:
        reply = reply[0]
        return {
            "uuid": reply[1],
            "address_in": reply[2],
            "txid_in": reply[3],
            "confirmations": reply[4],
            "value_coin": reply[5],
            "coin": reply[6],
            "status": reply[7],
            "txid_out": reply[8],
            "value_forwarded_coin": reply[9]
        }

if __name__ == "__main__":
    server.run()
```
## Add your own endpoints
To add your own endpoint is quite easy, all you need is basic fastapi knowledge and your off.
It's the same as adding a endpoint using fastapi apart from the fact that it's not `@app.*` but `@server.app.*`
For example:
```py
from cryptapi import Server

server = Server()

@server.app.get("/")
async def root():
    return "hello world"

if __name__ == "__main__":
    server.run()
```
Also take in note that `/api/callback` is reserved for cryptapi's callbacks.

## Responses:
/new:
```json
{
    "status": "success",
    "address": "MA8iCxn2KmEyoZUPSDWXPbyBH3BytyosWY",
    "user": "8a7ae3a0-8e4d-4621-b2f1-be757a1a093d"
}
```
/check (pending)
```json
{
    "uuid": "b786c633-7b97-4c81-ab78-c244d125061e",
    "address_in": "MA8iCxn2KmEyoZUPSDWXPbyBH3BytyosWY",
    "txid_in": "3dd793b258022df421382cf6b370b739e32d21a605e091b1c695c74684c1739e",
    "confirmations": 0,
    "value_coin": "0.002",
    "coin": "ltc",
    "status": "pending",
    "txid_out": null,
    "value_forwarded_coin": null
}
```
/check (confirmed)
```json
{
    "uuid": "b786c633-7b97-4c81-ab78-c244d125061e",
    "address_in": "MA8iCxn2KmEyoZUPSDWXPbyBH3BytyosWY",
    "txid_in": "3dd793b258022df421382cf6b370b739e32d21a605e091b1c695c74684c1739e",
    "confirmations": 0,
    "value_coin": "0.002",
    "coin": "ltc",
    "status": "completed",
    "txid_out": "b30be3f0e1b8412fc7adbf463d0022387fa0e721f7c485c904143eff34d461f9",
    "value_forwarded_coin": "0.00119789"
}
```
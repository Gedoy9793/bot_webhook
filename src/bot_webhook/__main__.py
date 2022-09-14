import asyncio
from .flask import app


app.run()
asyncio.get_event_loop().run_forever()
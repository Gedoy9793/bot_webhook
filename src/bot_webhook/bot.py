import asyncio
import json
from threading import Thread

import websockets

from .hooks import getHook

_bots = {}

class Bot:
    def __new__(cls, name='defaule'):
        if name in _bots:
            return _bots[name]
        else:
            obj = object.__new__(cls)
            _bots[name] = obj
            return obj

    def __init__(self) -> None:
        self._send_list = []
        self._send_list_semaphore = asyncio.Semaphore(value=0)

    def schedule(self, url, verify, qq, syncId=0):
        self.url = url
        self.verify = verify
        self.bot = qq
        self.syncId = syncId

    def start(self):
        self.main_task: asyncio.Task = None

        def live_thread():
            async def main():
                self.main_task = asyncio.create_task(self.connect())
                await self.main_task

            asyncio.run(main())
            if self.main_task._exception is not None:
                self.handler.onException(self.main_task._exception)

        self.thread = Thread(target=live_thread)
        self.thread.setDaemon(True)
        self.thread.start()
        return self.thread

    def stop(self):
        self.main_task.cancel()

    async def connect(self):
        self.websocket = await websockets.connect(f"ws://{self.url}/all?verifyKey={self.verify}&qq={self.bot}")
        print("connected")
        await asyncio.wait([self._recv(), self._send()])

    async def _recv(self):
        self.session = json.loads(await self.websocket.recv()).get('data').get('session')
        while True:
            recv = json.loads(await self.websocket.recv())
            getHook(recv['data']['type'])(self, recv['data'])

    async def _send(self):
        while True:
            await self._send_list_semaphore.acquire()
            data = self._send_list.pop(0)
            await self.websocket.send(json.dumps({
                'syncId': data['syncId'],
                'command': data['command'],
                'subCommand': data['subCommand'],
                'content': data['content']
            }))

    def send(self, data, cmd, scmd=None):
        self._send_list.append({
            'syncId': self.syncId,
            'command': cmd,
            'subCommand': scmd,
            'content': data
        })
        self._send_list_semaphore.release()
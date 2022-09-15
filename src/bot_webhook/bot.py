import asyncio
import json
from threading import Thread

import websockets
from . import settings

from .hooks import getHook

_bots = {}

class Bot:
    session = None
    connected = False

    def __new__(cls, name='defaule'):
        if name in _bots:
            return _bots[name]
        else:
            obj = object.__new__(cls)
            _bots[name] = obj
            return obj

    def __init__(self) -> None:
        self._send_list = []

        self.main_task: asyncio.Task = None
        self.loop = asyncio.new_event_loop()
        self._send_list_semaphore = asyncio.Semaphore(value=0, loop=self.loop)

        def live_thread():
            asyncio.set_event_loop(self.loop)

            async def main():
                self.main_task = asyncio.create_task(self.connect())
                await self.main_task

            self.loop.run_until_complete(main())
            if self.main_task._exception is not None:
                self.handler.onException(self.main_task._exception)

        self.thread = Thread(target=live_thread)
        self.thread.setDaemon(True)

    def schedule(self, url, verify, qq, syncId=0):
        self.url = url
        self.verify = verify
        self.bot = qq
        self.syncId = syncId

    def start(self):
        self.thread.start()
        return self.thread

    def stop(self):
        self.main_task.cancel()

    async def _get_connect(self):
        while True:
            try:
                return await websockets.connect(f"ws://{self.url}/all?verifyKey={self.verify}&qq={self.bot}" + (f"&sessionKey={self.session}" if self.session is not None else ""))
            except ConnectionRefusedError:
                await asyncio.sleep(1)

    async def connect(self):
        self.websocket = await self._get_connect()
        self.connected = True
        await asyncio.wait([self._recv(), self._send()])

    async def _recv(self):
        self.session = json.loads(await self.websocket.recv()).get('data').get('session')
        while True:
            try:
                while not self.connected:
                    await asyncio.sleep(1)
                recv = json.loads(await self.websocket.recv())
                if recv.get("data").get("type") is not None:
                    print(recv)
                    getHook(recv['data']['type'])(self, recv['data'])
            except:
                self.connected = False
                self.websocket = await self._get_connect()
                self.connected = True

    async def _send(self):
        while True:
            await self._send_list_semaphore.acquire()
            data = self._send_list.pop(0)
            while not self.connected:
                await asyncio.sleep(1)
            while self.session is None:
                await asyncio.sleep(1)
            if data.get('content') is not None:
                data['content']['sessionKey'] = self.session
            await self.websocket.send(json.dumps(data))

    def send(self, data, cmd, scmd=None):
        send_data = {
            'syncId': self.syncId,
            'command': cmd,
            'subCommand': scmd,
            'content': data
        }
        self._send_list.append(send_data)
        self._send_list_semaphore.release()

    def send_group_text(self, msg):
        self.send({
            "target":settings.QQ_GROUP,
            "messageChain":[
                { "type": "Plain", "text": msg },
            ]
        }, 'sendGroupMessage')

    def send_text(self, qq, msg):
        self.send({
            "target": qq,
            "messageChain":[
                { "type": "Plain", "text": msg },
            ]
        }, 'sendFriendMessage')

import asyncio

class EventBus:

    def __init__(self):
        self.subscribers = []

    async def publish(self, event):
        for sub in self.subscribers:
            await sub(event)

    def subscribe(self, fn):
        self.subscribers.append(fn)

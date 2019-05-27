from datetime import datetime

class Melee():
    def __init__(self):
        self.talked = False
        self.date = datetime.today().weekday() 

    async def on_message(self, message):
        if 'melee' in message.content.lower() and not self.talked and self.date == 4:
            self.talked = True
            msg = 'bora' if 'bora melee' in message.content.lower() else 'bora melee'
            await message.channel.send(msg)

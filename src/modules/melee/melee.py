class Melee():
    def __init__(self):
        self.talked = False
    
    async def on_message(self, message):
        if 'melee' in message.content.lower() and not self.talked:
            self.talked = True
            msg = 'bora' if 'bora melee' in message.content.lower() else 'bora melee'
            await message.channel.send(msg)
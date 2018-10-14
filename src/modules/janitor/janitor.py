import time

class Janitor():
    def __init__(self):
        self.last_attempt = 0

    async def on_message(self, message):
        if message.channel.name == 'waifus' and message.author.bot and self.is_claimable(message):
            if self.check_cooldown():
                await message.add_reaction('💖')
        elif message.content.startswith('$repeat') and message.channel.name in ['spam', 'waifus']:
            await message.channel.send(' '.join(message.content.split()[1:]))

    def is_claimable(self, message):
        return message.embeds and message.embeds[0].image.url

    def check_cooldown(self):
        current_time = time.time()
        if current_time - self.last_attempt >= 3600:
            self.last_attempt = current_time
            return True
        return False

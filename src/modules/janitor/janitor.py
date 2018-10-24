import time
import os
from util import is_banned

class Janitor():
    def __init__(self):
        self.last_attempt = 0
        self.can_react = False
        self.hunting = []

    async def on_message(self, message):
        if message.channel.name == 'waifus' and message.author.bot and self.is_claimable(message):
            if self.check_cooldown() and self.can_react:
                if self.hunting:
                    if message.embeds[0].author.name.lower() in map(lambda x: x.lower(), self.hunting):
                        self.remove_hunted(message.embeds[0].author.name)
                        await self.react(message)
                else:
                    await self.react(message)
        elif message.channel.name == 'waifus' and self.is_roll(message.content):
            self.can_react = True
        elif message.content.startswith('$repeat') and message.channel.name in ['spam', 'waifus'] and not is_banned(message.author):
            await message.channel.send(' '.join(message.content.split()[1:]))
        elif message.content.startswith('$hunting') and message.channel.name in ['spam', 'waifus']:
            await message.channel.send(f'I am hunting: { self.format_list(self.hunting) }')
        elif message.content.startswith('$hunt') and message.author.id == os.environ['OWNER_ID']:
            character = ' '.join(message.content.split()[1:])
            if character.lower() in map(lambda x: x.lower(), self.hunting):
                await message.add_reaction('❌')
            else:
                self.hunting.append(character)
                await message.add_reaction('✅')

    async def react(self, message):
        self.can_react = False
        await message.add_reaction('💖')
    
    def format_list(self, list):
        if len(list) == 0:
            return 'nobody'
        return ', '.join(list)
    
    def remove_hunted(self, hunted):
        hunted_index = None
        for i in range(len(self.hunting)):
            if hunted.lower() == self.hunting[i].lower():
                hunted_index = i
        self.hunting.pop(hunted_index)

    def is_claimable(self, message):
        return message.embeds and message.embeds[0].image.url

    def is_roll(self, message):
        return message.startswith('$') and message[1] in ['h', 'w', 'm']

    def check_cooldown(self):
        current_time = time.time()
        if current_time - self.last_attempt >= 3600:
            self.last_attempt = current_time
            return True
        return False

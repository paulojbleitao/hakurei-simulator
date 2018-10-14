import discord
from modules.markov.markov_commands import MarkovCommands
from modules.janitor.janitor import Janitor

class HakureiSimulator(discord.Client):
    def __init__(self):
        super().__init__()
        self.markov = MarkovCommands()
        self.janitor = Janitor()

    async def on_ready(self):
        print(f'\n\nLogging in as {self.user.name}')

        await self.change_presence(game=discord.Game(name='with words'))
        print(f'Successfully logged in and booted...!')

    async def on_message(self, message):
        await self.janitor.on_message(message)
        await self.markov.on_message(message)

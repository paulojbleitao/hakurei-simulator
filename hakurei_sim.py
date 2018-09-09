import discord
from markov import Markov
from my_token import TOKEN

description = """
A bot that utilizes Markov chains to generate text based on user's messages.
"""

class HakureiSimulator(discord.Client):
    def __init__(self):
        super().__init__()
        self.prefix = 'h!'
        self.markov = Markov()

    def is_command(self, message):
        return (message.content.startswith(self.prefix)
                or message.content.startswith(self.user.mention))

    async def on_ready(self):
        print(f'\n\nLogging in as {self.user.name}')

        await self.change_presence(game=discord.Game(name='with words'))
        print(f'Successfully logged in and booted...!')

    async def on_message(self, message):
        if not message.author.bot:
            if not self.is_command(message):
                self.markov.add_message(message.content)
            else:
                await self.select_command(message)
    
    async def select_command(self, message):
        command = await self.format_message(message.content)
        if command == 'talk':
            await self.talk(message.channel)
        elif command == 'help':
            await self.help(message.channel)
        else:
            await self.unknown_command(message.channel)

    async def format_message(self, message):
        if message.startswith(self.prefix):
            m = message.replace(self.prefix, '')
        else:
            m = message.replace(self.user.mention, '')
        
        return m.strip()

    async def talk(self, channel):
        await channel.send(self.markov.generate_message())

    async def help(self, channel):
        message = ("Hi! To use a command, start your message with `h!` or by mentioning me.\n\n" +
            "The commands currently available are:\n" +
            "\t- **help**: to make me send this very message again, though I'm not sure why you would want to do that.\n" +
            "\t- **talk**: to make me say a random sentence based on *your* messages!")

        await channel.send(message)

    async def unknown_command(self, channel):
        await channel.send("Sorry, I don't understand. Try typing `h! help`!")

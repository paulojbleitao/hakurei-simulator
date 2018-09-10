import discord
from markov import Markov
from my_token import TOKEN

class HakureiSimulator(discord.Client):
    def __init__(self):
        super().__init__()
        self.prefix = 'h!'
        self.markov = Markov()

    async def on_ready(self):
        print(f'\n\nLogging in as {self.user.name}')

        await self.change_presence(game=discord.Game(name='with words'))
        print(f'Successfully logged in and booted...!')
   
    def is_command(self, message):
        return (message.content.startswith(self.prefix)
                or message.content.startswith(self.user.mention))

    # this blocks an annoying user
    def is_zino(self, user):
        return user.id == 320379142774194176

    async def on_message(self, message):
        if not message.author.bot:
            if not self.is_command(message) and message.guild:
                if not self.is_zino(message.author):
                    self.markov.add_message(message.content)
            else:
                await self.select_command(message)
    
    async def select_command(self, message):
        if not message.guild or message.channel.name == 'spam':
            command = await self.format_message(message.content)
            if command == 'talk':
                await self.talk(message.channel)
            elif command == 'help':
                await self.help(message.channel)
            elif command == 'stats':
                await self.stats(message.channel)
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

    async def stats(self, channel):
        await channel.send(self.markov.statistics())

    async def help(self, channel):
        message = (
            "Hi! To use a command, start your message with `h!` or by mentioning me.\n\n"
            "The commands currently available are:\n"
            "\t- **help**: to make me send this very message again, though I'm not sure why you would want to do that.\n"
            "\t- **talk**: to make me say a random sentence based on *your* messages!\n"
            "\t- **stats**: to see some potentially interesting numbers!"
        )

        await channel.send(message)

    async def unknown_command(self, channel):
        await channel.send("Sorry, I don't understand. Try typing `h! help`!")

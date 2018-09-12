import discord
from markov import Markov
from my_token import TOKEN
from util import is_banned, is_hakurei_command, format_message

class HakureiSimulator(discord.Client):
    def __init__(self):
        super().__init__()
        self.prefix = 'h!'
        self.markov = Markov()

    async def on_ready(self):
        print(f'\n\nLogging in as {self.user.name}')

        await self.change_presence(game=discord.Game(name='with words'))
        print(f'Successfully logged in and booted...!')

    async def on_message(self, message):
        if not message.author.bot:
            if not is_hakurei_command(message) and message.guild:
                if not is_banned(message.author):
                    self.markov.add_message(message.content, message.author.name)
            else:
                await self.select_command(message)
    
    async def select_command(self, message):
        if not message.guild or message.channel.name == 'spam':
            command = format_message(message.content)
            if command == 'talk':
                await self.talk(message.channel)
            elif command == 'help':
                await self.help(message.channel)
            elif command == 'stats':
                await self.stats(message.channel)
            elif command.startswith('stats'):
                await self.word_stats(command, message.channel)
            else:
                await self.unknown_command(message.channel)

    async def talk(self, channel):
        await channel.send(self.markov.generate_message())

    async def stats(self, channel):
        await channel.send(self.markov.statistics())

    async def word_stats(self, command, channel):
        words = command.split()
        if len(words) > 2:
            await channel.send('Sorry, I can only provide the stats for one word at a time!')
        else:
            await channel.send(self.markov.word_statistics(words[1]))

    async def help(self, channel):
        message = (
            "Hi! To use a command, start your message with `h!` or by mentioning me.\n\n"
            "The commands currently available are:\n"
            "\t- **help**: to make me send this very message again, though I'm not sure why you would want to do that.\n"
            "\t- **talk**: to make me say a random sentence based on *your* messages!\n"
            "\t- **stats**: to see some potentially interesting numbers!\n\n"
            "You can check out my source code here: <https://github.com/paulojbleitao/hakurei-simulator>"
        )

        await channel.send(message)

    async def unknown_command(self, channel):
        await channel.send("Sorry, I don't understand. Try typing `h! help`!")

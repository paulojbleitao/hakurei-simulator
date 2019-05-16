banlist = [320379142774194176, 235917117575266304]
def is_banned(user):
    return user.id in banlist

prefix = 'h!'
my_mention = '<@487127745009025026>'
def is_hakurei_command(message):
    return (message.content.startswith(prefix)
            or message.content.startswith(my_mention))

def format_message(message):
    if message.startswith(prefix):
        m = message.replace(prefix, '')
    else:
        m = message.replace(my_mention, '')
    
    return m.strip()

def is_mention(word):
    return word.startswith('<@') and word.endswith('>')

def is_command(word):
    return word == 'h!' or word.startswith('!') or word.startswith('.')

def is_link(word):
    return word.startswith('http://') or word.startswith('https://')

def is_valid(word):
    return not (is_mention(word)
                or is_command(word)
                or is_link(word))

def is_channel_allowed(channel):
    print(channel.category_id)
    return (channel.category_id in [493563857290133504]
           or channel.name == 'hakusim-test')

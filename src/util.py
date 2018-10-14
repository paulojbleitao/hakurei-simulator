banlist = [320379142774194176]
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

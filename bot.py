import discord, os, json, requests, random, sqlite3
import commands, log

# load cfg
with open('config.json') as cfg_file:
    cfg = json.load(cfg_file)

CLIENT_TOKEN = cfg['token']

def reddit_link(subreddit):
    resp = requests.get(f'https://www.reddit.com/r/{subreddit}/hot/.json?limit=100', headers = {'User-agent': 'BentoBot 0.1'}).json()

    index = random.randrange(1, 100)

    link = resp['data']['children'][index]['data']['url']

    return link

def add_quote(message):
    conn = sqlite3.connect('quotes.db')
    conn.execute('CREATE TABLE IF NOT EXISTS quotes (string quote, string auth, datetime date)')

    quote = message.content[10:]
    auth = message.author.display_name
    date = message.created_at
    conn.execute('INSERT INTO quotes VALUES(?,?,?)',(quote, auth, date))

class BentoClient(discord.Client):
    async def on_ready(self):
        print('Logged on as: ', self.user)
        await client.change_presence(activity = discord.Game(name = '!help'))

    async def on_message(self, message):

        if message.author == self.user:
            return

        if message.content[:1] == '!':
            print('command detected - ' + message.content)

            args = message.content.split()

            command = args[0][1:]

            if command == 'hentai':

                link = reddit_link('hentai')

                await message.channel.send(link)

            elif command == 'animeme':

                link = reddit_link('animemes')

                await message.channel.send(link)

            elif command == 'meirl':

                link = reddit_link('anime_irl')

                await message.channel.send(link)
            
            elif command == 'addquote':
                add_quote(message)
                await message.channel.send('quote saved.')
            else:
                await message.channel.send('Bruv what the fuck are you saying?')            

client = BentoClient()

client.run(CLIENT_TOKEN)

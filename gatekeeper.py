import discord
from discord.ext import commands
import random
import string

client = commands.Bot(command_prefix='$')
client.remove_command("help")

@client.command(pass_context=True)
async def generate(ctx):
    N = 24
    res = ''.join(random.choices(string.ascii_uppercase + string.digits, k = N))    
    channel = ctx.message.channel
    await channel.send(str(res))
    with open("codes.txt", 'a') as f:
        f.write(str(res + '\n'))
    

@client.command(pass_context=True)
async def codes(ctx):
    with open("codes.txt", 'r') as h:
        for line in h:
                print(line.rstrip('\n'))
    
@client.event
async def on_message(message):
    if message.content.startswith('$authenticate'):
        channel = message.channel
        await channel.send("Send your auth key.")
        list = open("codes.txt").read().splitlines()

        def check(m):
            return m.content in list
        msg = await client.wait_for('message', check=check)
        await channel.send('Authenticated'.format(msg))
        guild = message.guild
        member = message.author
        role = discord.utils.get(guild.roles, name="Authenticated")
        await member.add_roles(role)
    await client.process_commands(message)
    

client.run("")

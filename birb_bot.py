import asyncio
import json
import random

import aiohttp
import discord
from discord.ext import commands

client = commands.Bot(command_prefix='birb ', case_insensitive=True)
client.remove_command('help')


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(name='bell toy', type=discord.ActivityType.playing))
    print("Logged in as {birb bot}!")


snipe_message_content = None
snipe_message_author = None
snipe_message_id = None


@client.command()
async def snipe(message):
    if snipe_message_content == None:
        await message.channel.send("Theres nothing to snipe.")
    else:
        embed = discord.Embed(description=f"{snipe_message_content}")
        embed.set_footer(text=f"Asked by {message.author.name}#{message.author.discriminator}",
                         icon_url=message.author.avatar_url)
        embed.set_author(name=f"<@{snipe_message_author}>")
        await message.channel.send(embed=embed)
        return


@client.event
async def on_message_delete(message):
    global snipe_message_content
    global snipe_message_author
    global snipe_message_id

    snipe_message_content = message.content
    snipe_message_author = message.author.id
    snipe_message_id = message.id
    await asyncio.sleep(60)

    if message.id == snipe_message_id:
        snipe_message_author = None
        snipe_message_content = None
        snipe_message_id = None


@client.command()
async def balance(ctx):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()

    wallet_amt = users[str(user.id)]["wallet"]
    bank_amt = users[str(user.id)]["bank"]

    em = discord.Embed(title=f"{ctx.author.name}'s balance", color=discord.Color.purple())
    em.add_field(name="Wallet:", value=wallet_amt)
    em.add_field(name="Bank:", value=bank_amt)
    await ctx.send(embed=em)


@client.command()
async def werk(ctx):
    await open_account(ctx.author)

    user = ctx.author

    users = await get_bank_data()

    earnings = random.randint(100, 850)

    await ctx.send(f",u went to walmert and earned {earnings} dolllars!!!!")

    users[str(user.id)]["wallet"] += earnings

    with open("birb_bank.json", "w") as f:
        json.dump(users, f)


@client.command()
async def beg(ctx):
    await open_account(ctx.author)

    user = ctx.author

    users = await get_bank_data()

    earnings = random.randint(10, 101)

    await ctx.send(f",somone gav u {earnings} dolllars!!!!")

    users[str(user.id)]["wallet"] += earnings

    with open("birb_bank.json", "w") as f:
        json.dump(users, f)


async def open_account(user):
    users = await get_bank_data()

    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["wallet"] = 0
        users[str(user.id)]["bank"] = 0

    with open("birb_bank.json", "w") as f:
        json.dump(users, f, indent=4)


async def get_bank_data():
    with open("birb_bank.json", "r") as f:
        users = json.load(f)

        return users


@client.command()
async def help(ctx):
    await ctx.send(
        'i am brib want sed her are commands plese give seed\n\nban - make bad pepl begone\n\nkick - angerrry bite person >:((((\n\npic - get cute birbs\n\nmute - make bad poepl be quiet\n\nconsume - yummy messages go nom (purge messages)\n\nsnipe - find them delete messages\n\nmy prefix is birb - never forget')


@client.command()
async def pic(ctx):
    async with aiohttp.ClientSession() as session:
        async with session.get('https://api.ksoft.si/images/rand-reddit/cockatiel', params={
            "remove_nsfw": "true",
            "span": "all"
        }, headers={"Authorization": f"Token 3aecfb32359f66871a0c1abc9fc0eaa790c05884"}) as resp:
            data = await resp.json()
    embed = discord.Embed(title=data['title'], url=data['source'], description=data['author'], color=0xDFC39A)
    embed.set_image(url=data['image_url'])
    await ctx.send(embed=embed)


@client.command()
async def kick(ctx, member: discord.Member, *, reason):
    if ctx.author.guild_permissions.administrator or ctx.author.guild_permissions.manage_members:
        embed = discord.Embed(title="Goodbye:wave:", url=str(member.avatar_url), color=0x00fbff)
        embed.add_field(name=f'''User "{str(member)}" got kicked''', value=f"""Reason: {str(reason)}""", inline=False)
        embed.set_footer(text=f"Requested by {str(ctx.author)}")
        await ctx.send(embed=embed)
        await member.ban(reason=reason)
    if not ctx.author.guild_permissions.administrator or ctx.author.guild_permissions.manage_members:
        await ctx.send('hey!!1!1! u cant do taht!!1!11!!!')
        print(f"{ctx.author} tried to kick someone without perms")


@client.command()
async def ban(ctx, member: discord.Member = None, *, reason=None):
    if ctx.author.guild_permissions.administrator or ctx.author.guild_permissions.manage_members:
        embed = discord.Embed(title="Goodbye:wave:", url=str(member.avatar_url), color=0x00fbff)
        embed.add_field(name=f'''User "{str(member)}" got banned''', value=f"""Reason: {str(reason)}""", inline=False)
        embed.set_footer(text=f"Requested by {str(ctx.author)}")
        await ctx.send(embed=embed)
        await member.ban(reason=reason)
    if not ctx.author.guild_permissions.administrator or ctx.author.guild_permissions.manage_members:
        await ctx.send('hey!!1!1! u cant do taht!!1!11!!!')
        print(f"{ctx.author} tried to ban someone without perms")


@client.command()
async def consume(ctx, limit: int):
    await ctx.message.delete()
    await ctx.channel.purge(limit=limit)
    await ctx.send(f"eaten `{limit}` messages")


@client.command()
async def mute(ctx, user, reason):
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    if not role:
        muted = await ctx.guild.create_role(name="Muted", reason="To use for muting")

    for channel in ctx.guild.channels:
        if isinstance(channel, discord.TextChannel):
            await channel.set_permissions(muted, send_messages=False, read_message_history=False, read_messages=False)


client.run('NzM3ODA1NzQ3MTUyMzU1Mzc5.XyCtJQ.9aXu7LYIMAtCVCsWo9pLG8SSHtk')

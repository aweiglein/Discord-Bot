import discord
import random
from discord.ext import commands
import praw
import datetime
from datetime import datetime, timedelta

bot = commands.Bot(command_prefix = '.')

# bot is ready
@bot.event
async def on_ready():
    print('bot is ready')
    
# message when a new user joins 
@bot.event
async def on_member_join(member):
    print(f'{member} has joined the server')
    
# message when a user laeves 
@bot.event
async def on_member_remove(member):
    print(f'{member} has left the server')

    
# ping in milliseconds
@bot.command()
async def ping(ctx):
    await ctx.send(f'pong! (round{bot.latency * 1000}) ms')

# 8ball questions and random answers
@bot.command()
async def eightball(ctx, *, question):
    responses = [
        'It is certain',
        'Without a doubt',
        'You may rely on it',
        'Yes definitely',
        'It is decidedly so',
        'As I see it, yes',
        'Most likely',
        'Yes',
        'Outlook good',
        'Signs point to yes',
        'Reply hazy try again',
        'Better not tell you now',
        'Ask again later',
        'Cannot predict now',
        'Concentrate and ask again',
        'Don’t count on it',
        'Outlook not so good',
        'My sources say no',
        'Very doubtful',
        'My reply is no']
    if '?' in question:
        await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')
    else:
        await ctx.send(f'Question: {question}?\nAnswer: {random.choice(responses)}')


@bot.command()
async def findBoardgame(ctx, *, favoriteGame):
    reddit = praw.Reddit(client_id = 'CLIENT ID',
                        client_secret = 'CLIENT SECRET',
                        username = 'USERNAME',
                        password = 'PASSWORD',
                        user_agent = 'USERAGENT')

    subreddit = reddit.subreddit('boardgames')
    top_boardgames = subreddit.top('month')
    count = 0
    for submission in top_boardgames:      
        if favoriteGame in submission.title and not submission.stickied:
            count += 1
            await ctx.send(f'\n{count}. Title: {submission.title}\nLink: {submission. url}\nUpvotes: {submission.ups}')

        else:
            await ctx.send(f'There are no mentions of {favoriteGame} in the top posts this month.')
            break

# clear last 5 messages
@bot.command()
async def clear(ctx, amount=40):
    await ctx.channel.purge(limit=amount)

# manually kick user
@bot.command()
async def kick(ctx, member : discord.Member, *, reason=None):
    await member.kick(reason=reason)

# manually ban user
@bot.command()
async def ban(ctx, member : discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'Banned: {member.mention}')

@bot.command()
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned: {user.mention}')
            return

bot.run('BOT TOKEN')
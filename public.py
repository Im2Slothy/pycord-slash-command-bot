#THIS REQUIRES PY CORD TO WORK! IF YOU DON'T HAVE IT VISIT THIS LINK FOR HELP! https://guide.pycord.dev/installation #
#Bot created by Slothy#4484 <-- Don't remove this if you plan on taking all this for yourself :)#

import discord
import random
import datetime
from datetime import timedelta
import os
import json
import math
from pydoc import describe
import random
from tkinter import Entry
from typing_extensions import Self
import asyncio
import discord
import aiohttp
import typing
bot = discord.Bot()


@bot.event
async def on_ready():
    print('The Public Bot is online')




# Start of Basic Random Commands to Add to your server #

#Bot's ping command#
@bot.command(description="Sends the bot's latency.") # this decorator makes a slash command
async def ping(ctx): # a slash command will be created with the name "ping"
    embed = discord.Embed(title='My ping!', description=f"**Pong! {round(bot.latency * 1000)}ms**", color=0xFF5733)
    await ctx.respond(embed=embed)

#Bot's Repeat Command#
@bot.command(description='Repeat After Me!')
async def repeat(ctx, *, message):
    await ctx.respond(message)
    await ctx.message.delete()

#Bot's FAQ Command#
@bot.command(description='FAQ!')
async def faq(ctx):
    embed = discord.Embed(title='FAQ!', description=f"PUT SOMETHING HERE", color=0xFF5733)
    await ctx.respond(embed=embed)
 
#Bot's Basic Command - Change to you're liking this is just an example#
@bot.command(description='Puggis')
async def pug(ctx):
  await ctx.respond("Bella Puggis Uggis Wuggis") # <--- This could be used for EX. users does Twitch and it displays Twitch.
 # If you want an embed do this and remove ^
 #embed = discord.Embed(title='pug', description=f'Bella Puggis Uggis Wuggis!', color=0xFF5733)
 #ctx.respond(embed=embed)

#Guild Member Count Command#
@bot.command(description='Member Count')
async def members(ctx):
    a=ctx.guild.member_count
    b=discord.Embed(title=f"Members in {ctx.guild.name}",description=a, color=0xFF5733)
    await ctx.respond(embed=b)
    
#8 ball Command#
@bot.command(description='8 Ball!')
async def _8ball(ctx,*, question):
    responses = ['It is certain',

                     'It is decidedly so',

                     'Without a doubt',

                     'Yes, definitely',

                     'You may rely on it',

                     'As I see it, yes',

                     'Most likely',

                     'Outlook good',

                     'Yes',

                     'Signs point to yes',

                     'Reply hazy try again',

                     'Ask again later',

                     'Better not tell you now',

                     'Cannot predict now',

                     'Concentrate and ask again',

                     'Do not count on it',

                     'My reply is no',

                     'My sources say no',

                     'Outlook not so good',

                     'Very doubtful']

    embed=discord.Embed(title=f"The 8Ball Says!",description=f'Question: {question}\nAnswer: {random.choice(responses)}',color=0x660066)
    await ctx.respond(embed=embed) 


#Random Fact Command#
@bot.command(description="Get a random fact.")
async def randomfact(self, context: Context) -> None:
    async with aiohttp.ClientSession() as session:
        async with session.get("https://uselessfacts.jsph.pl/random.json?language=en") as request:
            if request.status == 200:
                data = await request.json()
                embed = discord.Embed(description=data["text"],color=0xD75BF4)
            else:
                embed = discord.Embed(title="Error!",description="There is something wrong with the API, please try again later",color=0xE02B2B)
            await context.send(embed=embed)

# Random meme from reddit
@bot.command(description="Returns random memes from reddit.")
async def meme(ctx):
  res = requests.get("https://meme-api.herokuapp.com/gimme/memes").json() # Getting Requests
  meme_title = res['title']
  meme_link = res['postLink']
  meme_img = res['url']
  meme_author = res['author']
  meme_likes = res['ups']
  # Creating Embed
  x = discord.Embed(title=f"{meme_title}", url=f"{meme_link}")
  x.set_image(url=meme_img)
  x.set_footer(text=f"Redditor: {meme_author} • 👍 {meme_likes} | Requested By {ctx.author}")
  x.set_author(name=meme_author, url=f"https://www.reddit.com/user/{meme_author}", icon_url='https://media.discordapp.net/attachments/880439870374436864/882131944391999488/Reddit.png?width=417&height=417')
  await ctx.respond(embed=x)

 #Timer Command#
@bot.command(description='Timer')
async def timer(ctx, number:int):
    try:
        if number < 0:
            await ctx.respond('number cant be a negative')
        elif number > 300:
            await ctx.respond('number must be under 300')
        else:
            message = await ctx.send(number) # <--- Sometimes says sending the commmand but it'll still count down. Not sure why
            while number != 0:
                number -= 1
                await message.edit(content=number)
                await asyncio.sleep(1)
            await message.edit(content='Ended!')

    except ValueError:
        await ctx.respond('time was not a number')
        
#Poll Command#
@bot.command(description='Poll')
async def poll(ctx, option1: str, option2: str, *, question):
  if option1==None and option2==None:
    ctx.respond("You need to add another option...")
  elif option1==None:
    ctx.respond("You need to add another option...")
  elif option2==None:
    ctx.respond("You need to add another option...")
  else:
    await ctx.channel.purge(limit=1)
    message = await ctx.respond(f"```New poll: \n{question}```\n**✅ = {option1}**\n**❎ = {option2}**")
    await message.add_reaction('❎')
    await message.add_reaction('✅')
 
#User info Command#
@bot.command(description='user info')
async def userinfo(ctx , member: discord.Member = None):

    date_format = "%a, %d %b %Y %I:%M %p"
    members = sorted(ctx.guild.members, key=lambda m: m.joined_at)
    member = ctx.author if not member else member
    roles = [role for role in member.roles if role.name != '@everyone']

    embed = discord.Embed(color=0xdfa3ff, description=member.mention)
    embed.set_author(name=str(member), icon_url=member.avatar.url)
    embed.set_thumbnail(url=member.avatar.url)
    embed.add_field(name="Joined", value=member.joined_at.strftime(date_format))
    embed.add_field(name="Join position", value=str(members.index(member)+1))
    embed.add_field(name="Registered", value=member.created_at.strftime(date_format))
    if len(member.roles) > 1:
        role_string = ' '.join([r.mention for r in member.roles][1:])
        embed.add_field(name="Roles [{}]".format(len(member.roles)-1), value=role_string, inline=False)
        perm_string = ', '.join([str(p[0]).replace("_", " ").title() for p in member.guild_permissions if p[1]])
        embed.set_footer(text='ID: ' + str(member.id))
        return await ctx.respond(embed=embed)
      
#----------------------------------MODERATION COMMANDS----------------------------------------------------------#

#Clear messages#
@bot.command(description="Delete a number of messages.",) #<--- Possible Command Fix? Will text later
@discord.default_permissions(manage_messages = True)
async def clear(self, context: Context, amount: int) -> None:
    purged_messages = await context.channel.purge(limit=amount)
    embed = discord.Embed(
        title="Chat Cleared!",
        description=f"**{context.author}** cleared **{len(purged_messages)}** messages!",
        color=0x9C84EF)
    await context.send(embed=embed)

      
#Kick Member Command#
@bot.command(description="Kicks People!") # Kicks people
@discord.default_permissions(kick_members = True)
async def kick(ctx, member : discord.Member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.respond(f'{member.mention} has been kicked!')
      

#Ban Member Command#
@bot.command(description="Bans People!") # Bans people
@discord.default_permissions(ban_members = True)
async def ban(ctx, member : discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.respond(f'Banned {member.mention}')
    await ctx.respond('**Be gone!**')


#HackBan (Ban User not in your discord)
@bot.command(description="Bans a user without the user having to be in the server.")
@discord.default_permissions(ban_members = True)
async def hackban(self, context: Context, user_id: str, *, reason: str = "Not specified") -> None:
    try:
        await self.bot.http.ban(user_id, context.guild.id, reason=reason)
        user = self.bot.get_user(int(user_id)) or await self.bot.fetch_user(int(user_id))
        embed = discord.Embed(
            title="User Banned!",
            description=f"**{user} (ID: {user_id}) ** was banned by **{context.author}**!",color=0x9C84EF)
        embed.add_field(name="Reason:",value=reason)
        await context.send(embed=embed)
    except Exception as e:
            embed = discord.Embed(title="Error!",description="An error occurred while trying to ban the user. Make sure ID is an existing ID that belongs to a user.",color=0xE02B2B)
    await context.send(embed=embed)

#Unban members#
@bot.command()
async def unban(ctx, *, member):
    bans = await ctx.guild.bans(limit=150).flatten()
    if not bans:
        await ctx.respond("**The Ban List is empty!**")
        return
    try:
        member_id = int(member)
        user = await bot.fetch_user(member_id)
    except ValueError:
        try:
            name, discriminator = member.split("#")
            user = discord.utils.get(bans, name=name, discriminator=discriminator).user
        except:
            await ctx.respond("**Invalid user format. Please use either the user ID or username#discriminator.**")
            return
    if user in [ban_entry.user for ban_entry in bans]:
        await ctx.guild.unban(user)
        await ctx.respond(f"**Unbanned {user.name}**")
    else:
        await ctx.respond("**The user isn't banned.**")

#mute command#
@bot.command(description="mutes a specified member.") #<--- Should be mute command fix
@discord.default_permissions(mute_members = True)
async def mute(self, member : discord.Member, time : str,*, reason=None):
    ftime = time2sec(time)
    await member.timeout(timeout = utcnow() + timedelta(seconds = ftime), reason = reason)
    await bot.reply(f'{member.mention} has been muted for {time}.')

bot.run('TOKEN')

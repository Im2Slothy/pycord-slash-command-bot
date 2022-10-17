#THIS REQUIRES PY CORD TO WORK! IF YOU DON'T HAVE IT VISIT THIS LINK FOR HELP! https://guide.pycord.dev/installation #
#Bot created by Slothy#4484 <-- Don't remove this if you plan on taking all this for yourself :)#

import discord
import random
bot = discord.Bot()


@bot.event
async def on_ready():
    print('The Public Bot is online')




# Start of Basic Random Commands to Add to your server #

#Bot's ping command#
@bot.command(description="Sends the bot's latency.") # this decorator makes a slash command
async def ping(ctx): # a slash command will be created with the name "ping"
    embed = discord.Embed(title='My ping!', description=f"**Pong! {round(bot.latency * 1000)}ms**", color=discord.Color.black())
    ctx.respond(embed=embed)

#Bot's Repeat Command#
@bot.command(description='Repeat After Me!')
async def repeat(ctx, *, message):
    await ctx.respond(message)
    await ctx.message.delete()

#Bot's FAQ Command#
@bot.command(description='FAQ!')
async def faq(ctx):
    embed = discord.Embed(title='FAQ!', description=f"PUT SOMETHING HERE", color=discord.Color.purple())
 
#Bot's Basic Command - Change to you're liking this is just an example#
@bot.command(description='Puggis')
async def pug(ctx):
  await ctx.respond("Bella Puggis Uggis Wuggis") # <--- This could be used for EX. users does Twitch and it displays Twitch.
 # If you want an embed do this and remove ^
 #embed = discord.Embed(title='pug', description=f'Bella Puggis Uggis Wuggis!', color=0xFF5733)
 #ctx.respond(embed=embed)

#Guild Member Count Command#
@bor.command(description='Member Count')
async def members(ctx):
    a=ctx.guild.member_count
    b=discord.Embed(title=f"Members in {ctx.guild.name}",description=a,color=discord.Color((0xffff00)))
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
    
 #Timer Command#
@bot.command(description='Timer')
async def timer(ctx, number:int):
    try:
        if number < 0:
            await ctx.respond('number cant be a negative')
        elif number > 300:
            await ctx.respond('number must be under 300')
        else:
            message = await ctx.respond(number)
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
@bot.command('user info')
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
      
#------MODERATION------#
#Clear Chat Command#
@bot.command(description="Clears Chat!") #Clears Chat
@commands.has_guild_permissions(clear_messages = True)
async def clear(ctx, amount=5):
        await ctx.channel.purge(limit=amount)
        await ctx.respond('Messages have been cleared!')
      
#Kick Member Command#
@bot.command(description="Kicks People!") # Kicks people
@commands.has_guild_permissions(kick_members = True)
async def kick(ctx, member : discord.Member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.respond(f'{member.mention} has been kicked!')
      
#Ban Member Command#
@bot.command(description="Bans People!") # Bans people
@commands.has_guild_permissions(ban_members = True)
async def ban(ctx, user: typing.Union[discord.Member, int], *, reason=None):
    guild = client.get_guild(665944107025301504)
    if user in ctx.guild.members:
        await user.ban(reason=reason)
        await ctx.respond(f'Banned {user.mention}. That felt good.')
        #send banned user a message
        await user.send(f'You have been banned from {guild.name} for {reason}')
    else:
        await guild.ban(discord.Object(id = user))
        await ctx.respond(f'User has been hackbanned!\nUser: <@{user}>')
 client.run('TOKEN')
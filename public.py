#THIS REQUIRES PY CORD TO WORK! IF YOU DON'T HAVE IT VISIT THIS LINK FOR HELP! https://guide.pycord.dev/installation #
#Bot created by Slothy#4484 <-- Don't remove this if you plan on taking all this for yourself :)#

import discord
from discord.ext import commands, tasks
import random
from datetime import timedelta
import json
from pydoc import describe
from tkinter import Entry
from typing_extensions import Self
import asyncio
import requests
import datetime as time
import datetime
from tkinter.messagebox import NO
from discord import Embed
import json
from datetime import time
import time
import youtube_dl


bot = discord.Bot()

lock = asyncio.Lock()


youtube_dl.utils.bug_reports_message = lambda: ""


ytdl_format_options = {
    "format": "bestaudio/best",
    "outtmpl": "%(extractor)s-%(id)s-%(title)s.%(ext)s",
    "restrictfilenames": True,
    "noplaylist": True,
    "nocheckcertificate": True,
    "ignoreerrors": False,
    "logtostderr": False,
    "quiet": True,
    "no_warnings": True,
    "default_search": "auto",
    "source_address": (
        "0.0.0.0"
    ),  # Bind to ipv4 since ipv6 addresses cause issues at certain times
}

ffmpeg_options = {"options": "-vn"}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source: discord.AudioSource, *, data: dict, volume: float = 0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get("title")
        self.url = data.get("url")

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(
            None, lambda: ytdl.extract_info(url, download=not stream)
        )

        if "entries" in data:
            # Takes the first item from a playlist
            data = data["entries"][0]

        filename = data["url"] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)



#------------------------------------LOGs---------------------------------------------
role_message_id = (
    0,
)

emoji_to_role = {
    discord.PartialEmoji(
        name="👌"
    ): 0,  # ID of the role associated with unicode emoji '👌'.
    discord.PartialEmoji(
        name="✅"
    ): 0,  # ID of the role associated with unicode emoji '✅'.
    discord.PartialEmoji(
        name="🧓"
    ): 0,  # ID of the role associated with a partial emoji's ID.
}

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f'Something fun?'))

    await initialize_money_data()
    reset_deletion_count.start()

async def initialize_money_data():
    with open('YOURJSONFILENAME.json', 'r') as f:
        data = json.load(f)
    guild = bot.get_guild(786225335360290826)  # Replace YOUR_GUILD_ID with your actual guild ID

    for member in guild.members:
        user_id = str(member.id)
        if user_id not in data:
            data[user_id] = {
                'balance': 500,
                'last_payday': 0,
            }

    with open('YOURJSONFILENAME.json', 'w') as f:
        json.dump(data, f)
    print("Money data initialized.")

@bot.event
async def on_raw_reaction_add(payload: discord.RawReactionActionEvent):
    """Gives a role based on a reaction emoji."""
    # Make sure that the message the user is reacting to is the one we care about.
    if payload.message_id != role_message_id:
        return

    guild = bot.get_guild(payload.guild_id)
    if guild is None:
        # Make sure we're still in the guild, and it's cached.
        return

    try:
        role_id = emoji_to_role[payload.emoji]
    except KeyError:
        # If the emoji isn't the one we care about then exit as well.
        return

    role = guild.get_role(role_id)
    if role is None:
        # Make sure the role still exists and is valid.
        return

    try:
        # Finally, add the role.
        await payload.member.add_roles(role)
    except discord.HTTPException:
        # If we want to do something in case of errors we'd do it here.
        pass


@bot.event
async def on_raw_reaction_remove(payload: discord.RawReactionActionEvent):
    """Removes a role based on a reaction emoji."""
    # Make sure that the message the user is reacting to is the one we care about.
    if payload.message_id != role_message_id:
        return

    guild = bot.get_guild(payload.guild_id)
    if guild is None:
        # Make sure we're still in the guild, and it's cached.
        return

    try:
        role_id = emoji_to_role[payload.emoji]
    except KeyError:
        # If the emoji isn't the one we care about then exit as well.
        return

    role = guild.get_role(role_id)
    if role is None:
        # Make sure the role still exists and is valid.
        return

    # The payload for `on_raw_reaction_remove` does not provide `.member`
    # so we must get the member ourselves from the payload's `.user_id`.
    member = guild.get_member(payload.user_id)
    if member is None:
        # Make sure the member still exists and is valid.
        return

    try:
        # Finally, remove the role.
        await member.remove_roles(role)
    except discord.HTTPException:
        # If we want to do something in case of errors we'd do it here.
        pass




# Threshold value for number of deleted roles/channels
THRESHOLD = 3

# ID of the "Commissioners" role
COMMISSIONERS_ROLE_ID = 0

# Dictionary to store count of deleted roles/channels for each user
user_deletion_count = {}

@tasks.loop(minutes=5)
async def reset_deletion_count():
    global user_deletion_count
    user_deletion_count = {}

@bot.event
async def on_guild_channel_delete(channel):
    try:
        log = await channel.guild.audit_logs(limit=1, action=discord.AuditLogAction.channel_delete).flatten()
        user = log[0].user
        member = channel.guild.get_member(user.id)
        
        if member and COMMISSIONERS_ROLE_ID not in [role.id for role in member.roles]:
            await update_deletion_count(user.id)
            guild = bot.get_guild(ID)
            logchannel = guild.get_channel(ID)
            await logchannel.send(f"{member.mention} has deleted a channel.\nChannel that was deleted: {channel.name}\n<@&786226115147988994>")
            
            if user_deletion_count[user.id] >= THRESHOLD:
                await member.edit(roles=[])
                channel = guild.get_channel(ID)
                await channel.send(f"{member.mention} has had all their roles removed for deleting 3 channels in a short amount of time. If this is a mistake please add their roles back.")
    except Exception as e:
        print(f"Error in on_guild_channel_delete: {e}")

@bot.event
async def on_guild_role_delete(role):
    try:
        log = await role.guild.audit_logs(limit=1, action=discord.AuditLogAction.role_delete).flatten()
        user = log[0].user
        member = role.guild.get_member(user.id)
        
        if member and COMMISSIONERS_ROLE_ID not in [role.id for role in member.roles]:
            await update_deletion_count(user.id)
            guild = bot.get_guild(ID)
            logchannel = guild.get_channel(ID)
            await logchannel.send(f"{member.mention} has deleted a role.\nRole that was deleted: {role.name}\n<@&786226115147988994>")
            
            if user_deletion_count[user.id] >= THRESHOLD:
                await member.edit(roles=[])
                channel = guild.get_channel(ID)
                await channel.send(f"{member.mention} has had all their roles removed for deleting 3 channels in a short amount of time. If this is a mistake please add their roles back.")
    except Exception as e:
        print(f"Error in on_guild_role_delete: {e}")

async def update_deletion_count(user_id):
    if user_id in user_deletion_count:
        user_deletion_count[user_id] += 1
    else:
        user_deletion_count[user_id] = 1



@bot.event
async def on_message_delete(message):
    if message.author == bot.user:
        return
    elif message.author.bot == True:
        return
    delete_embed=discord.Embed(title = f"Message Deleted", description= f'**User:** <@{message.author.id}>\n**Channel:** <#{message.channel.id}>\n**Server:** {message.guild}\n**Message:** \n{message.content}', color=0xbf0404)
    delete_embed.set_footer(text=f"Message ID: {message.id}")
    delete_embed.set_author(name =f"{message.author}", icon_url=message.author.avatar.url)
    archive_delete=bot.get_channel(ID) #Grabs the ID of the Deleted Messages Channel where the archive is to be stored.
    if message.attachments:
        new_url = message.attachments[0].url.replace('cdn.discordapp.com', 'media.discordapp.net')
        delete_embed.set_image(url=new_url)
    else:
        pass
    await archive_delete.send(embed=delete_embed)

@bot.event
async def on_message_edit(message_before, message_after):
    if message_after.author.bot:
        return
    embed=discord.Embed(title = f"Message Edited", description= f'**User:** <@{message_before.author.id}>\n**Channel:** <#{message_before.channel.id}>\n**Server:** {message_before.guild}\n**Unedited Message:** \n{message_before.content}\n**Edited Message:**\n{message_after.content}', color=0xbf0404)
    embed.set_footer(text=f"Message ID: {message_before.id}")
    embed.set_author(name =f"{message_after.author}", icon_url=f"{message_after.author.avatar.url}")
    embed.timestamp = time.datetime.utcnow()
    embed.set_footer(text=f"ID: {message_before.author.id}")
    channel=bot.get_channel(ID)
    await channel.send(embed=embed)


@bot.event
async def on_reaction_remove(reaction, user):
    message = reaction.message
    channel = bot.get_channel(ID)
    embed=discord.Embed(title=f"**A reacton from a message was removed!**".format(message.author.name), description=f"User that removed reaction: <@{user.id}>", color=0x660066)
    embed.add_field(name="**This is the channel the message reaction was removed in:**", value=str(message.channel), inline=False)
    embed.add_field(name="**This is the message that had a reaction removed:**", value=message.content, inline=True)
    embed.add_field(name="**This was the emoji reaction that was removed:**", value=str(reaction), inline=True)
    await channel.send(embed=embed)

#----------MEMBER JOIN AND LEAVE---------- BOT GOING ONLINE -----------------------------


class nitroButtons(discord.ui.View):
    @discord.ui.button(label=f'{"Claim":⠀^37}', custom_id="fun (nitro)", style=discord.ButtonStyle.success)
    async def nitroButton(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.send_message(content="Oh no it was a fake", ephemeral=True)
        await asyncio.sleep(2)

        message = await interaction.original_response()

        await message.edit(content="Prepare to get rickrolled...(it's a good song anyway)")
        await asyncio.sleep(2)

        await message.edit(content="https://i.imgur.com/NQinKJB.gif")

        button.disabled = True
        button.style = discord.ButtonStyle.secondary
        button.label = f'{"Claimed":⠀^39}'

        embed = discord.Embed(
            title="You received a gift, but...",
            description="The gift link has either expired or has been\nrevoked.",
            color=3092790,
        )
        embed.set_thumbnail(url="https://i.imgur.com/w9aiD6F.png")

        await interaction.message.edit(view=self, embed=embed)

@bot.command(brief="based on pog bot's nitro command")
async def nitro(ctx):
    embed = discord.Embed(
        title="You've been gifted a subscription!",
        description="You've been gifted Nitro for **1 month!**\nExpires in **24 hours**",
        color=3092790,
    )
    embed.set_thumbnail(url="https://i.imgur.com/w9aiD6F.png")

    view = nitroButtons(timeout=180.0)
    await ctx.channel.purge(limit=1)
    await ctx.respond("Prank in motion", ephemeral=True)
    await ctx.respond(embed=embed, view=view)



@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f'over passengers'))

    await initialize_money_data()

async def initialize_money_data():
    with open('YOURJSONFILENAME.json', 'r') as f:
        data = json.load(f)
    guild = bot.get_guild(ID)  # Replace YOUR_GUILD_ID with your actual guild ID

    for member in guild.members:
        user_id = str(member.id)
        if user_id not in data:
            data[user_id] = {
                'balance': 500,
                'last_payday': 0,
            }

    with open('YOURJSONFILENAME.json', 'w') as f:
        json.dump(data, f)
    print("Money data initialized.")

@bot.event
async def on_member_join(member):
    guild = bot.get_guild(ID)
    channel = guild.get_channel(ID)
    role = discord.utils.get(guild.roles, name="Member", id=ID)
    embed=discord.Embed(title="Member Has Joined The Discord", description=f"This is a cool log to show who joined the server!")
    embed.add_field(name="Name", value=f"{member.display_name}", inline=True)
    embed.add_field(name="Discord", value=f"{member.mention}", inline=True)
    embed.set_footer(text='ID: ' + str(member.id))
    embed.set_footer(text="Stay cool!")
    embed.timestamp = time.datetime.utcnow()
    embed.set_footer(text=f"ID: {member.id}")
    await channel.send(embed=embed)

@bot.event
async def on_member_remove(member):
    guild = bot.get_guild(ID)
    channel = guild.get_channel(ID)
    embed=discord.Embed(title="Member Has Left The Discord", description=f"The member below has left our server. You'll find their roles and other information to help you identify the person!")
    embed.add_field(name="Name", value=f"{member.display_name}", inline=True)
    embed.add_field(name="Discord", value=f"{member.mention}", inline=True)
    if len(member.roles) > 1:
        role_string = ' '.join([r.mention for r in member.roles][1:])
        embed.add_field(name="Roles [{}]".format(len(member.roles)-1), value=role_string, inline=False)
        perm_string = ', '.join([str(p[0]).replace("_", " ").title() for p in member.guild_permissions if p[1]])
        embed.set_footer(text='ID: ' + str(member.id))
        embed.set_footer(text="Stay cool!")
    embed.timestamp = time.datetime.utcnow()
    embed.set_footer(text=f"ID: {member.id}")
    await channel.send(embed=embed)




@bot.command()
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
      
@bot.command()
async def johncount(ctx):
    await ctx.respond(f"https://media.discordapp.net/attachments/953763484213051442/1020851254873821184/john2.png")

@bot.command(help = "what does the magic conch say to you?")
async def conch(ctx,*, question):
    shell = ["https://media.discordapp.net/attachments/1066094079496167575/1072610302199349339/RPReplay_Final1675790799.mov", "https://media.discordapp.net/attachments/1066094079496167575/1072610281408176138/RPReplay_Final1675790470.mov", "https://media.discordapp.net/attachments/1066094079496167575/1072610275951399043/RPReplay_Final1675790369.mov", "https://media.discordapp.net/attachments/1066094079496167575/1072610270972743731/RPReplay_Final1675790239.mov", "https://media.discordapp.net/attachments/1066094079496167575/1072610265276891207/RPReplay_Final1675779095.mov", "https://media.discordapp.net/attachments/1066094079496167575/1072610260088533112/RPReplay_Final1675779029.mov", "https://media.discordapp.net/attachments/1066094079496167575/1072610254329761843/RPReplay_Final1675778960.mov"] 
    pick = ((random.choice(shell)))
    b=discord.Embed(title=f"The Conch has spoken!",description=f'Answer:',color=0x660066)
    await ctx.respond(embed=b)  
    await ctx.respond(f"{pick}")


@bot.command()
async def repeat(ctx, *, message):
    this = await ctx.respond("Message Sent. Deleting in... Now!")
    await ctx.send(message)
    await ctx.message.delete()
    await asyncio.sleep(5)
    await this.delete()


@bot.command()
async def pug(ctx):
    await ctx.respond("https://media.discordapp.net/attachments/763487896304353310/975123673482678282/unknown.png")
    await ctx.respond('Bella Puggis Uggis Wuggis!')


@bot.command()
async def ping(ctx):
    b=discord.Embed(title=f"Ping?!",description=f"Pong! {round(bot.latency * 1000)}ms",color=0xFF5733)
    await ctx.respond(embed=b)


@bot.command(aliases=['8ball', 'test'])

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

    b=discord.Embed(title=f"The 8Ball Says!",description=f'Question: {question}\nAnswer: {random.choice(responses)}',color=0x660066)
    await ctx.respond(embed=b)  


@bot.command()
async def twitch(ctx):
        b=discord.Embed(title=f"The Twitch!",description="https://www.twitch.tv/jamesblondie",color=0x6495ED)
        await ctx.respond(embed=b)

@bot.command(aliases=["mc"])
async def members(ctx):
    a=ctx.guild.member_count
    b=discord.Embed(title=f"Members in {ctx.guild.name}",description=a,color=discord.Color((0xffff00)))
    await ctx.respond(embed=b, ephemeral=True)
      

# ----------------------------- XP STUFF -----------------------------

# Event to handle messages (including images)

xp_lock = asyncio.Lock()

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    # XP for sending a message
    xp_gain = 10

    # Additional XP for sending an image
    if any(attachment.url.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')) for attachment in message.attachments):
        xp_gain += 25

    # Check for the word "Kanye" and delete the message
    if "kanye" in message.content.lower():
        await message.delete()
        await message.channel.send("No Ye Allowed")
        return  # Return immediately to avoid processing XP and commands

    await update_xp_and_check_rank(message, xp_gain)

    await bot.process_commands(message)

async def is_channel(ctx):
    return ctx.channel.id == 1021947000394108929



# Define Role IDs for each rank
promo_IDS = {
    0: None,         # No role for Rank 0
    1: 1138348105167818767,  # Replace with actual Role ID for Rank 1
    2: 1138348136801255545,  # Replace with actual Role ID for Rank 2
    3: 1138348174189285377,  # Replace with actual Role ID for Rank 3
    4: 1138348204639928331,  # Replace with actual Role ID for Rank 4
    5: 1138348226706145453,  # Replace with actual Role ID for Rank 5
}

async def update_xp_and_check_rank(ctx, xp_gain):
    async with xp_lock:  # Acquire the lock

        user_id = str(ctx.author.id)
        with open('xpjson.json', 'r') as f:
            data = json.load(f)

        if user_id not in data:
            data[user_id] = {'xp': 0, 'rank': 0}

        data[user_id]['xp'] += xp_gain

        old_rank = data[user_id]['rank']
        new_rank = get_rank(data[user_id]['xp'])

        # Check if the user ranked up
        if new_rank > old_rank:
            data[user_id]['rank'] = new_rank
            # Remove old role and add new one
            old_role = discord.utils.get(ctx.guild.roles, id=promo_IDS[old_rank])
            new_role = discord.utils.get(ctx.guild.roles, id=promo_IDS[new_rank])
            if old_role:
                await ctx.author.remove_roles(old_role)
            if new_role:
                await ctx.author.add_roles(new_role)

            # Congratulate the user in the bot command channel
            command_channel = discord.utils.get(ctx.guild.text_channels, name='🚦signal-box')
            if command_channel:
                await command_channel.send(f"Congratulations {ctx.author.mention}! You've ranked up to Rank {new_rank}!")

        # Don't forget to save the updated data
        with open('xpjson.json', 'w') as f:
            json.dump(data, f)




# Function to get the rank based on XP
def get_rank(xp):
    if xp < 100:
        return 0
    elif xp < 1000:
        return 1
    elif xp < 7500:
        return 2
    elif xp < 15000:
        return 3
    elif xp < 30000:
        return 4
    else:
        return 5

#    ---------------------^^^ XP SYSYEM ^^^-----------------------



@bot.command()
async def bank(ctx):
    with open('YOURJSONFILENAME.json', 'r') as f:
        data = json.load(f)
    user_id = str(ctx.author.id)
    if user_id not in data:
        embed = discord.Embed(
            title="Bank",
            description="You don't have any money yet.",
            color=discord.Color.red()
        )
    else:
        balance = data[user_id]['balance']
        embed = discord.Embed(
            title="Bank",
            description=f"Your balance: {balance} coins.",
            color=discord.Color.green()
        )
    await ctx.respond(embed=embed, ephemeral=True)

@bot.command()
async def leaderboard(ctx):
    royal_purple = 0x8A2BE2

    # First Embed (XP Leaderboard)
    with open('xpjson.json', 'r') as f:
        xp_data = json.load(f)
    top_xp_users = sorted(xp_data.items(), key=lambda x: x[1]['xp'], reverse=True)[:5]

    # Second Embed (Economy Leaderboard)
    with open('YOURJSONFILENAME.json', 'r') as f:
        economy_data = json.load(f)
    top_economy_users = sorted(economy_data.items(), key=lambda x: x[1]['balance'], reverse=True)[:5]

    # Create a single embed for both leaderboards
    combined_embed = discord.Embed(title="Leaderboards", color=royal_purple)
    combined_embed.set_thumbnail(url=ctx.guild.icon.url)  # Set the server's icon as the thumbnail

    # Add fields for XP Leaderboard
    combined_embed.add_field(name="XP Leaderboard", value="Top 5 Users by XP", inline=False)
    for i, (xp_user_id, xp_user_data) in enumerate(top_xp_users, 1):
        xp_member = ctx.guild.get_member(int(xp_user_id))
        xp_username = xp_member.display_name if xp_member else "Unknown User"
        xp_rank = xp_user_data['rank']
        xp = xp_user_data['xp']
        combined_embed.add_field(name=f"{i}. {xp_username}", value=f"Rank: {xp_rank}\nXP: {xp}", inline=True)

    combined_embed.add_field(name="", value="---------------------------------------------------", inline=False)

    # Add fields for Economy Leaderboard
    combined_embed.add_field(name="Economy Leaderboard", value="Top 5 Users by Balance", inline=False)
    for i, (economy_user_id, economy_user_data) in enumerate(top_economy_users, 1):
        economy_user = bot.get_user(int(economy_user_id))
        economy_username = economy_user.name if economy_user else "Unknown User"
        economy_balance = economy_user_data['balance']
        combined_embed.add_field(name=f"{i}. {economy_username}", value=f"Balance: {economy_balance:,}", inline=True)

    # Send the combined embed
    await ctx.respond(embed=combined_embed)


@bot.command()
async def transfer(ctx, recipient: discord.Member, amount: int):
    # Retrieve the user's balance from the JSON file
    with open('YOURJSONFILENAME.json', 'r') as f:
        data = json.load(f)
    
    sender_id = str(ctx.author.id)
    recipient_id = str(recipient.id)
    
    # Check if the sender has enough coins to transfer
    if sender_id not in data or data[sender_id]['balance'] < amount:
        await ctx.respond("You don't have enough coins to make this transfer.")
        return
    
    # Perform the coin transfer
    data[sender_id]['balance'] -= amount
    data[recipient_id]['balance'] += amount
    
    # Save the updated data back to the JSON file
    with open('YOURJSONFILENAME.json', 'w') as f:
        json.dump(data, f)
    
    await ctx.respond(f"Successfully transferred **{amount}** coins to <@{recipient_id}>.")

@bot.command()
async def payday(ctx):
    with open('YOURJSONFILENAME.json', 'r') as f:
        data = json.load(f)
    user_id = str(ctx.author.id)
    current_time = int(datetime.datetime.now().timestamp())  # Use datetime.datetime.now() to get the current timestamp
    
    if user_id in data and current_time - data[user_id]['last_payday'] < 900:
        time_left = 900 - (current_time - data[user_id]['last_payday'])
        minutes, seconds = divmod(time_left, 60)
        embed = discord.Embed(
            title="Payday",
            description=f"You can claim your payday in {minutes} minutes and {seconds} seconds.",
            color=discord.Color.red()
        )
    else:
        if user_id not in data:
            data[user_id] = {
                'balance': 0,
                'last_payday': 0
            }
        data[user_id]['balance'] += 150
        data[user_id]['last_payday'] = current_time
        with open('YOURJSONFILENAME.json', 'w') as f:
            json.dump(data, f)
        
        # Get user's current balance
        user_balance = data[user_id]['balance']
        
        # Get user's position on the leaderboard
        leaderboard = sorted(data.keys(), key=lambda x: data[x]['balance'], reverse=True)
        user_position = leaderboard.index(user_id) + 1
        
        embed = discord.Embed(
            title="Payday",
            description="Here, take some coins. Enjoy! (+150 coins!)",
            color=discord.Color.green()
        )
        embed.add_field(name="Your current balance", value=str(user_balance), inline=False)
        embed.add_field(name="Your position on the global leaderboard", value=f"#{user_position}", inline=False)
        
    await ctx.respond(embed=embed)



@bot.command()
async def coinflip(ctx, bet: int):
    user_id = str(ctx.author.id)
    
    # Retrieve the user's balance from the JSON file
    with open('YOURJSONFILENAME.json', 'r') as f:
        data = json.load(f)
    
    if user_id not in data:
        await ctx.respond("You don't have any money yet.")
        return
    
    coins = data[user_id]['balance']
    
    # Check if the user has enough coins to place the bet
    if bet > coins:
        await ctx.respond("You don't have enough coins to place that bet.")
        return
    
    # Perform the coin flip
    result = random.choice(["Heads", "Tails"])
    
    # Calculate the payout or loss
    if result == "Heads":
        payout = bet
    else:
        payout = -bet
    
    # Update the balance
    coins += payout
    
    # Update the user's balance in the data dictionary
    data[user_id]['balance'] = coins
    
    # Write the updated data dictionary back to the JSON file
    with open('YOURJSONFILENAME.json', 'w') as f:
        json.dump(data, f)
    
    # Create an embed for the result message
    embed = discord.Embed(title="Coin Flip", color=0xFFD700)
    embed.add_field(name="Result", value=result, inline=False)
    
    if payout > 0:
        embed.add_field(name="Congratulations!", value=f"You won {payout} coins!", inline=False)
    else:
        embed.add_field(name="Better luck next time!", value=f"You lost {abs(payout)} coins.", inline=False)
    
    embed.set_footer(text="Your balance: {} coins".format(coins))
    
    # Send the embed as the result message
    await ctx.respond(embed=embed)


import random

@bot.command()
async def slots(ctx, bet: int):
    user_id = str(ctx.author.id)

    # Retrieve the user's balance from the JSON file
    with open('YOURJSONFILENAME.json', 'r') as f:
        data = json.load(f)

    if user_id not in data:
        await ctx.respond("You don't have any money yet.")
        return

    coins = data[user_id]['balance']

    # Check if the user has enough coins to place the bet
    if bet > coins:
        await ctx.respond("You don't have enough coins to place that bet.")
        return

    # Define the slot machine symbols and their corresponding payout values
    symbols = ['🍒', '🍀', '🍪', '🌻', '6⃣']
    payouts = {
        ('2⃣', '2⃣', '6⃣'): (50 * bet, 5),     # 5% chance of winning
        ('🍀', '🍀', '🍀'): (25 * bet, 10),    # 10% chance of winning
        ('🍒', '🍒', '🍒'): (20 * bet, 15),    # 15% chance of winning
        ('2⃣', '6⃣', '🍀'): (4 * bet, 25),    # 25% chance of winning
        ('🍒', '🍒', ''): (3 * bet, 45),      # 45% chance of winning
        ('🌻', '🌻', '🌻'): (100 * bet, 2),   # 2% chance of winning
        ('🍪', '🍪', '🍪'): (40 * bet, 8),    # 8% chance of winning
        ('6⃣', '6⃣', '6⃣'): (200 * bet, 99),  # 1% chance of winning
        ('🍀', '🌻', '🌻'): (10 * bet, 20),   # 20% chance of winning
    }


    # Spin the slots
    slots = [random.choice(symbols) for _ in range(3)]

    # Calculate the payout and determine if the user wins
    winning_combination = payouts.get(tuple(slots))
    if winning_combination is not None and random.randint(1, 100) <= winning_combination[1]:
        payout = winning_combination[0]
    else:
        payout = 0

    # Update the balance
    coins -= bet
    coins += payout

    # Update the user's balance in the data dictionary
    data[user_id]['balance'] = coins

    # Write the updated data dictionary back to the JSON file
    with open('YOURJSONFILENAME.json', 'w') as f:
        json.dump(data, f)

    # Format the slots result
    slots_result = ' '.join(slots)

    # Create the embed
    embed = discord.Embed(title="Slots Result", color=discord.Color.random())
    embed.add_field(name="Slots", value=slots_result, inline=False)
    embed.add_field(name="Your bid", value=str(bet), inline=False)
    embed.add_field(name="New Balance", value=str(coins), inline=False)

    # Send the result message as an embed
    if payout > 0:
        embed.description = f"Congratulations! You won {payout} coins!"
    else:
        embed.description = f"Better luck next time! You lost {bet} coins."

    await ctx.respond(embed=embed)



@bot.command()
async def rps(ctx, bet: int, choice: str):
    user_id = str(ctx.author.id)
    
    # Retrieve the user's balance from the JSON file
    with open('YOURJSONFILENAME.json', 'r') as f:
        data = json.load(f)
    
    if user_id not in data:
        await ctx.respond("You don't have any money yet.")
        return
    
    coins = data[user_id]['balance']
    
    # Check if the user has enough coins to place the bet
    if bet > coins:
        await ctx.respond("You don't have enough coins to place that bet.")
        return
    
    # Validate the user's choice
    choices = ['rock', 'paper', 'scissors']
    if choice not in choices:
        await ctx.respond("Invalid choice. Please choose either 'rock', 'paper', or 'scissors'.")
        return
    
    # Generate the bot's choice
    bot_choice = random.choice(choices)
    
    # Determine the winner
    if choice == bot_choice:
        result = "tie"
        payout = 0
    elif (choice == "rock" and bot_choice == "scissors") or \
         (choice == "paper" and bot_choice == "rock") or \
         (choice == "scissors" and bot_choice == "paper"):
        result = "win"
        payout = bet
    else:
        result = "loss"
        payout = -bet
    
    # Update the balance
    coins += payout
    
    # Update the user's balance in the data dictionary
    data[user_id]['balance'] = coins
    
    # Write the updated data dictionary back to the JSON file
    with open('YOURJSONFILENAME.json', 'w') as f:
        json.dump(data, f)
    
    # Create an embed to display the result
    embed = discord.Embed(title="Rock-Paper-Scissors Result", color=0x3498db)
    embed.add_field(name=f"{ctx.author.display_name}'s Choice", value=choice, inline=False)
    embed.add_field(name="Bot's Choice", value=bot_choice, inline=False)
    
    if result == "tie":
        embed.add_field(name="Result", value="It's a tie!", inline=False)
    elif result == "win":
        embed.add_field(name="Result", value=f"{ctx.author.display_name} wins {bet} coins!", inline=False)
    else:
        embed.add_field(name="Result", value=f"{ctx.author.display_name} loses {bet} coins!", inline=False)
    
    embed.set_footer(text=f"{ctx.author.display_name}'s Balance: {coins} coins")
    
    # Send the result embed
    await ctx.respond(embed=embed)

#----------------------------------MODERATION COMMANDS----------------------------------------------------------#


#Clear messages#
@bot.command(description="Clears Chat!") # Kicks people
@discord.ext.commands.has_any_role(Role_IDs, ID, ID) 
async def clear(ctx, amount: int) -> None:
    await ctx.channel.purge(limit=amount)
    confirmation_message = await ctx.respond('Messages have been cleared!')
    logs = bot.get_channel(LOG_Channel_ID)
    b = discord.Embed(title=f"Discord Log // Cleared Messages", description=f'Ran By: {ctx.author.mention}\nActual Command Finish: **{amount}** Messages have been cleared by {ctx.author.mention} in **{ctx.channel.name}**', color=0x660066)
    await logs.send(embed=b)
    await asyncio.sleep(5)
    await confirmation_message.delete()

#Kick Member Command# 
@bot.command(description="Kicks People!") # Kicks people
@discord.ext.commands.has_any_role(Role_IDs, ID, ID) 
async def kick(ctx, member : discord.Member, *, reason=None):
        logs=bot.get_channel(LOG_Channel_ID)
        b=discord.Embed(title=f"Discord Log // Kicked User",description=f'Ran By: {ctx.author.mention}\nActual Command Finish: {member.mention} has just kicked',color=0x660066)
        await member.kick(reason=reason)
        await logs.send(embed=b)
        this = await ctx.respond(f'{member.mention} has been kicked!')
        await asyncio.sleep(5)
        await this.delete()

@bot.command(description="Bans People!")
@discord.ext.commands.has_any_role(Role_IDs, ID, ID) 
async def ban(ctx, *, member, reason=None):
    guild = bot.get_guild(786225335360290826)

    try:
        member_id = int(member)
        user = await bot.fetch_user(member_id)
    except ValueError:
        await ctx.respond("**Invalid user ID format. Please use a valid user ID.**")
        return
    logs=bot.get_channel(LOG_Channel_ID)
    b=discord.Embed(title=f"Discord Log // Banned",description=f'Ran By: {ctx.author.mention}\nActual Command Finish: <@{member}> has just banned\nReason: **{reason}**',color=0x660066)
    await logs.send(embed=b)
    await guild.ban(user, reason=reason)
    await ctx.respond(f"**Banned {user.name}**\nReason: {reason}")

#Unban members#
@bot.command()
@discord.ext.commands.has_any_role(Role_IDs, ID, ID) 
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
        logs=bot.get_channel(LOG_Channel_ID)
        b=discord.Embed(title=f"Discord Log // Unbanned User",description=f'Ran By: {ctx.author.mention}\nActual Command Finish: <@{member}> has just been unbanned',color=0x660066)
        await logs.send(embed=b)
        await ctx.respond(f"**Unbanned {user.name}**")
    else:
        await ctx.respond("**The user isn't banned.**")

@bot.command()
async def timeout(ctx: discord.ApplicationContext, member: discord.Member, minutes: int):
        """Apply a timeout to a member."""

        duration = datetime.timedelta(minutes=minutes)
        await member.timeout_for(duration)
        await ctx.respond(f"Member timed out for {minutes} minutes.")


@bot.command()
async def moveall(ctx, channel: discord.VoiceChannel):
    voice_state = ctx.author.voice  # Get the voice state of the author of the command
    sc = voice_state.channel

    if voice_state and voice_state.channel:  # Check if the author is connected to a voice channel
        for member in voice_state.channel.members:
            await member.move_to(channel)
    else:
        await ctx.send("You're not connected to a voice channel.")




bot.run('yourid')

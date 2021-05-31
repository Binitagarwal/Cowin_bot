import asyncio
from os import getenv
import discord
from datetime import date
from datetime import timedelta
from discord import colour
from discord.embeds import Embed
from discord.ext import commands
from dotenv import load_dotenv
from discord.guild import Guild
import cowin
from datetime import date
from datetime import timedelta

load_dotenv()
TOKEN = getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='&')

@bot.command(name='create-channel')
@commands.has_role('admin')
async def create_channel(ctx, channel_name='cowin-update'):
    guild = ctx.guild
    print(type(guild))
    print("channel ",guild.text_channels)
    existing_channel = discord.utils.get(guild.text_channels, name=channel_name)
    if not existing_channel:
        print(f'Creating a new channel: {channel_name}')
        await guild.create_text_channel(channel_name)

#checks slots at particular pin every 10 seconds
@bot.command(name='slots',help="Checks vaccine slots every 10 second \n 1st argument is pin and \n 2nd argument (yes/no) shows/not show no vaccine msg")
async def hello(ctx,arg=721101,show='no'):
    guild = ctx.guild
    channel_name = 'cowin-update'
    existing_channel = discord.utils.get(guild.text_channels,name=channel_name)
    channel = discord.utils.get(guild.channels,name = channel_name)

    if not existing_channel:
        print(f'Creating a new channel: {channel_name}')
        await ctx.guild.create_text_channel(channel_name)

    while(True):
        date_today = date.today() 
        date_tommorrow = date.today() + timedelta(days = 1)
        date_today = date_today.strftime("%d-%m-%Y")
        date_tommorrow = date_tommorrow.strftime("%d-%m-%Y")
        
        result = cowin.slotsmdn(arg)
        if result == "No slots":
            embed = discord.Embed(
                title=f"Slots availability for vaccine in pincode:{arg}",
                type = "rich",
                colour=colour.Color(0xE5E242),
                description = "No slots"
            )
            if show.lower()!='no':
                await channel.send(embed=embed)
            else:
                print("working")
        else:
            today = result[date_today]
            ans = discord.Embed(
                    title=f"Slots availability for vaccine in Pincode:{arg}",
                    type = "rich",
                    colour=colour.Color(0xE5E242),
                )
            try:
                tommorrow = result[date_tommorrow]    
                for i in today:
                    ans.add_field(name="Slots for {a} on date:{c}".format(a=i,c=today),value="{b}".format(b=today[i]),inline=False)
                for i in tommorrow:
                    ans.add_field(name="Slots for {a} on date:{c}".format(a=i,c=tommorrow),value="{b}".format(b=tommorrow[i]),inline=False)
                await channel.send(embed=ans)

            except:
                for i in today:
                    ans.add_field(name="Slots for {a} on date:{c}".format(a=i,c=today),value="{b}".format(b=today[i]),inline=False) 
                await channel.send(embed=ans)
        try: 
            msg = await bot.wait_for('message',check=lambda m: m.author==ctx.author and (m.channel == ctx.channel or m.channel==channel),timeout=10.0)
        except asyncio.TimeoutError:
            continue
        else:
            if msg.content.lower() == 'stop':
                exit = Embed(
                    title = "The Program has stopped",
                    type  = "rich",
                    colour = colour.Color(0xE5E242),
                )
                await channel.send(embed=exit)
                return
        


bot.run(TOKEN) 


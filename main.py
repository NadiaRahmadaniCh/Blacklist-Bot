import discord
from discord.ext import commands
import random
import config
import DiscordUtils

# Untuk Memberi Bot Prefix
client = commands.Bot(command_prefix='BL', intents=discord.Intents.all())
client.remove_command("help")
music = DiscordUtils.Music()


@client.event
async def on_ready():
  print(f'Logged in as {client.user.name}')
  print('_____________________________')
  #ActivityType.Watching bsa diganti (Watching, Playing, listening)
  await client.change_presence(activity=discord.Activity(
      type=discord.ActivityType.watching, name="𝗕𝗹𝗮𝗰𝗸𝗹𝗶𝘀𝘁"))


# Command Help
@client.command()
async def help(ctx):
  await ctx.send("Help Command blm di Set..")


# Untuk Menghitung Latency Bot (Ping)
@client.command(aliases=['p'])
async def ping(ctx):
  await ctx.send(f'Pong! {round(client.latency * 1000)}ms')


# Untuk Menghapus Pesan (Purge)
@client.command(alliases=['delete', 'clear', 'hapus'])
@commands.has_permissions(administrator=True)
async def purge(ctx, amount=1):
  if (not ctx.author.guild_permissions.manage_messages):
    await ctx.send('Bot tidak memiliki Permission ``Manage Messages``')
  ammount = amount + 1
  if amount > 101:
    await ctx.send('Gabisa hapus lebih dari 100 Pesan!')
  else:
    await ctx.channel.purge(limit=ammount)
    await ctx.send(embed=discord.Embed(
        description=f'**{amount}** Pesan Dihapus', color=discord.Color.red()))


# Embed
@client.command()
async def embed(ctx):
  embed_message = discord.Embed(
      title='Blacklist Bot',
      description=
      'Blacklist Bot adalah Bot Discord Yang Dibuat Untuk Membantu Di Blacklist Server Discord Anda.',
      color=discord.Color.red())

  await ctx.send(embed=embed_message)


# Info Server
@client.command()
async def info(ctx):
  embed = discord.Embed(
      title="𝗕𝗹𝗮𝗰𝗸𝗹𝗶𝘀𝘁",
      description=
      "Welcome to 𝗕𝗹𝗮𝗰𝗸𝗹𝗶𝘀𝘁, \ni make this server to be enjoyable for everyone, \nwe hope everybody enjoy their time with us, and stay along with our journey!",
      color=discord.Color.darker_grey())
  embed.set_thumbnail(
      url=
      "https://media.discordapp.net/attachments/714414410961256469/1164233302429925486/Blacklist.jpeg"
  )
  await ctx.send(embed=embed)


# Say Commands
@client.command()
async def say(ctx, saymsg=None):
  if saymsg == None:
    return await ctx.send('Masukkan pesannya..', ephemeral=True)
  await ctx.send(saymsg)


# Music Bot Join
@client.command()
async def join(ctx):
  voicetrue = ctx.author.voice
  if voicetrue is None:
    return await ctx.send('Masuk ke Voice Channel dulu..')
  await ctx.author.voice.channel.connect()
  await ctx.send('Joined to Voice Channel', ephemeral=True)


# Music Bot Leave
@client.command(alliases=['dc'])
async def leave(ctx):
  mevoicetrue = ctx.guild.me.voice
  if mevoicetrue is None:
    return await ctx.send('Bot tidak berada di Voice Channel..')
  await ctx.voice_client.disconnect()
  await ctx.send('Left Voice Channel', ephemeral=True)


# Bot Music Play
@client.command()
async def play(ctx, *, url):
  player = music.get_player(guild_id=ctx.guild.id)
  if not player:
    player = music.create_player(ctx, ffmpeg_error_betterfix=True)
  if not ctx.voice_client.is_playing():
    await player.queue(url, search=True)
    song = await player.play()
    await ctx.send(f'Playing `{song.name}`')
  else:
    song = await player.queue(url, search=True)
    await ctx.send(f'Added `{song.name}` to queue')

client.run(config.TOKEN)

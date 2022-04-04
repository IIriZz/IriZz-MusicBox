# -*- coding: utf-8 -*-
# music.py

import discord
import youtube_dl
from discord.ext import commands


class Music(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def join(self, ctx):
        if ctx.author.voice is None:
            await ctx.send('Ты меня не слушаешь 👂')
        voice_channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            await voice_channel.connect()
        else:
            await ctx.voice_client.move_to(voice_channel)

    @commands.command()
    async def disconnect(self, ctx):
        await ctx.send('⚡ Съёбываю ⚡')
        await ctx.voice_client.disconnect()

    @commands.command()
    async def pause(self, ctx):
        if ctx.voice_client.is_playing():
            await ctx.voice_client.pause()
        else:
            await ctx.send(f'{ctx.message.author}, ты уши по утрам моешь? Музыка не играет вообще-то ⏸')

    @commands.command()
    async def resume(self, ctx):
        if ctx.voice_client.is_paused():
            await ctx.voice_client.resume()
        else:
            await ctx.send(f'{ctx.message.author}, ты совсем глухой? Музыка тут давно ебашит 🎶')

    @commands.command()
    async def play(self, ctx, url):
        ctx.voice_client.stop()

        FFMPEG_OPTIONS = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': '-vn'
        }

        YDL_OPTIONS = {
            'format': 'bestaudio/best'
        }

        vc = ctx.voice_client

        with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
            url2 = info['formats'][0]['url']
            source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
            vc.play(source)
        await ctx.send(f'Какой-то гондон, по имени {ctx.message.author}, запустил это')


    @commands.command(pass_context=True)
    @commands.has_permissions(administrator=True)
    async def help(self, ctx):
        emb = discord.Embed(
            title='Помощь для низших форм жизни',
            colour=discord.Colour.gold()
        )

        emb.add_field(name='$join', value='Вступить в голосовой чат 👂', inline=False)
        emb.add_field(name='$play {url}', value='Сыграть музыку {ссылка на музыку} 🎶', inline=False)
        emb.add_field(name='$pause', value='Поставить музыку на паузу ⏸', inline=False)
        emb.add_field(name='$resume', value='Продолжить играть музыку ▶', inline=False)
        emb.add_field(name='$disconnect', value='Выйти из голосового чата ⚡', inline=False)

        await ctx.send(embed=emb)


def setup(client):
    client.add_cog(Music(client))

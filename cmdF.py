import nextcord
from nextcord.ext import commands
from pytube import YouTube
from stream import stream
from os import remove


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def join(self, ctx):
        """
        Joins commands author's voice channel

        """
        if ctx.voice_client:
            return await ctx.voice_client.move_to(ctx.author.voice.channel)
        await ctx.author.voice.channel.connect()

    @commands.command()
    async def leave(self, ctx):
        """
        Leaves current voice channel

        """
        if ctx.voice_client:
            remove("sandro.mp3")
            return await ctx.voice_client.disconnect()

    @commands.command()
    # When invoked, join channel and play audio
    async def play(self, ctx, *, URL):
        """

        Plays audio from youtube search query
        
        param [URL]: URL or youtube search query

        """
        yt = YouTube(URL)
        # Check if audio is playing
        if ctx.voice_client:
            return await ctx.send("Já estou em um canal! Miau!")

        await ctx.guild.change_voice_state(
            channel=ctx.author.voice.channel, self_deaf=True
        )

        # If not, create voice client and join channel
        async with ctx.typing():
            await ctx.author.voice.channel.connect()

            audio_info = stream(URL)[0]

            audio_source = nextcord.PCMVolumeTransformer(
                nextcord.FFmpegPCMAudio(audio_info)
            )

            audio_source.volume = 1

            ctx.voice_client.play(audio_source)
            await ctx.send("Tocando: {}".format(stream(URL)[1]))

    @commands.command()
    async def stop(self, ctx):
        """
        Stops playing audio and leaves channel

        """
        if ctx.voice_client.is_playing():
            await ctx.send("Saindo. Miau!")
            remove("sandro.mp3")
            return await ctx.voice_client.disconnect()

        await ctx.send("Nada pra parar! Miau!")

    @commands.command()
    async def pause(self, ctx):
        """
        Pauses current audio, if any

        """
        if ctx.voice_client:
            return ctx.voice_client.pause()
        await ctx.send("Não tem nada tocando! Miau!")

    @commands.command()
    async def resume(self, ctx):
        """
        Resumes current audio, if any

        """
        if ctx.voice_client.is_paused():
            return ctx.voice_client.resume()
        await ctx.send("Não tem nada tocando! Miau!")

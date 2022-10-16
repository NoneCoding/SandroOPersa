import nextcord
from nextcord.ext import commands
from pytube import YouTube
from stream import stream
from os import remove
from collections import deque
from asyncio import sleep



class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Create empty list for storing queued up audios
    line = deque([])

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
            await ctx.voice_client.disconnect()
            remove("sandro.mp3")
            Music.line.clear()
            return

    @commands.command()
    # When invoked, join channel and play audio
    async def play(self, ctx, *, URL):
        """

        Plays audio from youtube search query
        
        param [URL]: URL or youtube search query

        """
        # Check if audio is playing
        if ctx.voice_client:
            Music.line.append(URL)
            return

        Music.line.append(URL)
        
        await ctx.guild.change_voice_state(
            channel=ctx.author.voice.channel, self_deaf=True
        )

        # If not, create voice client and join channel
        async with ctx.typing():
            await ctx.author.voice.channel.connect()
            
            # Play while queue is not empty
            while len(Music.line) > 0:
                audio_info = stream(Music.line[0])
                
                audio_source = nextcord.PCMVolumeTransformer(
                    nextcord.FFmpegPCMAudio(audio_info[0])
                )

                audio_source.volume = 1

                ctx.voice_client.play(audio_source)
                await ctx.send("Tocando: {}".format(audio_info[1]))
            
                await sleep(audio_info[2])
                Music.line.popleft()

    @commands.command()
    async def stop(self, ctx):
        """
        Stops playing audio and leaves channel

        """
        if ctx.voice_client:
            await ctx.send("Limpando a fila e saindo. Miau!")
            remove("sandro.mp3")
            Music.line.clear()
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
        
    @commands.command()
    async def queue(self, ctx, *, URL):
        """
        Adds audio to queue
        
        param [URL]: URL or youtube search query
        
        """
        Music.line.append(URL)
        return await ctx.send(f"Adicionando música à fila. Sua música está na posição {len(Music.line)}! Miau!")
    
    @commands.command()
    async def remove(self, ctx, pos):
        """
        Removes item from queue
        
        param [pos]: position of element to remove from queue
        
        """
        Music.line.remove(Music.line[int(pos)])
        return
    
    @commands.command()
    async def list_all(self, ctx):
        """
        Lists all items in the current queue
        
        """
        lista = "Fila: "
        
        for i in range(len(Music.line)):
            lista += f"\n\n{i}. {Music.line[i]}"
        
        return await ctx.send(f"``` {lista} ```")
    
    @commands.command()
    async def clear(self, ctx):
        """
        Clear the queue
        
        """
        
        Music.line.clear()
        return

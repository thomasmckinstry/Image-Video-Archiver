import discord
import requests
import urllib.request

from discord.ext import commands

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
imageArr = [".jpg", ".jpeg", ".png"]
#soundArr = [".wav", ".mp3", ".ogg"]
videoArr = [".webm", ".mp4"]

@bot.event
async def on_ready():
    print("bot is online")

@bot.command()
async def archiveDocs(ctx):
    print()
    image = 0
    video = 0
    sound = 0

    count = 0
    failedImage = 0
    failedVideo = 0

    async for message in ctx.channel.history(limit=None, before=None, after=None, around=None, oldest_first=True):

        count += 1
        #print(count)

        if len(message.attachments) > 0:
            for i in message.attachments:
                if 'image' == i.content_type:
                    filename = str(image) + message.channel.name + message.created_at.strftime('%d %b %y') + '.png'
                    image += 1
                    await i.save(f'Image/' + filename)
                    #print("saved Image" + str(image))

                if 'video' == i.content_type:
                    #print("hit video")
                    filename = str(video) + message.channel.name + message.created_at.strftime('%d %b %y') + '.mp4'
                    video += 1
                    await i.save(f'Video/'+filename)
                    #print("saved Video" + str(video))
                    
        if message.embeds: 
            #print("hit embeds")  
            for i in message.embeds:
                #print("hit embeds loop 1")
                extensionStr = ""
                for j in range(len(i.url)-4, 0, -1):
                    
                    if i.url[j : j+4] in imageArr or i.url[j : j+4] in videoArr:
                        extensionStr = i.url[j : j+4]

                    if j <= len(i.url)-5:
                        if i.url[j : j+6] in imageArr or i.url[j : j+6] in videoArr:
                            extensionStr = i.url[j : j+6]
                
                #print(i.url + " url")
                #print(extensionStr + " extension")

                url = i.url

                #print(url)

                if (extensionStr in imageArr):
                    filename = str(image) + message.channel.name + message.created_at.strftime('%d %b %y') + extensionStr

                    try:
                        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                        response = urllib.request.urlopen(req)

                        imageFile = response.read()

                        with open('Image/' + filename, 'wb') as f:
                            f.write(imageFile)
                            #print("saved embedded Image" + str(image))

                        image += 1

                    except:
                        print("Image " + filename + " failed to save")
                        failedImage += 1
                        continue

                if (extensionStr in videoArr):
                    #print("hit video if")
                    #print(url)

                    filename = str(video) + message.channel.name + message.created_at.strftime('%d %b %y') + extensionStr
                    try:
                        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                        response = urllib.request.urlopen(req)

                        videoFile = response.read()

                        with open('Video/' + filename, 'wb') as f:
                            f.write(videoFile)

                            video += 1

                    except:
                        print("Video " + filename + " failed to save")
                        failedVideo += 1
                        continue

                    #urllib.request.urlopen("https://www.youtube.com/")

    await message.channel.send("Saved " + str(video) + " videos")
    await message.channel.send("Saved " + str(image) + " images")
    await message.channel.send(str(count) + " Messages were scanned")           

def getFileType(str):
    extensionStr = ""
    for j in range(len(i.url)-4, 0, -1):
                    
        if i.url[j : j+4] in imageArr or i.url[j : j+4] in videoArr:
            extensionStr = i.url[j : j+4]
            return extensionStr

        if j <= len(i.url)-5:
            if i.url[j : j+6] in imageArr or i.url[j : j+6] in videoArr:
                extensionStr = i.url[j : j+6]
                return extensionStr

bot.run("MTA5NDY5ODQ0NzkwMDI1NDI0MA.GwDbx8.pdoJ4yDR9eFgk3oGcD2EuD91JSsdQQQus1V3S8")


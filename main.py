import os
from threading import Thread
from flask import Flask
import discord
from discord.ext import commands

# --- 1. 슬립 방지용 Flask 웹 서버 ---
app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run_flask)
    t.start()

# --- 2. 디스코드 봇 설정 ---
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} 봇이 로그인했습니다!')

@bot.event
async def on_member_join(member):
    # 채널 이름을 '입장로그'로 변경했습니다
    channel = discord.utils.get(member.guild.text_channels, name="입장로그")
    
    if channel:
        created_at_unix = int(member.created_at.timestamp())
        joined_at_unix = int(member.joined_at.timestamp()) if member.joined_at else 0

        embed = discord.Embed(
            title=f"{member.guild.member_count}번째 멤버가 입장했어요",
            color=0x5865F2
        )
        embed.add_field(name="유저", value=f"{member.mention} ({member.name})", inline=False)
        embed.add_field(name="서버 입장 시간", value=f"<t:{joined_at_unix}:F> (<t:{joined_at_unix}:R>)", inline=False)
        embed.add_field(name="계정 생성일", value=f"<t:{created_at_unix}:F> (<t:{created_at_unix}:R>)", inline=False)
        embed.set_thumbnail(url=member.display_avatar.url)

        await channel.send(embed=embed)

keep_alive()

# 따옴표 안에 본인의 디스코드 봇 토큰을 넣으세요
TOKEN = os.getenv('BOT_TOKEN')
bot.run(TOKEN)

import discord
from discord.ext import commands
import os

# 1. 멤버 이벤트를 수신하기 위한 인텐트(Intents) 설정
intents = discord.Intents.default()
intents.members = True  # 입장/퇴장 감지에 필수!

bot = commands.Bot(command_prefix="!", intents=intents)

# 2. 채널 ID 설정 (각 채널 우클릭 -> ID 복사 후 숫자로 변경)
JOIN_LOG_CHANNEL_ID = 123456789012345678   # '입장로그' 채널 ID
LEAVE_LOG_CHANNEL_ID = 987654321098765432  # '퇴장로그' 채널 ID

@bot.event
async def on_ready():
    print(f"성공적으로 로그인했습니다: {bot.user.name}")

# 서버 입장 로그
@bot.event
async def on_member_join(member):
    channel = bot.get_channel(1536591105133510717)
    if channel:
        embed = discord.Embed(
            title="📥 멤버 입장",
            description=f"{member.mention} ({member.name}) 님이 서버에 입장하셨습니다.",
            color=discord.Color.green()
        )
        if member.avatar:
            embed.set_thumbnail(url=member.avatar.url)
        await channel.send(embed=embed)

# 서버 퇴장 로그
@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(1536591136699842621)
    if channel:
        embed = discord.Embed(
            title="📤 멤버 퇴장",
            description=f"**{member.name}** 님이 서버에서 나가셨습니다.",
            color=discord.Color.red()
        )
        if member.avatar:
            embed.set_thumbnail(url=member.avatar.url)
        await channel.send(embed=embed)

# 환경 변수 TOKEN 불러오기
TOKEN = os.getenv('TOKEN')
bot.run(TOKEN)

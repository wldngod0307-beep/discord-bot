import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.members = True  # 멤버 이벤트 감지 필수

bot = commands.Bot(command_prefix="!", intents=intents)

# 1. 채널 ID 설정 (각 채널 우클릭 -> ID 복사 후 입력)
JOIN_LOG_CHANNEL_ID = 1536591105133510717   # 입장로그 채널 ID
LEAVE_LOG_CHANNEL_ID = 1536591136699842621  # 퇴장로그 채널 ID (실제 채널 ID 입력)

# 2. 입장 임베드 하단 배너 이미지 URL (원하는 이미지 주소 입력)
IMAGE_URL = "https://example.com/your-banner.jpg"

@bot.event
async def on_ready():
    # 봇 상태를 '방해금지(dnd)'로 설정
    await bot.change_presence(status=discord.Status.dnd)
    print(f"성공적으로 로그인했습니다: {bot.user.name}")

# 입장 로그
@bot.event
async def on_member_join(member):
    channel = bot.get_channel(JOIN_LOG_CHANNEL_ID)
    if not channel:
        return

    # 서버 총 멤버 수
    member_count = len(member.guild.members)
    
    # 시간 타임스탬프 (디스코드 자체 상대시간 포맷 적용)
    join_time = int(member.joined_at.timestamp()) if member.joined_at else int(discord.utils.utcnow().timestamp())
    created_time = int(member.created_at.timestamp())

    embed = discord.Embed(
        title=f"{member_count}번째 멤버가 입장했어요",
        color=0x3498db  # 파란색 테두리
    )
    embed.add_field(
        name="유저", 
        value=f"{member.mention} ({member.name})", 
        inline=False
    )
    embed.add_field(
        name="서버에 입장한 시간", 
        value=f"<t:{join_time}:f> (<t:{join_time}:R>)", 
        inline=False
    )
    embed.add_field(
        name="계정 생성일", 
        value=f"<t:{created_time}:f> (<t:{created_time}:R>)", 
        inline=False
    )

    # 유저 프로필 썸네일 (오른쪽 상단)
    avatar_url = member.display_avatar.url
    embed.set_thumbnail(url=avatar_url)

    # 하단 배너 이미지 설정 (IMAGE_URL이 제대로 등록된 경우)
    if IMAGE_URL and IMAGE_URL.startswith("http"):
        embed.set_image(url=IMAGE_URL)

    await channel.send(embed=embed)

# 퇴장 로그
@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(LEAVE_LOG_CHANNEL_ID)
    if not channel:
        return

    # 시간 타임스탬프
    leave_time = int(discord.utils.utcnow().timestamp())
    created_time = int(member.created_at.timestamp())

    embed = discord.Embed(
        title="멤버가 퇴장했어요",
        color=0xe74c3c  # 빨간색 테두리
    )
    embed.add_field(
        name="유저", 
        value=f"{member.mention} ({member.name})", 
        inline=False
    )
    embed.add_field(
        name="서버에서 퇴장한 시간", 
        value=f"<t:{leave_time}:f> (<t:{leave_time}:R>)", 
        inline=False
    )
    embed.add_field(
        name="계정 생성일", 
        value=f"<t:{created_time}:f> (<t:{created_time}:R>)", 
        inline=False
    )

    # 유저 프로필 썸네일 (오른쪽 상단)
    avatar_url = member.display_avatar.url
    embed.set_thumbnail(url=avatar_url)

    await channel.send(embed=embed)

TOKEN = os.getenv('TOKEN')
bot.run(TOKEN)

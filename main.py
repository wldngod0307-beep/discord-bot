import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.members = True  # 멤버 이벤트 감지 필수

bot = commands.Bot(command_prefix="!", intents=intents)

# -------------------------------------------------------------
# ⚙️ 서버별 로그 채널 ID 설정 딕셔너리
# -------------------------------------------------------------
SERVER_CONFIG = {
    # 1번째 서버 (지우갓ㅣ본서버 천상천하 유아독존)
    1521465987180793936: {
        "join": 1521480677957177434,   # 입장로그 채널 ID
        "leave": 1521507163074461798   # 퇴장로그 채널 ID
    },

    # --- 예비 서버 틀 (유미갓ㅣlog) ---
    # # 2번째 서버
    1536399242740895837: {
         "join": 1536591105133510717,
         "leave": 1536591136699842621
    # },
}

IMAGE_URL = ""

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.dnd)
    print(f"성공적으로 로그인했습니다: {bot.user.name} (ID: {bot.user.id})")

# -------------------------------------------------------------
# 🛠️ 공통 로그 전송 함수
# -------------------------------------------------------------
async def send_member_log(member, channel_id, is_join):
    if not channel_id:
        return

    # 1. 캐시에서 채널 가져오기
    channel = bot.get_channel(channel_id)

    # 2. 캐시에 없으면 API 직접 요청 (fetch_channel + 예외 처리)
    if channel is None:
        try:
            channel = await bot.fetch_channel(channel_id)
        except discord.NotFound:
            print(f"[경고] 채널을 찾을 수 없습니다: {channel_id}")
            return
        except discord.Forbidden:
            print(f"[경고] 채널에 접근할 권한이 없습니다: {channel_id}")
            return
        except discord.HTTPException as e:
            print(f"[에러] 채널 조회 실패: {e}")
            return

    # 3. 메시지 전송 가능한 채널 유형인지 검사
    if not isinstance(channel, discord.abc.Messageable):
        print(f"[경고] {channel_id} 채널은 메시지를 보낼 수 있는 채널 유형이 아닙니다.")
        return

    event_time = int(discord.utils.utcnow().timestamp())
    created_time = int(member.created_at.timestamp())

    # 입/퇴장 문구 및 설정
    if is_join:
        member_count = member.guild.member_count
        title = f"{member_count:,}번째 멤버가 입장했어요"
        description = None
        time_field_name = "서버에 입장한 시간"
        color = 0x3498DB  # 파란색
    else:
        title = "멤버가 퇴장했어요"
        description = None
        time_field_name = "서버에서 퇴장한 시간"
        color = 0xE74C3C  # 빨간색

    embed = discord.Embed(
        title=title,
        description=description,
        color=color
    )

    embed.add_field(
        name="유저",
        value=f"{member.mention} ({member.display_name})",
        inline=False
    )

    embed.add_field(
        name=time_field_name,
        value=f"<t:{event_time}:f> (<t:{event_time}:R>)",
        inline=False
    )

    embed.add_field(
        name="계정 생성일",
        value=f"<t:{created_time}:f> (<t:{created_time}:R>)",
        inline=False
    )

    embed.set_thumbnail(url=member.display_avatar.url)

    if is_join and IMAGE_URL and IMAGE_URL.startswith("http"):
        embed.set_image(url=IMAGE_URL)

    # 4. 권한 및 전송 예외 처리
    try:
        await channel.send(embed=embed)
    except discord.Forbidden:
        print(f"[경고] {channel_id} 채널에 메시지를 보낼 권한이 없습니다.")
    except discord.HTTPException as e:
        print(f"[에러] Discord API 전송 실패: {e}")

# -------------------------------------------------------------
# 📩 이벤트 핸들러 (가독성 개편 버전)
# -------------------------------------------------------------
@bot.event
async def on_member_join(member):
    config = SERVER_CONFIG.get(member.guild.id)
    if not config:
        return

    channel_id = config.get("join")
    if not channel_id:
        return

    await send_member_log(member, channel_id, is_join=True)

@bot.event
async def on_member_remove(member):
    config = SERVER_CONFIG.get(member.guild.id)
    if not config:
        return

    channel_id = config.get("leave")
    if not channel_id:
        return

    await send_member_log(member, channel_id, is_join=False)

# -------------------------------------------------------------
# 🔑 토큰 검사 및 실행
# -------------------------------------------------------------
TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise RuntimeError("TOKEN 환경변수가 설정되지 않았습니다. Discloud Variables를 확인하세요.")

bot.run(TOKEN)

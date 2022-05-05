import discord, asyncio, datetime, pytz
import openpyxl
from captcha.image import ImageCaptcha
import random

client = discord.Client()

@client.event
async def on_ready(): # 봇이 실행되면 한 번 실행됨
    print("LoginBot")
    print(f"BotName : {client.user.name}")
    print(f"BotId : {client.user.id}")
    print("Discord activity : S!도움")
    print("Code : Visual Studio Code")
    print("Prefix : S!")
    print("------------------Error Message------------------")
    await client.change_presence(status=discord.Status.online, activity=discord.Game("S!도움"))

@client.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.channels, name = '✋ㅣ환영')
    await channel.send(f"환영합니다, {member.mention}, 님.")

@client.event
async def on_message(message):
    if message.content == "S!테스트": # 메세지 감지
        await message.channel.send ("{} | {}, 안녕하세요".format(message.author, message.author.mention))
        await message.author.send ("{} | {}, 유저, 안녕하세요".format(message.author, message.author.mention))

    if message.content.startswith ("S!청소"):
        i = (message.author.guild_permissions.administrator)

        if i is True:
            amount = message.content[4:]
            channel = client.get_channel(971642583539417098)
            await message.channel.purge(limit=1)
            await message.channel.purge(limit=int(amount))

            embed = discord.Embed(title="메시지 삭제 알림", description="최근 디스코드 채팅 {}개가\n관리자 {}님의 요청으로 인해 정상 삭제 조치 되었습니다".format(amount, message.author), color=0x000000)
            embed.set_footer(text="Bot Made by. Kns#0221", icon_url="https://yt3.ggpht.com/a/AATXAJx_8hCiLplpKrKdqpcrNz1QLs0PeVeC0RlbCQ=s900-c-k-c0xffffffff-no-rj-mo")
            await channel.send(embed=embed)
        
        if i is False:
            await message.channel.purge(limit=1)
            await message.channel.send("{}, 당신은 명령어를 사용할 수 있는 권한이 없습니다".format(message.author.mention))
    
    if message.content.startswith ("S!인증 "):
        if message.author.guild_permissions.administrator:
            await message.delete()
            user = message.mentions[0]

            embed = discord.Embed(title="인증 시스템", description="인증이 정상적으로 완료 되었습니다 !",timestamp=datetime.datetime.now(pytz.timezone('UTC')), color=0xff0000)
            embed.add_field(name="인증 대상자", value=f"{user.name} ( {user.mention} )", inline=False)
            embed.add_field(name="담당 관리자", value=f"{message.author} ( {message.author.mention} )", inline=False)
            embed.set_footer(text="Bot Made by. Kns#0221")
            await message.author.send (embed=embed)
            role = discord.utils.get(message.guild.roles, name = '팬분들')
            await user.add_roles(role)

        else:
            await message.delete()
            await message.channel.send(embed=discord.Embed(title="권한 부족", description = message.author.mention + "님은 권한이 없습니다", color = 0xff0000))

    if message.content.startswith ("S!핑"):
        pings = round(client.latency*1000)
        if pings < 100:
            pinglevel = '🔵 매우좋음'
        elif pings < 300: 
            pinglevel = '🟢 양호함'
        elif pings < 400: 
            pinglevel = '🟡 보통'
        elif pings < 6000: 
            pinglevel = '🔴 나쁨'
        else: 
            pinglevel = '⚪ 매우나쁨'
        embed = discord.Embed(title='핑', description=f'{pings} ms\n{pinglevel}')
        await message.channel.send(embed=embed)

    if message.content.startswith ("S!켑챠"):
        Image_captcha = ImageCaptcha()
        a = ""
        for i in range(6):
            a += str(random.randint(0, 9))

        name = str(message.author.id) + ".png"
        Image_captcha.write(a, name)

        await message.channel.send(file=discord.File(name))
        def check(msg):
            return msg.author == message.author and msg.channel == message.channel

        try:
            msg = await client.wait_for("message", timeout=10, check=check)
        except:
            await message.channel.send("시간초과입니다.")
            return

        if msg.content == a:
            await message.channel.send("정답입니다.")
        else:
            await message.channel.send("오답입니다.")

    if message.content.startswith ("S!알림"):
        await message.channel.purge(limit=1)
        i = (message.author.guild_permissions.administrator)
        if i is True:
            notice = message.content[4:]
            channel = client.get_channel(971642583539417098)
            embed = discord.Embed(title="**뭐니봇 공지사항**", description="\n――――――――――――――――――――――――――――\n\n{}\n\n――――――――――――――――――――――――――――".format(notice),timestamp=datetime.datetime.now(pytz.timezone('UTC')), color=0x00ff00)
            embed.set_footer(text="Bot Made by. Kns#0221 | 담당 관리자 : {}".format(message.author), icon_url="https://yt3.ggpht.com/a/AATXAJx_8hCiLplpKrKdqpcrNz1QLs0PeVeC0RlbCQ=s900-c-k-c0xffffffff-no-rj-mo")
            embed.set_thumbnail(url="https://external-preview.redd.it/-k5TdA1W5YH-jzeVO21AdcfsXoOYjC8AFANwEYXfHfQ.jpg?auto=webp&s=bb9bbab24b9552c0fbb418fc49838e79d3e6d76a")
            await channel.send ("@everyone", embed=embed)
            await message.author.send("*[ BOT 자동 알림 ]* | 정상적으로 공지가 채널에 작성이 완료되었습니다 : )\n```ini\n[ 기본 작성 설정 채널 ] : {}\n[ 공지 발신자 ] : {}\n\n[ 내용 ]\n{}\n```".format(channel, message.author, notice))
 
        if i is False:
            await message.channel.send("{}, 당신은 관리자가 아닙니다".format(message.author.mention))

    if message.content.startswith ('S!정보'):
        date = datetime.datetime.utcfromtimestamp(((int(message.author.id) >> 22) + 1420070400000) / 1000)
        embed = discord.Embed(color=0x00ff00)
        embed.add_field(name="이름", value=message.author.name, inline=True)
        embed.add_field(name="서버닉네임", value=message.author.display_name, inline=True)
        embed.add_field(name="가입일", value=str(date.year) + "년" + str(date.month) + "월" + str(date.day) + "일", inline=True)
        embed.add_field(name="아이디", value=message.author.id, inline=True)
        embed.set_thumbnail(url=message.author.avatar_url)
        await message.channel.send(embed=embed)

    if message.content.startswith ("병신"):
        await message.channel.purge(limit=1)
        channel = client.get_channel(971642583539417098)
        embed = discord.Embed(title="뭐니봇 알림", description="",timestamp=datetime.datetime.now(pytz.timezone('UTC')), color=0xff0000)
        embed.add_field(name=f"**{message.author.name} (이)가 욕설사용을 하였습니다.**", value="> 삭제된 내용 `병신`\n", inline=False)
        embed.set_footer(text="Bot Made by. Kns#0221")
        await channel.send (embed=embed)

    if message.content.startswith ("닥쳐"):
        await message.channel.purge(limit=1)
        channel = client.get_channel(971642583539417098)
        embed = discord.Embed(title="뭐니봇 알림", description="",timestamp=datetime.datetime.now(pytz.timezone('UTC')), color=0xff0000)
        embed.add_field(name=f"**{message.author.name} (이)가 욕설사용을 하였습니다.**", value="> 삭제된 내용 `닥쳐`\n", inline=False)
        embed.set_footer(text="Bot Made by. Kns#0221")
        await channel.send (embed=embed)

    if message.content.startswith ("븅신"):
        await message.channel.purge(limit=1)
        channel = client.get_channel(971642583539417098)
        embed = discord.Embed(title="뭐니봇 알림", description="",timestamp=datetime.datetime.now(pytz.timezone('UTC')), color=0xff0000)
        embed.add_field(name=f"**{message.author.name} (이)가 욕설사용을 하였습니다.**", value="> 삭제된 내용 `븅신`\n", inline=False)
        embed.set_footer(text="Bot Made by. Kns#0221")
        await channel.send (embed=embed)
    
    if message.content.startswith ("시발"):
        await message.channel.purge(limit=1)
        channel = client.get_channel(971642583539417098)
        embed = discord.Embed(title="뭐니봇 알림", description="",timestamp=datetime.datetime.now(pytz.timezone('UTC')), color=0xff0000)
        embed.add_field(name=f"**{message.author.name} (이)가 욕설사용을 하였습니다.**", value="> 삭제된 내용 `시발`\n", inline=False)
        embed.set_footer(text="Bot Made by. Kns#0221")
        await channel.send (embed=embed)

    if message.content.startswith ("씨발"):
        await message.channel.purge(limit=1)
        channel = client.get_channel(971642583539417098)
        embed = discord.Embed(title="뭐니봇 알림", description="",timestamp=datetime.datetime.now(pytz.timezone('UTC')), color=0xff0000)
        embed.add_field(name=f"**{message.author.name} (이)가 욕설사용을 하였습니다.**", value="> 삭제된 내용 `씨발`\n", inline=False)
        embed.set_footer(text="Bot Made by. Kns#0221")
        await channel.send (embed=embed)

    if message.content.startswith ("S!골라"):
        choice = message.content.split(" ")
        choicenumber = random.randint(1, len(choice)-1)
        choiceresult = choice[choicenumber]
        await message.channel.send(choiceresult)

    if message.content.startswith ("S!OnlineBot"):
        await message.channel.purge(limit=1)
        channel = client.get_channel(971642583539417098)
        embed = discord.Embed(title="봇 온라인", description="",timestamp=datetime.datetime.now(pytz.timezone('UTC')), color=0x00ff00)
        embed.add_field(name="**뭐니 봇**", value="🟢OnlineBot", inline=False)
        embed.set_footer(text="Bot Made by. Kns#0221")
        await channel.send(embed=embed)

    if message.content.startswith ("S!OfflineBot"):
        await message.channel.purge(limit=1)
        channel = client.get_channel(971642583539417098)
        embed = discord.Embed(title="봇 오프라인", description="",timestamp=datetime.datetime.now(pytz.timezone('UTC')), color=0x00ff00)
        embed.add_field(name="**뭐니 봇**", value="🔴OfflineBot", inline=False)
        embed.set_footer(text="Bot Made by. Kns#0221")
        await channel.send(embed=embed)

    if message.content.startswith ("S!도움"):
        embed = discord.Embed(title="뭐냐봇 안내", description="",timestamp=datetime.datetime.now(pytz.timezone('UTC')), color=0xff0000)
        embed.add_field(name="**기본 뭐냐봇 명령어사용법**", value="> 뭐냐봇 접두사는 `S!`이다!\n", inline=False)
        embed.add_field(name="**관리자 명령어**", value="> `S!알림(이봇 개발자 외엔 사용은 자제해주세요)`\n> `S!인증 (사용자 이름)`\n> `S!청소 (원하는 개수)`\n", inline=False)
        embed.add_field(name="**일반 명령어**", value="> `S!봇개발`\n> `S!핑`\n> `S!정보`\n> `S!켑챠`\n> `S!골라 (예시: 짜장면 짬뽕)`", inline=False)
        embed.add_field(name="**봇 오류**", value="> 봇이 오류날시에는 Kns#0221 로 DM문의바랍니다\n 또는 #🛠ㅣ봇버그-문의 채널에 문의 바랍니다\n문의방법: ```신청자: (자기이름)\n신고사유: (봇 버그 사유)\nKns#0221```", inline=False)
        embed.set_footer(text="Bot Made by. Kns#0221")
        await message.author.send (embed=embed)
        await message.channel.send (embed=embed)

    if message.content.startswith ("S!봇개발"):
        await message.channel.send("봇 개발 코드\n```python\n#시작하기전에 pip install dicord는 꼭 해주세요\nimport discord, asyncio\n\nclient = discord.Client()\n\n@client.event\nasync def on_ready(): # 봇이 실행되면 한 번 실행됨\n    print('Start')\n    await client.change_presence(status=discord.Status.online, activity=discord.Game('봇의 상태매세지'))\n\n# 봇을 실행시키기 위한 토큰을 작성해주는 곳\nclient.run('BotToken')\n```")

    if message.author.bot:
        return None
    if message.content.endswith("함"):
        file = discord.File("pic\함.jpg")
        await message.channel.send(file=file)
        await message.channel.send("그런 함은 침몰했습니다")
    if message.content.endswith("엄"):
        file = discord.File("pic\엄준식.gif")
        await message.channel.send(file=file)
        await message.channel.send("엄준식라이더")
    if message.content.endswith("가"):
        file = discord.File("pic\가면라이더.jpg")
        await message.channel.send(file=file)
        await message.channel.send("가면라이더")
    if message.content.endswith("두"):
        file = discord.File("pic\두리안.jpg")
        await message.channel.send(file=file)
        await message.channel.send("두리안라이더")
    if message.content.endswith("딱"):
        file = discord.File("pic\딱지.jpg")
        await message.channel.send(file=file)
        await message.channel.send("딱지라이더")
    if message.content.endswith("바"):
        file = discord.File("pic\바이올린.jpg")
        await message.channel.send(file=file)
        await message.channel.send("바이올린라이더")
    if message.content.endswith("빨"):
        file = discord.File("pic\빨래.gif")
        await message.channel.send(file=file)
        await message.channel.send("빨래라이더")
    if message.content.endswith("자"):
        file = discord.File("pic\자전거.jpg")
        await message.channel.send(file=file)
        await message.channel.send("자전거라이더")
    if message.content.endswith("전"):
        file = discord.File("pic\전기톱.jpg")
        await message.channel.send(file=file)
        await message.channel.send("전기톱라이더")
    if message.content.endswith("좀"):
        file = discord.File("pic\좀비.jpg")
        await message.channel.send(file=file)
        await message.channel.send("좀비라이더")
    if message.content.endswith("중"):
        file = discord.File("pic\중력.jpg")
        await message.channel.send(file=file)
        await message.channel.send("중력라이더")
    if message.content.endswith("지"):
        file = discord.File("pic\지나가던.jpg")
        await message.channel.send(file=file)
        await message.channel.send("지나가던라이더")
    if message.content.endswith("카"):
        file = discord.File("pic\카베동.jpg")
        await message.channel.send(file=file)
        await message.channel.send("카베동라이더")
    if message.content.endswith("트"):
        file = discord.File("pic\트럼펫.jpg")
        await message.channel.send(file=file)
        await message.channel.send("트럼펫라이더")
    if message.content.endswith("하"):
        file = discord.File("pic\하이킥.jpg")
        await message.channel.send(file=file)
        await message.channel.send("하이킥라이더")
    if message.content.endswith("히"):
        file = discord.File("pic\히틀러라이더.jpg")
        await message.channel.send(file=file)
        await message.channel.send("히틀러라이더")
    if message.content.endswith("신"):
        file = discord.File("pic\신호등.jpg")
        await message.channel.send(file=file)
        await message.channel.send("신호등라이더")
    if message.content.endswith("고"):
        file = discord.File("pic\고자.jpg")
        await message.channel.send(file=file)
        await message.channel.send("고자라이더")
    if message.content.endswith("야"):
        file = discord.File("pic\야구.gif")
        await message.channel.send(file=file)
        await message.channel.send("야구라이더")
    if message.content.endswith("라"):
        file = discord.File("pic\라디오.jpg")
        await message.channel.send(file=file)
        await message.channel.send("라디오라이더")
    if message.content.endswith("도"):
        file = discord.File("pic\도둑.jpg")
        await message.channel.send(file=file)
        await message.channel.send("도둑라이더")
    if message.content.endswith("요"):
        file = discord.File("pic\요리사.gif")
        await message.channel.send(file=file)
        await message.channel.send("요리사라이더")
    if message.content.endswith("냐"):
        file = discord.File("pic\야옹이.jpg")
        await message.channel.send(file=file)
        await message.channel.send("야옹이라이더")
    if message.content.endswith("니"):
        file = discord.File("pic\니그로.jpg")
        await message.channel.send(file=file)
        await message.channel.send("니그로라이더")
    if message.content.endswith("낌"):
        file = discord.File("pic\낌새.jpg")
        await message.channel.send(file=file)
        await message.channel.send("낌새를 느끼고 놀란 라이더")
    if message.content.endswith("마"):
        file = discord.File("pic\마법.jpg")
        await message.channel.send(file=file)
        await message.channel.send("마법전사유캔도")
    if message.content.endswith("발"):
        file = discord.File("pic\발차기.jpg")
        await message.channel.send(file=file)
        await message.channel.send("발차기라이더")
    if message.content.endswith("아"):
        file = discord.File("pic\아이.jpg")
        await message.channel.send(file=file)
        await message.channel.send("아이라이더")
    if message.content.endswith("과"):
        file = discord.File("pic\과거.jpg")
        await message.channel.send(file=file)
        await message.channel.send("과거의 의사는 거짓으론 속일 수 없어 라이더")
    if message.content.endswith("음"):
        file = discord.File("pic\음악.jpg")
        await message.channel.send(file=file)
        await message.channel.send("음악라이더")
    if message.content.endswith("틀"):
        file = discord.File("pic\틀딱.jpg")
        await message.channel.send(file=file)
        await message.channel.send("틀딱라이더")
    if message.content.endswith("암"):
        file = discord.File("pic\암살자.jpg")
        await message.channel.send(file=file)
        await message.channel.send("암살자라이더")
    if message.content.endswith("손"):
        file = discord.File("pic\손목시계.JPG")
        await message.channel.send(file=file)
        await message.channel.send("손목시계라이더")
    if message.content.endswith("슈"):
        file = discord.File("pic\슈.jpg")
        await message.channel.send(file=file)
        await message.channel.send("슈퍼 히어로 대전 라이더")
    if message.content.endswith("기"):
        file = discord.File("pic\기차.jpg")
        await message.channel.send(file=file)
        await message.channel.send("기차 라이더")
    if message.content.endswith("다"):
        file = discord.File("pic\다이아몬드.jpg")
        await message.channel.send(file=file)
        await message.channel.send("다이아몬드 라이더")
    if message.content.endswith("게"):
        file = discord.File("pic\게.jpg")
        await message.channel.send(file=file)
        await message.channel.send("그런 게는 죽어야 합니다")
    if message.content.endswith("굴"):
        file = discord.File("pic\굴.jpg")
        await message.channel.send(file=file)
        await message.channel.send("엄마가 섬그늘에 굴 따러 가면라이더")
    if message.content.endswith("해"):
        file = discord.File("pic\물놀이.jpg")
        await message.channel.send(file=file)
        await message.channel.send("해변가 물놀이 라이더")
    if message.content.endswith("유"):
        file = discord.File("pic\유.jpg")
        await message.channel.send(file=file)
        await message.channel.send("유ㄱ덕 라이더")
    if message.content.endswith("만"):
        file = discord.File("pic\만두.jpg")
        await message.channel.send(file=file)
        await message.channel.send("만두 라이더")
    if message.content.endswith("짜"):
        file = discord.File("pic\짜장면.jpg")
        await message.channel.send(file=file)
        await message.channel.send("짜장면 배달부 라이더")
    if message.content.endswith("무"):
        file = discord.File("pic\무면허.jpg")
        await message.channel.send(file=file)
        await message.channel.send("무면허 라이더")
    if message.content.endswith("노"):
        file = discord.File("pic\노스트라.jpg")
        await message.channel.send(file=file)
        await message.channel.send("노스트라다무스")
    if message.content.endswith("나"):
        file = discord.File("pic\나는.jpg")
        await message.channel.send(file=file)
        await message.channel.send("나는 우주의 존재 라이더")
    if message.content.endswith("왜"):
        file = discord.File("pic\왜.jpg")
        await message.channel.send(file=file)
        await message.channel.send("왜 보고만 있는거냐고 물어보는 라이더")
    if message.content.endswith("온"):
        file = discord.File("pic\온두.jpg")
        await message.channel.send(file=file)
        await message.channel.send("온두루루 킷딴디스카")
    if message.content.endswith("인"):
        file = discord.File("pic\인형극.gif")
        await message.channel.send(file=file)
        await message.channel.send("인형극 라이더")
    if message.content.endswith("관"):
        file = discord.File("pic\관짝.gif")
        await message.channel.send(file=file)
        await message.channel.send("관짝 라이더")
    if message.content.endswith("작"):
        file = discord.File("pic\작살.gif")
        await message.channel.send(file=file)
        await message.channel.send("작살에 맞은 라이더")
    if message.content.endswith("더"):
        file = discord.File("pic\더이라면가.jpg")
        await message.channel.send(file=file)
        await message.channel.send("더이라면가")
    if message.content.endswith("제"):
        file = discord.File("pic\제로투.JPG")
        await message.channel.send(file=file)
        await message.channel.send("제로투 라이더")
    if message.content.endswith("행"):
        file = discord.File("pic\행글라이더.jpg")
        await message.channel.send(file=file)
        await message.channel.send("행글라이더")
    if message.content.endswith("미"):
        file = discord.File("pic\미안.jpg")
        await message.channel.send(file=file)
        await message.channel.send("미안해하는 라이더")
    if message.content.endswith("할"):
        file = discord.File("pic\그렇지.png")
        await message.channel.send(file=file)
        await message.channel.send("할 때마다 새로운 기분이고...")
    if message.content.endswith("?"):
        file = discord.File("pic\물음표.jpg")
        await message.channel.send(file=file)
        await message.channel.send("? 라이더")
    if message.content.endswith("시"):
        file = discord.File("pic\시간조종.gif")
        await message.channel.send(file=file)
        await message.channel.send("시간 조종 라이더")
    if message.content.endswith("그"):
        file = discord.File("pic\그래프라이더.gif")
        await message.channel.send(file=file)
        await message.channel.send("그래프라이더")
    if message.content.endswith("친"):
        file = discord.File("pic\친한.jpg")
        await message.channel.send(file=file)
        await message.channel.send("친한듯이 말걸지 말라")
    if message.content.endswith("오"):
        file = discord.File("pic\오렌지.jpeg")
        await message.channel.send(file=file)
        await message.channel.send("오렌지암즈 라이더")
    if message.content.endswith("수"):
        file = discord.File("pic\수확라이더.png")
        await message.channel.send(file=file)
        await message.channel.send("수확라이더")
    if message.content.endswith("장"):
        file = discord.File("pic\장애인.gif")
        await message.channel.send(file=file)
        await message.channel.send("장애인라이더")
# 봇을 실행시키기 위한 토큰을 작성해주는 곳
client.run('OTcxNjM5Nzk4MTk4NTY2OTMz.Gl0LR_.kWYTrpINlqSIQsIvagwvndEBtQJKXD_67LXcSo')
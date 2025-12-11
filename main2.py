import os
import requests
import discord
from discord.ext import tasks, commands

# ====== 環境変数 ======
TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

# ====== チェックするURL ======
CHECK_URL = "https://l-tike.com/order/?gLcode=30850&gPfKey=20251201000002092282&gEntryMthd=01&gScheduleNo=1&gCarrierCd=08&gPfName=%E3%82%B8%E3%82%A7%E3%83%95%E3%83%A6%E3%83%8A%E3%82%A4%E3%83%86%E3%83%83%E3%83%89%E5%B8%82%E5%8E%9F%E3%83%BB%E5%8D%83%E8%91%89%EF%BC%88%EF%BC%AA%EF%BC%92%E3%83%AA%E3%83%BC%E3%82%B0%E3%83%97%E3%83%AC%E3%83%BC%E3%82%AA%E3%83%95%EF%BC%89&gBaseVenueCd=35799"

# ====== Discord Bot 設定 ======
intents = discord.Intents.default()
intents.message_content = True  # ← これがないと !ping が動かない

bot = commands.Bot(command_prefix="!", intents=intents)

# ====== チケットチェック関数 ======
def check_ticket():
    try:
        res = requests.get(CHECK_URL, timeout=5)
        text = res.text

        # 再販を判断するキーワード
        keywords = ["受付中", "〇", "残り", "購入"]
        return any(k in text for k in keywords)

    except Exception as e:
        print("エラー:", e)
        return False

# ====== Bot 起動時 ======
@bot.event
async def on_ready():
    print("Bot 起動しました！")
    ticket_checker.start()

# ====== 定期チェック（1分ごと） ======
@tasks.loop(minutes=1)
async def ticket_checker():
    print("チェック中…")

    if check_ticket():
        channel = bot.get_channel(CHANNEL_ID)
        if channel:
            await channel.send("🎫 **ジェフ自由席が再販されたぞ！急げ！**")
            await channel.send(CHECK_URL)

# ====== 動作確認コマンド ======
@bot.command()
async def ping(ctx):
    await ctx.send("pong!")

# ====== Bot 実行 ======
bot.run(TOKEN)

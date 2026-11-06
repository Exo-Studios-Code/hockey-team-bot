import discord
from discord.ext import commands, tasks
import datetime
import json
import os
import random

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

# ====== CESTY K SOUBORŮM ======
SAVE_DIR = "data"
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

TEAM_FILE = os.path.join(SAVE_DIR, "team.json")
MATCH_FILE = os.path.join(SAVE_DIR, "matches.json")
ATTEND_FILE = os.path.join(SAVE_DIR, "attendance.json")
RESULTS_FILE = os.path.join(SAVE_DIR, "results.json")
TIPS_FILE = os.path.join(SAVE_DIR, "tips.json")

# ====== LOAD & SAVE ======
def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def load_json(path):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

TEAM_MEMBERS = load_json(TEAM_FILE) or {
    "Ex0Gen": "RD/RW/G",
    "NugentHopkins": "LW",
    "_D": "C",
    "98 Nečas": "RD",
    "17 Hronek": "LD",
    "makovec": "RW/LW",
    "fridl": "RD/RW/C",
    "Xaven": "G",
    "gameshoot": "G"
}
MATCH_SCHEDULE = load_json(MATCH_FILE) or []
ATTENDANCE = load_json(ATTEND_FILE) or {}
MATCH_RESULTS = load_json(RESULTS_FILE) or []
TIPS = load_json(TIPS_FILE) or {}

# ====== BOT START ======
@bot.event
async def on_ready():
    print(f"CoachBot je online jako {bot.user}")

# ====== PŘÍKAZY ======
@bot.command()
async def myrole(ctx):
    user = ctx.author.display_name
    position = TEAM_MEMBERS.get(user)
    if position:
        await ctx.send(f"{user}, tvoje pozice v týmu je: **{position}**")
    else:
        await ctx.send(f"{user}, nejsi zatím v databázi týmových pozic.")

@bot.command()
async def training(ctx):
    now = datetime.datetime.now().strftime("%A")
    if now in ["Monday", "Thursday"]:
        await ctx.send("🗡️ Dnes je trénink: **19:00 - 20:00** (pokud není zápas)")
    else:
        await ctx.send("❌ Dnes trénink není. Trénujeme každé pondělí a čtvrtek 19:00 - 20:00")

@bot.command()
async def sestava(ctx):
    msg = (
        "**🔴 První formace – ELITE:**\n"
        "LW: NugentHopkins\nC: _D\nRD: 98 Nečas\nLD: 17 Hronek\nG: Xaven\n\n"
        "**🔵 Druhá formace – ROTACE:**\n"
        "LW/RW: makovec\nC: _D (rotuje)\nRD: Ex0Gen\nLD: fridl\nG: Xaven"
    )
    await ctx.send(msg)

@bot.command()
async def pingteam(ctx):
    mentions = " ".join([f"<@{member.id}>" for member in ctx.guild.members if not member.bot])
    await ctx.send(f"🚀 **Ping týmu!**\n{mentions}")

@bot.command()
async def pridatzapas(ctx, typ: str, datum: str, cas: str):
    MATCH_SCHEDULE.append({"typ": typ, "datum": datum, "cas": cas})
    save_json(MATCH_FILE, MATCH_SCHEDULE)
    await ctx.send(f"✅ Zápas typu `{typ}` byl přidán na **{datum} v {cas}**.")

@bot.command()
async def zapasy(ctx):
    if not MATCH_SCHEDULE:
        await ctx.send("ℹ️ Zatím nejsou naplánované žádné zápasy.")
    else:
        msg = "**📅 Naplánované zápasy:**\n"
        for z in MATCH_SCHEDULE:
            msg += f"- {z['typ'].capitalize()} zápas: {z['datum']} v {z['cas']}\n"
        await ctx.send(msg)

@bot.command()
async def prijdu(ctx):
    user = ctx.author.display_name
    ATTENDANCE[user] = "✅ Přijdu"
    save_json(ATTEND_FILE, ATTENDANCE)
    await ctx.send(f"{user} označen jako **PŘIJDU** na trénink/zápas.")

@bot.command()
async def neprijdu(ctx):
    user = ctx.author.display_name
    ATTENDANCE[user] = "❌ Nepřijdu"
    save_json(ATTEND_FILE, ATTENDANCE)
    await ctx.send(f"{user} označen jako **NEPŘIJDU** na trénink/zápas.")

@bot.command()
async def dochazka(ctx):
    if not ATTENDANCE:
        await ctx.send("⚠️ Zatím nikdo nevyplnil docházku.")
    else:
        msg = "**📝 Docházka:**\n"
        for user, status in ATTENDANCE.items():
            msg += f"{user}: {status}\n"
        await ctx.send(msg)

@bot.command()
async def mojestats(ctx):
    user = ctx.author.display_name
    prijdu = sum(1 for u, v in ATTENDANCE.items() if u == user and v == "✅ Přijdu")
    neprijdu = sum(1 for u, v in ATTENDANCE.items() if u == user and v == "❌ Nepřijdu")
    await ctx.send(f"📊 {user}, tvoje docházka: \n✅ Přijdu: {prijdu}x\n❌ Nepřijdu: {neprijdu}x")

@bot.command()
async def zapiszapas(ctx, datum: str, vysledek: str):
    MATCH_RESULTS.append({"datum": datum, "vysledek": vysledek})
    save_json(RESULTS_FILE, MATCH_RESULTS)
    await ctx.send(f"📁 Zápas z {datum} byl zaznamenán s výsledkem {vysledek}.")

@bot.command()
async def vysledky(ctx):
    if not MATCH_RESULTS:
        await ctx.send("📭 Žádné zaznamenané výsledky.")
    else:
        msg = "**📊 Výsledky zápasů:**\n"
        for z in MATCH_RESULTS:
            msg += f"- {z['datum']}: {z['vysledek']}\n"
        await ctx.send(msg)

@bot.command()
async def tip(ctx, vysledek: str):
    user = ctx.author.display_name
    TIPS[user] = vysledek
    save_json(TIPS_FILE, TIPS)
    await ctx.send(f"🔮 {user} tipoval výsledek: **{vysledek}**")

@bot.command()
async def vsechnytipy(ctx):
    if not TIPS:
        await ctx.send("📝 Zatím nikdo netipoval.")
    else:
        msg = "**🎯 Tipy hráčů:**\n"
        for u, t in TIPS.items():
            msg += f"{u}: {t}\n"
        await ctx.send(msg)

@bot.command()
async def tiprank(ctx):
    msg = "**🏆 Žebříček tipérů (náhodné skóre):**\n"
    for user in TIPS:
        score = random.randint(0, 10)
        msg += f"{user}: {score} bodů\n"
    await ctx.send(msg)

@bot.command()
async def faceoff(ctx):
    members = [m.display_name for m in ctx.guild.members if not m.bot]
    winner = random.choice(members)
    await ctx.send(f"🏒 Face-off vyhrává: **{winner}**!")

@bot.command()
async def hokejquiz(ctx):
    questions = [
        "Kdo drží rekord v počtu gólů v NHL?",
        "Kolik hráčů je na ledě v týmu při plném počtu?",
        "Jak dlouhá je trestná lavice za hákování?"
    ]
    await ctx.send(f"❓ Hokejový kvíz: {random.choice(questions)}")

@bot.command()
async def motivace(ctx):
    quotes = [
        "Síla týmu je každý jednotlivec. Síla jednotlivce je tým.",
        "Tvrdá práce porazí talent, když talent nepracuje tvrdě.",
        "Každý pád tě posílí. Zvedni se a hraj dál."
    ]
    await ctx.send(f"💬 {random.choice(quotes)}")

@bot.command()
async def taktika(ctx, typ: str):
    taktiky = {
        "break": "🎯 *Breakout taktika:* Rychlé přihrávky od obránce na křídlo, následně průnik středem.",
        "presilovka": "🔥 *Přesilovka:* Hra 1-3-1, puk nechat rotovat do střely z mezikruží.",
        "obrana": "🛡️ *Defenziva:* Zónová obrana s tlakem na mantinel, žádné průniky středem."
    }
    await ctx.send(taktiky.get(typ, "❌ Neznámý typ taktiky. Použij break, presilovka nebo obrana."))

bot.run(os.getenv("DISCORD_TOKEN"))

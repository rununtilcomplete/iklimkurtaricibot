import discord
from discord.ext import commands
import tensorflow as tf
import numpy as np
from PIL import Image
import io
import os
import random



intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


@bot.command()
async def merhaba(ctx):
    await ctx.send(f"Merhabalar! ben {bot.user}, benim buradaki görevim birçok şekil yollarla iklim değişikliğine dikkat çekmek ve çözüm sunmak. Bana !yardim yazarak komutlarımı görebilirsin.")

@bot.command()
async def yardim(ctx):
    await ctx.send("!merhaba : botun görevinin özellikleri")
    await ctx.send("!atikoyun : kısa bir atık eşleştirme oyunu")
    await ctx.send("!iklimoyun : iklim değişikliği hakkında doğru-yanlış oyunu")
    await ctx.send("!karbonemisyon : karbon ayak izinizi hesaplayan bir anket")
    await ctx.send("!oneri : iklim değişikliği hakkında bilgi edinmek için kaynak önerir")


atik_turleri = [
    "Plastik",
    "Elektronik",
    "Cam",
    "Kağıt",
    "Metal",
    "Organik"
]

atik_list = {
    "Plastik": ["pet şişe", "poşet", "plastik paketleme", "plastik yemek kutusu"],
    "Elektronik": ["ekran", "radyo", "ısıtma sistemi", "soğutma sistemi"],
    "Cam": ["gazoz şişesi", "alkol şişesi", "hap şişesi", "kavanoz"],
    "Kağıt": ["gazete", "kağıt", "karton kutu", "kağıt poşet"],
    "Metal": ["teneke", "konserve", "hurda", "alüminyum folyo"],
    "Organik": ["meyve", "sebze", "dökülmüş ağaç yaprağı", "yumurta kabuğu"]
}
@bot.command()
async def atikoyun(ctx):
    tur = random.choice(list(atik_list.keys()))
    atik = random.choice(atik_list[tur])

    await ctx.send(
        f"**Atık Oyunu!**\n\n"
        f"Bu atık hangi türe girer?\n\n"
        f"**{atik}**\n\n"
        f"Seçenekler: Plastik, Elektronik, Cam, Kağıt, Metal, Organik"
    )

    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel

    try:
        cevap = await bot.wait_for("message", timeout=15.0, check=check)
        if cevap.content.lower() == tur.lower():
            await ctx.send("**Doğru! Tebrikler! Unutma, her küçük adım iklim değişikliğiyle mücadelede büyük bir fark yaratır!**")
        else:
            await ctx.send(f"**Yanlış!** Doğru cevap: **{tur}**")
    except:
        await ctx.send("**Süre doldu!**")

@bot.command()
async def iklimoyun(ctx):
    iklim_sorular = [
    ("Küresel ısınmanın ana nedeni insan faaliyetleridir.", "doğru"),
    ("Plastik atıklar doğada birkaç ayda yok olur.", "yanlış"),
    ("Ağaçlar karbon dioksiti emer.", "doğru"),
    ("Yenilenebilir enerji kaynakları çevreye zarar vermez.", "doğru"),
    ("İklim değişikliği sadece sıcaklık artışıyla ilgilidir.", "yanlış"),
    ("Fosil yakıtlar sera gazı salınımını artırır.", "doğru"),
    ("Geri dönüşüm iklim değişikliğini azaltmaya yardımcı olur.", "doğru"),
    ("Cam atıklar geri dönüştürülemez.", "yanlış")
]
    soru, cevap = random.choice(iklim_sorular)

    await ctx.send(
        f"**İklim Oyunu – Doğru mu Yanlış mı?**\n\n"
        f"{soru}\n\n"
        f"Cevapla: **doğru** / **yanlış**"
    )

    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel

    try:
        mesaj = await bot.wait_for("message", timeout=15.0, check=check)

        if mesaj.content.lower() == cevap:
            await ctx.send("**Doğru cevap! Tebrikler!** 🎉")
        else:
            await ctx.send(f"**Yanlış!** Doğru cevap: **{cevap.upper()}**")
    except:
        await ctx.send("**Süre doldu!**")

sorular = [
    "Haftada kaç gün et tüketiyorsun? (0-7)",
    "Günlük ulaşım türün nedir? (yürüyüş / toplu taşıma / araba)",
    "Günde kaç saat elektronik cihaz kullanıyorsun? (sayı)",
    "Evinin ana enerji kaynağı nedir? (fosil / elektrik / yenilenebilir)",
]

kullanici_durumlari = {}

@bot.event
async def on_ready():
    print(f"{bot.user} aktif.")

@bot.command()
async def karbonemisyon(ctx):
    kullanici_durumlari[ctx.author.id] = {
        "adim": 0,
        "puan": 0
    }
    await ctx.send("Karbon ayak izi hesaplamasına başlıyoruz.")
    await ctx.send(sorular[0])

@bot.event
async def on_message(mesaj):
    if mesaj.author.bot:
        return

    kullanici_id = mesaj.author.id
    if kullanici_id in kullanici_durumlari:
        durum = kullanici_durumlari[kullanici_id]
        adim = durum["adim"]

        try:
            if adim == 0:
                et_gunu = int(mesaj.content)
                durum["puan"] += et_gunu * 2

            elif adim == 1:
                secim = mesaj.content.lower()
                if secim == "yürüyüş":
                    durum["puan"] += 0
                elif secim == "toplu taşıma":
                    durum["puan"] += 3
                elif secim == "araba":
                    durum["puan"] += 6
                else:
                    await mesaj.channel.send("Geçerli bir seçenek yaz.")
                    return

            elif adim == 2:
                saat = int(mesaj.content)
                durum["puan"] += saat * 1

            elif adim == 3:
                enerji = mesaj.content.lower()
                if enerji == "fosil":
                    durum["puan"] += 6
                elif enerji == "elektrik":
                    durum["puan"] += 3
                elif enerji == "yenilenebilir":
                    durum["puan"] += 0
                else:
                    await mesaj.channel.send("Geçerli bir seçenek yaz.")
                    return

            durum["adim"] += 1

            if durum["adim"] < len(sorular):
                await mesaj.channel.send(sorular[durum["adim"]])
            else:
                puan = durum["puan"]

                if puan < 10:
                    seviye = "Düşük karbon ayak izi"
                elif puan < 20:
                    seviye = "Orta karbon ayak izi"
                else:
                    seviye = "Yüksek karbon ayak izi"

                await mesaj.channel.send(
                    f"Hesaplama tamamlandı.\n"
                    f"Karbon puanın: {puan}\n"
                    f"Durum: {seviye}"
                )

                del kullanici_durumlari[kullanici_id]

        except ValueError:
            await mesaj.channel.send("Lütfen geçerli bir sayı veya seçenek gir.")

    await bot.process_commands(mesaj)

yardim= ["https://www.ipcc.ch/",
          "https://science.nasa.gov/climate-change/",
          "https://www.climate.gov/news-features/understanding-climate/",
          "https://www.wwf.org.uk/learn/",
          "https://www.un.org/en/climatechange"]

onerri = ["Haftada 1 gün daha az et tüketmek yıllık emisyonunu düşürebilir.",
            "Toplu taşıma kullanmak bireysel karbon ayak izini azaltır.",
            "Elektronik cihazları kullanmadığında kapatmak enerji tasarrufu sağlar.",
            "Yenilenebilir enerji kaynaklarına geçiş yapmak çevreye olumlu katkı sağlar.",
            "Geri dönüşüm yapmak atık miktarını azaltır ve kaynakları korur."]



@bot.command()
async def oneri(ctx):
    link = random.choice(yardim)
    onerrri = random.choice(onerri)
    await ctx.send(onerrri)
    await ctx.send(f"İklim değişikliği hakkında daha fazla bilgi edinmek için bazı kaynaklar öneriyorum: {link}")



@bot.command()
async def icantstoptheloneliness(ctx):
    await ctx.send("https://youtu.be/6bALJxjL8jw?si=-ej8_00wrph-ZQGn")


bot.run("YOUR_BOT_TOKEN_HERE")


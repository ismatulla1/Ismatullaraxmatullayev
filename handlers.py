from telegram import Update
from telegram.ext import ContextTypes
from database import add_user, count_referrals
from config import DEFAULT_THRESHOLD, CHANNEL_ID
from utils import send_unique_invite_link


# ✅ Foydalanuvchi ko‘rinadigan nomini olish
def get_display_name(user):
    if user.username:
        return f"@{user.username}"
    elif user.first_name:
        return user.first_name
    else:
        return str(user.id)


# 🚀 /start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    name = get_display_name(user)

    # referalni tekshirish
    args = context.args
    invited_by = int(args[0]) if args else None

    # bazaga qo‘shish
    add_user(user.id, invited_by)

    # referallar sonini hisoblash
    referrals = count_referrals(user.id)

    if referrals >= DEFAULT_THRESHOLD:
        # 🎉 7 ta odamdan keyin yopiq kanal uchun bir martalik link yaratamiz
        invite_link = await context.bot.create_chat_invite_link(
            chat_id=CHANNEL_ID,
            member_limit=1  # faqat bitta odam ishlata oladi
        )
        await update.message.reply_text(
            f"🎉 Tabriklaymiz, {name}!\n"
            f"Siz {DEFAULT_THRESHOLD} ta do‘st taklif qildingiz ✅\n\n"
            f"🔗 Mana yopiq kanal linki:\n{invite_link.invite_link}"
        )
    else:
        # ❌ Hali limitga yetmagan bo‘lsa
        ref_link = send_unique_invite_link(user.id)
        await update.message.reply_text(
            f"🎉Assalomu alaykum! , {name}! 👋\n"
            f" Atestatsiya va Fizikadan Milliy sertifikat imtixoniga bepul tayyorlanish imkoniyati\n"
            f"""📝 Referal havolasi:

🌟 Har bir yangi do‘stni taklif qilganingizda, sizga bonus ball beriladi!

🚀 Har bir ovoz sizni sertifikat tomon yana bir qadam yaqinlashtiradi!

💥 Takliflar ko‘paygan sayin, imkoniyatlar ham kengayadi!
"""
            f"Siz hozircha {referrals} ta odam taklif qildingiz.\n"
            f"{DEFAULT_THRESHOLD} ta odam taklif qilsangiz, yopiq kanal linkini olasiz!\n\n"
            f"📢 Sizning referal linkingiz:\n{ref_link}"
        )


# 🚀 /referrals komandasi
async def get_referrals(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    name = get_display_name(user)

    referrals = count_referrals(user.id)
    await update.message.reply_text(
        f"{name}, siz hozircha {referrals} ta odamni taklif qildingiz."
    )


# 🚀 /help komandasi
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    name = get_display_name(user)

    await update.message.reply_text(
        f"📋 Yo‘riqnoma, {name}:\n\n"
        f"1️⃣ Bot sizga referal link beradi.\n"
        f"2️⃣ Sizning do‘stlaringiz o‘sha link orqali kirsa, sizga ball qo‘shiladi.\n"
        f"3️⃣ {DEFAULT_THRESHOLD} ta odam taklif qilsangiz, yopiq kanal uchun maxsus link olasiz."
    )

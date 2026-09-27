import asyncio
import logging
import json
import os
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "8779396683:AAE9tBDGn43dluGmWB2JhxNS-9ZJb-3fFSI"
ADMIN_ID = 788712525
DB_FILE = "users_db.json"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- BAZA E TË DHËNAVE PËR BALANCËN ---
def load_db():
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

def get_user_balance(user_id):
    db = load_db()
    return db.get(str(user_id), 0)

def add_user_balance(user_id, amount):
    db = load_db()
    current = db.get(str(user_id), 0)
    db[str(user_id)] = current + amount
    save_db(db)
    return db[str(user_id)]

# --- MENUTË ---
menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="⭐ Stars olish"), KeyboardButton(text="🎁 Gift olish")],
        [KeyboardButton(text="👤 Hisobim"), KeyboardButton(text="👥 Referal")],
        [KeyboardButton(text="📖 Qo'llanma"), KeyboardButton(text="📞 Admin")]
    ],
    resize_keyboard=True
)

stars_inline_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="⭐ 50 — 11,000 so'm", callback_data="buy_stars_50_11000")],
        [InlineKeyboardButton(text="⭐ 100 — 21,000 so'm", callback_data="buy_stars_100_21000")],
        [InlineKeyboardButton(text="⭐ 150 — 31,000 so'm", callback_data="buy_stars_150_31000")],
        [InlineKeyboardButton(text="⭐ 200 — 41,000 so'm", callback_data="buy_stars_200_41000")],
        [InlineKeyboardButton(text="⭐ 250 — 51,000 so'm", callback_data="buy_stars_250_51000")],
        [InlineKeyboardButton(text="⭐ 300 — 61,000 so'm", callback_data="buy_stars_300_61000")],
        [InlineKeyboardButton(text="⭐ 400 — 81,000 so'm", callback_data="buy_stars_400_81000")],
        [InlineKeyboardButton(text="⭐ 500 — 101,000 so'm", callback_data="buy_stars_500_101000")],
        [InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_to_menu")]
    ]
)

gift_inline_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="💖 15 ⭐ — 3,000 so'm", callback_data="buy_gift_Yurak_3000")],
        [InlineKeyboardButton(text="🧸 15 ⭐ — 3,000 so'm", callback_data="buy_gift_Ayiqcha_3000")],
        [InlineKeyboardButton(text="🎁 25 ⭐ — 5,500 so'm", callback_data="buy_gift_Sovg'a_5500")],
        [InlineKeyboardButton(text="🌹 25 ⭐ — 5,500 so'm", callback_data="buy_gift_Roza_5500")],
        [InlineKeyboardButton(text="🎂 50 ⭐ — 10,500 so'm", callback_data="buy_gift_Tort_10500")],
        [InlineKeyboardButton(text="🚀 50 ⭐ — 10,500 so'm", callback_data="buy_gift_Raketa_10500")],
        [InlineKeyboardButton(text="💍 50 ⭐ — 10,500 so'm", callback_data="buy_gift_Uzuk_10500")],
        [InlineKeyboardButton(text="💐 50 ⭐ — 10,500 so'm", callback_data="buy_gift_Guldasta_10500")],
        [InlineKeyboardButton(text="🏆 100 ⭐ — 20,000 so'm", callback_data="buy_gift_Kubok_20000")],
        [InlineKeyboardButton(text="💎 100 ⭐ — 20,000 so'm", callback_data="buy_gift_Olmos_20000")],
        [InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_to_menu")]
    ]
)

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    welcome_text = (
        "Xush kelibsiz!\n\n"
        "⭐ **Stars sotib olish:** Tez va hamyonbop narxlarda Telegram Stars xarid qiling.\n"
        "🎁 **Gift sotib olish:** Do'stlaringiz va yaqinlaringiz uchun ayiqcha va boshqa sovg'alar oling!\n\n"
        "Kerakli bo'limni tanlang 👇"
    )
    await message.answer(welcome_text, reply_markup=menu)

@dp.message(F.text == "⭐ Stars olish")
async def stars_handler(message: types.Message):
    await message.answer("⭐ Stars miqdorini tanlang:", reply_markup=stars_inline_menu)

@dp.message(F.text == "🎁 Gift olish")
async def gift_handler(message: types.Message):
    await message.answer("🎁 Gift tanlang:", reply_markup=gift_inline_menu)

@dp.callback_query(F.data.startswith("buy_stars_"))
async def process_buy_stars(callback: types.CallbackQuery):
    parts = callback.data.split("_")
    stars_num = parts[2]
    price_num = parts[3]
    
    msg_text = (
        f"💳 **To'lov usuli:** Visa / Uzcard / Humo\n"
        f"📌 **Siz tanladingiz:** {stars_num} ⭐ ({price_num} so'm)\n\n"
        f"💳 **Karta:** `4916990352067950`\n"
        f"🆔 **Sizning ID:** `{callback.from_user.id}`\n\n"
        f"Pulni o'tkazib, chek va ID ingizni adminga yuboring: @okeni_stars_bor"
    )
    await callback.message.edit_text(msg_text)
    await callback.answer()

@dp.callback_query(F.data.startswith("buy_gift_"))
async def process_buy_gift(callback: types.CallbackQuery):
    parts = callback.data.split("_")
    gift_name = parts[2]
    price_num = parts[3]
    
    msg_text = (
        f"💳 **To'lov usuli:** Uzcard / Humo / Visa\n"
        f"📌 **Siz tanladingiz:** {gift_name} ({price_num} so'm)\n\n"
        f"💳 **Karta:** `5614683015491525`\n"
        f"🆔 **Sizning ID:** `{callback.from_user.id}`\n\n"
        f"Pulni o'tkazib, chek va ID ingizni adminga yuboring: @VENOX_Uz1"
    )
    await callback.message.edit_text(msg_text)
    await callback.answer()

@dp.callback_query(F.data == "back_to_menu")
async def back_handler(callback: types.CallbackQuery):
    await callback.message.delete()
    await callback.message.answer("Asosiy menyu:", reply_markup=menu)

@dp.message(F.text == "👤 Hisobim")
async def account_handler(message: types.Message):
    user = message.from_user
    balance = get_user_balance(user.id)
    await message.answer(f"Sizning ma'lumotlaringiz:\nID: {user.id}\nIsm: {user.first_name}\nBalans: {balance:,} so'm".replace(",", " "))

@dp.message(F.text == "👥 Referal")
async def referal_handler(message: types.Message):
    user_id = message.from_user.id
    await message.answer(
        f"Referal tizimi:\nDo'stlaringizni taklif qiling va 100 so'm oling!\n\n"
        f"Sizning havolangiz:\nhttps://t.me/VENOX_UZ_STARS_BOT?start={user_id}"
    )

@dp.message(F.text == "📖 Qo'llanma")
async def guide_handler(message: types.Message):
    await message.answer("Qo'llanma tez orada qo'shiladi.")

@dp.message(F.text == "📞 Admin")
async def admin_handler(message: types.Message):
    await message.answer("Adminlar bilan bog'lanish:\n⭐ Stars bo'yicha: @okeni_stars_bor\n🎁 Gift bo'yicha: @VENOX_Uz1")

@dp.message(Command("send"))
async def send_money_cmd(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("Siz admin emassiz!")
        return

    try:
        args = message.text.split()
        target_id = int(args[1])
        amount = int(args[2].replace(".", "").replace(",", "").replace("som", "").replace("so'm", ""))
        
        new_balance = add_user_balance(target_id, amount)
        
        await bot.send_message(
            target_id, 
            f"✅ **Balansingiz to'ldirildi!**\n"
            f"💰 Qo'shildi: {amount:,} so'm\n"
            f"💳 Hozirgi balansingiz: {new_balance:,} so'm".replace(",", " ")
        )
        await message.answer(f"✅ {target_id} ID egalasiga {amount:,} so'm qo'shildi!\nYangi balans: {new_balance:,} so'm".replace(",", " "))
    except IndexError:
        await message.answer("❌ Noto'g'ri format!\nMisol: `/send 8527026238 11000`")
    except Exception as e:
        await message.answer(f"Xatolik yuz berdi: {e}")

async def main():
    logging.basicConfig(level=logging.INFO)
    print("Bot ishlashga tayyor!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

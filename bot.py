from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

API_ID = 36112539
API_HASH = "c9797b78de5e31facde739d92253b2a1"
BOT_TOKEN = "8975966534:AAE3gIBCyVmQKaVA0pVH6vqqS_AZEsV4kXs"
OWNER_ID = 1942474531
DB_CHANNEL = -1003911942501

app = Client(
    "cineflix_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

@app.on_message(filters.command("start") & filters.regex(r"file_(\d+)"))
async def send_file(client, message: Message):
    try:
        file_id = int(message.text.split("file_")[1])
        await client.copy_message(
            chat_id=message.chat.id,
            from_chat_id=DB_CHANNEL,
            message_id=file_id
        )
    except Exception as e:
        await message.reply_text("❌ File nahi mili!")

@app.on_message(filters.command("start"))
async def start(client, message: Message):
    await message.reply_text(
        f"🎬 **CineFlix Stream Bot**\n\n"
        f"Namaste {message.from_user.mention}!\n\n"
        f"Movies aur Web Series ke links yahan milenge!",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🌐 CineFlix Website", url="https://cinema1.free.nf")],
        ])
    )

@app.on_message(filters.command("help"))
async def help_cmd(client, message: Message):
    await message.reply_text(
        "**CineFlix Bot Help**\n\n"
        "/start - Bot shuru karo\n"
        "/help - Help dekho\n\n"
        "**Admin:** Mujhe file bhejo — permanent link milega!"
    )

@app.on_message(filters.private & filters.media & filters.user(OWNER_ID))
async def get_link(client, message: Message):
    msg = await message.reply_text("⏳ Link generate ho raha hai...")
    try:
        forwarded = await message.forward(DB_CHANNEL)
        file_id = forwarded.id
        stream_link = f"https://t.me/cineflix989_bot?start=file_{file_id}"
        await msg.edit_text(
            f"✅ **Link Ready!**\n\n"
            f"🔗 **Permanent Link:**\n`{stream_link}`\n\n"
            f"✅ Yeh link kabhi expire nahi hoga!",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔗 Link Kholo", url=stream_link)],
            ])
        )
    except Exception as e:
        await msg.edit_text(f"❌ Error: {str(e)}")

print("🎬 CineFlix Bot chal raha hai...")
app.run()

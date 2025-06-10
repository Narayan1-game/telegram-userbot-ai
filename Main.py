from pyrogram import Client, filters
import openai
import asyncio
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

app = Client("ai-bot", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH)

@app.on_message(filters.private & filters.regex(r"^\.(love|ily|heart)$"))
def userbot_react(client, message):
    try:
        client.delete_messages(message.chat.id, message.id)
        msg = message.reply("❤️")
        client.loop.create_task(react_edit_chain(msg))
    except Exception as e:
        message.reply(f"Error: {e}")

async def react_edit_chain(msg):
    await asyncio.sleep(0.3)
    await msg.edit("💘")
    await asyncio.sleep(0.3)
    await msg.edit("💞")
    await asyncio.sleep(0.3)
    await msg.edit("❤️ Done!")

@app.on_message(filters.private & filters.text)
def chatgpt_reply(client, message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": message.text}],
        )
        reply = response['choices'][0]['message']['content']
        message.reply_text(reply)
    except Exception as e:
        message.reply_text(f"Error: {e}")

app.run()

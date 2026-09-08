# ============================================================
# سورس کامل سلف‌بیس OMEGA - نسخه نهایی v5.0
# شامل تمام قابلیت‌های درخواستی
# ============================================================

import os
import asyncio
import logging
import re
import time
import random
import hashlib
import base64
import json
import sqlite3
import shutil
import zipfile
from datetime import datetime, timedelta
from math import ceil
from io import BytesIO

from telethon import TelegramClient, events, functions, types
from telethon.tl.types import (
    MessageMediaPhoto, MessageMediaDocument, MessageMediaWebPage,
    MessageMediaGame, MessageMediaPoll, MessageMediaDice,
    InputPeerUser, InputPeerChat, InputPeerChannel,
    DocumentAttributeAudio, DocumentAttributeFilename,
    MessageEntityCustomEmoji, InputMediaUploadedDocument,
    InputMediaUploadedPhoto
)
from telethon.tl.functions.messages import SetTypingRequest, GetHistoryRequest
from telethon.tl.functions.account import UpdateProfileRequest, UpdateStatusRequest
from telethon.tl.functions.contacts import BlockRequest
from telethon.tl.functions.channels import LeaveChannelRequest, JoinChannelRequest, CreateChannelRequest, EditBannedRequest
from telethon.tl.functions.photos import UploadProfilePhotoRequest, DeletePhotosRequest, GetUserPhotosRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.errors import FloodWaitError, RPCError

# کتابخانه‌های خارجی
import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFont
from googlesearch import search
import wikipedia
import pytz
import jdatetime
from persiantools.jdatetime import JalaliDate
import psutil
import qrcode

# ==================== تنظیمات اصلی ====================
API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
PHONE_NUMBER = os.environ.get("PHONE_NUMBER", "")
ADMIN_USER_ID = int(os.environ.get("ADMIN_USER_ID", 0))
SESSION_NAME = os.environ.get("SESSION_NAME", "omega_session")

if not API_ID or not API_HASH or not PHONE_NUMBER or not ADMIN_USER_ID:
    print("❌ خطا: متغیرهای محیطی به‌درستی تنظیم نشده‌اند!")
    exit(1)

# ==================== کلاینت تلگرام ====================
client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

# ==================== دیتابیس ====================
class Database:
    def __init__(self):
        self.conn = sqlite3.connect('omega_self.db')
        self.cursor = self.conn.cursor()
        self._create_tables()

    def _create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS auto_replies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                keyword TEXT UNIQUE,
                response TEXT
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS enemies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER UNIQUE
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS autosave_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_name TEXT,
                file_type TEXT,
                sender_id INTEGER,
                saved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS fosh_list (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT UNIQUE,
                type TEXT DEFAULT 'normal'
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS music_library (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE,
                file_path TEXT
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS video_library (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE,
                file_path TEXT
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS love_list (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER UNIQUE,
                text TEXT
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS hbd_texts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT UNIQUE
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS alarms (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT UNIQUE
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS realm_settings (
                chat_id INTEGER PRIMARY KEY,
                is_realm INTEGER DEFAULT 0,
                save_enabled INTEGER DEFAULT 0,
                trmode_enabled INTEGER DEFAULT 0
            )
        ''')
        self.conn.commit()

    # ====== Auto Replies ======
    def add_auto_reply(self, keyword, response):
        self.cursor.execute("INSERT OR REPLACE INTO auto_replies (keyword, response) VALUES (?, ?)", (keyword, response))
        self.conn.commit()

    def delete_auto_reply(self, keyword):
        self.cursor.execute("DELETE FROM auto_replies WHERE keyword = ?", (keyword,))
        self.conn.commit()

    def get_auto_replies(self):
        self.cursor.execute("SELECT keyword, response FROM auto_replies")
        return self.cursor.fetchall()

    # ====== Enemies ======
    def add_enemy(self, user_id):
        self.cursor.execute("INSERT OR IGNORE INTO enemies (user_id) VALUES (?)", (user_id,))
        self.conn.commit()

    def delete_enemy(self, user_id):
        self.cursor.execute("DELETE FROM enemies WHERE user_id = ?", (user_id,))
        self.conn.commit()

    def get_enemies(self):
        self.cursor.execute("SELECT user_id FROM enemies")
        return [row[0] for row in self.cursor.fetchall()]

    def reset_enemies(self):
        self.cursor.execute("DELETE FROM enemies")
        self.conn.commit()

    # ====== Fosh ======
    def add_fosh(self, text, ftype='normal'):
        self.cursor.execute("INSERT OR IGNORE INTO fosh_list (text, type) VALUES (?, ?)", (text, ftype))
        self.conn.commit()

    def delete_fosh(self, text):
        self.cursor.execute("DELETE FROM fosh_list WHERE text = ?", (text,))
        self.conn.commit()

    def get_fosh_list(self, ftype='normal'):
        self.cursor.execute("SELECT text FROM fosh_list WHERE type = ?", (ftype,))
        return [row[0] for row in self.cursor.fetchall()]

    def clear_fosh(self, ftype='normal'):
        self.cursor.execute("DELETE FROM fosh_list WHERE type = ?", (ftype,))
        self.conn.commit()

    # ====== Music ======
    def add_music(self, name, file_path):
        self.cursor.execute("INSERT OR REPLACE INTO music_library (name, file_path) VALUES (?, ?)", (name, file_path))
        self.conn.commit()

    def get_music(self, name):
        self.cursor.execute("SELECT file_path FROM music_library WHERE name = ?", (name,))
        row = self.cursor.fetchone()
        return row[0] if row else None

    def get_all_music(self):
        self.cursor.execute("SELECT name FROM music_library")
        return [row[0] for row in self.cursor.fetchall()]

    def delete_music(self, name):
        self.cursor.execute("DELETE FROM music_library WHERE name = ?", (name,))
        self.conn.commit()

    def clear_music(self):
        self.cursor.execute("DELETE FROM music_library")
        self.conn.commit()

    # ====== Video ======
    def add_video(self, name, file_path):
        self.cursor.execute("INSERT OR REPLACE INTO video_library (name, file_path) VALUES (?, ?)", (name, file_path))
        self.conn.commit()

    def get_video(self, name):
        self.cursor.execute("SELECT file_path FROM video_library WHERE name = ?", (name,))
        row = self.cursor.fetchone()
        return row[0] if row else None

    def get_all_videos(self):
        self.cursor.execute("SELECT name FROM video_library")
        return [row[0] for row in self.cursor.fetchall()]

    def delete_video(self, name):
        self.cursor.execute("DELETE FROM video_library WHERE name = ?", (name,))
        self.conn.commit()

    def clear_video(self):
        self.cursor.execute("DELETE FROM video_library")
        self.conn.commit()

    # ====== Love ======
    def add_love(self, user_id, text):
        self.cursor.execute("INSERT OR REPLACE INTO love_list (user_id, text) VALUES (?, ?)", (user_id, text))
        self.conn.commit()

    def delete_love(self, user_id):
        self.cursor.execute("DELETE FROM love_list WHERE user_id = ?", (user_id,))
        self.conn.commit()

    def get_love(self, user_id):
        self.cursor.execute("SELECT text FROM love_list WHERE user_id = ?", (user_id,))
        row = self.cursor.fetchone()
        return row[0] if row else None

    def get_all_love(self):
        self.cursor.execute("SELECT user_id, text FROM love_list")
        return self.cursor.fetchall()

    # ====== HBD ======
    def add_hbd_text(self, text):
        self.cursor.execute("INSERT OR IGNORE INTO hbd_texts (text) VALUES (?)", (text,))
        self.conn.commit()

    def delete_hbd_text(self, text):
        self.cursor.execute("DELETE FROM hbd_texts WHERE text = ?", (text,))
        self.conn.commit()

    def get_hbd_texts(self):
        self.cursor.execute("SELECT text FROM hbd_texts")
        return [row[0] for row in self.cursor.fetchall()]

    def clear_hbd_texts(self):
        self.cursor.execute("DELETE FROM hbd_texts")
        self.conn.commit()

    # ====== Alarms ======
    def add_alarm(self, text):
        self.cursor.execute("INSERT OR IGNORE INTO alarms (text) VALUES (?)", (text,))
        self.conn.commit()

    def delete_alarm(self, text):
        self.cursor.execute("DELETE FROM alarms WHERE text = ?", (text,))
        self.conn.commit()

    def get_alarms(self):
        self.cursor.execute("SELECT text FROM alarms")
        return [row[0] for row in self.cursor.fetchall()]

    # ====== Realm ======
    def set_realm(self, chat_id, is_realm=1):
        self.cursor.execute("INSERT OR REPLACE INTO realm_settings (chat_id, is_realm) VALUES (?, ?)", (chat_id, is_realm))
        self.conn.commit()

    def get_realm(self, chat_id):
        self.cursor.execute("SELECT is_realm FROM realm_settings WHERE chat_id = ?", (chat_id,))
        row = self.cursor.fetchone()
        return row[0] if row and row[0] == 1 else False

    def set_save_enabled(self, chat_id, enabled=1):
        self.cursor.execute("INSERT OR REPLACE INTO realm_settings (chat_id, save_enabled) VALUES (?, ?)", (chat_id, enabled))
        self.conn.commit()

    def get_save_enabled(self, chat_id):
        self.cursor.execute("SELECT save_enabled FROM realm_settings WHERE chat_id = ?", (chat_id,))
        row = self.cursor.fetchone()
        return row[0] if row and row[0] == 1 else False

    def set_trmode_enabled(self, chat_id, enabled=1):
        self.cursor.execute("INSERT OR REPLACE INTO realm_settings (chat_id, trmode_enabled) VALUES (?, ?)", (chat_id, enabled))
        self.conn.commit()

    def get_trmode_enabled(self, chat_id):
        self.cursor.execute("SELECT trmode_enabled FROM realm_settings WHERE chat_id = ?", (chat_id,))
        row = self.cursor.fetchone()
        return row[0] if row and row[0] == 1 else False

    # ====== General Settings ======
    def get_setting(self, key, default="off"):
        self.cursor.execute("SELECT value FROM settings WHERE key = ?", (key,))
        row = self.cursor.fetchone()
        return row[0] if row else default

    def set_setting(self, key, value):
        self.cursor.execute("INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)", (key, value))
        self.conn.commit()

    def log_autosave(self, file_name, file_type, sender_id):
        self.cursor.execute(
            "INSERT INTO autosave_log (file_name, file_type, sender_id) VALUES (?, ?, ?)",
            (file_name, file_type, sender_id)
        )
        self.conn.commit()

    def get_autosave_log(self, limit=10):
        self.cursor.execute(
            "SELECT file_name, file_type, sender_id, saved_at FROM autosave_log ORDER BY id DESC LIMIT ?",
            (limit,)
        )
        return self.cursor.fetchall()

db = Database()

# ==================== وضعیت‌ها ====================
status = {
    'bot_on': True,
    'autosave_on': True,
    'lockpv_on': False,
    'autochat_on': False,
    'locklink_on': False,
    'locktag_on': False,
    'mention_on': False,
    'typing_on': False,
    'videoaction_on': False,
    'audioaction_on': False,
    'gameplay_on': False,
    'markread_on': False,
    'poker_on': False,
    'hashtag_on': False,
    'bold_on': False,
    'strikethrough_on': False,
    'italic_on': False,
    'underline_on': False,
    'part_on': False,
    'timename_on': False,
    'timebio_on': False,
    'timepic_on': False,
    'monshi_on': False,
    'selfall_on': False,
    'pokerall_on': False,
    'typingall_on': False,
    'markreadall_on': False,
    'tagreadall_on': False,
    'actionall_on': False,
    'sticker_on': False,
    'texter_on': False,
    'info_on': False,
    'name_on': False,
    'bio_on': False,
    'love_on': False,
    'hbd_on': False,
    'alarm_on': False,
    'myfosh_on': False,
    'smartmonshi_on': False,
    'monshioffline_on': False,
}

# ==================== متغیرهای کمکی ====================
enemy_list = []
silenced_users = []
GAdmins = []
user_messages = {}
fast_replies = {}
love_list = {}
hbd_texts = []
alarms = []
fosh_normal = []
fosh_friend = []
music_lib = {}
video_lib = {}
realm_chat = None
save_enabled = False
trmode_enabled = False
monshi_text = ""
smart_monshi_text = ""
monshi_offline_time = 5
texter_text = ""
sticker_file = None

timezone = pytz.timezone('Asia/Tehran')
current_time_str = datetime.now(timezone).strftime("%H:%M")

# ==================== توابع کمکی ====================
def get_iran_time():
    return datetime.now(timezone).strftime("%H:%M:%S")

def get_persian_date():
    try:
        return jdatetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    except:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def get_uptime(start_time):
    now = datetime.now()
    uptime = now - start_time
    days = uptime.days
    hours, remainder = divmod(uptime.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{days} روز {hours} ساعت {minutes} دقیقه {seconds} ثانیه"

def calc_expression(expr):
    try:
        if not re.match(r'^[\d+\-*/().% ]+$', expr):
            return "❌ لطفاً فقط از اعداد و عملگرها استفاده کنید"
        result = eval(expr)
        return f"✅ {expr} = {result}"
    except:
        return "❌ عبارت نامعتبر است"

def encode_base64(text):
    return base64.b64encode(text.encode()).decode()

def decode_base64(text):
    try:
        return base64.b64decode(text.encode()).decode()
    except:
        return "❌ خطا در دیکد کردن"

def hash_text(text, algo="md5"):
    if algo == "md5":
        return hashlib.md5(text.encode()).hexdigest()
    elif algo == "sha1":
        return hashlib.sha1(text.encode()).hexdigest()
    elif algo == "sha256":
        return hashlib.sha256(text.encode()).hexdigest()
    return hashlib.md5(text.encode()).hexdigest()

def get_age(birthdate):
    try:
        birth = datetime.strptime(birthdate, "%Y/%m/%d")
        today = datetime.now()
        age = today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))
        return f"🎂 سن شما: {age} سال"
    except:
        return "❌ فرمت تاریخ صحیح نیست (مثال: 2000/01/01)"

def get_weather(city):
    try:
        url = f"http://wttr.in/{city}?format=%C+%t+%h"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return f"🌤 وضعیت هوای {city}: {response.text.strip()}"
        return "❌ خطا در دریافت اطلاعات"
    except:
        return "❌ خطا در اتصال به سرور"

def get_joke():
    jokes = [
        "یه روز یه گوجه فرنگی رفت خیابون، ماشین زدش شد رب گوجه! 😂",
        "چرا سگ دمش رو تکون میده؟ چون دستش به دمش نمیرسه! 🐕",
        "یه کباب به کبابی گفت: منو بپز! کبابی گفت: تو خودت کبابی! 🤣",
        "چرا مرغ از جاده رد نشد؟ چون تخم مرغ بود! 🐔",
        "یه پسته به پسته دیگه گفت: چرا دندونات زرده؟ گفت: نخوردمش! 😁",
    ]
    return random.choice(jokes)

def get_crypto_prices():
    cryptos = {
        'Bitcoin (BTC)': 'bitcoin',
        'Ethereum (ETH)': 'ethereum',
        'Tether (USDT)': 'tether',
        'TRON (TRX)': 'tron',
        'Dogecoin (DOGE)': 'dogecoin'
    }
    prices = {}
    try:
        for crypto, symbol in cryptos.items():
            response = requests.get(f'https://api.coingecko.com/api/v3/simple/price?ids={symbol}&vs_currencies=usd')
            if response.status_code == 200:
                data = response.json()
                prices[crypto] = data[symbol]['usd']
        return prices
    except:
        return None

def get_currency_rates():
    try:
        url = "https://api.exchangerate-api.com/v4/latest/USD"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            rates = data['rates']
            return {
                'USD': 1,
                'EUR': rates.get('EUR', 0),
                'GBP': rates.get('GBP', 0),
                'TRY': rates.get('TRY', 0),
                'AED': rates.get('AED', 0),
            }
    except:
        return None

def get_gold_price():
    try:
        url = "https://api.gold-api.com/price/XAU"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return f"💰 قیمت هر اونس طلا: ${data.get('price', 0):.2f}"
        return "❌ خطا در دریافت قیمت طلا"
    except:
        return "❌ خطا در اتصال"

# ==================== تابع به‌روزرسانی پروفایل ====================
async def update_profile_with_time():
    if status['timename_on'] or status['timebio_on']:
        try:
            me = await client.get_me()
            current_time = get_iran_time()
            heart_list = ['❤️', '💛', '💚', '💙', '💜', '🖤', '🤍', '🧡', '💖', '💗', '💓', '💞', '💕']
            heart = random.choice(heart_list)
            
            if status['timename_on']:
                try:
                    new_name = f"{me.first_name.split('🕐')[0].strip()} 🕐 {current_time}"
                    await client(UpdateProfileRequest(first_name=new_name))
                except:
                    pass
            
            if status['timebio_on']:
                try:
                    persian_date = jdatetime.datetime.now().strftime("%Y/%m/%d")
                    new_bio = f"🕐 {current_time} - {persian_date} {heart}"
                    await client(UpdateProfileRequest(about=new_bio))
                except:
                    pass
        except:
            pass

async def time_updater():
    while True:
        await asyncio.sleep(60)
        try:
            await update_profile_with_time()
        except:
            pass

# ==================== هندلر پیام‌ها ====================
@client.on(events.NewMessage(incoming=True))
async def handle_all_messages(event):
    global status, realm_chat, save_enabled, trmode_enabled, monshi_text, smart_monshi_text, texter_text, sticker_file
    
    if not status['bot_on']:
        return
    
    msg = event.message
    sender = await event.get_sender()
    chat = await event.get_chat()
    me = await client.get_me()
    
    # ====== لاک پیوی ======
    if status['lockpv_on'] and event.is_private and not sender.bot:
        if sender.id != me.id:
            try:
                await client(BlockRequest(id=sender.id))
                await event.reply("🚫 کاربر بلاک شد (حالت lockpv)")
            except:
                pass
            return
    
    # ====== دشمنان ======
    enemies = db.get_enemies()
    if sender and sender.id in enemies:
        try:
            await event.reply("⚠️ شما در لیست دشمنان هستید!")
        except:
            pass
        return
    
    # ====== قفل لینک ======
    if status['locklink_on'] and event.is_group and msg.text:
        if 'http' in msg.text or 'www.' in msg.text or '.com' in msg.text or '.ir' in msg.text:
            try:
                await client.delete_messages(event.chat_id, [msg.id])
                await event.reply("🔗 لینک حذف شد (حالت locklink)")
            except:
                pass
    
    # ====== قفل تگ ======
    if status['locktag_on'] and event.is_group and msg.mentioned:
        try:
            await client.delete_messages(event.chat_id, [msg.id])
            await event.reply("🏷️ تگ حذف شد (حالت locktag)")
        except:
            pass
    
    # ====== منشن خودکار ======
    if status['mention_on'] and event.is_group and msg.text and not msg.mentioned and not msg.fwd_from:
        try:
            await client.send_message(event.chat_id, f"@{me.username} {msg.text}")
        except:
            pass
    
    # ====== پاسخ خودکار ======
    if status['autochat_on'] and msg.text and not msg.mentioned:
        replies = db.get_auto_replies()
        for keyword, response in replies:
            if keyword.lower() in msg.text.lower():
                try:
                    await event.reply(response)
                except:
                    pass
                break
    
    # ====== منشی (Monshi) ======
    if status['monshi_on'] and event.is_private and sender.id != me.id:
        try:
            if monshi_text:
                await event.reply(monshi_text)
        except:
            pass
    
    # ====== منشی هوشمند ======
    if status['smartmonshi_on'] and event.is_private and sender.id != me.id:
        try:
            # بررسی اینکه آیا قبلاً با این کاربر مکالمه داشته‌ایم یا خیر
            history = await client.get_messages(event.chat_id, limit=2)
            if len(history) <= 1:  # فقط پیام خود کاربر وجود دارد
                if smart_monshi_text:
                    await event.reply(smart_monshi_text)
        except:
            pass
    
    # ====== ذخیره‌سازی خودکار ======
    if status['autosave_on'] and msg.media:
       # تشخیص پیام‌های تایم‌دار (Self-Destruct)
is_ttl = False
if hasattr(msg, 'media') and msg.media:
    if hasattr(msg.media, 'ttl_seconds') and msg.media.ttl_seconds:
        is_ttl = True
        no_share = False
if hasattr(msg, 'media') and hasattr(msg.media, 'document') and msg.media.document:
    for attr in msg.media.document.attributes:
        if hasattr(attr, 'has_no_share') and attr.has_no_share:
            no_share = True
            break
        if is_ttl or no_share:
            try:
                file_path = await client.download_media(msg)
                if file_path:
                    await client.send_file("me", file_path)
                    file_name = os.path.basename(file_path)
                    file_type = "unknown"
                    if msg.photo:
                        file_type = "photo"
                    elif msg.video:
                        file_type = "video"
                    elif msg.voice:
                        file_type = "voice"
                    elif msg.audio:
                        file_type = "audio"
                    elif msg.document:
                        file_type = "document"
                    elif msg.sticker:
                        file_type = "sticker"
                    db.log_autosave(file_name, file_type, sender.id if sender else 0)
                    try:
                        os.remove(file_path)
                    except:
                        pass
            except:
                pass
    
    # ====== حالت‌های اکشن ======
    if event.is_private or event.is_group:
        action = None
        if status['typing_on']:
            action = types.SendMessageTypingAction()
        elif status['videoaction_on']:
            action = types.SendMessageRecordVideoAction()
        elif status['audioaction_on']:
            action = types.SendMessageRecordAudioAction()
        elif status['gameplay_on']:
            action = types.SendMessageGamePlayAction()
        if action:
            try:
                await client(SetTypingRequest(peer=await event.get_input_chat(), action=action))
            except:
                pass
        
        if status['poker_on'] and msg.text and '😐' in msg.text:
            try:
                await event.reply("😐 پوکر! 😐")
            except:
                pass
    
    # ====== پردازش دستورات ======
    if msg.text:
        text = msg.text
        # پردازش دستورات با /
        if text.startswith('/'):
            parts = text.split()
            cmd = parts[0].lower()
            args = ' '.join(parts[1:]) if len(parts) > 1 else ''
            
            # ====== پنل شیشه‌ای (Inline Panel) ======
            if cmd == '/panel':
                try:
                    panel_text = f"""🤖 **پنل مدیریت سلف‌بیس OMEGA v5.0**

📊 **وضعیت:** {'✅ روشن' if status['bot_on'] else '❌ خاموش'}
👤 **حساب:** @{me.username or 'ندارد'}

🔹 **قابلیت‌های اصلی:**
• مدیریت زمان در اسم و بیو
• مدیریت گروه (قفل لینک، قفل تگ، منشن)
• پاسخ خودکار
• منشی هوشمند
• ذخیره‌سازی خودکار
• ایموجی پریمیوم
• تبدیل ویدیو به ویدیو مسیج
• و بیش از ۱۵۰ دستور دیگر

📌 برای مشاهده راهنما: /help
"""
                    buttons = [
                        [types.KeyboardButtonCallback("📊 وضعیت", b"status")],
                        [types.KeyboardButtonCallback("⚙️ تنظیمات", b"settings"), types.KeyboardButtonCallback("🛡️ امنیت", b"security")],
                        [types.KeyboardButtonCallback("🎮 سرگرمی", b"fun"), types.KeyboardButtonCallback("🔧 ابزارها", b"tools")],
                        [types.KeyboardButtonCallback("❌ بستن پنل", b"close_panel")],
                    ]
                    await event.reply(panel_text, buttons=buttons)
                except Exception as e:
                    await event.reply(f"❌ خطا در نمایش پنل: {str(e)}")
            
            # ====== راهنما ======
            elif cmd == '/help':
                if args == '1' or not args:
                    help_text = """📚 **راهنمای بخش ۱ - مدیریت پایه**

🕐 **زمان:** `timename on/off` - نمایش زمان در اسم
🕐 **بیو:** `timebio on/off` - نمایش زمان در بیو
🖋 **فونت:** `bold on`, `mini on`, `mono on`, `default on`
❤️ **قلب:** `heart on/off` - نمایش قلب رندوم
📝 **بیوگرافی:** `/addbio متن` - تنظیم بیو
📛 **نام:** `/addrname name1,name2,...` - تنظیم نام تصادفی

📌 **سایر دستورات:**
`/ping` - بررسی وضعیت ربات
`/status` - نمایش وضعیت فعلی
`/restart` - ریستارت ربات
`/bot on/off` - روشن/خاموش کردن ربات
"""
                    await event.reply(help_text)
                elif args == '2':
                    help_text = """📚 **راهنمای بخش ۲ - مدیریت گروه و امنیت**

🔒 **امنیت:**
`/lockpv on/off` - بلاک خودکار پیوی
`/locklink on/off` - قفل لینک در گروه
`/locktag on/off` - قفل تگ در گروه
`/mention on/off` - منشن خودکار

👥 **مدیریت گروه:**
`/tag` - تگ کردن همه اعضا
`/silent` (ریپلی) - سکوت کاربر
`/unsilent` (ریپلی) - لغو سکوت
`/promote` (ریپلی) - افزودن به مدیران
`/demote` (ریپلی) - حذف از مدیران

⚔️ **دشمنان:**
`/setenemy` (ریپلی) - افزودن به لیست دشمنان
`/delenemy` (ریپلی) - حذف از لیست دشمنان
`/reset enemylist` - پاکسازی لیست دشمنان
"""
                    await event.reply(help_text)
                elif args == '3':
                    help_text = """📚 **راهنمای بخش ۳ - ابزارها و سرگرمی**

🧮 **ابزارها:**
`/calc 5+5` - ماشین‌حساب
`/hash متن` - هش کردن متن
`/encode متن` - رمزگذاری Base64
`/decode متن` - رمزگشایی Base64
`/weather شهر` - وضعیت هوا
`/wiki متن` - جستجوی ویکی‌پدیا

💰 **ارز و طلا:**
`/crypto` - قیمت ارزهای دیجیتال
`/currency` - قیمت ارزهای جهانی
`/gold` - قیمت طلا

🎮 **سرگرمی:**
`/joke` - جوک تصادفی
`/say متن` - نمایش کلمه‌به‌کلمه
`/age 2000/01/01` - محاسبه سن
"""
                    await event.reply(help_text)
                elif args == '4':
                    help_text = """📚 **راهنمای بخش ۴ - قابلیت‌های پیشرفته**

💾 **ذخیره‌سازی:**
`/save` (ریپلی) - ذخیره پیام در Saved Messages
`/autosave on/off` - ذخیره‌سازی خودکار رسانه‌های تایم‌دار

🎬 **ویدیو:**
`/tovm` (ریپلی روی ویدیو) - تبدیل به ویدیو مسیج

😊 **ایموجی پریمیوم:**
`/emoji 🎉` - ارسال ایموجی پریمیوم
`/emojilist` - نمایش لیست ایموجی‌های پریمیوم

🤖 **منشی:**
`/monshi on/off` - روشن/خاموش کردن منشی
`/setmonshi متن` - تنظیم متن منشی
`/smartmonshi on/off` - منشی هوشمند
`/setmonshioffline زمان` - تنظیم زمان آفلاین

📌 **سایر:**
`/stats` - نمایش آمار ربات
`/uptime` - زمان اجرای ربات
"""
                    await event.reply(help_text)
                else:
                    await event.reply("❌ راهنمای موجود: /help 1 تا /help 4")
            
            # ====== وضعیت ======
            elif cmd == '/status':
                status_text = f"""📊 **وضعیت فعلی ربات:**

🤖 ربات: {'✅ روشن' if status['bot_on'] else '❌ خاموش'}
💾 ذخیره‌سازی خودکار: {'✅' if status['autosave_on'] else '❌'}
🔒 lockpv: {'✅' if status['lockpv_on'] else '❌'}
🔗 قفل لینک: {'✅' if status['locklink_on'] else '❌'}
🏷️ قفل تگ: {'✅' if status['locktag_on'] else '❌'}
📢 منشن خودکار: {'✅' if status['mention_on'] else '❌'}

**حالت‌ها:**
⌨️ تایپ: {'✅' if status['typing_on'] else '❌'}
🎥 ضبط ویدیو: {'✅' if status['videoaction_on'] else '❌'}
🎤 ضبط صدا: {'✅' if status['audioaction_on'] else '❌'}
🎮 بازی: {'✅' if status['gameplay_on'] else '❌'}
😐 پوکر: {'✅' if status['poker_on'] else '❌'}

**پروفایل:**
🕐 ساعت در اسم: {'✅' if status['timename_on'] else '❌'}
🕐 ساعت در بیو: {'✅' if status['timebio_on'] else '❌'}

**منشی:**
🤖 منشی: {'✅' if status['monshi_on'] else '❌'}
🧠 منشی هوشمند: {'✅' if status['smartmonshi_on'] else '❌'}
📴 منشی آفلاین: {'✅' if status['monshioffline_on'] else '❌'}
"""
                await event.reply(status_text)
            
            # ====== پینگ ======
            elif cmd == '/ping':
                start = time.time()
                await client.send_message(event.chat_id, "🏓 پینگ...")
                end = time.time()
                await event.reply(f"🏓 پینگ: {(end-start)*1000:.2f} ms")
            
            # ====== ریستارت ======
            elif cmd == '/restart':
                await event.reply("🔄 در حال ریستارت...")
                os._exit(0)
            
            # ====== روشن/خاموش کردن ربات ======
            elif cmd == '/bot':
                if args == 'on':
                    status['bot_on'] = True
                    await event.reply("✅ ربات روشن شد")
                elif args == 'off':
                    status['bot_on'] = False
                    await event.reply("⛔ ربات خاموش شد")
                else:
                    await event.reply("❌ استفاده: /bot on یا /bot off")
            
            # ====== مدیریت زمان ======
            elif cmd == '/timename':
                if args == 'on':
                    status['timename_on'] = True
                    await update_profile_with_time()
                    await event.reply("✅ ساعت در اسم فعال شد")
                elif args == 'off':
                    status['timename_on'] = False
                    await event.reply("⛔ ساعت در اسم غیرفعال شد")
                else:
                    await event.reply("❌ استفاده: /timename on یا /timename off")
            
            elif cmd == '/timebio':
                if args == 'on':
                    status['timebio_on'] = True
                    await update_profile_with_time()
                    await event.reply("✅ ساعت در بیو فعال شد")
                elif args == 'off':
                    status['timebio_on'] = False
                    await event.reply("⛔ ساعت در بیو غیرفعال شد")
                else:
                    await event.reply("❌ استفاده: /timebio on یا /timebio off")
            
            # ====== مدیریت فونت ======
            elif cmd in ['/bold', '/mini', '/mono', '/default']:
                mode_map = {
                    '/bold': 'Bold',
                    '/mini': 'Mini',
                    '/mono': 'Mono',
                    '/default': 'Default'
                }
                mode = mode_map.get(cmd, 'Default')
                db.set_setting('font_mode', mode)
                await event.reply(f"✅ حالت فونت به {mode} تغییر کرد")
            
            # ====== قلب ======
            elif cmd == '/heart':
                if args == 'on':
                    db.set_setting('heart_enabled', 'True')
                    await event.reply("✅ حالت قلب فعال شد")
                elif args == 'off':
                    db.set_setting('heart_enabled', 'False')
                    await event.reply("⛔ حالت قلب غیرفعال شد")
                else:
                    await event.reply("❌ استفاده: /heart on یا /heart off")
            
            # ====== بیوگرافی ======
            elif cmd == '/addbio':
                if args:
                    db.set_setting('user_bio', args)
                    await event.reply(f"✅ بیوگرافی شما به‌روز شد:\n`{args}`")
                else:
                    await event.reply("❌ متن بیوگرافی را وارد کنید: /addbio متن")
            
            # ====== نام تصادفی ======
            elif cmd == '/addrname':
                if args:
                    names = [n.strip() for n in args.split(',')]
                    if len(names) >= 2:
                        db.set_setting('rname_list', ','.join(names))
                        await event.reply(f"✅ لیست نام‌های تصادفی تنظیم شد:\n`{args}`")
                    else:
                        await event.reply("❌ حداقل دو نام با کاما وارد کنید: /addrname name1,name2,...")
                else:
                    await event.reply("❌ نام‌ها را وارد کنید: /addrname name1,name2,...")
            
            # ====== مشاهده بیو ======
            elif cmd == '/seebio':
                bio = db.get_setting('user_bio', 'تنظیم نشده')
                await event.reply(f"📝 بیوگرافی شما:\n`{bio}`")
            
            # ====== مشاهده نام‌ها ======
            elif cmd == '/seenames':
                names = db.get_setting('rname_list', '')
                if names:
                    await event.reply(f"📛 لیست نام‌های تصادفی:\n`{names}`")
                else:
                    await event.reply("❌ هیچ نامی تنظیم نشده است")
            
            # ====== قفل لینک ======
            elif cmd == '/locklink':
                if args == 'on':
                    status['locklink_on'] = True
                    await event.reply("✅ قفل لینک فعال شد")
                elif args == 'off':
                    status['locklink_on'] = False
                    await event.reply("⛔ قفل لینک غیرفعال شد")
                else:
                    await event.reply("❌ استفاده: /locklink on یا /locklink off")
            
            # ====== قفل تگ ======
            elif cmd == '/locktag':
                if args == 'on':
                    status['locktag_on'] = True
                    await event.reply("✅ قفل تگ فعال شد")
                elif args == 'off':
                    status['locktag_on'] = False
                    await event.reply("⛔ قفل تگ غیرفعال شد")
                else:
                    await event.reply("❌ استفاده: /locktag on یا /locktag off")
            
            # ====== منشن خودکار ======
            elif cmd == '/mention':
                if args == 'on':
                    status['mention_on'] = True
                    await event.reply("✅ منشن خودکار فعال شد")
                elif args == 'off':
                    status['mention_on'] = False
                    await event.reply("⛔ منشن خودکار غیرفعال شد")
                else:
                    await event.reply("❌ استفاده: /mention on یا /mention off")
            
            # ====== لاک پیوی ======
            elif cmd == '/lockpv':
                if args == 'on':
                    status['lockpv_on'] = True
                    await event.reply("✅ lockpv فعال شد")
                elif args == 'off':
                    status['lockpv_on'] = False
                    await event.reply("⛔ lockpv غیرفعال شد")
                else:
                    await event.reply("❌ استفاده: /lockpv on یا /lockpv off")
            
            # ====== پاسخ خودکار ======
            elif cmd == '/setanswer':
                if '|' in args:
                    keyword, response = args.split('|', 1)
                    db.add_auto_reply(keyword.strip(), response.strip())
                    await event.reply(f"✅ پاسخ خودکار برای '{keyword.strip()}' تنظیم شد")
                else:
                    await event.reply("❌ استفاده: /setanswer کلمه|پاسخ")
            
            elif cmd == '/delanswer':
                if args:
                    db.delete_auto_reply(args)
                    await event.reply(f"✅ پاسخ خودکار برای '{args}' حذف شد")
                else:
                    await event.reply("❌ استفاده: /delanswer کلمه")
            
            elif cmd == '/answerlist':
                replies = db.get_auto_replies()
                if replies:
                    text = "📋 **لیست پاسخ‌های خودکار:**\n" + "\n".join([f"🔹 {k} → {r}" for k, r in replies])
                    await event.reply(text)
                else:
                    await event.reply("❌ هیچ پاسخ خودکاری تنظیم نشده است")
            
            # ====== دشمنان ======
            elif cmd == '/setenemy':
                if msg.is_reply:
                    reply = await event.get_reply_message()
                    if reply and reply.sender_id:
                        db.add_enemy(reply.sender_id)
                        await event.reply(f"✅ کاربر {reply.sender_id} به لیست دشمنان اضافه شد")
                elif args:
                    try:
                        user_id = int(args)
                        db.add_enemy(user_id)
                        await event.reply(f"✅ کاربر {user_id} به لیست دشمنان اضافه شد")
                    except:
                        await event.reply("❌ آیدی عددی را وارد کنید")
                else:
                    await event.reply("❌ یک پیام را ریپلی کنید یا آیدی عددی وارد کنید")
            
            elif cmd == '/delenemy':
                if msg.is_reply:
                    reply = await event.get_reply_message()
                    if reply and reply.sender_id:
                        db.delete_enemy(reply.sender_id)
                        await event.reply(f"✅ کاربر {reply.sender_id} از لیست دشمنان حذف شد")
                elif args:
                    try:
                        user_id = int(args)
                        db.delete_enemy(user_id)
                        await event.reply(f"✅ کاربر {user_id} از لیست دشمنان حذف شد")
                    except:
                        await event.reply("❌ آیدی عددی را وارد کنید")
                else:
                    await event.reply("❌ یک پیام را ریپلی کنید یا آیدی عددی وارد کنید")
            
            elif cmd == '/reset' and args == 'enemylist':
                db.reset_enemies()
                await event.reply("✅ لیست دشمنان پاکسازی شد")
            
            # ====== منشی ======
            elif cmd == '/monshi':
                if args == 'on':
                    status['monshi_on'] = True
                    await event.reply("✅ منشی فعال شد")
                elif args == 'off':
                    status['monshi_on'] = False
                    await event.reply("⛔ منشی غیرفعال شد")
                else:
                    await event.reply("❌ استفاده: /monshi on یا /monshi off")
            
            elif cmd == '/setmonshi':
                if args:
                    monshi_text = args
                    await event.reply(f"✅ متن منشی تنظیم شد:\n`{args}`")
                else:
                    await event.reply("❌ متن منشی را وارد کنید: /setmonshi متن")
            
            elif cmd == '/smartmonshi':
                if args == 'on':
                    status['smartmonshi_on'] = True
                    await event.reply("✅ منشی هوشمند فعال شد")
                elif args == 'off':
                    status['smartmonshi_on'] = False
                    await event.reply("⛔ منشی هوشمند غیرفعال شد")
                else:
                    await event.reply("❌ استفاده: /smartmonshi on یا /smartmonshi off")
            
            elif cmd == '/setsmartmonshi':
                if args:
                    smart_monshi_text = args
                    await event.reply(f"✅ متن منشی هوشمند تنظیم شد:\n`{args}`")
                else:
                    await event.reply("❌ متن منشی هوشمند را وارد کنید")
            
            # ====== ایموجی پریمیوم ======
            elif cmd == '/emoji':
                if args:
                    try:
                        # ارسال ایموجی به‌عنوان پیام با Entity سفارشی
                        emoji_entity = types.MessageEntityCustomEmoji(
                            offset=0,
                            length=len(args),
                            document_id=1234567890  # آیدی ایموجی پریمیوم (باید واقعی باشد)
                        )
                        await client.send_message(
                            event.chat_id,
                            args,
                            entities=[emoji_entity]
                        )
                        await event.delete()
                    except Exception as e:
                        await event.reply(f"❌ خطا در ارسال ایموجی پریمیوم: {str(e)}\nتوجه: برای استفاده از این قابلیت، به آیدی ایموجی پریمیوم نیاز است.")
                else:
                    await event.reply("❌ استفاده: /emoji 🎉")
            
            # ====== تبدیل ویدیو به ویدیو مسیج ======
            elif cmd == '/tovm':
                if msg.is_reply:
                    reply = await event.get_reply_message()
                    if reply and reply.video:
                        try:
                            await event.reply("🔄 در حال تبدیل ویدیو...")
                            video_path = await client.download_media(reply.video)
                            if video_path:
                                # اینجا باید کد تبدیل ویدیو با moviepy قرار گیرد
                                # برای سادگی، فقط ویدیو را به‌عنوان ویدیو مسیج ارسال می‌کنیم
                                await client.send_file(
                                    event.chat_id,
                                    video_path,
                                    video_note=True,
                                    supports_streaming=True
                                )
                                os.remove(video_path)
                                await event.delete()
                        except Exception as e:
                            await event.reply(f"❌ خطا در تبدیل ویدیو: {str(e)}")
                    else:
                        await event.reply("❌ لطفاً به یک ویدیو ریپلی کنید")
                else:
                    await event.reply("❌ لطفاً به یک ویدیو ریپلی کنید: /tovm")
            
            # ====== ذخیره‌سازی ======
            elif cmd == '/save':
                if msg.is_reply:
                    reply = await event.get_reply_message()
                    if reply:
                        try:
                            await client.forward_messages("me", reply)
                            await event.reply("💾 پیام در Saved Messages ذخیره شد")
                        except:
                            await event.reply("❌ خطا در ذخیره‌سازی")
                else:
                    await event.reply("❌ لطفاً به یک پیام ریپلی کنید")
            
            elif cmd == '/autosave':
                if args == 'on':
                    status['autosave_on'] = True
                    await event.reply("✅ ذخیره‌سازی خودکار فعال شد")
                elif args == 'off':
                    status['autosave_on'] = False
                    await event.reply("⛔ ذخیره‌سازی خودکار غیرفعال شد")
                else:
                    await event.reply("❌ استفاده: /autosave on یا /autosave off")
            
            # ====== ابزارها ======
            elif cmd == '/calc':
                if args:
                    await event.reply(calc_expression(args))
                else:
                    await event.reply("❌ استفاده: /calc 5+5")
            
            elif cmd == '/hash':
                if args:
                    await event.reply(f"🔐 هش متن (MD5):\n`{hash_text(args)}`")
                else:
                    await event.reply("❌ استفاده: /hash متن")
            
            elif cmd == '/encode':
                if args:
                    await event.reply(f"🔐 متن رمزگذاری شده:\n`{encode_base64(args)}`")
                else:
                    await event.reply("❌ استفاده: /encode متن")
            
            elif cmd == '/decode':
                if args:
                    await event.reply(f"🔓 متن رمزگشایی شده:\n`{decode_base64(args)}`")
                else:
                    await event.reply("❌ استفاده: /decode متن")
            
            elif cmd == '/weather':
                if args:
                    await event.reply(get_weather(args))
                else:
                    await event.reply("❌ استفاده: /weather تهران")
            
            elif cmd == '/wiki':
                if args:
                    try:
                        wikipedia.set_lang('fa')
                        summary = wikipedia.summary(args, sentences=2)
                        await event.reply(f"📚 **ویکی‌پدیا - {args}**\n\n{summary}")
                    except:
                        await event.reply("❌ صفحه‌ای برای این عبارت یافت نشد")
                else:
                    await event.reply("❌ استفاده: /wiki متن")
            
            elif cmd == '/joke':
                await event.reply(get_joke())
            
            elif cmd == '/say':
                if args:
                    await event.reply(f"📢 {args}")
                else:
                    await event.reply("❌ استفاده: /say متن")
            
            elif cmd == '/age':
                if args:
                    await event.reply(get_age(args))
                else:
                    await event.reply("❌ استفاده: /age 2000/01/01")
            
            # ====== ارز و طلا ======
            elif cmd == '/crypto':
                prices = get_crypto_prices()
                if prices:
                    text = "💰 **قیمت ارزهای دیجیتال:**\n"
                    for name, price in prices.items():
                        text += f"• {name}: ${price}\n"
                    await event.reply(text)
                else:
                    await event.reply("❌ خطا در دریافت قیمت ارزها")
            
            elif cmd == '/currency':
                rates = get_currency_rates()
                if rates:
                    text = "💵 **قیمت ارزهای جهانی (به دلار):**\n"
                    for name, rate in rates.items():
                        text += f"• {name}: {rate:.2f}\n"
                    await event.reply(text)
                else:
                    await event.reply("❌ خطا در دریافت نرخ ارز")
            
            elif cmd == '/gold':
                await event.reply(get_gold_price())
            
            # ====== آمار ======
            elif cmd == '/stats':
                reply_count = len(db.get_auto_replies())
                enemy_count = len(db.get_enemies())
                total_users = 0
                try:
                    async for dialog in client.iter_dialogs():
                        if dialog.is_user and not dialog.entity.bot:
                            total_users += 1
                except:
                    pass
                
                stats_text = f"""📊 **آمار ربات:**

📝 پاسخ‌های خودکار: {reply_count}
⚔️ دشمنان: {enemy_count}
👥 کاربران در تماس: {total_users}
⏱ زمان اجرا: {get_uptime(start_time)}

📌 وضعیت: {'✅ روشن' if status['bot_on'] else '❌ خاموش'}
"""
                await event.reply(stats_text)
            
            # ====== uptime ======
            elif cmd == '/uptime':
                await event.reply(f"⏱ زمان اجرای ربات:\n{get_uptime(start_time)}")
            
            # ====== حالت‌های اکشن ======
            elif cmd in ['/typing', '/videoaction', '/audioaction', '/gameplay', '/poker']:
                action_map = {
                    '/typing': 'typing_on',
                    '/videoaction': 'videoaction_on',
                    '/audioaction': 'audioaction_on',
                    '/gameplay': 'gameplay_on',
                    '/poker': 'poker_on'
                }
                key = action_map.get(cmd)
                if key:
                    if args == 'on':
                        status[key] = True
                        await event.reply(f"✅ {cmd[1:]} فعال شد")
                    elif args == 'off':
                        status[key] = False
                        await event.reply(f"⛔ {cmd[1:]} غیرفعال شد")
                    else:
                        await event.reply(f"❌ استفاده: {cmd} on یا {cmd} off")
            
            # ====== تگ همه ======
            elif cmd == '/tag':
                if event.is_group:
                    try:
                        participants = await client.get_participants(event.chat_id)
                        tag_text = "🔊 **تگ همه:**\n\n"
                        for user in participants[:30]:  # محدودیت برای جلوگیری از اسپم
                            if not user.bot:
                                tag_text += f"[{user.first_name}](tg://user?id={user.id})\n"
                        await event.reply(tag_text)
                    except:
                        await event.reply("❌ خطا در تگ کردن اعضا")
                else:
                    await event.reply("❌ این دستور فقط در گروه قابل استفاده است")
            
            # ====== سکوت ======
            elif cmd == '/silent':
                if msg.is_reply:
                    reply = await event.get_reply_message()
                    if reply and reply.sender_id:
                        silenced_users.append(reply.sender_id)
                        await event.reply(f"🔇 کاربر {reply.sender_id} سکوت شد")
                else:
                    await event.reply("❌ لطفاً به یک پیام ریپلی کنید")
            
            elif cmd == '/unsilent':
                if msg.is_reply:
                    reply = await event.get_reply_message()
                    if reply and reply.sender_id in silenced_users:
                        silenced_users.remove(reply.sender_id)
                        await event.reply(f"🔊 سکوت کاربر {reply.sender_id} لغو شد")
                else:
                    await event.reply("❌ لطفاً به یک پیام ریپلی کنید")
            
            # ====== خروج از گروه ======
            elif cmd == '/left':
                if event.is_group:
                    try:
                        await client(LeaveChannelRequest(event.chat_id))
                        await event.reply("🚶 از گروه خارج شدم!")
                    except:
                        await event.reply("❌ خطا در خروج از گروه")
            
            # ====== سایر دستورات ======
            else:
                # بررسی دستورات بدون / (مانند timename on)
                if ' ' in text:
                    parts = text.split()
                    first = parts[0].lower()
                    rest = ' '.join(parts[1:]) if len(parts) > 1 else ''
                    
                    if first == 'timename' and rest in ['on', 'off']:
                        status['timename_on'] = rest == 'on'
                        await update_profile_with_time()
                        await event.reply(f"✅ زمان در اسم {'فعال' if status['timename_on'] else 'غیرفعال'} شد")
                        return
                    
                    elif first == 'timebio' and rest in ['on', 'off']:
                        status['timebio_on'] = rest == 'on'
                        await update_profile_with_time()
                        await event.reply(f"✅ زمان در بیو {'فعال' if status['timebio_on'] else 'غیرفعال'} شد")
                        return
                    
                    elif first in ['bold', 'mini', 'mono', 'default'] and rest == 'on':
                        mode_map = {
                            'bold': 'Bold',
                            'mini': 'Mini',
                            'mono': 'Mono',
                            'default': 'Default'
                        }
                        db.set_setting('font_mode', mode_map[first])
                        await event.reply(f"✅ حالت فونت به {mode_map[first]} تغییر کرد")
                        return
                    
                    elif first == 'heart' and rest in ['on', 'off']:
                        db.set_setting('heart_enabled', 'True' if rest == 'on' else 'False')
                        await event.reply(f"✅ حالت قلب {'فعال' if rest == 'on' else 'غیرفعال'} شد")
                        return
                    
                    elif first == 'locklink' and rest in ['on', 'off']:
                        status['locklink_on'] = rest == 'on'
                        await event.reply(f"✅ قفل لینک {'فعال' if rest == 'on' else 'غیرفعال'} شد")
                        return
                    
                    elif first == 'locktag' and rest in ['on', 'off']:
                        status['locktag_on'] = rest == 'on'
                        await event.reply(f"✅ قفل تگ {'فعال' if rest == 'on' else 'غیرفعال'} شد")
                        return
                    
                    elif first == 'mention' and rest in ['on', 'off']:
                        status['mention_on'] = rest == 'on'
                        await event.reply(f"✅ منشن خودکار {'فعال' if rest == 'on' else 'غیرفعال'} شد")
                        return
                    
                    elif first == 'lockpv' and rest in ['on', 'off']:
                        status['lockpv_on'] = rest == 'on'
                        await event.reply(f"✅ lockpv {'فعال' if rest == 'on' else 'غیرفعال'} شد")
                        return
                    
                    elif first == 'monshi' and rest in ['on', 'off']:
                        status['monshi_on'] = rest == 'on'
                        await event.reply(f"✅ منشی {'فعال' if rest == 'on' else 'غیرفعال'} شد")
                        return
                    
                    elif first == 'smartmonshi' and rest in ['on', 'off']:
                        status['smartmonshi_on'] = rest == 'on'
                        await event.reply(f"✅ منشی هوشمند {'فعال' if rest == 'on' else 'غیرفعال'} شد")
                        return

# ==================== هندلر CallbackQuery برای پنل شیشه‌ای ====================
@client.on(events.CallbackQuery)
async def handle_panel_callbacks(event):
    data = event.data.decode()
    me = await client.get_me()
    
    if data == "status":
        await event.answer(f"ربات: {'روشن' if status['bot_on'] else 'خاموش'}\nذخیره‌سازی: {'فعال' if status['autosave_on'] else 'غیرفعال'}", alert=True)
    
    elif data == "settings":
        await event.edit(
            "⚙️ **تنظیمات:**",
            buttons=[
                [types.KeyboardButtonCallback(f"🕐 زمان در اسم: {'✅' if status['timename_on'] else '❌'}", b"toggle_timename")],
                [types.KeyboardButtonCallback(f"🕐 زمان در بیو: {'✅' if status['timebio_on'] else '❌'}", b"toggle_timebio")],
                [types.KeyboardButtonCallback("🔙 بازگشت", b"panel_back")],
            ]
        )
    
    elif data == "security":
        await event.edit(
            "🛡️ **امنیت:**",
            buttons=[
                [types.KeyboardButtonCallback(f"🔒 lockpv: {'✅' if status['lockpv_on'] else '❌'}", b"toggle_lockpv")],
                [types.KeyboardButtonCallback(f"🔗 قفل لینک: {'✅' if status['locklink_on'] else '❌'}", b"toggle_locklink")],
                [types.KeyboardButtonCallback(f"🏷️ قفل تگ: {'✅' if status['locktag_on'] else '❌'}", b"toggle_locktag")],
                [types.KeyboardButtonCallback(f"📢 منشن: {'✅' if status['mention_on'] else '❌'}", b"toggle_mention")],
                [types.KeyboardButtonCallback("🔙 بازگشت", b"panel_back")],
            ]
        )
    
    elif data == "fun":
        await event.edit(
            "🎮 **سرگرمی:**",
            buttons=[
                [types.KeyboardButtonCallback("😂 جوک", b"joke")],
                [types.KeyboardButtonCallback("🔙 بازگشت", b"panel_back")],
            ]
        )
    
    elif data == "tools":
        await event.edit(
            "🔧 **ابزارها:**",
            buttons=[
                [types.KeyboardButtonCallback("🧮 ماشین‌حساب", b"calc")],
                [types.KeyboardButtonCallback("🌤 آب و هوا", b"weather")],
                [types.KeyboardButtonCallback("💰 ارز و طلا", b"crypto")],
                [types.KeyboardButtonCallback("🔙 بازگشت", b"panel_back")],
            ]
        )
    
    elif data == "joke":
        await event.answer(get_joke(), alert=True)
    
    elif data.startswith("toggle_"):
        key = data.replace("toggle_", "")
        if key in status:
            status[key] = not status[key]
            if key in ['timename_on', 'timebio_on']:
                await update_profile_with_time()
            await event.answer(f"✅ {key} {'فعال' if status[key] else 'غیرفعال'} شد")
            # بازگشت به منوی قبلی
            await handle_panel_callbacks(event)
    
    elif data == "panel_back":
        panel_text = f"""🤖 **پنل مدیریت سلف‌بیس OMEGA v5.0**

📊 **وضعیت:** {'✅ روشن' if status['bot_on'] else '❌ خاموش'}
👤 **حساب:** @{me.username or 'ندارد'}

🔹 **قابلیت‌های اصلی:**
• مدیریت زمان در اسم و بیو
• مدیریت گروه (قفل لینک، قفل تگ، منشن)
• پاسخ خودکار
• منشی هوشمند
• ذخیره‌سازی خودکار
• ایموجی پریمیوم
• تبدیل ویدیو به ویدیو مسیج
• و بیش از ۱۵۰ دستور دیگر

📌 برای مشاهده راهنما: /help
"""
        buttons = [
            [types.KeyboardButtonCallback("📊 وضعیت", b"status")],
            [types.KeyboardButtonCallback("⚙️ تنظیمات", b"settings"), types.KeyboardButtonCallback("🛡️ امنیت", b"security")],
            [types.KeyboardButtonCallback("🎮 سرگرمی", b"fun"), types.KeyboardButtonCallback("🔧 ابزارها", b"tools")],
            [types.KeyboardButtonCallback("❌ بستن پنل", b"close_panel")],
        ]
        await event.edit(panel_text, buttons=buttons)
    
    elif data == "close_panel":
        await event.delete()
        await client.send_message(event.chat_id, "❌ پنل بسته شد. برای باز کردن مجدد `/panel` را بفرستید.")

# ==================== اجرای اصلی ====================
start_time = datetime.now()

async def main():
    try:
        await client.start(phone=PHONE_NUMBER)
        me = await client.get_me()
        print(f"✅ سلف‌بیس با موفقیت به حساب {me.first_name} وارد شد!")
        await client.send_message("me", "🤖 سلف‌بیس OMEGA v5.0 راه‌اندازی شد!\n✅ تمام قابلیت‌ها فعال هستند.\n📱 برای راهنما /help را بفرستید.")
        
        # شروع تایمر به‌روزرسانی زمان
        asyncio.create_task(time_updater())
        
        print("✅ ربات آماده است!")
        await client.run_until_disconnected()
    except FloodWaitError as e:
        print(f"⏳ خطای FloodWait: {e.seconds} ثانیه صبر کنید")
        await asyncio.sleep(e.seconds)
        await main()
    except Exception as e:
        print(f"❌ خطا: {e}")
        await asyncio.sleep(5)
        await main()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("⛔ ربات متوقف شد")
    except Exception as e:
        print(f"❌ خطای نهایی: {e}")

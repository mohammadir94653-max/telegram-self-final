from telethon import Button, types
from lib import *

client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

@client.on(events.InlineQuery)
async def inline_handler(event):
    if event.sender_id == admin_user_id and event.text == "/panel":
        text = f"سلام ادمین عزیز لطفا زبان هلپر را انتخاب کنید"
        buttons = [[Button.inline("فارسی 🇮🇷", b"langfa")]]
        builder = event.builder
        result = builder.article(
            title="هلپر",
            description="راهنما",
            text=text,
            buttons=buttons
        )
        await event.answer([result])
    else:
        pass

@client.on(events.CallbackQuery)
async def callback(event):
    if event.sender_id == admin_user_id and event.data == b"langfa":
        text = f"به راهنما خوش آمدید چطور میتونم کمکتون کنم؟"
        turn_on_button = Button.inline("✵ᴛɪᴍᴇ ɴᴀᴍᴇ ᴏɴ✵", b"turn_on")
        turn_off_button = Button.inline("✵ᴛɪᴍᴇ ɴᴀᴍᴇ ᴏғғ✵", b"turn_off")
        turn_on_pic = Button.inline("✵ᴛɪᴍᴇ ᴘɪᴄ ᴏɴ✵", b"turn_on_pic")
        turn_off_pic = Button.inline("✵ᴛɪᴍᴇ ᴘɪᴄ ᴏғғ✵", b"turn_off_pic")
        turn_on_bio_button = Button.inline("✵ʙɪᴏ ᴏɴ✵", b"turn_on_bio")
        turn_off_bio_button = Button.inline("✵ʙɪᴏ ᴏꜰꜰ✵", b"turn_off_bio")
        bio_button = Button.inline("✵sᴇᴇ ʙɪᴏ✵", b"bio")
        fonts_button = Button.inline("✵ᴄʜᴀɴɢᴇ ғᴏɴᴛ✵", b"fonts")
        help_button = Button.inline("✵ʜᴇʟᴘ✵", b"help")
        next_button = Button.inline("✘ᴄʟᴏsᴇ✘", b"close_panel")

        buttons = [
            [turn_on_button, turn_off_button],
            [turn_on_bio_button, turn_off_pic],
            [turn_on_pic, turn_off_bio_button],
            [bio_button,fonts_button],
            [help_button],
            [next_button]
        ]
        await event.edit(text,buttons=buttons)
    elif event.sender_id == admin_user_id and event.data == b"close_panel":
        close_panel_message = f'✵𝐏𝐚𝐧𝐞𝐥 𝐂𝐥𝐨𝐬𝐞𝐝 𝐁𝐲 [𝐀𝐝𝐦𝐢𝐧](tg://user?id={admin_user_id})'
        await event.edit(close_panel_message)
    elif event.sender_id == admin_user_id and event.data == b"Back":
        text = f"به راهنما خوش آمدید چطور میتونم کمکتون کنم؟"
        turn_on_button = Button.inline("✵ᴛɪᴍᴇ ɴᴀᴍᴇ ᴏɴ✵", b"turn_on")
        turn_off_button = Button.inline("✵ᴛɪᴍᴇ ɴᴀᴍᴇ ᴏғғ✵", b"turn_off")
        turn_on_pic = Button.inline("✵ᴛɪᴍᴇ ᴘɪᴄ ᴏɴ✵", b"turn_on_pic")
        turn_off_pic = Button.inline("✵ᴛɪᴍᴇ ᴘɪᴄ ᴏғғ✵", b"turn_off_pic")
        turn_on_bio_button = Button.inline("✵ʙɪᴏ ᴏɴ✵", b"turn_on_bio")
        turn_off_bio_button = Button.inline("✵ʙɪᴏ ᴏꜰꜰ✵", b"turn_off_bio")
        bio_button = Button.inline("✵sᴇᴇ ʙɪᴏ✵", b"bio")
        fonts_button = Button.inline("✵ᴄʜᴀɴɢᴇ ғᴏɴᴛ✵", b"fonts")
        help_button = Button.inline("✵ʜᴇʟᴘ✵", b"help")
        next_button = Button.inline("✘ᴄʟᴏsᴇ✘", b"close_panel")

        buttons = [
            [turn_on_button, turn_off_button],
            [turn_on_bio_button, turn_off_pic],
            [turn_on_pic, turn_off_bio_button],
            [bio_button,fonts_button],
            [help_button],
            [next_button]
        ]
        await event.edit(text,buttons=buttons)
    elif event.sender_id == admin_user_id and event.data == b"help":
        panel = f'''
        از دستورات زیر استفاده کنید:
        \n`timename` on|off : زمان در اسم روشن|خاموش
        \n`timepic` on|off : زمان در پروفایل روشن|خاموش
        \n`mini` on : فونت مینی روشن
        \n`bio` on|off : بیو روشن|خاموش
        \n`default` on : فونت عادی
        \n`bold` on : فونت بولد
        \n`mono` on : فونت یه مدلی
        \n`heart` on|off : حالت قلب روشن|خاموش 
        \n`rname` on|off :  اسم تصادفی روشن|خاموش
        \n`see rname` : دیدن اسم های تصادفی
        \n`see bio` : دیدن بیو
        \n`/addbio` (time,DATE,heart) [text]: این دستور برای اضافه کردن یک بیوگرافی یا توضیح کوتاه به پروفایل شما می‌تواند استفاده شود، که می‌تواند به دیگران در یادگیری بیشتر درباره شما کمک کند.
        \n`/addlname` (time,heart) [text]: متن تنظیمی برای تایم نیم است و دارای متغییر است که time زمان و heart قلب رندوم قرار میدهد
        \n`/addrname` [name1,name2,...]: برای تنظیم نام رندوم است
        \n`/delrname`: برای حذف نام رندوم است
        \n`see lname` : دیدن متن لست نیم
        \n`/ping` - زمان پاسخ دهی ربات را دریافت کنید.
        \n`/mem` - مصرف حافظه فعلی ربات را دریافت کنید.
        \n`/gmusic` [query] - در SoundCloud برای پیدا کردن یک قطعه موسیقی و دانلود آن جستجو کنید.
        \n`/tarikh` - تاریخ شمسی (ایرانی) فعلی را دریافت کنید.
        \n`/gmsg` [message] - یک پیام را با نمایش هر حرف به تدریج نمایش دهید.
        \n`/weather` [city] - اطلاعات آب و هوای فعلی شهر مورد نظر را دریافت کنید.
        \n/info [@username] - اطلاعاتی درباره کاربری را که آن را مشخص می کنید دریافت کنید.
        \n`/setprof` - عکس پروفایل ربات را (با پاسخ به تصویر) تنظیم کنید.
        \n`/rinfo` - با پاسخ دادن به یکی از پیام های کاربر، اطلاعات درباره کاربر را دریافت کنید.
        '''
        back_button = Button.inline("ʙᴀᴄᴋ ⬸", b"Back")
        help_1 = Button.inline("ᴘᴀɢᴇ Ⅰ", b"help")
        help_2 = Button.inline("ᴘᴀɢᴇ Ⅱ", b"help_1")
        help_3 = Button.inline("ᴘᴀɢᴇ Ⅲ", b"help_2")
        help_4 = Button.inline("ᴘᴀɢᴇ ɪᴠ", b"help_3")
        buttons = [
            [help_1,help_2,help_3,help_4],
            [back_button]
        ]
        await event.edit(panel, buttons=buttons)
    elif event.sender_id == admin_user_id and event.data == b"help_1":
        panel = f'''
        از دستورات زیر استفاده کنید:
        \n`/backupchat`: این دستور می‌تواند برای پشتیبان گیری از تمام تاریخچه گفتگو، از جمله پیام‌ها، تصاویر و سایر محتواها استفاده شود، که می‌تواند برای اهداف بایگانی یا در صورت از دست دادن داده‌ها مفید باشد.
        \n`/create_channel`: این دستور برای ایجاد یک کانال یا چت گروهی جدید در داخل پلتفرم پیام رسانی مورد استفاده قرار می‌گیرد، که می‌تواند برای سازماندهی گفتگوها در مورد موضوعات خاص یا با گروه‌های خاص از افراد مفید باشد.
        \n`/calc`: این دستور برای انجام محاسبات ساده مانند جمع، تفریق، ضرب و تقسیم مستقیماً در رابط گفتگو استفاده می‌شود.
        \n`/silent`:این دستور اگر روی کاربری ریپلی شود کاربر را در لیست سکوت قرار میدهد و اگر در زمان سکوت بیشتر از 5 پیام ارسال کند کاربر را بلاک میکند.
        \n`/unsilent`:برای در اوردن کاربر از حالت /silent.
        \n`/tag`: این دستور برای تگ کردن تمامی افراد گروه میباشد.
        \n`/Del`:اگر روی پیامی ریپلای شود اون پیام را پاک میکند.
        \n`/GSilent`:برای سکوت کردن کاربر در گروه میباشد.
        \n`/GUnSilent`: در اوردن کاربر از حالت سکوت گروه.
        \n`/promote`:ادمین کردن کاربر برای انجام دستورات گروهی.
        \n`/demote`: برای عزل کردن کاربر از حالت ادمین
        \n`/Gmedia`:اگر روی یک ویدیو ریپلی شود ان را در حافظه سلف ذخیره و هر جایی که بخواهید میتوانید ان را ارسال کنید.
        \n`/Ggit` [repo Link] : دانلود ریپازیتوری از گیتهاب
        \n`/copycontent` [post Link] : پست های چنل هایی که فروارد آنها بسته است را سیو میکند
        \n`tpic` (`set` | `prv`) : برای ست کردن و مشاهده کردن تایم پیک است
        \n`/logout` : ربات از حساب شما خارج میشود
        \n`/chkdomain` [domian] : برای برسی در دسترس بودن یا نبودن یک دامنه
        '''
        back_button = Button.inline("ʙᴀᴄᴋ ⬸", b"Back")
        help_1 = Button.inline("ᴘᴀɢᴇ Ⅰ", b"help")
        help_2 = Button.inline("ᴘᴀɢᴇ Ⅱ", b"help_1")
        help_3 = Button.inline("ᴘᴀɢᴇ Ⅲ", b"help_2")
        help_4 = Button.inline("ᴘᴀɢᴇ ɪᴠ", b"help_3")
        buttons = [
            [help_1,help_2,help_3,help_4],
            [back_button]
        ]
        await event.edit(panel, buttons=buttons)
    elif event.sender_id == admin_user_id and event.data == b"help_2":
        panel = f'''
        از دستورات زیر استفاده کنید:
        \n`/Smedia` [Name]:ارسال ویدیو سیو شده در حافظه سلف.
        \n`/Lmedia`:مشاهده ویدیو یا عکس های ذخیره شده در حافظه سلف.
        \n`/Freplay` [add] or [remove]:برای تنظیم کلمه برای پاسخ سریع توسط سلف .
        \n`/Lreplay`: مشاهده لیست کلمات ریپلای سریع.
        \n`/whois` [domain Name]:برای دریافت اطلاعات دامنه.
        \n`/Scrypto`: دریافت قیمت ارز های دیجیتال.
        \n`/sreplace` [key1],[key2]:اگر بر روی متنی ریپلی شود مقدار key1 را با مقدار key2 در متن عوض میکند
        \n`/Convertdate` [miladi date]:تبدیل تاریخ میلادی به شمسی.
        \n`/randnum` [num1]-[num2]:ارسال عدد رندوم بین num1 و num2 .
        \n`/setname` [name]:اسم شما را عوض میکند.
        \n`/sfootball`:نشان دادن وضعیت تیم ها در Bundesliga.
        \n`/setcolor` [green,pink,blue,red,yellow,purple,orange]:رنگ عکس ریپلای شده را به رنگ جلوی دستور تغییر میدهد.
        \n`/flood` [number] - [text1,text2,...]:به صورت رندوم به تعداد مشخص شده از بین کلمات تعیین شده پیام میفرستد.
        \n`/orcen` [ENtext] : متن را تبدیل به ویس میکند و میفرستد.
        \n`/setfname` [name] : اگر روی یک موزیک ریپلای شود نام اون رو به نام جلوی دستور تغییر میدهد
        \n`/screen` [domain] : از سایت مورد نظر اسکریین شات میگیرد.
        \n`/yt` [YT Video Link] : ویدیو یوتیوب مورد نظر را دانلود میکند و میفرستد .
        \n`/Sproxy`:دریافت پروکسی رایگان.
        \n`/Sv2ray`:دریافت سرور v2ray رایگان.
        '''
        back_button = Button.inline("ʙᴀᴄᴋ ⬸", b"Back")
        help_1 = Button.inline("ᴘᴀɢᴇ Ⅰ", b"help")
        help_2 = Button.inline("ᴘᴀɢᴇ Ⅱ", b"help_1")
        help_3 = Button.inline("ᴘᴀɢᴇ Ⅲ", b"help_2")
        help_4 = Button.inline("ᴘᴀɢᴇ ɪᴠ", b"help_3")
        buttons = [
            [help_1,help_2,help_3,help_4],
            [back_button]
        ]
        await event.edit(panel, buttons=buttons)
    elif event.sender_id == admin_user_id and event.data == b"help_3":
        panel = f'''
        از دستورات زیر استفاده کنید:
        \n`/time` [capital of country]: با قرار دادن پایتخت یک کشور زمان آن را به شما نشان می دهد
        \n`newtimer` [name]: یک تایمر با نام دلخواه برای شما ایجاد میکند
        \n`deltimer` [name]: تایمر مورد نظر را پاک می کند
        \n`timers` : تایمر ها را نمایش میدهد
        \n`clean timers` : تایمر ها را پاک میکند
        \n`gfile` [link] : با قرار دادن لینک جلو دستور آن را دانلود میکند
        \n`getip` [ip] : اطلاعات ip را میدهد
        \n`/sunextract`یا `/استخراج فایل` : اگر روی یک فایل زیپ ریپلای شود آن را اکسترکت میکند
        \n`Stv` : لینک پخش آنلاین تلویزیون
        \n`sqr` یا `به qr` : تبدیل به qrcode
        \n`readqr` یا `خواندن qr` : qrcode میخونه
        \n`cleanall` یا `پاکسازی همه` [txt] : پیام مورد نظر را در گروه پاک میکند 
        \n`setusername` [txt] : نام کاربری تنظیم میکند
        \n`kick` [usernames] or [numerical user IDs] : یوزر مورد نظر از گروه کیک میکنه
        \n`cleanb` [link 1] [link 2] : پیام های بین دو لینک پاک میکنه
        \n`/rem` [num] - حذف پیام‌های اخیر در گروه تا تعداد مشخص شده.
        \n`/sgoogle` [query] - جستجوی کوتاهی در گوگل برای پیدا کردن پاسخ به سوال شما.
        \n`/wiki` [query] - جستجوی کوتاهی در ویکی‌پدیای فارسی برای پیدا کردن پاسخ به سوال شما.
        \n`/save`: این دستور می‌تواند برای ذخیره یک گفتگو یا لاگ چت به یک فایل استفاده شود، که می‌تواند برای نگهداری یک رکورد از بحث‌های مهم یا به اشتراک گذاری با دیگران مفید باشد.
        \n`/reload`: این دستور برای بازنشانی رابط گفتگو یا کد ربات استفاده می‌شود، که می‌تواند در صورت وجود هرگونه خطا یا خللی که باید حل شود مفید باشد.
        \n`ReadAll`(Pvs-Gps-Channels-Bots): با توجه به مقداری که جلوش هست پیام های اونجا سین میکنه
        \n`Del`(Videos-Photos-Voices-Files-Notes-Gifs): متغییر رو به روشو در اون چت همه شو پاک میکنه
        \n`typing` [on|off]: اگه در پیوی کسی بفرستی برای اون شخص حالت تایپینگ میگیری
        \n`Pvinfo`: اطلاعات اون چت میده
        '''
        back_button = Button.inline("ʙᴀᴄᴋ ⬸", b"Back")
        help_1 = Button.inline("ᴘᴀɢᴇ Ⅰ", b"help")
        help_2 = Button.inline("ᴘᴀɢᴇ Ⅱ", b"help_1")
        help_3 = Button.inline("ᴘᴀɢᴇ Ⅲ", b"help_2")
        help_4 = Button.inline("ᴘᴀɢᴇ ɪᴠ", b"help_3")
        buttons = [
            [help_1,help_2,help_3,help_4],
            [back_button]
        ]
        await event.edit(panel, buttons=buttons)
    elif event.sender_id == admin_user_id and event.data == b"turn_on":
        with open('settings/time.txt', 'w') as f:
            f.write('True')
        back_button = Button.inline("ʙᴀᴄᴋ ⬸", b"Back")
        buttons = [[back_button]]
        text = f"**❈Time Name [Activated](tg://user?id={admin_user_id})!**"
        await event.edit(text, buttons=buttons)
    elif event.sender_id == admin_user_id and event.data == b"turn_off":
        with open('settings/time.txt', 'w') as f:
            f.write('False')
        back_button = Button.inline("ʙᴀᴄᴋ ⬸", b"Back")
        buttons = [[back_button]]
        text = f"**❈Time Name [DeActivated](tg://user?id={admin_user_id})!**"
        await event.edit(text, buttons=buttons)
    elif event.sender_id == admin_user_id and event.data == b"turn_on_pic":
        with open('settings/timepic.txt', 'w') as f:
            f.write('True')
        back_button = Button.inline("ʙᴀᴄᴋ ⬸", b"Back")
        buttons = [[back_button]]
        text = f"**❈Time Pic [Activated](tg://user?id={admin_user_id})!**"
        await event.edit(text, buttons=buttons)
    elif event.sender_id == admin_user_id and event.data == b"turn_off_pic":
        with open('settings/timepic.txt', 'w') as f:
            f.write('False')
        back_button = Button.inline("ʙᴀᴄᴋ ⬸", b"Back")
        buttons = [[back_button]]
        text = f"**❈Time Pic [DeActivated](tg://user?id={admin_user_id})!**"
        await event.edit(text, buttons=buttons)
    elif event.sender_id == admin_user_id and event.data == b"turn_on_bio":
        with open('settings/bioinfo.txt', 'w') as f:
            f.write('True')
        back_button = Button.inline("ʙᴀᴄᴋ ⬸", b"Back")
        buttons = [[back_button]]
        text = f"**❈Bio Activated!**"
        await event.edit(text, buttons=buttons)
    elif event.sender_id == admin_user_id and event.data == b"turn_off_bio":
        with open('settings/bioinfo.txt', 'w') as f:
            f.write('False')
        back_button = Button.inline("ʙᴀᴄᴋ ⬸", b"Back")
        buttons = [[back_button]]
        text = f"**❈Bio DeActivated!**"
        await event.edit(text, buttons=buttons)
    elif event.sender_id == admin_user_id and event.data == b"bio":
        with open('settings/bio.txt', 'r') as f:
                bio = f.read()
        back_button = Button.inline("ʙᴀᴄᴋ ⬸", b"Back")
        buttons = [[back_button]]
        text = f"**❈Your Bio : \n{bio}**"
        await event.edit(text, buttons=buttons)
    elif event.sender_id == admin_user_id and event.data == b"fonts":
        with open('settings/mode.txt', 'r') as f:
            mode = f.read().strip()
        default_font_button = Button.inline("✵ᴅᴇғᴀᴜʟᴛ✵", b"default_font")
        Mono_font_button = Button.inline("✵ᴍᴏɴᴏ✵", b"Mono_font")
        bold_font_button = Button.inline("✵ʙᴏʟᴅ✵", b"bold_font")
        preview_button = Button.inline("✵ʟɪᴠᴇ ᴘʀᴇᴠɪᴇᴡ✵", b"time_page_panel")
        if mode == "Default":
            default_font_button = Button.inline("✅ ᴅᴇғᴀᴜʟᴛ", b"default_font")
        if mode == "Mono":
            Mono_font_button = Button.inline("✅ ᴍᴏɴᴏ", b"Mono_font")
        elif mode == "Bold":
            bold_font_button = Button.inline("✅ ʙᴏʟᴅ", b"bold_font")
        elif mode == "Mini":
            Mini_font_button = Button.inline("✅ ᴍɪɴɪ", b"Mini_font")
        back_button = Button.inline("ʙᴀᴄᴋ ⬸", b"Back")
        buttons = [[default_font_button], [Mono_font_button], [bold_font_button], [Mini_font_button], [preview_button], [back_button]]
        font_message = "Select a font option:\n\nNote⚠: To see the preview of available fonts, refer to the second page or select the Live Preview Button"
        await event.edit(font_message, buttons=buttons)
    elif event.sender_id == admin_user_id and event.data == b"time_page_panel":
        message = f'This Fonts Are Available Now:\nNote:To choose, you can click on the change font button from the main menu or click on one of the fonts below'
        current_time = datetime.datetime.now().strftime("%H:%M")
        current_bold_time = current_time.replace("0", "𝟎").replace("1", "𝟏").replace("2", "𝟐").replace("3", "𝟑").replace("4", "𝟒").replace("5", "𝟓").replace("6", "𝟔").replace("7", "𝟕").replace("8", "𝟖").replace("9", "𝟗")
        current_mode_time = current_time.replace("0", "０").replace("1", "１").replace("2", "２").replace("3", "３").replace("4", "４").replace("5", "５").replace("6", "６").replace("7", "７").replace("8", "８").replace("9", "９")
        current_mini_time = current_time.replace("0", "⁰").replace("1", "¹").replace("2", "²").replace("3", "³").replace("4", "⁴").replace("5", "⁵").replace("6", "⁶").replace("7", "⁷").replace("8", "⁸").replace("9", "⁹")
        time_button = Button.inline(text=f"Default: {current_time}", data='fonts')
        time_bold_button = Button.inline(text=f"Bold: {current_bold_time}", data='fonts')
        time_mode_button = Button.inline(text=f"Mono: {current_mode_time}", data='fonts')
        time_mini_button = Button.inline(text=f"Mini: {current_mini_time}", data='fonts')
        await event.edit(message, buttons=[[time_button, time_bold_button],[time_mode_button,time_mini_button],[Button.inline("Back ⬸", b"Back")]])
    elif event.sender_id == admin_user_id and event.data == b"default_font":
        with open('settings/mode.txt', 'w') as f:
            f.write('Default')
        Default_message = "Font Mode Change To Default"
        bold_font_button = Button.inline("✵ʙᴏʟᴅ✵", b"bold_font")
        Mono_font_button = Button.inline("✵ᴍᴏɴᴏ✵", b"Mono_font")
        Mini_font_button = Button.inline("✵ᴍɪɴɪ✵", b"Mini_font")
        preview_button = Button.inline("✵ʟɪᴠᴇ ᴘʀᴇᴠɪᴇᴡ✵", b"time_page_panel")
        default_font_button = Button.inline("✅ ᴅᴇғᴀᴜʟᴛ", b"default_font")
        back_button = Button.inline("ʙᴀᴄᴋ ⬸", b"Back")
        buttons = [[default_font_button], [Mono_font_button], [bold_font_button], [Mini_font_button], [preview_button], [back_button]]
        await event.edit(Default_message, buttons=buttons)
    elif event.sender_id == admin_user_id and event.data == b"bold_font":
        with open('settings/mode.txt', 'w') as f:
            f.write('Bold')
        Default_message = "Font Mode Change To Bold"
        bold_font_button = Button.inline("✅ ʙᴏʟᴅ", b"bold_font")
        Mono_font_button = Button.inline("✵ᴍᴏɴᴏ✵", b"Mono_font")
        Mini_font_button = Button.inline("✵ᴍɪɴɪ✵", b"Mini_font")
        preview_button = Button.inline("✵ʟɪᴠᴇ ᴘʀᴇᴠɪᴇᴡ✵", b"time_page_panel")
        default_font_button = Button.inline("✵ᴅᴇғᴀᴜʟᴛ✵", b"default_font")
        back_button = Button.inline("ʙᴀᴄᴋ ⬸", b"Back")
        buttons = [[default_font_button], [Mono_font_button], [bold_font_button], [Mini_font_button], [preview_button], [back_button]]
        await event.edit(Default_message, buttons=buttons)
    elif event.sender_id == admin_user_id and event.data == b"Mono_font":
        with open('settings/mode.txt', 'w') as f:
            f.write('Mono')
        Default_message = "Font Mode Change To Mono"
        bold_font_button = Button.inline("✵ʙᴏʟᴅ✵", b"bold_font")
        Mono_font_button = Button.inline("✅ ᴍᴏɴᴏ", b"Mono_font")
        Mini_font_button = Button.inline("✵ᴍɪɴɪ✵", b"Mini_font")
        preview_button = Button.inline("✵ʟɪᴠᴇ ᴘʀᴇᴠɪᴇᴡ✵", b"time_page_panel")
        default_font_button = Button.inline("✵ᴅᴇғᴀᴜʟᴛ✵", b"default_font")
        back_button = Button.inline("ʙᴀᴄᴋ ⬸", b"Back")
        buttons = [[default_font_button], [Mono_font_button], [bold_font_button], [Mini_font_button], [preview_button], [back_button]]
        await event.edit(Default_message, buttons=buttons)
    elif event.sender_id == admin_user_id and event.data == b"Mini_font":
        with open('settings/mode.txt', 'w') as f:
            f.write('Mini')
        Default_message = "Font Mode Change To Mini"
        bold_font_button = Button.inline("✵ʙᴏʟᴅ✵", b"bold_font")
        Mono_font_button = Button.inline("✵ᴍᴏɴᴏ✵", b"Mono_font")
        Mini_font_button = Button.inline("✅ ᴍɪɴɪ", b"Mini_font")
        preview_button = Button.inline("✵ʟɪᴠᴇ ᴘʀᴇᴠɪᴇᴡ✵", b"time_page_panel")
        default_font_button = Button.inline("✵ᴅᴇғᴀᴜʟᴛ✵", b"default_font")
        back_button = Button.inline("ʙᴀᴄᴋ ⬸", b"Back")
        buttons = [[default_font_button], [Mono_font_button], [bold_font_button], [Mini_font_button], [preview_button], [back_button]]
        await event.edit(Default_message, buttons=buttons)
    else:
        await event.answer('دوست عزیز شما ادمین نیستید', alert=True)

client.run_until_disconnected()
# Telegram Self-Bot

## نصب و آماده‌سازی

git clone https://github.com/MhdiTaheri/TelegramSelf.git  
cd TelegramSelf  
pip install -r requirements.txt  

سپس فایل lib/Information.py را ویرایش کرده و مقادیر زیر را تنظیم کنید:  
api_id, api_hash, admin_user_id, helper_username, bot_token

## اجرا

python3 main.py  
python3 helper.py  

اگر با بستن ترمینال ربات خاموش می‌شود، از دستور زیر استفاده کنید:  
nohup python3 main.py &  
nohup python3 helper.py &

## آپدیت

cd TelegramSelf  
git pull origin main

## نکته مهم

با وجود قابلیت نمایش زمان در نام و بیو، بهتر است برای دیدن ساعت به بالای صفحه گوشی یا پایین مانیتور نگاه کنید، زیرا تلگرام برای نمایش ساعت در بیو و اسم ساخته نشده است.
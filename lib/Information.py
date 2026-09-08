from .library import *

admin_user_id = 7268478044  # <--- آیدی عددی خودتان را اینجا وارد کنید
api_id = 33684592  # <--- api_id خود را اینجا وارد کنید
api_hash = '4ca8a596e43a3309f3f4cd04d427d3a1'  # <--- api_hash خود را اینجا وارد کنید
helper_username = 'helperbotforselfbot'  # <--- یوزرنیم ربات هلپر (بدون @)
bot_token = '8909112757:AAEHwzZB9qYnSX-G7-p8b1-7GM_rFB_tH0M'  # <--- توکن ربات هلپر

client_id = '01e7dc6b41c3471b94efe87abeb05919'
client_secret = '4f5f93af1ced4b0d9ba8440606803639'

client = TelegramClient('TRself-MT', api_id, api_hash)
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

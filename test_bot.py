#!/usr/bin/env python3
"""
Telegram Bot Test Script
Bu script'i yerel ortamda test etmek için kullanın
"""

import os
import sys

def test_telegram_connection():
    """Telegram bağlantısını test et"""
    print("🔍 Telegram Bot Test Başlatılıyor...\n")
    
    # Environment variables kontrol
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    
    if not token:
        print("❌ TELEGRAM_BOT_TOKEN bulunamadı!")
        print("   .env dosyası oluşturun veya export edin:")
        print("   export TELEGRAM_BOT_TOKEN='your_token_here'")
        return False
    
    if not chat_id:
        print("❌ TELEGRAM_CHAT_ID bulunamadı!")
        print("   .env dosyası oluşturun veya export edin:")
        print("   export TELEGRAM_CHAT_ID='your_chat_id_here'")
        return False
    
    print(f"✅ Token bulundu: {token[:10]}...")
    print(f"✅ Chat ID bulundu: {chat_id}\n")
    
    # Bot bilgilerini al
    import requests
    
    print("📡 Bot bilgileri alınıyor...")
    try:
        url = f"https://api.telegram.org/bot{token}/getMe"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        if data.get('ok'):
            bot_info = data['result']
            print(f"✅ Bot aktif!")
            print(f"   Bot Adı: {bot_info.get('first_name')}")
            print(f"   Username: @{bot_info.get('username')}")
            print(f"   Bot ID: {bot_info.get('id')}\n")
        else:
            print(f"❌ Bot hatası: {data}")
            return False
    except Exception as e:
        print(f"❌ Bot'a bağlanılamadı: {e}")
        return False
    
    # Test mesajı gönder
    print("📤 Test mesajı gönderiliyor...")
    try:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        payload = {
            'chat_id': chat_id,
            'text': '🧪 *Test Mesajı*\n\nBot başarıyla çalışıyor! ✅\n\n_Bu bir test mesajıdır._',
            'parse_mode': 'Markdown'
        }
        
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        if data.get('ok'):
            print("✅ Test mesajı başarıyla gönderildi!")
            print("   Telegram'ınızı kontrol edin.\n")
            return True
        else:
            print(f"❌ Mesaj gönderilemedi: {data}")
            return False
    except Exception as e:
        print(f"❌ Mesaj gönderme hatası: {e}")
        return False

def get_chat_id_helper():
    """Chat ID bulmaya yardımcı ol"""
    print("\n" + "="*60)
    print("📋 CHAT ID BULMA REHBERİ")
    print("="*60 + "\n")
    
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not token:
        print("❌ Önce TELEGRAM_BOT_TOKEN ayarlayın!")
        return
    
    print("1. Bot'unuza bir mesaj gönderin (örn: /start)")
    print("2. Ardından aşağıdaki komutu çalıştırın:\n")
    print(f"curl https://api.telegram.org/bot{token}/getUpdates\n")
    print("3. Sonuçta 'chat':{'id':123456789} şeklinde bir değer bulun")
    print("4. Bu sayıyı TELEGRAM_CHAT_ID olarak kullanın\n")
    
    # Otomatik getUpdates dene
    try:
        import requests
        print("📡 Otomatik kontrol yapılıyor...")
        url = f"https://api.telegram.org/bot{token}/getUpdates"
        response = requests.get(url, timeout=10)
        data = response.json()
        
        if data.get('ok') and data.get('result'):
            print("\n✅ Mesajlar bulundu!\n")
            for update in data['result'][-3:]:  # Son 3 mesaj
                chat = update.get('message', {}).get('chat', {})
                print(f"Chat ID: {chat.get('id')}")
                print(f"Chat Type: {chat.get('type')}")
                print(f"Name: {chat.get('first_name', '')} {chat.get('last_name', '')}")
                print(f"Username: @{chat.get('username', 'N/A')}")
                print("-" * 40)
        else:
            print("\n⚠️ Henüz mesaj bulunamadı.")
            print("   Bot'unuza bir mesaj gönderin ve tekrar deneyin.")
    except Exception as e:
        print(f"❌ Hata: {e}")

def main():
    print("""
╔═══════════════════════════════════════════════════════╗
║     🤖 TELEGRAM BOT TEST ARACI                        ║
╚═══════════════════════════════════════════════════════╝
    """)
    
    # .env dosyası varsa yükle
    try:
        from dotenv import load_dotenv
        if os.path.exists('.env'):
            load_dotenv()
            print("✅ .env dosyası yüklendi\n")
        else:
            print("⚠️ .env dosyası bulunamadı (opsiyonel)\n")
    except ImportError:
        print("ℹ️ python-dotenv yüklü değil (opsiyonel)\n")
    
    # Argüman kontrolü
    if len(sys.argv) > 1 and sys.argv[1] == '--get-chat-id':
        get_chat_id_helper()
        return
    
    # Test yap
    success = test_telegram_connection()
    
    if success:
        print("="*60)
        print("✅ TÜM TESTLER BAŞARILI!")
        print("="*60)
        print("\n🚀 Şimdi GitHub Actions'ta çalıştırabilirsiniz:")
        print("   1. Kodu GitHub'a push edin")
        print("   2. Repository > Settings > Secrets ekleyin")
        print("   3. Actions sekmesinden workflow'u çalıştırın")
    else:
        print("\n" + "="*60)
        print("❌ TEST BAŞARISIZ!")
        print("="*60)
        print("\n💡 Çözüm için:")
        print("   python test_bot.py --get-chat-id")
    
    print("\n")

if __name__ == "__main__":
    main()

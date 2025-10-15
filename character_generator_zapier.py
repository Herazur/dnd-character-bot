import requests
import random
import os
from datetime import datetime

class DnDCharacterBot:
    def __init__(self):
        self.zapier_webhook = os.environ.get('ZAPIER_WEBHOOK_URL')
        
        self.races = [
            'Elf', 'Dwarf', 'Human', 'Halfling', 'Dragonborn', 
            'Tiefling', 'Half-Elf', 'Half-Orc', 'Gnome', 'Aasimar'
        ]
        
        self.classes = [
            'Warrior', 'Mage', 'Rogue', 'Paladin', 'Ranger',
            'Cleric', 'Barbarian', 'Bard', 'Warlock', 'Monk', 'Druid'
        ]
        
        self.styles = [
            'digital art', 'fantasy art', 'concept art', 
            'detailed portrait', 'epic fantasy', 'dungeons and dragons style'
        ]
        
        self.backgrounds = [
            'mystical forest', 'ancient castle', 'dark dungeon',
            'magical library', 'mountain peak', 'tavern interior',
            'battlefield', 'enchanted garden'
        ]
        
        self.details = [
            'wearing ornate armor', 'holding magical staff',
            'with glowing eyes', 'wielding legendary sword',
            'surrounded by magical aura', 'in heroic pose',
            'with mystical tattoos', 'wearing enchanted robes'
        ]
    
    def generate_character(self):
        """Rastgele bir D&D karakteri oluştur"""
        race = random.choice(self.races)
        char_class = random.choice(self.classes)
        style = random.choice(self.styles)
        background = random.choice(self.backgrounds)
        detail = random.choice(self.details)
        gender = random.choice(['male', 'female'])
        
        # Detaylı prompt
        prompt = (
            f"A {gender} {race} {char_class}, {detail}, "
            f"in {background}, {style}, highly detailed, "
            f"8k, professional fantasy artwork, cinematic lighting"
        )
        
        # Pollinations.ai görsel URL'si
        seed = random.randint(1, 1000000)
        encoded_prompt = requests.utils.quote(prompt)
        image_url = (
            f"https://image.pollinations.ai/prompt/{encoded_prompt}"
            f"?width=768&height=1024&seed={seed}&nologo=true"
        )
        
        # Pinterest için başlık ve açıklama
        title = f"{race} {char_class}"
        hashtags = "\n\n#DnD #RPG #FantasyArt #CharacterArt #DigitalArt #DungeonsAndDragons #TabletopGaming"
        description = f"{prompt[:450]}{hashtags}"
        
        return {
            'image_url': image_url,
            'title': title,
            'description': description,
            'prompt': prompt
        }
    
    def send_to_zapier(self, data):
        """Zapier webhook'una karakter verisini gönder"""
        if not self.zapier_webhook:
            print("❌ ZAPIER_WEBHOOK_URL bulunamadı!")
            return False
        
        try:
            print("📤 Zapier'a gönderiliyor...")
            
            # Query parameters olarak gönder (Zapier webhook için)
            response = requests.post(
                self.zapier_webhook,
                params={
                    'image_url': data['image_url'],
                    'title': data['title'],
                    'description': data['description']
                },
                timeout=30
            )
            
            if response.status_code == 200:
                print("✅ Zapier webhook tetiklendi!")
                print(f"✅ Pinterest'e pin oluşturulacak: {data['title']}")
                return True
            else:
                print(f"❌ Zapier hatası: HTTP {response.status_code}")
                print(f"❌ Yanıt: {response.text}")
                return False
                
        except requests.exceptions.Timeout:
            print("❌ Zaman aşımı: Zapier yanıt vermedi")
            return False
        except requests.exceptions.RequestException as e:
            print(f"❌ Bağlantı hatası: {e}")
            return False
        except Exception as e:
            print(f"❌ Beklenmeyen hata: {e}")
            return False
    
    def run(self):
        """Ana bot çalıştırma fonksiyonu"""
        print("=" * 70)
        print("🎲 D&D KARAKTER PORTRE BOTU - ZAPIER ENTEGRASYONU")
        print("=" * 70)
        
        # Karakter oluştur
        print("\n📝 Karakter oluşturuluyor...")
        data = self.generate_character()
        
        print(f"\n✓ Karakter: {data['title']}")
        print(f"✓ Prompt: {data['prompt'][:100]}...")
        print(f"✓ Görsel URL: {data['image_url'][:80]}...")
        
        # Zapier'a gönder (otomatik olarak Pinterest'e pin oluşturacak)
        print(f"\n📌 Pinterest'e paylaşılıyor (Zapier üzerinden)...")
        success = self.send_to_zapier(data)
        
        if success:
            print("\n" + "=" * 70)
            print("✅ BOT BAŞARIYLA TAMAMLANDI!")
            print("Pinterest'te yeni pin görünmesi 1-2 dakika sürebilir.")
            print("=" * 70)
            return True
        else:
            print("\n" + "=" * 70)
            print("❌ PAYLAŞIM BAŞARISIZ!")
            print("Zapier ayarlarınızı kontrol edin.")
            print("=" * 70)
            return False


if __name__ == "__main__":
    bot = DnDCharacterBot()
    bot.run()

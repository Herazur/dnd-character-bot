import requests
import random
import os
import urllib.parse

class DnDCharacterBot:
    def __init__(self):
        event = os.environ.get('IFTTT_EVENT_NAME')
        key = os.environ.get('IFTTT_KEY')
        
        if not event or not key:
            raise ValueError("❌ IFTTT_EVENT_NAME veya IFTTT_KEY bulunamadı! Secrets ayarlarını kontrol edin.")

        self.ifttt_webhook = f"https://maker.ifttt.com/trigger/{event}/json/with/key/{key}"
        
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
        
        prompt = (
            f"A {gender} {race} {char_class}, {detail}, "
            f"in {background}, {style}, highly detailed, "
            f"8k, professional fantasy artwork, cinematic lighting"
        )
        
        seed = random.randint(1, 1000000)
        encoded_prompt = urllib.parse.quote(prompt)
        image_url = (
            f"https://image.pollinations.ai/prompt/{encoded_prompt}"
            f"?width=768&height=1024&seed={seed}&nologo=true"
        )
        
        title = f"{race} {char_class}"
        hashtags = "\n\n#DnD #RPG #FantasyArt #CharacterArt #DigitalArt #DungeonsAndDragons #TabletopGaming"
        description = f"{prompt[:450]}{hashtags}"
        
        return {
            'image_url': image_url,
            'title': title,
            'description': description,
            'prompt': prompt
        }
    
    def send_to_ifttt(self, data):
        """IFTTT Webhook'una gönder"""
        try:
            print("📤 IFTTT'ye gönderiliyor...")

            # IFTTT Applet'inizdeki parametre isimlerine göre payload
            payload = {
                "image url": data['image_url'],  # IFTTT'deki parametre adı
                "title": data['title'],          # IFTTT'deki parametre adı
                "description": data['description'] # IFTTT'deki parametre adı
            }

            print(f"📊 Gönderilen veriler:")
            print(f"   Title: {data['title']}")
            print(f"   Image URL: {data['image_url']}")
            print(f"   Description: {data['description'][:100]}...")

            response = requests.post(
                self.ifttt_webhook,
                json=payload,
                timeout=45
            )
            
            if response.status_code == 200:
                print("✅ IFTTT webhook tetiklendi!")
                print(f"✅ Olay gönderildi: {data['title']}")
                return True
            else:
                print(f"❌ IFTTT hatası: HTTP {response.status_code}")
                print(f"❌ Yanıt: {response.text[:200]}")
                return False
                
        except requests.exceptions.Timeout:
            print("⚠️ Zaman aşımı: IFTTT yanıt vermedi")
            return False
        except requests.exceptions.RequestException as e:
            print(f"❌ Bağlantı hatası: {e}")
            return False
        except Exception as e:
            print(f"❌ Beklenmeyen hata: {e}")
            return False
    
    def run(self):
        print("=" * 70)
        print("🎲 D&D KARAKTER PORTRE BOTU - IFTTT ENTEGRASYONU")
        print("=" * 70)
        
        print("\n📝 Karakter oluşturuluyor...")
        data = self.generate_character()
        
        print(f"\n✓ Karakter: {data['title']}")
        print(f"✓ Prompt: {data['prompt'][:100]}...")
        print(f"✓ Görsel URL: {data['image_url'][:80]}...")
        
        print(f"\n📌 IFTTT'ye gönderiliyor...")
        success = self.send_to_ifttt(data)
        
        if success:
            print("\n" + "=" * 70)
            print("✅ BOT BAŞARIYLA TAMAMLANDI!")
            print("IFTTT eyleminin tetiklenmesi 1-2 dakika sürebilir.")
            print("=" * 70)
            return True
        else:
            print("\n" + "=" * 70)
            print("❌ PAYLAŞIM BAŞARISIZ!")
            print("IFTTT ayarlarınızı kontrol edin.")
            print("=" * 70)
            return False


if __name__ == "__main__":
    try:
        bot = DnDCharacterBot()
        bot.run()
    except Exception as e:
        print(f"❌ Bot çalıştırılırken hata oluştu: {e}")

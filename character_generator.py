import requests
import random
import time
import os
from datetime import datetime

class DnDCharacterBot:
    def __init__(self):
        self.ifttt_key = os.environ.get('IFTTT_KEY')
        self.ifttt_event = 'dnd_character_to_pinterest'
        
        # Karakter ırk ve sınıfları
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

    def generate_character_prompt(self):
        """Rastgele bir karakter prompt'u oluşturur"""
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
        
        character_name = f"{race} {char_class}"
        
        return prompt, character_name

    def generate_image(self, prompt):
        """Pollinations.ai ile görsel oluşturur"""
        # Pollinations.ai URL'si
        base_url = "https://image.pollinations.ai/prompt/"
        
        # URL encode için
        encoded_prompt = requests.utils.quote(prompt)
        
        # Görsel parametreleri
        seed = random.randint(1, 1000000)
        
        # Basitleştirilmiş URL (parametreler olmadan daha stabil)
        image_url = f"{base_url}{encoded_prompt}?width=768&height=1024&seed={seed}&nologo=true"
        
        print(f"Görsel URL'si: {image_url[:100]}...")
        
        try:
            # Görseli kontrol et (HEAD request ile hızlı)
            print(f"Görsel kontrol ediliyor...")
            
            # Basit GET request - timeout ve retry ile
            for attempt in range(3):
                try:
                    response = requests.get(image_url, timeout=30)
                    
                    if response.status_code == 200:
                        # Dosya olarak kaydet
                        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                        filename = f"character_{timestamp}.png"
                        
                        with open(filename, 'wb') as f:
                            f.write(response.content)
                        
                        print(f"✓ Görsel başarıyla oluşturuldu")
                        print(f"✓ Dosya: {filename}")
                        return filename, image_url
                    
                    elif response.status_code == 502:
                        print(f"⚠ Deneme {attempt + 1}/3: Sunucu geçici olarak meşgul, bekleniyor...")
                        time.sleep(5)
                        continue
                    else:
                        print(f"⚠ HTTP {response.status_code}, tekrar deneniyor...")
                        time.sleep(3)
                        continue
                        
                except requests.exceptions.Timeout:
                    print(f"⚠ Deneme {attempt + 1}/3: Zaman aşımı, tekrar deneniyor...")
                    time.sleep(5)
                    continue
                except requests.exceptions.RequestException as e:
                    print(f"⚠ Deneme {attempt + 1}/3: Bağlantı hatası ({e}), tekrar deneniyor...")
                    time.sleep(5)
                    continue
            
            # 3 deneme sonrası başarısız
            print(f"✗ 3 denemeden sonra görsel oluşturulamadı")
            return None, image_url  # URL'yi yine de döndür, belki çalışıyordur
            
        except Exception as e:
            print(f"✗ Beklenmeyen hata: {e}")
            return None, image_url

    def upload_to_imgur(self, image_path):
        """Imgur'a görsel yükler (opsiyonel, IFTTT için URL gerekiyorsa)"""
        # Not: Imgur API kullanmak için CLIENT_ID gerekir
        # Alternatif olarak direkt Pollinations URL'sini kullanabiliriz
        return None

    def post_to_pinterest(self, image_url, character_name, prompt):
        """IFTTT webhook ile Pinterest'e paylaşır"""
        if not self.ifttt_key:
            print("✗ IFTTT_KEY bulunamadı!")
            return False
        
        webhook_url = f"https://maker.ifttt.com/trigger/{self.ifttt_event}/with/key/{self.ifttt_key}"
        
        # Pinterest için description hazırla
        hashtags = "\n\n#DnD #RPG #FantasyArt #CharacterArt #DigitalArt #DungeonsAndDragons"
        description = f"{character_name} - {prompt[:400]}{hashtags}"
        
        # IFTTT'ye gönderilecek veri - BASİTLEŞTİRİLMİŞ FORMAT
        data = {
            'value1': image_url,           # Photo URL
            'value2': character_name,      # Pin Title (kısa)
            'value3': description[:500]    # Pin Description (limit 500)
        }
        
        try:
            print(f"📤 IFTTT'ye gönderiliyor...")
            response = requests.post(webhook_url, json=data, timeout=30)
            
            if response.status_code == 200:
                print(f"✓ IFTTT webhook tetiklendi!")
                print(f"✓ Pinterest'e gönderildi: {character_name}")
                return True
            else:
                print(f"✗ IFTTT hatası: HTTP {response.status_code}")
                print(f"✗ Yanıt: {response.text[:200]}")
                return False
                
        except Exception as e:
            print(f"✗ IFTTT paylaşım hatası: {e}")
            return False

    def run(self):
        """Ana bot çalıştırma fonksiyonu"""
        print("=" * 60)
        print("D&D Karakter Portre Botu Başlatıldı")
        print("=" * 60)
        
        # Karakter prompt'u oluştur
        prompt, character_name = self.generate_character_prompt()
        print(f"\n📝 Karakter: {character_name}")
        print(f"📝 Prompt: {prompt[:100]}...")
        
        # Görseli oluştur
        print(f"\n🎨 Görsel oluşturuluyor...")
        image_file, image_url = self.generate_image(prompt)
        
        if not image_url:
            print("\n✗ Bot çalıştırması başarısız!")
            return False
        
        # URL varsa devam et (dosya olmasa bile)
        print(f"\n📌 Pinterest'e paylaşılıyor...")
        time.sleep(3)  # API rate limit için bekleme
        success = self.post_to_pinterest(image_url, character_name, prompt)
        
        if success:
            print("\n" + "=" * 60)
            print("✓ Bot başarıyla tamamlandı!")
            print("=" * 60)
            return True
        else:
            print("\n⚠ Pinterest paylaşımı yapılamadı, ama görsel hazır:")
            print(f"🔗 {image_url}")
            return False


if __name__ == "__main__":
    bot = DnDCharacterBot()
    bot.run()

import requests
import random
import time
import os
from datetime import datetime

class DnDCharacterBot:
    def __init__(self):
        self.ifttt_key = os.environ.get('IFTTT_KEY')
        self.ifttt_event = 'pinterest_post'
        
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
        params = {
            'width': '768',
            'height': '1024',
            'seed': random.randint(1, 1000000),
            'nologo': 'true',
            'enhance': 'true'
        }
        
        # Tam URL oluştur
        image_url = f"{base_url}{encoded_prompt}"
        param_string = "&".join([f"{k}={v}" for k, v in params.items()])
        full_url = f"{image_url}?{param_string}"
        
        print(f"Görsel oluşturuluyor: {full_url[:100]}...")
        
        try:
            # Görseli indir
            response = requests.get(full_url, timeout=60)
            response.raise_for_status()
            
            # Dosya olarak kaydet
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"character_{timestamp}.png"
            
            with open(filename, 'wb') as f:
                f.write(response.content)
            
            print(f"✓ Görsel kaydedildi: {filename}")
            return filename, full_url
            
        except Exception as e:
            print(f"✗ Görsel oluşturma hatası: {e}")
            return None, None

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
        
        # IFTTT'ye gönderilecek veri
        data = {
            'value1': character_name,  # Başlık
            'value2': prompt[:500],     # Açıklama (Pinterest 500 karakter limiti)
            'value3': image_url         # Görsel URL
        }
        
        try:
            response = requests.post(webhook_url, json=data, timeout=30)
            response.raise_for_status()
            print(f"✓ Pinterest'e gönderildi: {character_name}")
            return True
        except Exception as e:
            print(f"✗ Pinterest paylaşım hatası: {e}")
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
        
        # Pinterest'e paylaş
        print(f"\n📌 Pinterest'e paylaşılıyor...")
        time.sleep(2)  # API rate limit için bekleme
        success = self.post_to_pinterest(image_url, character_name, prompt)
        
        if success:
            print("\n" + "=" * 60)
            print("✓ Bot başarıyla tamamlandı!")
            print("=" * 60)
            return True
        else:
            print("\n✗ Paylaşım başarısız!")
            return False


if __name__ == "__main__":
    bot = DnDCharacterBot()
    bot.run()

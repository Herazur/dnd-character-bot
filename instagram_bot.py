import os
import requests
import random
import base64
from datetime import datetime
from instagrapi import Client
from PIL import Image
from io import BytesIO

class InstagramDnDBot:
    def __init__(self, username, password, session_b64=None):
        """Instagram D&D Character Portrait Bot - Pollinations.ai (Completely Free)"""
        self.cl = Client()
        self.username = username
        self.password = password
        self.session_file = "instagram_session.json"

        if session_b64:
            self.decode_session(session_b64)

        self.login()

    def decode_session(self, session_b64):
        """Decode base64 session and save"""
        try:
            session_json = base64.b64decode(session_b64).decode('utf-8')
            with open(self.session_file, 'w') as f:
                f.write(session_json)
            print("✅ Session loaded from base64")
        except Exception as e:
            print(f"⚠️  Session decode error: {e}")

    def login(self):
        """Login to Instagram with session"""
        try:
            if os.path.exists(self.session_file):
                print("📂 Saved session found, loading...")
                self.cl.load_settings(self.session_file)
                self.cl.login(self.username, self.password)
                print(f"✅ Login successful with session: {self.username}")
                return
        except Exception as e:
            print(f"⚠️  Could not use session: {e}")

        try:
            print("🔐 Logging in to Instagram...")
            self.cl.delay_range = [2, 5]
            self.cl.login(self.username, self.password)
            self.cl.dump_settings(self.session_file)
            print(f"✅ Login successful and session saved: {self.username}")

        except Exception as e:
            print(f"❌ Login error: {e}")
            print(f"\n⚠️  TROUBLESHOOTING:")
            print(f"   1. Check your Instagram password")
            print(f"   2. If 2FA is enabled, session file is required")
            print(f"   3. Check if INSTAGRAM_SESSION_B64 exists in GitHub Secrets")
            raise

    def generate_character_portrait(self):
        """Generate diverse D&D character portraits with Pollinations.ai"""

        character_prompts = [
            # Classic Fantasy Races - Heroes
            "epic portrait of a male human paladin in shining silver armor, holy symbol glowing, heroic pose, divine light, fantasy art style",
            "female elf ranger with long blonde hair, leather armor, bow and quiver, forest background, mystical aura, high fantasy portrait",
            "male dwarf warrior with braided red beard, heavy plate armor, battle axe, determined expression, mountain hall setting",
            "female half-elf bard playing lute, colorful flowing robes, charming smile, tavern lighting, magical musical notes floating",
            "male tiefling warlock with purple skin and curved horns, dark robes, eldritch energy in hands, mysterious atmosphere",
            
            # Rogues and Assassins
            "female halfling rogue in dark leather armor, dual daggers, sneaky expression, shadowy alley background, noir lighting",
            "male half-orc barbarian with tribal tattoos, fur pelts, massive greataxe, fierce battle cry, stormy background",
            "female human monk in martial arts pose, simple robes, focused eyes, zen temple setting, flowing energy aura",
            
            # Spellcasters
            "elderly male wizard with long white beard, pointed hat, ornate staff, spell book floating, arcane symbols glowing around",
            "young female sorcerer with wild magic energy crackling, colorful robes, confident smirk, chaotic magical background",
            "male dragonborn cleric in ceremonial armor, dragon scale patterns, holy flame in hand, cathedral lighting",
            "female gnome artificer with steampunk goggles, inventor's apron, magical mechanical contraptions, workshop setting",
            
            # Exotic Races
            "male tabaxi monk with spotted fur pattern, martial arts stance, monastic robes, agile and graceful, bamboo forest",
            "female firbolg druid with gentle giant appearance, nature-covered clothing, woodland creatures nearby, serene forest glade",
            "male aarakocra ranger with eagle features, feathered arms, bow ready, mountain peak background, windswept",
            "female triton paladin with blue-green skin, coral armor, trident weapon, underwater palace lighting effects",
            
            # Dark and Mysterious
            "male drow assassin with white hair and dark skin, elegant black armor, poisoned daggers, underground city background",
            "female vampire spawn bloodhunter, pale skin, red eyes, dark leather coat, crimson energy, gothic atmosphere",
            "male death cleric in dark robes with skull motifs, necrotic energy swirling, graveyard setting, ominous mood",
            "female shadow monk emerging from darkness, masked face, shadowy tendrils, moonlit rooftop, stealthy pose",
            
            # Noble and Royal
            "regal male human fighter knight in ornate royal armor, longsword and shield, castle throne room, commanding presence",
            "elegant female elf wizard in flowing silk robes, circlet crown, levitating books, grand library setting, sophisticated",
            "noble male aasimar paladin with golden wings, radiant armor, divine sword, celestial light beams, heavenly atmosphere",
            
            # Wild and Primal
            "fierce female goliath barbarian with tribal markings, minimal armor, greatclub, mountain warrior, storm clouds behind",
            "male lizardfolk druid with scales and natural camouflage, bone staff, swamp background, primal connection to nature",
            "female shifter bloodhunter mid-transformation, bestial features emerging, hunter's gear, full moon lighting, feral intensity",
            
            # Arcane Specialists
            "male bladesinger elf dancing with sword and magic, graceful combat stance, arcane runes flowing, elegant deadly beauty",
            "female war wizard battle mage, combining martial and magical combat, armored robes, spell and sword, battlefield background",
            "male illusion wizard creating multiple mirror images, mysterious smile, reality-bending effects, dream-like setting",
            
            # Support Classes
            "kind female life cleric half-elf, healing hands glowing, compassionate expression, temple of healing, warm holy light",
            "charismatic male bard with elaborate costume, juggling magical items, crowd-pleasing performance, festival stage",
            "wise old male knowledge cleric with countless scrolls, ancient tomes floating, vast library, scholarly atmosphere",
            
            # Unconventional Heroes
            "cheerful female kenku bard with raven features, colorful performer outfit, mimicking sounds, street performer vibe",
            "gruff male tortle paladin with shell armor, serenity and strength, beach monastery, peaceful warrior monk",
            "mysterious warforged artificer, mechanical body with magical enhancements, glowing runes, forge workshop background",
            
            # Epic Level Characters
            "legendary male archmage with staff of power, reality-warping magic, floating above ancient tower, cosmic energy",
            "champion female knight in legendary armor, holy avenger sword glowing, dragon skull trophy, hall of heroes",
            "ancient male druid shapeshifter surrounded by spirit animals, ageless wisdom, primordial forest, nature's avatar",
            
            # Villainous Portraits
            "sinister male necromancer with skeletal minions, dark staff, green necrotic energy, crypt throne room, evil power",
            "cunning female assassin guildmaster, shadowy elegant outfit, poisoned blade collection, secret underground lair",
            "corrupted male antipaladin in blackened armor, cursed sword dripping darkness, fallen temple, unholy aura",
            
            # Party Composition Scenes
            "diverse adventuring party of five heroes standing together, dungeon entrance background, epic group portrait, heroic lighting",
            "legendary adventurers at tavern table planning quest, maps and dice, camaraderie moment, warm firelight",
            
            # Action Portraits
            "female ranger loosing arrow mid-combat, dynamic action pose, forest battle scene, focused determination",
            "male fighter in mid-swing with greatsword, muscles tensed, battlefield chaos, slow-motion epic moment",
            "spellcaster unleashing massive fireball, hands outstretched, explosive magical energy, dramatic lighting",
            
            # Cultural Variations
            "samurai-inspired human fighter with katana, eastern fantasy aesthetic, cherry blossom background, honorable warrior",
            "viking-themed barbarian with norse runes, fur and leather, longship in background, northern warrior culture",
            "desert nomad ranger with scimitar, flowing robes, sandstorm background, middle-eastern fantasy aesthetic"
        ]

        selected_prompt = random.choice(character_prompts)

        print(f"🎨 Creating D&D character portrait...")
        print(f"   Prompt: {selected_prompt[:80]}...")

        try:
            encoded_prompt = requests.utils.quote(selected_prompt)
            url = f"https://image.pollinations.ai/prompt/{encoded_prompt}"

            params = {
                "width": 1024,
                "height": 1024,
                "nologo": "true",
                "enhance": "true",
                "model": "flux",
                "seed": random.randint(1, 1000000)
            }

            response = requests.get(url, params=params, timeout=60)

            if response.status_code == 200:
                image = Image.open(BytesIO(response.content))
                print(f"✅ Character portrait created successfully!")
                return image, selected_prompt
            else:
                print(f"❌ API Error: {response.status_code}")

        except Exception as e:
            print(f"❌ Image generation error: {e}")

        return None, None

    def generate_caption(self):
        """D&D themed captions"""
        captions = [
            "🎲 Roll for initiative! Meet your next epic character! ⚔️\n\n✨ Need inspiration for your D&D campaign?\n\n#dnd #dungeonsanddragons #characterart #fantasyart #ttrpg #dndcharacter #rpg #fantasy #characterdesign",
            
            "🐉 From taverns to dragons' lairs - every hero has a story! 📖\n\nWhat class would you play?\n\n#dnd5e #dungeonsanddragons #dndart #fantasy #characterportrait #tabletopgaming #rpgart #dndcommunity",
            
            "⚔️ Your next adventure awaits! Which character calls to you? 🗡️\n\n#dnd #charactercreation #fantasycharacter #dungeonsanddragons #ttrpg #dndideas #rpgcharacter #heroicfantasy",
            
            "🎭 Every face tells a tale of courage, magic, and adventure! ✨\n\nComment your favorite class below! 👇\n\n#dnd #characterart #fantasy #dungeonsanddragons #dndcharacter #tabletop #rpg #epicfantasy",
            
            "🌟 Legendary heroes aren't born - they're rolled! 🎲\n\nWhat's your character's backstory?\n\n#dnd5e #characterdesign #fantasyart #dungeonsanddragons #ttrpgcommunity #dndart #rpglife",
            
            "🏰 From humble beginnings to legendary deeds! ⚔️\n\nTag your D&D party! 👥\n\n#dnd #dungeonsanddragons #party #fantasy #characterart #ttrpg #adventure #rpgcharacter",
            
            "🔮 Magic, steel, and destiny collide! Which path will you choose? 🗺️\n\n#dnd #charactercreation #fantasycharacter #dungeonsanddragons #ttrpgart #dndideas #rpg #epicadventure",
            
            "⚡ Every character is a blank page waiting for adventure! 📜\n\nShare your character's name below! ✍️\n\n#dnd5e #characterart #fantasy #dungeonsanddragons #ttrpgcharacter #dndcommunity #rpgart",
            
            "🎲 The dice are rolled, the story begins! Ready to play? 🗡️\n\n#dnd #tabletopgaming #characterportrait #dungeonsanddragons #fantasy #ttrpg #rpg #dndlife",
            
            "✨ In a world of magic and monsters, who will you become? 🐲\n\n#dnd #charactercreation #fantasyart #dungeonsanddragons #dndcharacter #ttrpgart #rpgcharacter #adventure",
            
            "🛡️ Warriors, wizards, rogues and more! The party needs YOU! 🎭\n\nWhat role do you play?\n\n#dnd5e #characterdesign #fantasy #dungeonsanddragons #tabletop #dndparty #rpg #ttrpglife",
            
            "🌙 From shadow to light, every character shines! ⭐\n\n#dnd #characterart #fantasycharacter #dungeonsanddragons #ttrpg #dndideas #rpgart #heroic",
            
            "🎪 Step into the spotlight - your character awaits! 🎭\n\nDouble tap if you love D&D! ❤️\n\n#dnd #charactercreation #fantasy #dungeonsanddragons #dndcommunity #ttrpg #rpglife #fantasyart",
            
            "⚔️ Forge your legend, one session at a time! 🔥\n\n#dnd5e #characterportrait #dungeonsanddragons #fantasy #ttrpgart #dndcharacter #rpg #epicquest",
            
            "🏹 Ready your weapons, prepare your spells - adventure calls! 🗺️\n\nComment your dream character build! 💭\n\n#dnd #characterdesign #fantasyart #dungeonsanddragons #tabletopgaming #ttrpg #rpgcharacter #adventure"
        ]
        return random.choice(captions)

    def post_image(self):
        """Generate portrait and post to Instagram"""
        print(f"\n{'='*70}")
        print(f"🎲 INSTAGRAM D&D CHARACTER BOT - Pollinations.ai (Free)")
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]")
        print(f"{'='*70}\n")

        image, prompt = self.generate_character_portrait()

        if image is None:
            print("❌ Could not generate portrait!")
            return False

        temp_path = "dnd_portrait.jpg"

        if image.size[0] > 1080 or image.size[1] > 1080:
            image.thumbnail((1080, 1080), Image.Resampling.LANCZOS)

        if image.mode == 'RGBA':
            background = Image.new('RGB', image.size, (255, 255, 255))
            background.paste(image, mask=image.split()[3])
            image = background

        image.save(temp_path, "JPEG", quality=95, optimize=True)
        file_size = os.path.getsize(temp_path) / 1024

        print(f"✅ Portrait ready:")
        print(f"   Size: {image.size[0]}x{image.size[1]}")
        print(f"   File: {file_size:.1f} KB")

        caption = self.generate_caption()

        try:
            print(f"\n📤 Uploading to Instagram...")
            self.cl.photo_upload(temp_path, caption=caption)
            self.cl.dump_settings(self.session_file)

            print(f"\n{'='*70}")
            print(f"🎉 SUCCESS! Character portrait posted! 🎉")
            print(f"{'='*70}")
            print(f"\n📝 Caption: {caption}")
            print(f"🎨 Character: {prompt}")
            print(f"\n✨ Next post: Tomorrow at scheduled time!\n")

            return True

        except Exception as e:
            error_msg = str(e)
            print(f"\n❌ Instagram posting error: {error_msg}")

            if "challenge_required" in error_msg or "checkpoint_challenge_required" in error_msg:
                print(f"\n⚠️  INSTAGRAM SECURITY CHECK REQUIRED!")
                print(f"\n📋 WHAT TO DO:")
                print(f"   1. Login to your Instagram account (phone/web)")
                print(f"   2. Approve the security notification")
                print(f"   3. Enter code from email/SMS (if received)")
                print(f"   4. Run bot again after completing challenge")

            if os.path.exists(self.session_file):
                os.remove(self.session_file)

            return False

        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)


if __name__ == "__main__":
    print("\n" + "="*70)
    print("🎲 INSTAGRAM D&D CHARACTER PORTRAIT BOT")
    print("   Powered by Pollinations.ai (100% Free)")
    print("="*70 + "\n")

    INSTAGRAM_USERNAME = os.environ.get('INSTAGRAM_USERNAME')
    INSTAGRAM_PASSWORD = os.environ.get('INSTAGRAM_PASSWORD')
    INSTAGRAM_SESSION_B64 = os.environ.get('INSTAGRAM_SESSION_B64')

    if not all([INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD]):
        print("❌ ERROR: Missing credentials!\n")
        print("Please set these environment variables:")
        print(f"   INSTAGRAM_USERNAME: {'✅' if INSTAGRAM_USERNAME else '❌'}")
        print(f"   INSTAGRAM_PASSWORD: {'✅' if INSTAGRAM_PASSWORD else '❌'}")
        print(f"   INSTAGRAM_SESSION_B64: {'✅ (set)' if INSTAGRAM_SESSION_B64 else '⚠️  (missing - 2FA issues possible)'}")
        print()
        exit(1)

    try:
        bot = InstagramDnDBot(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD, INSTAGRAM_SESSION_B64)
        success = bot.post_image()
        exit(0 if success else 1)

    except KeyboardInterrupt:
        print("\n\n⚠️  Bot stopped (Ctrl+C)\n")
        exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}\n")
        exit(1)
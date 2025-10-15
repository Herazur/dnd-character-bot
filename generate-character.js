const axios = require('axios');
const FormData = require('form-data');
const fs = require('fs').promises;
const path = require('path');

// D&D Karakter Elementleri
const races = [
  'Elf', 'Dwarf', 'Human', 'Halfling', 'Dragonborn', 'Tiefling', 
  'Half-Elf', 'Half-Orc', 'Gnome', 'Aasimar', 'Tabaxi', 'Goliath'
];

const classes = [
  'Wizard', 'Warrior', 'Rogue', 'Paladin', 'Cleric', 'Ranger',
  'Barbarian', 'Bard', 'Druid', 'Monk', 'Warlock', 'Sorcerer'
];

const styles = [
  'fantasy portrait', 'digital art', 'oil painting style',
  'concept art', 'dungeons and dragons style', 'pathfinder art style',
  'epic fantasy illustration', 'character portrait', 'heroic pose'
];

const attributes = [
  'mysterious', 'powerful', 'wise', 'fierce', 'noble',
  'battle-worn', 'elegant', 'rugged', 'mystical', 'charismatic'
];

const settings = [
  'in a tavern', 'in a dark forest', 'in a castle',
  'in a magical library', 'on a mountain peak', 'in ancient ruins',
  'in a throne room', 'in a mystical cave', 'at sunset', 'in moonlight'
];

// Random seçim fonksiyonu
function random(array) {
  return array[Math.floor(Math.random() * array.length)];
}

// Karakter prompt oluşturucu
function generateCharacterPrompt() {
  const race = random(races);
  const charClass = random(classes);
  const style = random(styles);
  const attribute = random(attributes);
  const setting = random(settings);
  
  const gender = Math.random() > 0.5 ? 'male' : 'female';
  
  const prompt = `A ${attribute} ${gender} ${race} ${charClass}, detailed ${style}, ${setting}, highly detailed face, dramatic lighting, professional quality, 4k, masterpiece`;
  
  return {
    prompt,
    race,
    class: charClass,
    gender,
    attribute,
    title: `${attribute.charAt(0).toUpperCase() + attribute.slice(1)} ${race} ${charClass}`
  };
}

// Pollinations.ai'dan görsel oluşturma
async function generateImage(prompt) {
  // Pollinations.ai URL encode edilmiş prompt kullanır
  const encodedPrompt = encodeURIComponent(prompt);
  const imageUrl = `https://image.pollinations.ai/prompt/${encodedPrompt}?width=1024&height=1024&seed=${Date.now()}&model=flux&nologo=true`;
  
  console.log('Görsel oluşturuluyor:', imageUrl);
  
  // Görselin base64 verisini al
  const response = await axios.get(imageUrl, {
    responseType: 'arraybuffer',
    timeout: 60000
  });
  
  return {
    url: imageUrl,
    buffer: Buffer.from(response.data, 'binary')
  };
}

// IFTTT webhook ile Pinterest'e gönder
async function postToPinterest(imageUrl, title, description) {
  const iftttKey = process.env.IFTTT_KEY;
  
  if (!iftttKey) {
    console.error('IFTTT_KEY bulunamadı!');
    return false;
  }
  
  const webhookUrl = `https://maker.ifttt.com/trigger/post_to_pinterest/with/key/${iftttKey}`;
  
  try {
    const response = await axios.post(webhookUrl, {
      value1: title,           // Pinterest başlık
      value2: description,     // Pinterest açıklama
      value3: imageUrl         // Görsel URL
    });
    
    console.log('Pinterest\'e gönderildi:', response.data);
    return true;
  } catch (error) {
    console.error('IFTTT hatası:', error.message);
    return false;
  }
}

// Log kaydetme
async function saveLog(character, imageUrl, success) {
  const logDir = path.join(__dirname, 'logs');
  
  try {
    await fs.mkdir(logDir, { recursive: true });
  } catch (err) {
    // Klasör zaten varsa hata vermez
  }
  
  const logFile = path.join(logDir, `${Date.now()}.json`);
  const logData = {
    timestamp: new Date().toISOString(),
    character,
    imageUrl,
    success,
    posted_to_pinterest: success
  };
  
  await fs.writeFile(logFile, JSON.stringify(logData, null, 2));
  console.log('Log kaydedildi:', logFile);
}

// Ana fonksiyon
async function main() {
  try {
    console.log('🎲 D&D Karakter Portre Botu Başlatılıyor...');
    
    // 1. Karakter oluştur
    const character = generateCharacterPrompt();
    console.log('\n📝 Karakter:', character);
    
    // 2. Görsel üret
    console.log('\n🎨 Görsel oluşturuluyor...');
    const image = await generateImage(character.prompt);
    console.log('✅ Görsel hazır:', image.url);
    
    // 3. Pinterest'e gönder
    console.log('\n📌 Pinterest\'e gönderiliyor...');
    const description = `${character.race} ${character.class} character art. ${character.prompt}\n\n#DnD #DungeonsAndDragons #FantasyArt #CharacterArt #RPG #${character.race} #${character.class}`;
    
    const success = await postToPinterest(
      image.url,
      character.title,
      description
    );
    
    // 4. Log kaydet
    await saveLog(character, image.url, success);
    
    if (success) {
      console.log('\n✅ İşlem başarıyla tamamlandı!');
    } else {
      console.log('\n⚠️ Pinterest\'e gönderilemedi ama görsel oluşturuldu');
    }
    
  } catch (error) {
    console.error('\n❌ Hata:', error.message);
    process.exit(1);
  }
}

main();

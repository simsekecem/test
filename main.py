from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager  # Otomatik olarak doğru sürüm ChromeDriver indirir
from selenium.webdriver.common.by import By
import time
import json
from datetime import datetime, timedelta
import os

# Chrome için başsız mod seçeneklerini ayarlayın
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument('--disable-gpu')

# ChromeDriver'ı otomatik olarak indirip kullanma
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Sayfayı aç
url = 'https://open.spotify.com/artist/5RmQ8k4l3HZ8JoPb4mNsML'
driver.get(url)

# Sayfanın yüklenmesini bekleyin
time.sleep(5)

# Tüm şarkı elemanlarını bul
song_elements = driver.find_elements(By.XPATH, "//div[@data-testid='tracklist-row']")

# Şarkı bilgilerini depolayacak liste
songs = []

for song in song_elements:
    song_name = song.find_element(By.XPATH, ".//div[@class='encore-text encore-text-body-medium encore-internal-color-text-base btE2c3IKaOXZ4VNAb8WQ standalone-ellipsis-one-line']").text
    plays = song.find_element(By.XPATH, ".//div[@class='encore-text encore-text-body-small HxDMwNr5oCxTOyqt85gi']").text
    plays = int(plays.replace('.', ''))

    songs.append({
        "Şarkı Adı": song_name,
        "Dinlenme Sayısı": plays,
        "O Günkü Dinlenme Sayısı": None,
        "Artış/Azalış": None
    })

driver.quit()

# JSON dosyasına yazma işlemleri devam ediyor...


# Bugünün tarihini al
today = datetime.now().strftime('%Y-%m-%d')

# Bir önceki günün tarihini al
yesterday = (datetime.now() - timedelta(1)).strftime('%Y-%m-%d')

# Önceki günün dosya adı
previous_filename = f'songs_{yesterday}.json'

# Önceki günün verisini kontrol et ve farkları hesapla
if os.path.exists(previous_filename):
    # Önceki günün dosyasını aç
    with open(previous_filename, 'r', encoding='utf-8') as f:
        previous_songs = json.load(f)

    # Şarkıları karşılaştır ve farkları bul
    for song in songs:
        for prev_song in previous_songs:
            if song["Şarkı Adı"] == prev_song["Şarkı Adı"]:
                # O günkü dinlenme sayısını hesapla
                song["O Günkü Dinlenme Sayısı"] = song["Dinlenme Sayısı"] - int(prev_song["Dinlenme Sayısı"])

                # Artış/Azalış hesapla
                if prev_song.get("O Günkü Dinlenme Sayısı") is not None:
                    song["Artış/Azalış"] = song["O Günkü Dinlenme Sayısı"] - prev_song["O Günkü Dinlenme Sayısı"]
                else:
                    song["Artış/Azalış"] = "Dün verisi mevcut değil"
                break
else:
    # Eğer önceki günün dosyası yoksa, o günkü dinlenme sayısı toplam dinlenme sayısına eşit olacaktır.
    for song in songs:
        song["O Günkü Dinlenme Sayısı"] = song["Dinlenme Sayısı"]
        song["Artış/Azalış"] = "Önceki gün verisi yok"

# Bugünkü dosya adı
filename = f'songs_{today}.json'

# Bugünkü veriyi JSON dosyasına yaz
with open(filename, 'w', encoding='utf-8') as f:
    json.dump(songs, f, ensure_ascii=False, indent=4)

import os
import json
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

# JSON dosyasının oluşturulacağı dizin
output_dir = '/app/data'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

def fetch_songs():
    # ChromeDriver'ı otomatik olarak indirip kullanma
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    # Sayfayı aç
    url = 'https://open.spotify.com/artist/5RmQ8k4l3HZ8JoPb4mNsML'
    driver.get(url)

    # Sayfanın yüklenmesini bekleyin
    time.sleep(5)  # Sayfanın tamamen yüklenmesi için biraz bekleyin (gerektiğinde bu süreyi artırabilirsiniz)

    # Tüm şarkı elemanlarını bul
    song_elements = driver.find_elements(By.XPATH, "//div[@data-testid='tracklist-row']")

    # Şarkı bilgilerini depolayacak liste
    songs = []

    for song in song_elements:
        # Şarkı ismini bul
        song_name = song.find_element(By.XPATH,
                                      ".//div[@class='encore-text encore-text-body-medium encore-internal-color-text-base btE2c3IKaOXZ4VNAb8WQ standalone-ellipsis-one-line']").text

        # Dinlenme sayısını bul
        plays = song.find_element(By.XPATH, ".//div[@class='encore-text encore-text-body-small HxDMwNr5oCxTOyqt85gi']").text

        # Dinlenme sayısını sayı olarak sakla (noktalardan kurtul)
        plays = int(plays.replace('.', ''))

        # Şarkı bilgilerini listeye ekle
        songs.append({
            "Şarkı Adı": song_name,
            "Dinlenme Sayısı": plays,  # Toplam dinlenme sayısı
            "O Günkü Dinlenme Sayısı": None,  # Henüz hesaplanmadı
            "Artış/Azalış": None  # Henüz hesaplanmadı
        })

    # Tarayıcıyı kapat
    driver.quit()

    return songs

def calculate_differences(songs):
    # Bugünün tarihini al
    today = datetime.now().strftime('%Y-%m-%d')

    # Bir önceki günün tarihini al
    yesterday = (datetime.now() - timedelta(1)).strftime('%Y-%m-%d')

    # Önceki günün dosya adı
    previous_filename = f'/app/data/songs_{yesterday}.json'

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

    return songs

def main():
    # Şarkı verilerini çek
    songs = fetch_songs()

    # Farkları hesapla
    songs_with_differences = calculate_differences(songs)

    # Bugünkü dosya adı ve yolu
    today = datetime.now().strftime('%Y-%m-%d')
    filename = os.path.join(output_dir, f'songs_{today}.json')

    # Bugünkü veriyi JSON dosyasına yaz
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(songs_with_differences, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()

# Temel imajı belirleyin
FROM python:3.12-slim

# Çalışma dizinini ayarla
WORKDIR /app

# Gereksinim dosyalarını kopyala
COPY requirements.txt .

# Python bağımlılıklarını yükle
RUN pip install --no-cache-dir -r requirements.txt

# Python scriptinizi kopyala
COPY main.py .

# Veriler için dizin oluştur
RUN mkdir -p /app/data

# Python scriptinizi çalıştır
CMD ["python", "main.py"]

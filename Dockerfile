# Base image olarak python:3.9-slim-buster kullanıyoruz
FROM python:3.9-slim-buster

# Çalışma dizinini belirliyoruz
WORKDIR /app

# requirements.txt dosyasını çalışma dizinine kopyalıyoruz
COPY requirements.txt .

# Python bağımlılıklarını yüklüyoruz
RUN pip install --no-cache-dir -r requirements.txt

# Python scriptinizi ve diğer dosyalarınızı kopyalıyoruz
COPY . .

# Python scriptinizi çalıştırıyoruz
CMD ["python", "main.py"]

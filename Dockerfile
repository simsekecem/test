# Selenium ve Chrome içeren bir temel imaj kullanıyoruz
FROM selenium/standalone-chrome:latest

# Çalışma dizinini belirliyoruz
WORKDIR /usr/src/app

# Proje dosyalarınızı Docker imajına kopyalıyoruz
COPY . .

# Python bağımlılıklarını yüklüyoruz
RUN pip install --no-cache-dir -r requirements.txt

# Python scriptinizi çalıştırıyoruz
CMD ["python", "main.py"]

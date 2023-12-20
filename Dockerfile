# Gunakan base image yang sesuai dengan runtime Anda
FROM python:3.10.11

# Set working directory di dalam container
WORKDIR /app

# Salin file dependencies
COPY requirements.txt .

# Install dependensi
RUN pip install --no-cache-dir -r requirements.txt

# Salin seluruh konten proyek ke dalam container
COPY . .

# Port yang harus diexpose sesuai dengan konfigurasi aplikasi Flask Anda
EXPOSE 5200

# Perintah untuk menjalankan aplikasi menggunakan Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:5200", "your_module_name:app"]
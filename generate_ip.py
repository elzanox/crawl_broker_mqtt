import csv
import random
import time
import os

# Rentang alamat IP yang diinginkan
start_ip = "103.127.96.0"
end_ip = "103.127.97.255"
output_csv = f'data/{start_ip}-{end_ip}.csv'
# Mengecek apakah file sudah ada
if not os.path.exists(output_csv):
    # Jika file tidak ada, maka kita membuatnya
    with open(output_csv, mode='w', newline='') as file_csv:
        # Membuat objek writer
        writer = csv.writer(file_csv)
        # Tidak ada penulisan data dalam contoh ini
    print(f"File CSV kosong dengan nama '{output_csv}' berhasil dibuat.")
else:
    print(f"File CSV dengan nama '{output_csv}' sudah ada. Tidak perlu membuat baru.")
    
def generate_ip_in_range(start_ip, end_ip):
    start_parts = list(map(int, start_ip.split('.')))
    end_parts = list(map(int, end_ip.split('.')))

    # Konversi IP awal dan akhir ke bentuk numerik
    start_num = (start_parts[0] << 24) + (start_parts[1] << 16) + (start_parts[2] << 8) + start_parts[3]
    end_num = (end_parts[0] << 24) + (end_parts[1] << 16) + (end_parts[2] << 8) + end_parts[3]

    # Menghasilkan alamat IP acak dalam rentang yang ditentukan
    random_num = random.randint(start_num, end_num)

    # Konversi angka acak kembali ke bentuk alamat IP
    random_ip_parts = [
        (random_num >> 24) & 0xFF,
        (random_num >> 16) & 0xFF,
        (random_num >> 8) & 0xFF,
        random_num & 0xFF
    ]

    ip_adress = ".".join(map(str, random_ip_parts))
    return ip_adress

def generate_ip_random():
    # Menghasilkan empat bagian angka antara 0 dan 255
    ip_parts = [random.randint(0, 255) for _ in range(4)]
    
    # Menggabungkan bagian-bagian IP menjadi satu string
    ip_address = '.'.join(map(str, ip_parts))
    
    return ip_address

def is_ip_exists(ip, filename=output_csv):
    # Mengecek apakah IP sudah ada dalam file CSV
    with open(filename, mode='r') as file:
        reader = csv.reader(file)
        # Mengecek setiap baris dalam file
        for row in reader:
            if row and row[0] == ip:
                return True
    return False

def save_to_csv(ip, filename=output_csv):
    # Menyimpan alamat IP ke dalam file CSV
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        # Menulis alamat IP baru
        writer.writerow([ip])
try:
    while True:
        new_ip = generate_ip_in_range(start_ip,end_ip)

        while is_ip_exists(new_ip):
            print(f"IP {new_ip} sudah ada dalam file CSV, menghasilkan IP baru...")
            new_ip = generate_ip_in_range(start_ip,end_ip)

        save_to_csv(new_ip)
        print(f"IP Address {new_ip} telah disimpan dalam file {output_csv}.")

        # Menunggu selama 1 detik sebelum menghasilkan IP berikutnya
        # time.sleep(0.1)

except KeyboardInterrupt:
    print("\nProgram dihentikan.")

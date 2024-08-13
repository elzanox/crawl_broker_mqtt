import paho.mqtt.client as mqtt
import pandas as pd
from tqdm import tqdm
import os
import csv
# Ganti dengan nama file CSV yang sesuai
# csv_file = 'result.csv'
csv_file = 'data/alamat_ip.csv'
headerr = ['ip_address','status','mqtt']
# Ganti dengan nama kolom yang ingin dibaca
target_column_name = 'ip_address'  # Contoh: membaca kolom dengan nama 'nama_kolom'

if not os.path.exists(csv_file):
    # Jika file tidak ada, maka kita membuatnya
    with open(csv_file, mode='w', newline='') as file_csv:
        # Membuat objek writer
        writer = csv.writer(file_csv)
        # Menulis data ke dalam file CSV
        writer.writerows(headerr)
        # Tidak ada penulisan data dalam contoh ini
    print(f"File CSV kosong dengan nama '{csv_file}' berhasil dibuat.")
else:
    print(f"File CSV dengan nama '{csv_file}' sudah ada. Tidak perlu membuat baru.")



def test_mqtt(ip, port):
    try:
        client = mqtt.Client()
        client.connect(ip, port, 60)
        print(f"Berhasil terhubung ke {ip}")
        client.disconnect()  # Memutuskan koneksi setelah berhasil terhubung
        return "berhasil"
    except Exception as e:
        print(f"IP Broker: {ip} Gagal, Error: {e}")
        return "gagal"
        
# Fungsi yang dipanggil ketika koneksi ke broker berhasil dibuat
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Koneksi ke broker berhasil.")
        # Subscribe pada topik tertentu setelah koneksi berhasil
        client.subscribe("#")
    else:
        print(f"Gagal terhubung ke broker dengan kode {rc}")

# Fungsi yang dipanggil ketika pesan diterima dari broker
def on_message(client, userdata, msg):
    print(f"Pesan diterima dari topik {msg.topic}: {msg.payload.decode()}")

# Inisialisasi objek client MQTT
client = mqtt.Client()

# Menetapkan fungsi callback ketika koneksi berhasil dibuat
client.on_connect = on_connect

# Menetapkan fungsi callback ketika pesan diterima
client.on_message = on_message

# Tentukan alamat broker dan port yang digunakan
# broker_address = "3.123.112.129"
port = 1883

# Membaca file CSV ke dalam DataFrame
df = pd.read_csv(csv_file)
ip_list = df['ip_address'].tolist()
# Terhubung ke broker menggunakan alamat dan port yang telah ditentukan
for ip in tqdm(df['ip_address'], desc="Testing IPs"):
    index = ip_list.index(ip)
    print(f"Mencoba: {index} {ip}")
    mqtt_val = test_mqtt(ip,port)
    # status_val = test_ping(ip)
# for index, ip in tqdm(enumerate(df['ip_address'][10937:], start=10937), desc="Testing IPs"):
#     index = ip_list.index(ip)
#     print(f"Mencoba: {index} {ip}")
#     mqtt_val = test_mqtt(ip,port)
#     # status_val = test_ping(ip)
    df.at[index, 'mqtt'] = mqtt_val
    df.to_csv(csv_file, index=False)

# Loop tak terhingga untuk menjaga koneksi tetap hidup
# client.loop_forever()

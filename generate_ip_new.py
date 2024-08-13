import ipaddress
import csv

def generate_ip(start_ip, end_ip):
    try:
        start_ip_obj = ipaddress.ip_address(start_ip)
        end_ip_obj = ipaddress.ip_address(end_ip)
        
        if start_ip_obj > end_ip_obj:
            raise ValueError("Alamat IP awal harus lebih kecil dari alamat IP akhir")

        ip_list = []
        for ip in range(int(start_ip_obj), int(end_ip_obj) + 1):
            ip_list.append(str(ipaddress.ip_address(ip)))

        return ip_list

    except ValueError as e:
        return str(e)

# Masukkan alamat IP awal dan akhir di bawah ini:
start_ip = "27.111.32.0"
end_ip = "27.111.47.255"

hasil = generate_ip(start_ip, end_ip)

# Tulis ke dalam file CSV
with open(f'{start_ip}-{end_ip}.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Alamat IP"])
    for ip in hasil:
        writer.writerow([ip])

print("Alamat IP telah disimpan di dalam file alamat_ip.csv")

import telebot
from scapy.all import ARP, Ether, srp
import socket

# Telegram vars
with open('../secrets/bot_token', 'r') as file:
    BOT_TOKEN = file.read().strip()
with open('../secrets/user_id', 'r') as file:
    USER_ID = int(file.read().strip())
bot = telebot.TeleBot(BOT_TOKEN)

def send_message(message):
    bot.send_message(USER_ID, message, parse_mode='html')

def scan_network(ip_range):
    arp_request = ARP(pdst=ip_range)
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    devices = []
    for element in answered_list:
        ip = element[1].psrc
        mac = element[1].hwsrc
        try:
            hostname = socket.gethostbyaddr(ip)[0]
        except (socket.herror, socket.gaierror):
            hostname = "Unknown"
        device = {"ip": ip, "mac": mac, "hostname": hostname}
        devices.append(device)
    return devices

def check_known_hosts(devices, known_hosts_file):
    known_hosts = set()
    with open(known_hosts_file, "r") as file:
        for line in file:
            mac_address = line.strip()
            known_hosts.add(mac_address)

    for device in devices:
        if device["mac"] not in known_hosts:
            message = ("🏠🛜⚠️ Unknown device detected on the network!\nName:" + device["hostname"] + "\nMAC:" + device["mac"] + "\nIP:" + device["ip"])
            send_message(message)

def main():
    ip_range = "192.168.1.0/24"  # Modify this to match your network range
    known_hosts_file = "known_hosts"
    devices = scan_network(ip_range)

    if devices:
        check_known_hosts(devices, known_hosts_file)

if __name__ == "__main__":
    main()


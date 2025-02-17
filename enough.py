from colorama import Fore, Style
from time import sleep
from os import system
from sms import SendSms
from concurrent.futures import ThreadPoolExecutor, wait

# Servisleri alma
servisler_sms = []
for attribute in dir(SendSms):
    attribute_value = getattr(SendSms, attribute)
    if callable(attribute_value) and not attribute.startswith('__'):
        servisler_sms.append(attribute)

def clear_screen():
    system("cls||clear")

def main_menu():
    clear_screen()
    print(f"""{Fore.LIGHTCYAN_EX}
     ______                         _     
    |  ____|                       | |    
    | |__   _ __   ___  _   _  __ _| |__  
    |  __| | '_ \ / _ \| | | |/ _` | '_ \ 
    | |____| | | | (_) | |_| | (_| | | | |
    |______|_| |_|\___/ \__,_|\__, |_| |_|
                               __/ |      
                              |___/      
    
    Sms: {len(servisler_sms)}           {Style.RESET_ALL}by {Fore.LIGHTRED_EX}@tingirifistik\n  
    """)
    print(f"{Fore.LIGHTMAGENTA_EX} 1- SMS Gönder (Normal)\n 2- SMS Gönder (Turbo)\n 3- Çıkış\n")

def get_phone_numbers():
    tel_liste = []
    print(Fore.LIGHTYELLOW_EX + "Telefon numarasını başında '+90' olmadan yazınız (Birden çoksa 'enter' tuşuna basınız): " + Fore.LIGHTGREEN_EX, end="")
    tel_no = input()
    if not tel_no:
        print(Fore.LIGHTYELLOW_EX + "Telefon numaralarının kayıtlı olduğu dosyanın dizinini yazınız: " + Fore.LIGHTGREEN_EX, end="")
        dizin = input()
        try:
            with open(dizin, "r", encoding="utf-8") as f:
                tel_liste = [i.strip() for i in f if len(i.strip()) == 10]
        except FileNotFoundError:
            print(Fore.LIGHTRED_EX + "Hatalı dosya dizini. Tekrar deneyiniz.")
            sleep(3)
            return None
    else:
        try:
            if len(tel_no) == 10 and tel_no.isdigit():
                tel_liste.append(tel_no)
            else:
                raise ValueError
        except ValueError:
            print(Fore.LIGHTRED_EX + "Hatalı telefon numarası. Tekrar deneyiniz.")
            sleep(3)
            return None
    return tel_liste

def get_mail():
    print(Fore.LIGHTYELLOW_EX + "Mail adresi (Bilmiyorsanız 'enter' tuşuna basın): " + Fore.LIGHTGREEN_EX, end="")
    mail = input()
    if mail and ("@" not in mail or ".com" not in mail):
        print(Fore.LIGHTRED_EX + "Hatalı mail adresi. Tekrar deneyiniz.")
        sleep(3)
        return None
    return mail

def normal_sms_mode():
    clear_screen()
    tel_liste = get_phone_numbers()
    if not tel_liste:
        return
    mail = get_mail()
    if mail is None:
        return
    print(Fore.LIGHTYELLOW_EX + f"Kaç adet SMS göndermek istiyorsun (Sonsuz için 'enter' tuşuna basınız): " + Fore.LIGHTGREEN_EX, end="")
    try:
        kere = input()
        kere = int(kere) if kere else None
    except ValueError:
        print(Fore.LIGHTRED_EX + "Hatalı giriş yaptın. Tekrar deneyiniz.")
        sleep(3)
        return
    print(Fore.LIGHTYELLOW_EX + "Kaç saniye aralıkla göndermek istiyorsun: " + Fore.LIGHTGREEN_EX, end="")
    try:
        aralik = int(input())
    except ValueError:
        print(Fore.LIGHTRED_EX + "Hatalı giriş yaptın. Tekrar deneyiniz.")
        sleep(3)
        return
    clear_screen()
    for tel_no in tel_liste:
        sms = SendSms(tel_no, mail)
        while kere is None or sms.adet < kere:
            for attribute in dir(SendSms):
                attribute_value = getattr(SendSms, attribute)
                if callable(attribute_value) and not attribute.startswith('__'):
                    exec(f"sms.{attribute}()")
                    sms.adet += 1
                    sleep(aralik)

def turbo_sms_mode():
    clear_screen()
    print(Fore.LIGHTYELLOW_EX + "Telefon numarasını başında '+90' olmadan yazınız: " + Fore.LIGHTGREEN_EX, end="")
    tel_no = input()
    if len(tel_no) != 10 or not tel_no.isdigit():
        print(Fore.LIGHTRED_EX + "Hatalı telefon numarası. Tekrar deneyiniz.")
        sleep(3)
        return
    mail = get_mail()
    if mail is None:
        return
    send_sms = SendSms(tel_no, mail)
    clear_screen()
    try:
        while True:
            with ThreadPoolExecutor() as executor:
                futures = [executor.submit(getattr(send_sms, method)) for method in dir(SendSms) if callable(getattr(SendSms, method)) and not method.startswith('__')]
                wait(futures)
    except KeyboardInterrupt:
        print("\nCtrl+C tuş kombinasyonu algılandı. Menüye dönülüyor...")
        sleep(2)

# Ana döngü
while True:
    main_menu()
    try:
        menu_choice = int(input(Fore.LIGHTYELLOW_EX + "Seçim: "))
    except ValueError:
        print(Fore.LIGHTRED_EX + "Hatalı giriş yaptın. Tekrar deneyiniz.")
        sleep(3)
        continue

    if menu_choice == 1:
        normal_sms_mode()
    elif menu_choice == 2:
        turbo_sms_mode()
    elif menu_choice == 3:
        print(Fore.LIGHTRED_EX + "Çıkış yapılıyor...")
        break
    else:
        print(Fore.LIGHTRED_EX + "Geçersiz seçim. Tekrar deneyiniz.")
        sleep(3)

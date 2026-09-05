import subprocess
import sys
import os

def pip_install(package):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--quiet", package])
        return True
    except:
        return False

def check_and_install(modules):
    for module in modules:
        try:
            __import__(module)
        except ImportError:
            print(f"[+] {module} yukleniyor...")
            if pip_install(module):
                print(f"[+] {module} yuklendi!")
            else:
                print(f"[-] {module} yuklenemedi!")

modules = ["requests", "colorama", "pyfiglet"]
check_and_install(modules)

import requests
from datetime import datetime
from requests import Session
from sys import exit
import string
import random
from colorama import Fore, Style, init
from os import path
import re
import pyfiglet
from cfonts import render

init(autoreset=True)

os.system("cls" if os.name == "nt" else "clear")

dexron_logo = render('DEXRON', colors=['white', 'blue'], align='center')
print(dexron_logo)
print("─────────────────────────────────────────────────────────────")
print("         Python dev ~ T.me/dexrontools ~ T.me/dexronpy")
print("─────────────────────────────────────────────────────────────")
print()

def print_success(message, *argv):
    print(Fore.GREEN + "[ OK ] " + Style.RESET_ALL + Style.BRIGHT, end="")
    print(message, end=" ")
    for arg in argv:
        print(arg, end=" ")
    print("")

def print_error(message, *argv):
    print(Fore.RED + "[ ERR ] " + Style.RESET_ALL + Style.BRIGHT, end="")
    print(message, end=" ")
    for arg in argv:
        print(arg, end=" ")
    print("")

def print_status(message, *argv):
    print(Fore.CYAN + "[ * ] " + Style.RESET_ALL + Style.BRIGHT, end="")
    print(message, end=" ")
    for arg in argv:
        print(arg, end=" ")
    print("")

def ask_question(message, *argv):
    message = Fore.CYAN + "[ ? ] " + Style.RESET_ALL + Style.BRIGHT + message
    for arg in argv:
        message = message + " " + arg
    print(message, end="")
    ret = input(": ")
    return ret

def parse_proxy_file(fpath):
    if not path.exists(fpath):
        print_error("Proxy dosyasi bulunamadi!")
        print_error("Program kapaniyor!")
        exit(0)
    
    proxies = []
    with open(fpath, "r") as proxy_file:
        for line in proxy_file.readlines():
            line = line.strip()
            if line:
                proxies.append(line)
    
    if len(proxies) > 50:
        proxies = random.choices(proxies, 50)
        
    print_success(f"{len(proxies)} proxy yuklendi!")
    return proxies

def random_str(length):
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for _ in range(length))

def get_user_agent():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:89.0) Gecko/20100101 Firefox/89.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
    ]
    return random.choice(user_agents)

def report_profile_attack(username, num_reports=1):
    ses = Session()

    user_agent = get_user_agent()
    page_headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "tr-TR,tr;q=0.8,en-US;q=0.5,en;q=0.3",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "DNT": "1",
        "User-Agent": user_agent,
    }
    report_headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "tr-TR,tr;q=0.8,en-US;q=0.5,en;q=0.3",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded",
        "DNT": "1",
        "Host": "help.instagram.com",
        "Origin": "help.instagram.com",
        "Pragma": "no-cache",
        "Referer": "https://help.instagram.com/contact/497253480400030",
        "TE": "Trailers",
        "User-Agent": user_agent,
    }
    try:
        res = ses.get("https://www.facebook.com/", timeout=10)
        res.raise_for_status()
    except Exception as e:
        print_error("Baglanti hatasi! (FacebookRequestsError)", e)
        return

    if '["_js_datr","' not in res.text:
        print_error("Baglanti hatasi! (CookieErrorJSDatr)")
        return
    
    try:
        js_datr = res.text.split('["_js_datr","')[1].split('",')[0]
    except:
        print_error("Baglanti hatasi! (CookieParsingError)")
        return

    page_cookies = {"_js_datr": js_datr}

    try:
        res = ses.get("https://help.instagram.com/contact/497253480400030", cookies=page_cookies, headers=page_headers, timeout=10)
        res.raise_for_status()
    except Exception as e:
        print_error("Baglanti hatasi! (InstagramRequestsError)", e)
        return

    if "datr" not in res.cookies.get_dict():
        print_error("Baglanti hatasi! (CookieErrorDatr)")
        return

    if '["LSD",[],{"token":"' not in res.text:
        print_error("Baglanti hatasi! (CookieErrorLSD)")
        return

    if not all(key in res.text for key in ['"__spin_r":', '"__spin_b":', '"__spin_t":', '"server_revision":', '"hsi":']):
        print_error("Baglanti hatasi! (CookieError)")
        return

    try:
        lsd = res.text.split('["LSD",[],{"token":"')[1].split('"},')[0]
        spin_r = res.text.split('"__spin_r":')[1].split(',')[0]
        spin_b = res.text.split('"__spin_b":')[1].split(',')[0].replace('"',"")
        spin_t = res.text.split('"__spin_t":')[1].split(',')[0]
        hsi = res.text.split('"hsi":')[1].split(',')[0].replace('"',"")
        rev = res.text.split('"server_revision":')[1].split(',')[0].replace('"',"")
        datr = res.cookies.get_dict()["datr"]
    except:
        print_error("Baglanti hatasi! (CookieParsingError)")
        return

    report_cookies = {"datr": datr}
    report_form = {
        "jazoest": "2723",
        "lsd": lsd,
        "instagram_username": username,
        "Field241164302734019_iso2_country_code": "IN",
        "Field241164302734019": "India",
        "support_form_id": "497253480400030",
        "support_form_hidden_fields": "{}",
        "support_form_fact_false_fields": "[]",
        "__user": "0",
        "__a": "1",
        "__dyn": "7xe6Fo4SQ1PyUhxOnFwn84a2i5U4e1Fx-ey8kxx0LxW0DUeUhw5cx60Vo1upE4W0OE2WxO0SobEa81Vrzo5-0jx0Fwww6DwtU6e",
        "__csr": "",
        "__req": "d",
        "__beoa": "0",
        "__pc": "PHASED:DEFAULT",
        "dpr": "1",
        "__rev": rev,
        "__s": "5gbxno:2obi73:56i3vc",
        "__hsi": hsi,
        "__comet_req": "0",
        "__spin_r": spin_r,
        "__spin_b": spin_b,
        "__spin_t": spin_t
    }

    for _ in range(num_reports):
        try:
            res = ses.post("https://help.instagram.com/ajax/help/contact/submit/page", data=report_form, headers=report_headers, cookies=report_cookies, timeout=10)
            res.raise_for_status()
            print_success("Bildirim gonderildi!")
        except Exception as e:
            print_error("Baglanti hatasi! (FormRequestsError)", e)
            return

def report_video_attack(video_url, num_reports=1):
    ses = Session()

    user_agent = get_user_agent()
    page_headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "tr-TR,tr;q=0.8,en-US;q=0.5,en;q=0.3",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "DNT": "1",
        "User-Agent": user_agent,
    }
    report_headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "tr-TR,tr;q=0.8,en-US;q=0.5,en;q=0.3",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded",
        "DNT": "1",
        "Host": "help.instagram.com",
        "Origin": "help.instagram.com",
        "Pragma": "no-cache",
        "Referer": "https://help.instagram.com/contact/497253480400030",
        "TE": "Trailers",
        "User-Agent": user_agent,
    }

    try:
        res = ses.get("https://www.facebook.com/", timeout=10)
        res.raise_for_status()
    except Exception as e:
        print_error("Baglanti hatasi! (FacebookRequestsError)", e)
        return

    if '["_js_datr","' not in res.text:
        print_error("Baglanti hatasi! (CookieErrorJSDatr)")
        return
    
    try:
        js_datr = res.text.split('["_js_datr","')[1].split('",')[0]
    except:
        print_error("Baglanti hatasi! (CookieParsingError)")
        return

    page_cookies = {"_js_datr": js_datr}

    try:
        res = ses.get("https://help.instagram.com/contact/497253480400030", cookies=page_cookies, headers=page_headers, timeout=10)
        res.raise_for_status()
    except Exception as e:
        print_error("Baglanti hatasi! (InstagramRequestsError)", e)
        return

    if "datr" not in res.cookies.get_dict():
        print_error("Baglanti hatasi! (CookieErrorDatr)")
        return

    if '["LSD",[],{"token":"' not in res.text:
        print_error("Baglanti hatasi! (CookieErrorLSD)")
        return

    if not all(key in res.text for key in ['"__spin_r":', '"__spin_b":', '"__spin_t":', '"server_revision":', '"hsi":']):
        print_error("Baglanti hatasi! (CookieError)")
        return

    try:
        lsd = res.text.split('["LSD",[],{"token":"')[1].split('"},')[0]
        spin_r = res.text.split('"__spin_r":')[1].split(',')[0]
        spin_b = res.text.split('"__spin_b":')[1].split(',')[0].replace('"',"")
        spin_t = res.text.split('"__spin_t":')[1].split(',')[0]
        hsi = res.text.split('"hsi":')[1].split(',')[0].replace('"',"")
        rev = res.text.split('"server_revision":')[1].split(',')[0].replace('"',"")
        datr = res.cookies.get_dict()["datr"]
    except:
        print_error("Baglanti hatasi! (CookieParsingError)")
        return

    report_cookies = {"datr": datr}
    report_form = {
        "jazoest": "2723",
        "lsd": lsd,
        "video_url": video_url,
        "Field241164302734019_iso2_country_code": "IN",
        "Field241164302734019": "India",
        "support_form_id": "497253480400030",
        "support_form_hidden_fields": "{}",
        "support_form_fact_false_fields": "[]",
        "__user": "0",
        "__a": "1",
        "__dyn": "7xe6Fo4SQ1PyUhxOnFwn84a2i5U4e1Fx-ey8kxx0LxW0DUeUhw5cx60Vo1upE4W0OE2WxO0SobEa81Vrzo5-0jx0Fwww6DwtU6e",
        "__csr": "",
        "__req": "d",
        "__beoa": "0",
        "__pc": "PHASED:DEFAULT",
        "dpr": "1",
        "__rev": rev,
        "__s": "5gbxno:2obi73:56i3vc",
        "__hsi": hsi,
        "__comet_req": "0",
        "__spin_r": spin_r,
        "__spin_b": spin_b,
        "__spin_t": spin_t
    }
    for _ in range(num_reports):
        try:
            res = ses.post("https://help.instagram.com/ajax/help/contact/submit/page", data=report_form, headers=report_headers, cookies=report_cookies, timeout=10)
            res.raise_for_status()
            print_success("Bildirim gonderildi!")
        except Exception as e:
            print_error("Baglanti hatasi! (FormRequestsError)", e)
            return

print("-" * 60)

def login_instagram(username, password):
    try:
        csrf_token = requests.get('https://www.instagram.com/accounts/login/').cookies['csrftoken']
        enc_password = f'#PWD_INSTAGRAM_BROWSER:0:{int(datetime.now().timestamp())}:{password}'
        headers = {
            "X-CSRFToken": csrf_token,
            "User-Agent": "Mozilla/5.0",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        response = requests.post(
            'https://www.instagram.com/accounts/login/ajax/',
            data={'username': username, 'enc_password': enc_password},
            headers=headers
        )
        return response.json()
    except Exception as e:
        return {"error": str(e)}

print("[+] DEXRON INSTAGRAM REPORT TOOL")
print()

ig_username = input("Instagram kullanici adi: ")
ig_password = input("Instagram sifre: ")
response_json = login_instagram(ig_username, ig_password)
print(response_json)

def main():
    print("\n[?] Secim yap:")
    print("    [1] Profil bildir")
    print("    [2] Video bildir")
    
    choice = input("Secim: ")

    if choice == "1":
        username = input("Bildirilecek kullanici adi: ")
        num_reports = int(input("Kac bildirim (varsayilan: 1): ") or "1")
        report_profile_attack(username, num_reports)
    elif choice == "2":
        video_url = input("Bildirilecek video URL: ")
        num_reports = int(input("Kac bildirim (varsayilan: 1): ") or "1")
        report_video_attack(video_url, num_reports)
    else:
        print_error("Gecersiz secim. Cikiliyor.")
        exit(1)

if __name__ == "__main__":
    main()
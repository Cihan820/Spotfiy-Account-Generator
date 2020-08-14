from colorama import Fore, init
import threading, requests, random, string, ctypes, names, time, os, sys

init()

ctypes.windll.kernel32.SetConsoleTitleW(' [Cihan820 Spotify Creator]   Loading...')  

created = 0
failed = 0
proxies = []
proxynum = -1

lock = threading.Lock()
s = requests.Session()

def GetProxies():
  global proxies
  try:
    proxies.clear()  
    r = requests.get('https://api.proxyscrape.com/?request=getproxies&proxytype=http&timeout=10000&ssl=yes')
    for line in r.text.splitlines():
      proxies.append(line)
    time.sleep(200)
    GetProxies()
  except:
    pass 

def GetThreads():
  global threads
  try:
    print(time.strftime(Fore.LIGHTBLUE_EX + "[%H:%M:%S]", time.localtime()) + Fore.RESET, end='')
    print(" | ", end='')
    threads = int(input("Threads: "))
    print()
  except:
    ctypes.windll.kernel32.SetConsoleTitleW(' [Spotify Creator]   Threads Must Be an Integer')  
    print(time.strftime(Fore.LIGHTBLUE_EX + "[%H:%M:%S]", time.localtime()) + Fore.RESET, end='')
    print(" | " + Fore.RED, end='')
    input("Threads Must Be an Integer\n")
    exit()

def Creator():
    global created
    global failed
    global proxies
    global proxynum

    proxynum += 1

    domains = ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 'icloud.com', 'mail.com', 'live.com', 'msn.com']
    
    gender = random.choice(['male', 'female'])
    if gender == 'male': 
      showgender = 'Male'
    else:
      showgender = 'Female'
    name = f"{names.get_first_name(gender=gender)}{random.choice(string.digits)}{random.choice(string.digits)}{random.choice(string.digits)}{random.choice(string.digits)}"
    birth_day = random.randint(1, 28)
    birth_month = random.randint(1, 12)
    birth_year = random.randint(1980, 2002)
    email = f'{name}{random.choice(string.digits)}{random.choice(string.digits)}@{random.choice(domains)}'
    password = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(random.randint(8, 12)))
    
    headers = {
       "User-agent": "S4A/2.0.15 (com.spotify.s4a; build:201500080; iOS 13.4.0) Alamofire/4.9.0",
       "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
       "Accept": "application/json, text/plain;q=0.2, */*;q=0.1",
       "App-Platform": "IOS",
       "Spotify-App": "S4A",
       "Accept-Language": "en-TZ;q=1.0",
       "Accept-Encoding": "gzip;q=1.0, compress;q=0.5",
       "Spotify-App-Version": "2.0.15"
    }

    data = {
       "displayname": name,
       "creation_point": "https://login.app.spotify.com?utm_source=spotify&utm_medium=desktop-win32&utm_campaign=organic",
       "birth_month": birth_month,
       "email": email,
       "password": password,
       "creation_flow": "desktop",
       "platform": "desktop",
       "birth_year": birth_year,
       "iagree": "1",
       "key": "4c7a36d5260abca4af282779720cf631",
       "birth_day": birth_day,
       "gender": gender,
       "password_repeat": password,
       "referrer": ""
    }

    try:
      r = s.post("https://spclient.wg.spotify.com/signup/public/v1/account/", headers=headers, data=data, proxies={'https':'https://' + str(proxies[proxynum])})
      if '{"status":1,"' in r.text:
        lock.acquire()  
        print(Fore.GREEN + f"[+] {email}:{password} | Birth Date: {birth_month}/{birth_day}/{birth_year} | Gender: {showgender} | Username: {name}")  
        lock.release()
        with open('Created.txt', 'a', encoding = 'UTF-8') as f: f.write(f"{email}:{password}\n")  
        with open('Capture.txt', 'a', encoding = 'UTF-8') as f: f.write(f"{email}:{password}  |  Birth Date: {birth_month}/{birth_day}/{birth_year}  |  Gender: {showgender}  |  Username: {name}\n")
        created += 1
        ctypes.windll.kernel32.SetConsoleTitleW(f' [Spotify Creator]   Created: {created}   |   Failed: {failed}   |   Threads: {threading.active_count()}/{threads}')  
      else:
        lock.acquire()  
        print(Fore.RED + f"[-] {email}:{password}")  
        lock.release()
        failed += 1
        ctypes.windll.kernel32.SetConsoleTitleW(f' [Spotify Creator]   Created: {created}   |   Failed: {failed}   |   Threads: {threading.active_count()}/{threads}')  
    except IndexError:
      proxynum = -1      
    except:
      pass  

def logo():
    os.system('cls')
    os.system("mode con: cols=110 lines=32")
    try:
        print(Fore.LIGHTBLUE_EX)
        msg = f"""
   _____                      ___ ___   ___  
  / ____(_) |                / _ \__ \ / _ \ 
 | |     _| |__   __ _ _ __ | (_) | ) | | | |
 | |    | | '_ \ / _` | '_ \ > _ < / /| | | |
 | |____| | | | | (_| | | | | (_) / /_| |_| |
  \_____|_|_| |_|\__,_|_| |_|\___/____|\___/ 
                                             
                                                                              \n
        """
        for l in msg:
            print(l, end="")
        print(Fore.RESET + "\t\t            Spotify Account Generator Cihan820")

    except KeyboardInterrupt:
        sys.exit()

logo()
print('  ')
threading.Thread(target=GetProxies).start()
GetThreads()

while True:
  while threading.active_count() < int(threads):
    threading.Thread(target=Creator).start()
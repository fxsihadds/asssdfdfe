import requests, json
import cloudscraper
import subprocess
from urllib.parse import urlparse
from helpers.timemanager import run_sync_in_thread

username = "31laj5twc2wba0a-country-in-session-oemgvulaxe-lifetime-120"
password = "kmqumffw953teoh"
proxy = "rp.scrapegw.com:6060"

proxies = {
    "http": f"http://{username}:{password}@{proxy}",
    "https": f"http://{username}:{password}@{proxy}",
}

session = requests.Session()
scraper = cloudscraper.create_scraper(sess=session)


def extract_value(source, left, right):
    """Extract value from the source based on delimiters"""
    try:
        start = source.index(left) + len(left)
        end = source.index(right, start)
        return source[start:end]
    except ValueError:
        return None

@run_sync_in_thread
def hoichoi_dl(inp_url: str, bot, status):
    print(inp_url)
    headers = {
        "Host": "prod-api.viewlift.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:135.0) Gecko/20100101 Firefox/135.0",
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json",
        "X-Api-Key": "PBSooUe91s7RNRKnXTmQG7z3gwD2aDTA6TlJp6ef",
        "Origin": "https://www.hoichoi.tv",
        "Referer": "https://www.hoichoi.tv/",
    }

    params = {
        "site": "hoichoitv",
        "deviceId": "browser-c60c460a-77c5-6514-1a8c-18524c2be46a",
    }

    json_data = {
        "email": "imtehazmunsi@hotmail.com",
        "password": "Secure_$1122",
    }

    try:
        response = scraper.post(
            "https://prod-api.viewlift.com/identity/signin",
            params=params,
            headers=headers,
            json=json_data,
        )
        response.raise_for_status()
        data = response.json()
        tok = data.get("authorizationToken")
        if not tok:
            raise ValueError("Authorization token not found!")
    except requests.RequestException as e:
        status.edit_text(f"Login failed: {e}")
        return
    except (json.JSONDecodeError, ValueError) as e:
        status.edit_text(f"Error parsing login response: {e}")
        return

    headers1 = {
    "Host": "www.hoichoi.tv",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:135.0) Gecko/20100101 Firefox/135.0",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": "https://www.hoichoi.tv/shows/mohanagar",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "Priority": "u=0",
    "Cookie": "cf_clearance=Z67u3aROYZ_1i0Pb3z78ffx4JhidstuJj8.o88tgGC4-1740757649-1.2.1.1-OzQC6.cPcUW8iyl3OXPjfOX2ya1Sj1qpX6P4yYf0_ZjK1bbYmal7nNA9pXRd5yI0em9QQk8ApTuAP..28TlsbC84GPCdtnNPsd2zAfFJBRrsZL2CZcVWuunfDVnuHrBAwJkKkJNfJFHjcHk8dytXRpnpgWQ1yjMkokw1gFcjxk_0Qm_t6mevsV7Ra61bDWZDJzzvxk61qYHSF2cw.BzFmJdrCkpUo3htHvpA1SLC9vCHuQVhN7MovVk60InasKTssqiDIUnV77q1Dd3pYHifhxXiniWHuiqDFIq4NTALWun6hul2bHmkPJOwQSQQjX4lMQiT.LdPrV8V39rsZEukB9sscHk3pnkz9ujhBnKkaHsYmIzXARl8NHFYuFNb8Uww6SChLDM16H4OjHdn1DatqEHhnn1Vtc_Hvy3RQIMTwIA; _clck=1ch14vu%7C2%7Cftt%7C0%7C1885; CookieConsent={stamp:%27HUZbijT7xA6a3JYq2/jl8oUKICd1joCBNbeHRzmESw56c8jKkyJYPw==%27%2Cnecessary:true%2Cpreferences:false%2Cstatistics:false%2Cmarketing:false%2Cmethod:%27explicit%27%2Cver:1%2Cutc:1740711677287%2Cregion:%27bd%27}; WZRK_G=8bccd71187ea4ba2a9766fc9af55d4c2; __spdt=a52f8a2a3c4a4bbcbdb8be1b260b099d; cto_bundle=Un-dKV9TRE16ajJ2VHlxVFZtOE1uQTElMkZHbHN6YnJnak5ydmo3RlBSZUlMMk01YkZCU3lUS3NxcTlyJTJGeDU0QXUycUR1YXVzNU5nU0FaMTJ2M2k1Y2NBdWtpWFV2RVR1Y1MlMkZyTExUUjhBMkhXcTdEUTVGSGQ5RFVsT1I0UGtZUkJvWEFlRVB2ejlJcnJGeSUyRm9yJTJGWnBzJTJCVU5EZGclM0QlM0Q; muxData=mux_viewer_id=500eb6a2-6a08-409e-aca4-f948986879c3&msn=0.6975856231240338&sid=f618cfcf-7338-4df2-b58b-90307031b196&sst=1740758054255&sex=1740760333216; _uetsid=35a8e740f5a411efb46c63fb86dcb802; _uetvid=35a93bc0f5a411efb05aefd6cf8c5330; WZRK_S_8W6-4W8-8R5Z=%7B%22p%22%3A1%2C%22s%22%3A1740757650%2C%22t%22%3A1740758887%7D; vl-user=c43c8128-36f1-47bd-b8c5-ac0bfa3e7f33; auth=true; isSubscribed=true",
}

    try:
        res = scraper.get(inp_url, headers=headers1)
        res.raise_for_status()
        video_id = extract_value(res.text, '"contentData":[{"gist":{"id":"', '",')
        if not video_id:
            raise ValueError("Video ID not found!")
    except requests.RequestException as e:
        status.edit_text(f"Failed to fetch video details: {e}")
        return
    except ValueError as e:
        status.edit_text(str(e))
        return

    headers = {
    "Host": "prod-api.viewlift.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:135.0) Gecko/20100101 Firefox/135.0",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Authorization": f"{tok}",
    "Origin": "https://www.hoichoi.tv",
    "Referer": "https://www.hoichoi.tv/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "cross-site",
}
    params = {
        "id": video_id,
        "deviceType": "web_browser",
        "contentConsumption": "web",
    }

    try:
        response = scraper.get(
            "https://prod-api.viewlift.com/entitlement/video/status",
            params=params,
            headers=headers,
            proxies=proxies
        )
        response.raise_for_status()
        url_data = extract_value(response.text, '"widevine":', "},")
        url = extract_value(url_data, '"url":"', '"')
        if not url:
            raise ValueError("Video URL not found!")
    except requests.RequestException as e:
        status.edit_text(f"Error fetching video URL: {e}")
        return
    except ValueError as e:
        status.edit_text(str(e))
        return

    parsed_url = urlparse(inp_url)
    name = parsed_url.path.split("/")[-1]

    command = [
        "N_m3u8DL-RE", f"{url}",
        "--key", "06096b2215a6463f951b6e687b87c0cf:ff66b86ebabe06b2f3301eb3601d9ad9",
        "--decryption-engine", "SHAKA_PACKAGER",
        "-sv", "res=720",
        "-sa", "best",
        "--save-name", f"{name}",
        "-M", "format=mp4",
    ]

    try:
        result = subprocess.run(command, shell=True, check=True)
        if result.returncode == 0:
            return f"{name}.mp4"
        else:
            raise RuntimeError("Download command failed!")
    except (subprocess.CalledProcessError, RuntimeError) as e:
        status.edit_text(f"Download error: {e}")
        return

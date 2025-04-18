import yt_dlp
import requests, json
from urllib.parse import urlparse
from pyrogram import Client, filters
from pyrogram.types import Message
from random import randint
import re
import subprocess

session = requests.Session()


def extract_value(source, left, right):
    """Extract value from the source based on delimiters"""
    try:
        start = source.index(left) + len(left)
        end = source.index(right, start)
        return source[start:end]
    except ValueError:
        return None


def bongo_url_extract_requests(url_input: str) -> str:
    if "subscribe" in url_input:
        id = url_input.split("=")[1]
    else:
        parsed_url = urlparse(url_input)
        id = parsed_url.path.split("/")[-1]
    # URL যেখানে রিকোয়েস্ট পাঠানো হবে
    url = "https://accounts.bongo-solutions.com/realms/bongo/protocol/openid-connect/token"

    # হেডারস সেট করা
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:135.0) Gecko/20100101 Firefox/135.0",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJDVUtWUkdUMFp3VEp3VEFfMDVPVXBwV1NwTzN6bzE5aUphVHJwdk9MTkpjIn0.eyJleHAiOjE3Mzk3ODMwOTMsImlhdCI6MTczOTY5NjY5MywiYXV0aF90aW1lIjoxNzM4ODIzMDMxLCJqdGkiOiIzYmNjMmZhYi03YWM1LTRhYjQtODIwNi1jMzczYWRhNGI1ZDYiLCJpc3MiOiJodHRwczovL2FjY291bnRzLmJvbmdvYmQuY29tL3JlYWxtcy9ib25nbyIsInN1YiI6ImYyZDU5NTVmLTZjYWYtNDQzYS1hNjI5LTIxZTRiZGRkMGE3MSIsInR5cCI6IkJlYXJlciIsImF6cCI6Im90cGxvZ2luIiwic2lkIjoiNTI3ZDdjZDUtMTM4YS00YzVjLTg2NWYtYmM3Y2FlZjMzMjBiIiwic2NvcGUiOiJvcGVuaWQiLCJzYWFzX21hcHBlciI6InNhYXMiLCJib25nb19pZCI6IjcxYzE2ODI0LWEwZWUtNGZhMC04MmRmLWU4MzA4NTZhMjE2ZSIsInByZWZlcnJlZF91c2VybmFtZSI6IiAiLCJjbGllbnRfaWQiOiJhYmZlYTQ2Mi1mNjRkLTQ5MWUtOWNkOS03NWVlMDAxZjQ1YjAiLCJjb3VudHJ5X2NvZGUiOiJCRCIsImlkZW50aXR5X3Byb3ZpZGVyIjoiIiwidXNlcl90eXBlIjoicmVndWxhciIsInZlcmlmaWVkX3Bob25lX251bWJlciI6Ijg4MDE4MzE2MjAyODgiLCJwbGF0Zm9ybV9pZCI6ImFiZmVhNDYyLWY2NGQtNDkxZS05Y2Q5LTc1ZWUwMDFmNDViMCIsInBob25lX251bWJlciI6Ijg4MDE4MzE2MjAyODgiLCJzb2NpYWxfY29ubmVjdGlvbnMiOnt9LCJlbWFpbCI6IiIsInVzZXJuYW1lIjoiODgwMTgzMTYyMDI4OCJ9.PQ2ksfHim-Kf9L6ynNlWOPSrMPrT6RzweBkgDhWqS-FDv8JjjczlkBrBAuq5NfkKMqiF_yQVjR7ME8lkCslDnHo-iYrE-7cp4boPxuJrd9ioonHbYZKUem2GtG8Wdtu2OBGn-NaSwZ2diADepd4IaB6h6H9YBGRtsE6ngfgSrx-4VoVvbYh-_v8USrJE-SBNZzVEDX7JxItSRE7gjVZCjfb1_UHEe32I4R0PlmSM297-R9ivknNESgMgn_5rFSS0L6bzA7i43JqDWPKZlzzjf7DZzn3p6IuA2OupGNc4zS3djfv2lLkQMXhECyVCCZrSZCZFCm8daHN_hJaL6CG6VVbq24Q4qORTgvb0s7yGK6WWzhC9H9anj4lhX2o3UP5DytQ7oVGA9BSIjiMIRMSVK7gdyONoLdBg2WD3toUibXMSJkzDnXIWaQl1a2G9KrG62bZt7bqougjNwLrhVvqs8ox9_vj1gRjgbYdhi5xbMs5LF7FbcwUqRXW3qDjPFlnBrWQqVL5UAB6GzklXkURQKKyj2xPq7rbnATWLMGoC-9b6XXFSRtNKxx_czWk3VOsT26MTTadpgKu4gwvrJBnErYsTTFQWH6Ledf8IlY5dUpLgnj_v3LYT35Ec2Lu68yvJkI3DnJr8VeR2ULCsd7TwyrrDNgNaGHn3788FwDJW85U",  # এখানে আপনার আসল অ্যাক্সেস টোকেন দিন
        "Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
        "Origin": "https://bongobd.com",
        "Referer": "https://bongobd.com/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site",
    }

    # ডাটা (বডি) সেট করা
    data = {
        "grant_type": "refresh_token",
        "refresh_token": "eyJhbGciOiJIUzUxMiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICI0NWRiZTZmZS1kZjJiLTQzNTktYWE4ZS1lODEyNjJmNmY1ZTIifQ.eyJleHAiOjE3NDI3MTEwMzEsImlhdCI6MTczOTY5NjY5MywianRpIjoiNGQ1YWU2YTMtODA4NS00M2U1LWI1YjEtZWUwODIzOTcwYmQ3IiwiaXNzIjoiaHR0cHM6Ly9hY2NvdW50cy5ib25nb2JkLmNvbS9yZWFsbXMvYm9uZ28iLCJhdWQiOiJodHRwczovL2FjY291bnRzLmJvbmdvYmQuY29tL3JlYWxtcy9ib25nbyIsInN1YiI6ImYyZDU5NTVmLTZjYWYtNDQzYS1hNjI5LTIxZTRiZGRkMGE3MSIsInR5cCI6IlJlZnJlc2giLCJhenAiOiJvdHBsb2dpbiIsInNpZCI6IjUyN2Q3Y2Q1LTEzOGEtNGM1Yy04NjVmLWJjN2NhZWYzMzIwYiIsInNjb3BlIjoib3BlbmlkIGJhc2ljIn0.4CNfqMba7P6uyITC9N1tjJFJOLp_FUuwadbS3hCMdrN_7vfzsNkx4Akg-FZpt9anBzBSWK74V6YDDtJ-n-q8Rg",
        "client_id": "otplogin",
        "client_secret": "hqLikcYccIpw02KmKNMSfXFloLvcVPPw",
    }

    response = session.post(url, headers=headers, data=data)
    # print(response.text)
    access_token = response.json()["access_token"]
    # refress_token = response.json()["refresh_token"]
    # id_token = response.json()["id_token"]
    # print(access_token)
    headers1 = {
        "Host": "api.bongo-solutions.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:135.0) Gecko/20100101 Firefox/135.0",
        "Accept": "*/*",
        "Accept-Language": "bn",
        "Accept-Encoding": "gzip, deflate, br",
        "Country-Code": "QkQ%3D",
        "Authorization": f"Bearer {access_token}",
        "Origin": "https://bongobd.com",
        "Referer": "https://bongobd.com/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site",
        "Te": "trailers",
    }

    res = session.get(
        url=f"https://api.bongo-solutions.com/ironman/api/v1/content/detail/{id}",
        headers=headers1,
    )
    #print(res.text)
    if "User is not authorized" in res.text:
        raise Exception(
            "This is A Rent a Buy Content, We are not Able to Download this type of Content"
        )
    name = res.json().get("title", "Unknown")
    mpd = extract_value(res.text, '"mpd":{"url":"', '"}}')
    link = extract_value(res.text, '"activeEncode":{"urls":{"hls":{"url":"', '"},')
    drm_id = extract_value(res.text, '{"type":"DRM","drm_id":"', '"}}')
    if not drm_id:
        command = [
    "N_m3u8DL-RE", 
    f"{link}", 
    '-sv','res=720',
    "-M", "format=mp4",
]
        headers = [
            "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:135.0) Gecko/20100101 Firefox/135.0",
            "Origin: https://bongobd.com",
            "Referer: https://bongobd.com/"
        ]
        for header in headers:
                command.extend(["--header", header])
        try:
            result = subprocess.run(command, shell=True)
            print("Command Output:", result.stdout)  
            print("Command Error:", result.stderr) 
        except subprocess.CalledProcessError as e:
            print(f"Error occurred: {e}") 
        return 
    print(link)
    ydl_opts = {
        "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:135.0) Gecko/20100101 Firefox/135.0",
            "Referer": "https://bongobd.com/",
        },
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(link, download=False)
        for format in info["formats"]:
            #print(format)
            if "height" in format and format["height"] == 720:
                # print(f"Selected Format ID: {format['format_id']} {format['url']}")
                headers = {
                    "Host": "vod.bongobd.com",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:135.0) Gecko/20100101 Firefox/135.0",
                    "Accept": "*/*",
                    "Accept-Language": "en-US,en;q=0.5",
                    "Accept-Encoding": "gzip, deflate, br, zstd",
                    "Origin": "https://bongobd.com",
                    "Connection": "keep-alive",
                    "Referer": "https://bongobd.com/",
                    "Sec-Fetch-Dest": "empty",
                    "Sec-Fetch-Mode": "cors",
                    "Sec-Fetch-Site": "same-site",
                    "TE": "trailers",
                }
                tok = session.get(format["url"], headers=headers)
                matches = re.findall(
                    r'URI="data:text/plain;base64,([A-Za-z0-9+/=]+)"', tok.text
                )

                if not matches:
                    raise Exception("Failed to extract token")

                headers = {
                    "Host": "opzz6laqi0.execute-api.ap-southeast-1.amazonaws.com",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:135.0) Gecko/20100101 Firefox/135.0",
                    "Accept": "application/json, text/plain, */*",
                    "Accept-Language": "en-US,en;q=0.5",
                    "Accept-Encoding": "gzip, deflate, br, zstd",
                    "Authorization": f"{access_token}",
                    "Origin": "https://bongobd.com",
                    "Connection": "keep-alive",
                    "Referer": "https://bongobd.com/",
                    "Sec-Fetch-Dest": "empty",
                    "Sec-Fetch-Mode": "cors",
                    "Sec-Fetch-Site": "cross-site",
                    "TE": "trailers",
                }
                print(drm_id)
                drm_id_token = session.get(
                    f"https://opzz6laqi0.execute-api.ap-southeast-1.amazonaws.com/test/api/v1/content/token?system_id={drm_id}&expiry=1740518001",
                    headers=headers,
                )
                id_token = drm_id_token.json()["token"]
                print(id_token)

                headers_drm = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:135.0) Gecko/20100101 Firefox/135.0",
                    "Accept": '"*/*"',
                    "Accept-Language": "en-US,en;q=0.5",
                    "Accept-Encoding": "gzip, deflate, br, zstd",
                    "Origin": "https://bongobd.com",
                    "Connection": "keep-alive",
                    "Sec-Fetch-Dest": "empty",
                    "Sec-Fetch-Mode": "no-cors",
                    "Sec-Fetch-Site": "cross-site",
                    "TE": "trailers",
                    "Content-type": "application/octet-stream",
                    "X-AxDRM-Message": f"{id_token}",
                    "Referer": "https://bongobd.com/",
                }
                headers_api = {
                    "Host": "108.181.133.95:8080",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:135.0) Gecko/20100101 Firefox/135.0",
                    "Accept": "application/json, text/plain, */*",
                    "Accept-Language": "en-US,en;q=0.5",
                    "Accept-Encoding": "gzip, deflate",
                    "Referer": "http://108.181.133.95:8080/",
                    "Content-Type": "application/json",
                    "Content-Length": "2595",
                    "Origin": "http://108.181.133.95:8080",
                    "Connection": "keep-alive",
                    "Priority": "u=0",
                }
                pass_data = {
                    "license": "https://417982d3-drm-widevine-licensing.axprod.net/AcquireLicense",
                    "headers": f"{headers_drm}",
                    "pssh": f"{matches[0]}",
                    "buildInfo": "google/sdk_gphone_x86/generic_x86:8.1.0/OSM1.180201.037/6739391:userdebug/dev-keys",
                    "proxy": "",
                    "cache": True,
                }
                api_url = "http://108.181.133.95:8080/wv"
                r = session.post(
                    api_url,
                    headers=headers_api,
                    json=pass_data,
                )
                key_kid = extract_value(
                    r.text, "<li style=\"font-family:'Courier'\">", "</li>"
                )
                # print(key_kid)
                if not key_kid:
                    raise Exception("Failed to extract key kid")
                cmd = [
                    "C:/Users/FxSihad/Downloads/Compressed/M.exe",
                    mpd,
                    "--key",f"{key_kid}",
                    "-sv", "res=720p",  # Select only 720p resolution
                ]

                cmd.extend(["--save-name", "video", "-M", "format=mp4"])

                try:
                    subprocess.run(cmd, check=True)
                except subprocess.CalledProcessError as e:
                    print(f"Error: {e}")


bongo_url_extract_requests(
    "https://bongobd.com/watch/mCcw71oUZSJ?contentUuid=73a2acbc-c82a-4b42-a8df-ac18cc2db9be"
)

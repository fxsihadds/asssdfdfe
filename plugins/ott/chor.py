from pyrogram import Client, filters
from pyrogram.types import Message
import re, os, time, random
from helpers.chorki_dl import corki_dl
from helpers.display_progress import progress_for_pyrogram
from helpers.c_video import get_video_duration, thumbnail_video
from helpers.hoichoi_dl import hoichoi_dl
from ..handlers.bongod_l import bongo_url_extract_requests
from ..extra.testdlp import handle_user_request

pattern = r"https?://(?:www\.)?(?:chorki\.com|bongobd\.com|hoichoi\.tv)\S*"

chorki_pattern = r"https?://(?:www\.)?chorki\.com\S*"
bongobd_pattern = r"https?://(?:www\.)?bongobd\.com\S*"
hoichoi_pattern = r"https?://(?:www\.)?hoichoi\.tv\S*"

@Client.on_message(filters.regex(pattern))
async def scrape_url(bot: Client, cmd: Message):
    if cmd.text:
        txt = cmd.text
        chorki_match = re.findall(chorki_pattern, txt)
        bongobd_match = re.findall(bongobd_pattern, txt)
        hoichoi_match = re.findall(hoichoi_pattern, txt)

        if chorki_match:
            status = await cmd.reply_text("`Downloading...`")
            url = chorki_match[0]
            path = corki_dl(url, bot, cmd)
            start_time = time.time()
            durations = get_video_duration(path)
            progress_args = ("<b>⎚ Uploading File...</b>", status, path, start_time)
            thumb = thumbnail_video(path)
            if path:
                await bot.send_video(
                    video=path,
                    chat_id=cmd.chat.id,
                    thumb=thumb,
                    caption=path or "",
                    duration=durations,
                    progress=progress_for_pyrogram,
                    progress_args=progress_args,
                )
                await status.delete()
                os.remove(path)

        elif bongobd_match:
            urls = bongobd_match[0]
            try:
                link, name = bongo_url_extract_requests(urls)
            except Exception as err:
                await cmd.reply_text(err)
            else:
                dl_path = f"your_download/{cmd.chat.id}/{random.randint(1, 20)}"
                await handle_user_request(link, name, cmd, dl_path)
                await bot.delete_messages(
                chat_id=cmd.chat.id, message_ids=[cmd.id]
            )
        elif hoichoi_match:
            status = await cmd.reply_text("`Downloading...`")
            url = hoichoi_match[0]
            path = await hoichoi_dl(url, bot, status)
            if not path:
                return
            start_time = time.time()
            durations = get_video_duration(path)
            progress_args = ("<b>⎚ Uploading File...</b>", status, path, start_time)
            thumb = thumbnail_video(path)
            if path:
                await bot.send_video(
                    video=path,
                    chat_id=cmd.chat.id,
                    thumb=thumb,
                    caption=path or "",
                    duration=durations,
                    progress=progress_for_pyrogram,
                    progress_args=progress_args,
                )
                await status.delete()
                os.remove(path)
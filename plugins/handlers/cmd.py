from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
import os, time
from ..handlers.rnd import regenerate_callback

# from helpers.forcesub import ForceSub
# from database.mongodbs import adduser, is_exsist
from ..handlers.ocr import ocr_image_single
from helpers._ocr_helpers import sub_images
from helpers.video_meta_data import META
from helpers.display_progress import progress_for_pyrogram
from ..handlers.testline import find_strings_from_txt
from pprint import pformat
from ..handlers.Translate_gpt import Translate_text
from pyrogram.errors import MessageNotModified  # Import the MessageNotModified
from helpers.User_Control import Subscription, user_check, subs_button
from ..handlers.gmailscrpaer import extract_email_passwords
from ..handlers.gscraper import extract_user_passwords

# Define the InlineKeyboardMarkup
_cmd_button = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("Tool", callback_data="tool"),
            InlineKeyboardButton("OTT-DRM ", callback_data="drm"),
            InlineKeyboardButton("Gates", callback_data="gates"),
        ],
        [
            InlineKeyboardButton("Admin", callback_data="admin"),
            InlineKeyboardButton("Close", callback_data="closed"),
        ],
    ]
)

tools_Click = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("Checkers", callback_data="checkers"),
            InlineKeyboardButton("Gates ", callback_data="gates"),
            InlineKeyboardButton("Others", callback_data="others"),
        ],
        [
            InlineKeyboardButton("Admin", callback_data="admin"),
            InlineKeyboardButton("Close", callback_data="closed"),
        ],
    ]
)


buttons = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("Generate", callback_data="generate"),
            InlineKeyboardButton("Refresh", callback_data="refresh"),
            InlineKeyboardButton("Close", callback_data="close"),
        ]
    ]
)


tools = """<i>Available commands:</i>
`.gscr` - `Extract email:pass`
`.uscr` - `Extract user:pass, number:pass`
`.paste` - `paste any text`
`.unzip` - `unzip a file`
`.ip` - `check your ip address`
`.rand` - `generate random details`
`.bomb` - `send prank messages to a friend`
`.temp` - `create a temporary email`
`.txt` - `create a text file`
`.nid` - `work with nid deals`
`.surl` - `create a short url`
"""

checkers = """<i>Available commands:</i>
`.hoi` - `validate hoichoi combo`
`.crun` - `validate crunchyroll combo`
`.chaupal` - `validate chaupal combo`
`.chor` - `validate chorki combo`

"""


others = """<i>Available commands:</i>
`.bin` - `validate bin`
`.bypass` - `bypass shortened urls`
`.remv` - `remove background from a photo`
`.gemi` - `use google ai for images and text`
`.genimg` - `generate an image`
`.gpt` - `translate text`
`.dl` - `download telegram-restricted videos`
`.redeem` - `purchase premium access`

"""
Gates = """<i>Available commands:</i>
`.vbv` - `check your 3ds card (vbv)`
`.3ds` - `validate your 3ds card`
`.b3` - `check your cc with braintree`
`.chk` - `check your cc with stripe`
`.auth` - `check your cc with braintree`
`.ayden` - `check your cc with ayden`
`.pp` - `check your cc with paypal`
`.stauth` - `check your cc with stripe`
`.bb` - `check your cc with bb`
`.cc` - `check your cc with braintree`

"""


admin = """<i>Available commands:</i>
`.register` - `add a user`
`.unregister` - `remove a user`
`.userlist` - `display the list of users`
`.restart` - `restart the program`
`.speedtest` - `test server speed`
"""

ott = """
<i>Available commands:</i>
<b>Now you can download from the following OTT platforms:</b>
<b>Bongbd</b> DRM✅
<b>Chorki</b> AES✅
<b>Hoichoi</b> DRM✅
***just send the link of the video and get Video File!***
Enjoy!🎉
"""


@Client.on_message(filters.command(["help", "start"]) & filters.incoming)
async def help_command(bot: Client, cmd: Message):
    await bot.send_chat_action(chat_id=cmd.chat.id, action=enums.ChatAction.TYPING)
    # force_sub = await ForceSub(Client, message)
    # if force_sub == 400: return
    user = await user_check(bot, cmd)
    if user:
        await cmd.reply_text("<code>𝖈𝖔𝖒𝖒𝖆𝖓𝖉𝖘: </code>", reply_markup=_cmd_button)


@Client.on_callback_query()
async def cmd(client, callback_query):
    response = callback_query.data
    message = callback_query.message
    try:
        if response == "tool" and callback_query.message.text != f"{tools}\n":
            await callback_query.edit_message_text(
                f"{tools}\n", reply_markup=tools_Click
            )

        elif response == "checkers" and callback_query.message.text != f"{checkers}\n":
            await callback_query.edit_message_text(
                f"{checkers}\n", reply_markup=_cmd_button
            )

        elif response == "others" and callback_query.message.text != f"{others}\n":
            await callback_query.edit_message_text(
                f"{others}\n", reply_markup=_cmd_button
            )
        elif response == "gates" and callback_query.message.text != f"{Gates}\n":
            await callback_query.edit_message_text(
                f"{Gates}\n", reply_markup=_cmd_button
            )
        elif response == "admin" and callback_query.message.text != f"{admin}\n":
            await callback_query.edit_message_text(
                f"{admin}\n", reply_markup=_cmd_button
            )
        elif response == "back" and callback_query.message.text != f"{admin}\n":
            await callback_query.edit_message_text(
                f"{admin}\n", reply_markup=_cmd_button
            )
        elif response == "drm" and callback_query.message.text != f"{ott}\n":
            await callback_query.edit_message_text(f"{ott}\n", reply_markup=_cmd_button)
        elif response == "closed":
            await callback_query.message.delete()
        elif response == "NewGenerate":
            await callback_query.edit_message_text("here are our Main Gmail!")

        elif response == "extract":
            ocr_images_store = f"ocrdict{callback_query.from_user.id}"
            status = await callback_query.message.reply_text(
                "<b>⎚ `Downloading...`</b>"
            )
            download = await client.download_media(message.video)
            await sub_images(
                client, status, download, ocr_images_store
            )  # Ensure to await here
            os.remove(download)
        elif response == "metadata":
            status = await callback_query.message.reply_text(
                "<b>⎚ `Downloading...`</b>"
            )
            video_path = await client.download_media(callback_query.message.video)
            v1 = META(path=video_path)
            result = v1.mediainfo_ext()

            # Format the output for easy copying
            formatted_result = pformat(result, indent=4, width=80)
            await status.edit_text(
                f"<b>Video Information:</b>\n<pre>{formatted_result}</pre>"
            )
            os.remove(video_path)
        elif response == "extaudio":
            status = await callback_query.message.reply_text(
                "<b>⎚ `Downloading...`</b>"
            )
            video_path = await client.download_media(message.video)
            v1 = META(path=video_path)
            result = v1.ext_audio()
            send = await client.send_document(
                chat_id=message.chat.id,
                document="audio/output_audio.mp3",  # Path to the file
                caption="Here is your audio file!",  # Optional caption
            )
            await status.delete()
            os.remove("audio/output_audio.mp3")
            os.remove(video_path)
        elif response == "spvideo":
            status = await callback_query.message.reply_text(
                "<b>⎚ `Downloading...`</b>"
            )
            video_path = await client.download_media(message.video)
            v1 = META(path=video_path)
            result = v1.split_video("output_part1.mp4", "output_part2.mp4")
            part_of_video = ["output_part1.mp4", "output_part2.mp4"]
            # Assuming 'part_of_video' contains a list of file paths for the split video parts
            for idx, items in enumerate(part_of_video):
                # Send each video part
                send = await client.send_video(
                    chat_id=message.chat.id,  # Target chat
                    video=items,  # Path to the video file
                    caption=f"Here is your Video Part {idx + 1}!",  # Caption with part number
                )
                os.remove(items)

            await status.delete()
            os.remove(video_path)
        elif response == "ocrdata":
            if message.photo:
                file_path = await client.download_media(message.photo)
                recognized_text = await ocr_image_single(file_path)
                await callback_query.message.reply_text(recognized_text)
                os.remove(file_path)
                # await asyncio.sleep(2)
                await client.delete_messages(
                    chat_id=message.chat.id, message_ids=[message.id]
                )
            else:
                await callback_query.message.reply_text("No photo to process.")
        elif response == "gentr":
            await Translate_text(client, callback_query)
            """text = await message.text
            await message.reply_text("This is An Text", text)
            return await message.reply_text("Futures Will be Available!")"""

        elif response == "about_gmail":
            await callback_query.edit_message_text("About Gmail!")
        elif response == "ulpextract":
            STATUS_ID = "<b>⎚ `Downloading The Text File...`</b>"
            start_time = time.time()
            file_name = message.document.file_name
            user_folder = f"downloads/{callback_query.from_user.id}"
            file_path = os.path.join(user_folder, file_name)
            if not os.path.exists(user_folder):
                os.makedirs(user_folder)

            user_res = await client.ask(
                message.chat.id,
                "Enter your keyword: (Single: e.g., Netflix | Multiple: e.g., Netflix Express): ✍",
            )
            # Extract the text of the response
            find_str = user_res.text.split()
            status = await message.reply_text("<b>⎚ `Processing...`</b>")
            await message.download(
                file_name=file_path,
                progress=progress_for_pyrogram,
                progress_args=(STATUS_ID, status, file_name, start_time),
            )
            await status.edit_text("<b>⎚ `Extracting The Text File...`</b>")
            for i in find_str:
                print(i)
                await find_strings_from_txt(i, file_path, message, client)

            os.remove(file_path)
            await status.delete()
        elif response == "gscr":
            status = await callback_query.message.reply_text(
                "<b>⎚ `Downloading...`</b>"
            )
            file_path = await client.download_media(message.document)
            with open(file_path, "r", encoding="utf-8") as file:
                text_to_scrape = file.read()
            email_passwords = extract_email_passwords(text_to_scrape)
            if len(email_passwords) > 0:
                # Create a file with the extracted email:password combinations
                filename = os.path.basename(file_path)
                with open(filename, "w", encoding="utf-8") as file:
                    for email_password in email_passwords:
                        file.write(email_password + "\n")
                await client.send_document(
                    chat_id=message.chat.id,
                    document=filename,
                    caption=f"<b>Extracted {len(email_passwords)} email:password</b>",
                )
                os.remove(filename)
                await status.delete()
            else:
                await status.edit_text(
                    text="<b>No email:password combinations found in the provided text ❌.</b>"
                )

        elif response == "uscr":
            status = await callback_query.message.reply_text(
                "<b>⎚ `Downloading...`</b>"
            )
            file_path = await client.download_media(message.document)
            with open(file_path, "r", encoding="utf-8") as file:
                text_to_scrape = file.read()
            email_passwords = extract_user_passwords(text_to_scrape)
            if len(email_passwords) > 0:
                # Create a file with the extracted email:password combinations
                filename = os.path.basename(file_path)
                with open(filename, "w", encoding="utf-8") as file:
                    for email_password in email_passwords:
                        file.write(email_password + "\n")
                await client.send_document(
                    chat_id=message.chat.id,
                    document=filename,
                    caption=f"<b>Extracted {len(email_passwords)} email:password</b>",
                )
                os.remove(filename)
                await status.delete()

        elif response == "trimvideo":
            # trim_video = "video"
            user_res = await client.ask(
                message.chat.id, "Write Your Second Start:end :✍"
            )
            find_str = user_res.text.split(":")
            print(find_str[0], find_str[1])
            video_path = await client.download_media(message.video)
            output_path = os.path.splitext(video_path)[0] + "_trimmed.mp4"
            v1 = META(path=video_path)
            result = v1.trim_video(output_path, int(find_str[0]), int(find_str[1]))
            send = await client.send_video(
                chat_id=message.chat.id,  # Target chat
                video=output_path,  # Path to the video file
                caption=f"Here is your Trim Video",  # Caption with part number
            )
            os.remove(output_path)
            os.remove(video_path)
        elif response == "buy_subs":
            suh = Subscription(callback_query.from_user.id)
            await callback_query.edit_message_text(
                "<b>I Have only 1 Plan!</b> \n`1 weekly - 2$`"
            )
            if suh.is_active():
                info_subs_get = suh.get_subscription_info()
                await callback_query.edit_message_text(
                    f"<b>You already have an active {info_subs_get.get('plan', 'N/A')} subscription! \n  Buy After Expired</b>",
                    reply_markup=subs_button,
                )
                return
            user_res = await client.ask(
                message.chat.id, "Do You Want to Active?(yes/no):✍"
            )
            if user_res.text.lower() == "yes":
                await callback_query.edit_message_text(
                    "<b>1 Week Subscription - 2$</b>"
                )
                user_res_1 = await client.ask(message.chat.id, "Send Your Payment ID:✍")
                if user_res_1.text == "ANTORWKBUY":
                    sub = suh.renew_subscription("weekly")
                    sub_info = suh.get_subscription_info()
                    msg = f"""

<b>Subscription Activated!</b>
<b>User ID</b>: {callback_query.from_user.id}
Plan: {sub_info.get('plan', 'N/A')}
Start Date: {sub_info.get('start_date', 'N/A')}
End Date: {sub_info.get('end_date', 'N/A')}
Status: {sub_info.get('status', 'N/A')}
"""
                    status = await message.reply_text(msg)
        elif response == "infoo":
            sub = Subscription(callback_query.from_user.id)
            sub_info = sub.get_subscription_info()

            msg = f"""
<b>User ID</b>: {callback_query.from_user.id}
Plan: {sub_info.get('plan', 'N/A')}
Start Date: {sub_info.get('start_date', 'N/A')}
End Date: {sub_info.get('end_date', 'N/A')}
Status: {sub_info.get('status', 'N/A')}
"""
            await callback_query.edit_message_text(msg, reply_markup=subs_button)
        elif response == "freetrails":
            sub = Subscription(callback_query.from_user.id)
            subcribe = sub.start_subscription("free_trial")
            sub_info = sub.get_subscription_info()
            if sub_info["status"] == "Expired":
                msg = f"""
<b>Free Trial Expired!</b>
<b>User ID</b>: {callback_query.from_user.id}
Plan: {sub_info.get('plan', 'N/A')}
Start Date: {sub_info.get('start_date', 'N/A')}
End Date: {sub_info.get('end_date', 'N/A')}
Status: {sub_info.get('status', 'N/A')}
"""
                await callback_query.edit_message_text(msg, reply_markup=subs_button)
            elif sub_info["status"] == "free_trial":
                msg = f"""
<b>Free Trial Activated!</b>
<b>User ID</b>: {callback_query.from_user.id}
Plan: {sub_info.get('plan', 'N/A')}
Start Date: {sub_info.get('start_date', 'N/A')}
End Date: {sub_info.get('end_date', 'N/A')}
Status: {sub_info.get('status', 'N/A')}
"""
                await callback_query.edit_message_text(msg, reply_markup=subs_button)

            else:
                msg = f"""
<b>Subscription Activated!</b>
<b>User ID</b>: {callback_query.from_user.id}
Plan: {sub_info.get('plan', 'N/A')}
Start Date: {sub_info.get('start_date', 'N/A')}
End Date: {sub_info.get('end_date', 'N/A')}
Status: {sub_info.get('status', 'N/A')}
"""
                await callback_query.edit_message_text(msg, reply_markup=subs_button)
        elif response == "regenerateadds":
            await regenerate_callback(client, callback_query)
    except MessageNotModified:
        await callback_query.answer("Click Another Button!..")
    except Exception as e:
        print(f"An error occurred: {e}")

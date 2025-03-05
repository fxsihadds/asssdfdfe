import os
import random
from PIL import Image
import ffmpeg

def get_size(size):
    """Get size in readable format"""

    units = ["Bytes", "KB", "MB", "GB", "TB", "PB", "EB"]
    size = float(size)
    i = 0
    while size >= 1024.0 and i < len(units):
        i += 1
        size /= 1024.0
    return "%.2f %s" % (size, units[i])



def get_video_duration(video_file_path):
    """Get video duration in seconds using ffmpeg."""
    try:
        probe = ffmpeg.probe(video_file_path)
        duration = float(probe['format']['duration'])
        return int(duration)
    except Exception as e:
        print(f"Error getting duration: {e}")
        return None


def thumbnail_video(video_file_path):
    """Generate a thumbnail from a random timestamp using ffmpeg."""
    duration = get_video_duration(video_file_path)
    if duration is None:
        return None

    random_time = random.randint(0, duration - 1)
    thumbnail_path = f"{random.randint(1, 100)}_thumbnail.png"

    try:
        (
            ffmpeg.input(video_file_path, ss=random_time)
            .output(thumbnail_path, vframes=1)
            .run(quiet=True, overwrite_output=True)
        )
        return thumbnail_path
    except Exception as e:
        print(f"Error generating thumbnail: {e}")
        return None


def split_scene(video_file_path) -> bool:
    """Splits a video file if its size is greater than 4000 MB."""
    if not os.path.isfile(video_file_path):
        print("File not found.")
        return False

    file_size_mb = round(os.path.getsize(video_file_path) / (1024 * 1024))
    print(f"File size: {file_size_mb} MB")

    if file_size_mb <= 4000:
        print("File is small enough to upload to Telegram.")
        return False

    duration = get_video_duration(video_file_path)
    if duration is None:
        return False

    num_segments = 2
    segment_duration = duration / num_segments
    output_directory = "your_download"
    os.makedirs(output_directory, exist_ok=True)

    for i in range(num_segments):
        start_time = int(i * segment_duration)
        end_time = int((i + 1) * segment_duration)
        output_file = os.path.join(
            output_directory, f"{os.path.basename(video_file_path)}_part{i + 1}.mp4"
        )

        try:
            (
                ffmpeg.input(video_file_path, ss=start_time, t=(end_time - start_time))
                .output(output_file, c="copy")
                .run(quiet=True, overwrite_output=True)
            )
            print(f"Segment {i + 1} saved: {output_file}")
        except Exception as e:
            print(f"Error splitting video: {e}")
            return False

    print("Video split into segments.")
    os.remove(video_file_path)
    return True


def get_file_size(video_file_path) -> bool:
    get_size = os.path.getsize(video_file_path)
    file_size_megabytes = round(get_size / (1024 * 1024))
    print(f"File size: {file_size_megabytes} MB")
    if file_size_megabytes < 2000:
        return True
    else:
        os.remove(video_file_path)
        return False

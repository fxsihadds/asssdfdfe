import os
import json
import ffmpeg
from pymediainfo import MediaInfo


class META:
    def __init__(self, path: str) -> None:
        if not os.path.isfile(path):
            raise FileNotFoundError(f"The file '{path}' does not exist.")
        self.path = path

    def meta_data_extract(self):
        try:
            # Extract metadata from the file
            result = ffmpeg.probe(self.path)
            streams = result.get("streams", [])
            
            # Write metadata to a file in JSON format
            with open("result.txt", mode="a", encoding="utf-8") as data:
                json.dump(streams, data, indent=4)
                data.write("\n")  # Add a newline for readability
            return streams
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def mediainfo_ext(self):
        media_info = MediaInfo.parse(self.path)
        for track in media_info.tracks:
            if track.track_type in ["Video", "Audio"]:
                return track.to_data()
        os.remove(self.path)

    def ext_audio(self):
        output_dir = "audio"
        output_file = os.path.join(output_dir, "output_audio.mp3")
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        try:
            # Extract audio using FFmpeg
            (
                ffmpeg
                .input(self.path)
                .output(output_file, acodec="libmp3lame", audio_bitrate="320k")
                .run(overwrite_output=True)
            )
            print(f"Audio extracted successfully: {output_file}")
        except Exception as e:
            print(f"An error occurred: {e}")
            os.remove(self.path)

    def split_video(self, output1, output2):
        try:
            # Get video duration
            duration = float(ffmpeg.probe(self.path)['format']['duration'])
            midpoint = duration / 2
            
            # Split video into two parts using FFmpeg
            (
                ffmpeg
                .input(self.path, ss=0, t=midpoint)
                .output(output1, vcodec="libx264", acodec="aac")
                .run(overwrite_output=True)
            )
            
            (
                ffmpeg
                .input(self.path, ss=midpoint)
                .output(output2, vcodec="libx264", acodec="aac")
                .run(overwrite_output=True)
            )
            print("Video split successfully.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def trim_video(self, output_path, start_time, end_time):
        try:
            # Get video duration
            duration = float(ffmpeg.probe(self.path)['format']['duration'])
            if start_time < 0 or end_time > duration or start_time >= end_time:
                raise ValueError("Invalid start_time or end_time.")
            
            # Trim video using FFmpeg
            (
                ffmpeg
                .input(self.path, ss=start_time, to=end_time)
                .output(output_path, vcodec="libx264", acodec="aac")
                .run(overwrite_output=True)
            )
            print(f"Video trimmed successfully and saved to {output_path}.")
        except Exception as e:
            print(f"An error occurred: {e}")





"""v1 = META(
    path="F:\Download\Desafio dos Jurados com a música Whenever, Wherever da Shakira - CANTA COMIGO.mp4"
)
v1.mediainfo_ext()
v1.ext_audio()"""

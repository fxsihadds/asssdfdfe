import subprocess

# Define the command as a list
command = [
    "N_m3u8DL-RE", 
    "https://vod.bongobd.com/vod/vod/919f93a7400e4149a70d204beb589074/b/0/b0fa75d4f05f4b539720a3dcf3a57a40/d3e4597fc66e4c2fb152b8ca3614a506.m3u8", 
    #"--key", "06096b2215a6463f951b6e687b87c0cf:ff66b86ebabe06b2f3301eb3601d9ad9", 
    #"--decryption-engine", "SHAKA_PACKAGER", 
    '-sv','res=720',
    #'-sa', 'cenc',
    "-M", "format=mp4",

]
headers = [
    "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:135.0) Gecko/20100101 Firefox/135.0",
    "Origin: https://bongobd.com",
    "Referer: https://bongobd.com/"
]
for header in headers:
        command.extend(["--header", header])
# Run the command and capture the output
try:
    result = subprocess.run(command, shell=True)
    print("Command Output:", result.stdout)  # Print the command output
    print("Command Error:", result.stderr)   # Print any errors
except subprocess.CalledProcessError as e:
    print(f"Error occurred: {e}")

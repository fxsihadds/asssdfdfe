import subprocess

# Define the command as a list
command = [
    "N_m3u8DL-RE", 
    "https://vhoichoi.viewlift.com/Renditions/20240918/1726653771823_toofan_bng_movie/dash/1726653771823_toofan_bng_movie.mpd", 
    "--key", "06096b2215a6463f951b6e687b87c0cf:ff66b86ebabe06b2f3301eb3601d9ad9", 
    "--decryption-engine", "SHAKA_PACKAGER", 
    '-sv','res=720',
    '-sa', 'cenc',
    "-M", "format=mp4",

]

# Run the command and capture the output
try:
    result = subprocess.run(command, shell=True)
    print("Command Output:", result.stdout)  # Print the command output
    print("Command Error:", result.stderr)   # Print any errors
except subprocess.CalledProcessError as e:
    print(f"Error occurred: {e}")
